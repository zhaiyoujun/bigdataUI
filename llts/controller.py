# coding: utf8

import logging
import signal

import zmq

import config
from agentPool import AgentPool
from const import RequestField, RequestType, AgentStatus, TaskStatus, RequestError
from log import InitLogging
from net import RecvMsg, SendMsg, Connect, Bind
from taskPool import TaskPool
from toolPool import ToolPool

Logger = logging.getLogger('')
InitLogging(config.CONTROLLER_LOG_FILE)
ControllerStopped = False


def SendTaskStatus(addr, task):
    try:
        sock = Connect(stype=zmq.DEALER, address=addr)
    except:
        Logger.exception("connect to %s to report task failed: %s", addr, str(task))
        return
    try:
        sock.setsockopt(zmq.LINGER, 0)  # sock.close 之后为对面还未收到的报告保留的时间设为 0
        SendMsg(sock, task)
        Logger.info("report task to %s: %s", addr, str(task))
    except:
        Logger.exception("report task to %s failed: %s", addr, str(task))
    finally:
        sock.close()


def KillTask(pubSock, taskId):
    if taskId not in TaskPool._tasks:
        Logger.warning('kill unknown task %s', taskId)
    elif taskId in TaskPool._status[TaskStatus.ENDED]:
        Logger.warning('kill ignored because task %s is ENDED', taskId)
    elif taskId in TaskPool._status[TaskStatus.FINISHED]:
        Logger.warning('kill ignored because task %s is FINISHED', taskId)
    elif taskId in TaskPool._status[TaskStatus.WAITING]:
        TaskPool.kill(taskId)
    else:
        SendMsg(pubSock, {RequestField.TYPE: RequestType.TASK_KILL, RequestField.TASK_ID: taskId})
        Logger.info('task %s will be killed by agents', taskId)


def Dispatch():
    global ControllerStopped

    pubSock = Bind(zmq.PUB, config.CONTROLLER_PUB_PORT)
    repSock = Bind(zmq.REP, config.CONTROLLER_REP_PORT)

    Logger.info('controller is ready')

    while not ControllerStopped:
        Logger.debug('start main loop')
        Logger.debug('Agent Statistic: %s', str(AgentPool.statistic()))
        Logger.debug('Task Statistic: %s', str(TaskPool.statistic()))

        # 检查agent丢失
        AgentPool.checkLost()

        # 清理过期的任务
        TaskPool.cleanTasks()

        try:
            msg = RecvMsg(repSock, alwaysWait=False)
        except:
            continue  # 超时

        reply = {}
        try:
            if RequestField.TYPE not in msg.keys():
                reply = RequestError.MISS_REQUEST_TYPE

            elif msg[RequestField.TYPE] == RequestType.TASK_SUBMIT:  # 提交任务
                task, inform = TaskPool.new(msg)
                Logger.info("client submitted new task %s: %s", task[RequestField.TASK_ID], str(task))
                reply[RequestField.TASK_ID] = task[RequestField.TASK_ID]
                if inform:
                    SendMsg(pubSock, {RequestField.TYPE: RequestType.TASK_INFORM})

            elif msg[RequestField.TYPE] == RequestType.TASK_KILL:  # 杀死任务
                Logger.info("client want to kill task %s", msg)
                task = TaskPool.query(msg)
                if task is not None:
                    KillTask(pubSock, task[RequestField.TASK_ID])
                else:
                    reply = RequestError.MISS_TASK

            elif msg[RequestField.TYPE] == RequestType.TASK_QUERY:  # 查询任务
                task = TaskPool.query(msg)
                Logger.info("client query task %s", msg)
                reply = RequestError.MISS_TASK if task is None else task

            elif msg[RequestField.TYPE] == RequestType.TASK_QUERY_CLAN:  # 查询任务族详情
                reply = TaskPool.queryClan(msg)
                reply = RequestError.MISS_TASK if reply is None else reply

            elif msg[RequestField.TYPE] == RequestType.AGENT_HEARTBEAT:  # Agent报告心跳
                AgentPool.update(msg)
                if msg[RequestField.AGENT_STATUS] == AgentStatus.FREE and TaskPool.hasWaiting():
                    SendMsg(pubSock, {RequestField.TYPE: RequestType.TASK_INFORM})

            elif msg[RequestField.TYPE] == RequestType.AGENT_EXIT:  # Agent主动退出
                AgentPool.exit(msg[RequestField.AGENT_ID])

            elif msg[RequestField.TYPE] == RequestType.TASK_APPLY:  # Agent申请任务
                agentId = msg[RequestField.AGENT_ID]
                task = TaskPool.fetchWaiting(agentId, AgentPool.getTags(agentId))
                reply = RequestError.NO_TASK if task is None else task

            elif msg[RequestField.TYPE] == RequestType.TASK_REPORT:  # Agent报告任务最新状态
                task = TaskPool.report(msg)
                if task.has_key(RequestField.ADDRESS):
                    SendTaskStatus(task[RequestField.ADDRESS], task)
                if task[RequestField.STATUS] == TaskStatus.ENDED:
                    for cid in TaskPool.getChildren(task[RequestField.TASK_ID]):
                        KillTask(pubSock, cid)

            elif msg[RequestField.TYPE] == RequestType.TASK_STATISTIC:  # task统计信息
                reply = TaskPool.statistic()

            elif msg[RequestField.TYPE] == RequestType.AGENT_STATISTIC:  # Agent统计信息
                reply = AgentPool.statistic()

            elif msg[RequestField.TYPE] == RequestType.TASK_DETAILS:  # task详细信息
                reply = TaskPool.details(
                    int(msg.get(RequestField.OFFSET, 0)),
                    int(msg.get(RequestField.LIMIT, -1)),
                    msg.get(RequestField.FATHER_ID, None),
                    int(msg.get(RequestField.DEEP, 1))
                )

            elif msg[RequestField.TYPE] == RequestType.AGENT_DETAILS:  # agent详细信息
                reply = AgentPool.details()

            elif msg[RequestField.TYPE] == RequestType.TOOL_DETAILS:  # tool详细信息
                reply = ToolPool.details()

            else:
                Logger.warning('message with type "%s" was ignored', msg[RequestField.TYPE])
                reply = RequestError.UNKNOWN_REQUEST_TYPE

            if not reply.has_key(RequestField.CODE):
                reply[RequestField.CODE] = 0

        except:
            Logger.exception('deal message failed: %s', str(msg))
            reply = RequestError.INTERNAL_ERROR

        SendMsg(repSock, reply)

    Logger.info('controller exit')


def Terminate(sig, extra):
    global ControllerStopped
    ControllerStopped = True
    Logger.info('signaled by %d', sig)


signal.signal(signal.SIGINT, Terminate)
signal.signal(signal.SIGTERM, Terminate)

if __name__ == '__main__':
    Dispatch()
