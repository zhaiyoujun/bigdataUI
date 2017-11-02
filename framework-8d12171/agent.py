# coding: utf8

import copy
import logging
import os
import random
import signal
import string
import subprocess
import thread
import threading
import time

import psutil
import zmq

import config
from const import RequestField, RequestType, AgentStatus, TaskStatus, TaskError, TaskErrorMsg
from log import InitLogging
from mcosUtil import MCOSUtil
from net import RecvMsg, SendAndRecv, Connect, MyIP
from toolPool import ToolPool

AgentStopped = False
RunTaskThread = None
AGENT_ID = 'AGENT_' + str(time.time()) + '_' + ''.join(random.choice(string.letters) for x in range(5))
InitLogging(config.AGENT_LOG_FILE + '.' + AGENT_ID)
Logger = logging.getLogger('')


def FetchProcessInfo(p):
    return {
        'pid': p.pid,
        'ppid': p.ppid(),
        'cmdline': p.cmdline(),
        'cwd': p.cwd(),
        'cpu_user': p.cpu_times().user,
        'cpu_system': p.cpu_times().system,
        'mem_rss': p.memory_info().rss,
        'mem_vms': p.memory_info().vms,
        'status': p.status(),
        'num_threads': p.num_threads(),
        'num_fds': p.num_fds(),
        'children': [FetchProcessInfo(c) for c in p.children()]
    }


class TaskMgr(object):
    _lock = thread.allocate_lock()
    _task = None

    @classmethod
    def isTask(cls, id):
        cls._lock.acquire()
        if cls._task is None:
            cls._lock.release()
            return False
        if id is not None and cls._task[RequestField.TASK_ID] != id:
            cls._lock.release()
            return False
        cls._lock.release()
        return True

    @classmethod
    def isEmpty(cls):
        return cls._task is None

    @classmethod
    def isEnded(cls):
        cls._lock.acquire()
        status = cls._task[RequestField.STATUS] if cls._task is not None else TaskStatus.FINISHED
        cls._lock.release()
        return status == TaskStatus.FINISHED or status == TaskStatus.ENDED

    @classmethod
    def isKilled(cls):
        cls._lock.acquire()
        killed = RequestField.KILLED in cls._task and cls._task[RequestField.KILLED]
        cls._lock.release()
        return killed

    @classmethod
    def clean(cls):
        cls._lock.acquire()
        cls._task = None
        cls._lock.release()
        Logger.debug("task cleaned")

    @classmethod
    def fill(cls, task):
        cls._lock.acquire()
        cls._task = task
        cls._lock.release()
        if task is not None:
            Logger.info("fetch task %s: %s", task[RequestField.TASK_ID], str(task))

    @classmethod
    def update(cls, fields):
        cls._lock.acquire()
        Logger.debug("task update: %s", str(fields))
        for k, v in fields.items():
            if v is None:
                cls._task.pop(k, None)
            else:
                cls._task[k] = v
        task = copy.deepcopy(cls._task)
        cls._lock.release()
        return task

    @classmethod
    def check(cls):
        cls._lock.acquire()
        task = None
        if cls._task is not None and RequestField.PROCESS_ID in cls._task:
            try:
                p = psutil.Process(cls._task[RequestField.PROCESS_ID])
                cls._task[RequestField.PROCESS_STATUS] = FetchProcessInfo(p)
            except:
                cls._task.pop(RequestField.PROCESS_STATUS, None)
            task = copy.deepcopy(cls._task)
        cls._lock.release()
        return task

    @classmethod
    def getTaskInfo(cls):
        cls._lock.acquire()
        info = '%s: %s' % (cls._task[RequestField.TASK_ID], str(cls._task))
        cls._lock.release()
        return info

    @classmethod
    def getKillInfo(cls, id):
        cls._lock.acquire()
        if cls._task is None:
            ended, pid = True, None
        elif id is not None and cls._task[RequestField.TASK_ID] != id:
            ended, pid = True, None
        elif cls._task[RequestField.STATUS] == TaskStatus.ENDED \
                or cls._task[RequestField.STATUS] == TaskStatus.FINISHED:
            ended, pid = True, None
        elif cls._task.has_key(RequestField.PROCESS_ID):
            ended, pid = False, cls._task[RequestField.PROCESS_ID]
        else:
            ended, pid = False, None
        cls._lock.release()
        return ended, pid


def SendHeartBeat(sock, status=None):
    if status is None:
        status = AgentStatus.FREE if TaskMgr.isEmpty() else AgentStatus.BUSY
    return SendAndRecv(sock, {
        RequestField.TYPE: RequestType.AGENT_HEARTBEAT,
        RequestField.AGENT_ID: AGENT_ID,
        RequestField.AGENT_IP: MyIP,
        RequestField.AGENT_TAG: config.AGENT_TAGS,
        RequestField.AGENT_STATUS: status
    })


def ReportTask(sock, task):
    Logger.debug("report task: %s", str(task))
    task[RequestField.TYPE] = RequestType.TASK_REPORT
    SendAndRecv(sock, task)


def FetchTask(sock):
    global AgentStopped
    if AgentStopped:
        return None
    task = SendAndRecv(sock, {
        RequestField.TYPE: RequestType.TASK_APPLY,
        RequestField.AGENT_ID: AGENT_ID
    })
    Logger.debug("fetch task: %s", str(task))
    return None if task[RequestField.CODE] != 0 else task


def TryEnterBusy():
    global RunTaskThread
    if RunTaskThread is not None and RunTaskThread.is_alive():
        # RunTaskThread 只在主线程中访问, 可以确保只有一个活跃的任务执行线程
        Logger.debug("still in busy status")
        return

    def _RunTask():
        def _PreExec():
            os.setpgid(os.getpid(), os.getpid())

        def _PrepareEnv(sock):
            Logger.info("preparing task")
            task = TaskMgr.update({
                RequestField.STATUS: TaskStatus.PREPARING,
                RequestField.PREPARE_TIME: time.time()})
            ReportTask(sock, task)

            workDir = config.AGENT_WORK_DIR + '/' + task[RequestField.TASK_ID]
            operation = task.get(RequestField.OPERATION)
            version = task.get(RequestField.OPERATION_VERSION)

            try:
                os.system('mkdir -p %s' % workDir)

                with open(workDir + '/' + 'task.info', 'w') as file:
                    for k, v in task.items():
                        file.write(k.encode('utf8') if isinstance(k, unicode) else str(k))
                        file.write('=')
                        file.write(v.encode('utf8') if isinstance(v, unicode) else str(v))
                        file.write('\n')

                with open(workDir + '/' + 'controller.info', 'w') as file:
                    controllerAddress = '%s:%d' % (config.CONTROLLER_IP, config.CONTROLLER_REP_PORT)
                    file.write('CONTROLLER_ADDRESS=tcp://%s\n' % controllerAddress)
                    file.write('AGENT_IP=%s\n' % MyIP)

                with open(workDir + '/' + 'agent.tags', 'w') as file:
                    for k, v in config.AGENT_TAGS.items():
                        file.write('%s %s\n' % (k, v))

                code, realVersion = ToolPool.prepare(operation, version, workDir)
                if code != 0:
                    return code, workDir, operation

                if config.MCOS_SUPPORT and RequestField.VISITOR in task:
                    dataDir = workDir + '/data'
                    MCOSUtil.Mount(task[RequestField.VISITOR], task.get(RequestField.VISITOR_TOKEN, ''), dataDir)

                if realVersion != version:
                    TaskMgr.update({
                        RequestField.OPERATION_VERSION: realVersion
                    })
            except:
                Logger.exception("prepare for task failed")
                return TaskError.TOOL_ERROR, workDir, operation

            return 0, workDir, operation

        def _RunTask(sock, workDir, operation):
            stdoutFile = open('%s/stdout.log' % workDir, 'w')
            stderrFile = open('%s/stderr.log' % workDir, 'w')
            stdinFile = open('/dev/null')
            process = subprocess.Popen(
                '%s/run.sh' % operation,
                shell=True, preexec_fn=_PreExec, cwd=workDir,
                stdout=stdoutFile, stderr=stderrFile, stdin=stdinFile)
            Logger.info('running task with pid %d', process.pid)
            ReportTask(sock, TaskMgr.update({
                RequestField.PROCESS_ID: process.pid,
                RequestField.WORK_DIR: workDir,
                RequestField.STATUS: TaskStatus.RUNNING,
                RequestField.RUN_TIME: time.time()
            }))
            exitCode = process.wait()

            def _FetchFileTail(path, keepBytes):
                if not os.path.exists(path):
                    return None
                try:
                    size = os.path.getsize(path)
                    with open(path, 'r') as f:
                        if size > keepBytes:
                            f.seek(-keepBytes, 2)
                            f.readline()  # 略过当前行，以防止返回的内容包含了半行

                        content = f.read()
                        for code in ['utf8', 'gbk']:
                            try:
                                return content.decode(code)
                            except:
                                pass

                        Logger.warn('%s decode error: %s', path, content.__repr__())
                        return 'decode Error, should be encoded in utf8 or gbk'
                except:
                    Logger.exception("fetch '%s' tail failed", path)
                return None

            stdoutCnt = _FetchFileTail('%s/stdout.log' % workDir, config.STDOUT_KEEP_BYTES)
            stderrCnt = _FetchFileTail('%s/stderr.log' % workDir, config.STDERR_KEEP_BYTES)
            reportLog = _FetchFileTail('%s/%s/report.log' % (workDir, operation), config.REPORT_LOG_KEEP_BYTES)

            return exitCode, stdoutCnt, stderrCnt, reportLog

        def _CleanEnv(sock, workDir):
            Logger.info('cleaning the workDir')
            if config.AGENT_WORK_DIR != '' and config.AGENT_CLEAN_WORK_DIR:
                os.system('rm -rf %s' % workDir)
            Logger.info("task finished")
            ReportTask(sock, TaskMgr.update({
                RequestField.STATUS: TaskStatus.FINISHED,
                RequestField.FINISH_TIME: time.time()}))

        def _Run(sock):
            exitCode, workDir, operation = _PrepareEnv(sock)
            reportLog = stdoutCnt = stderrCnt = None

            if exitCode != 0:  # 准备过程中出现了异常
                Logger.error('something wrong while preparing task')
            elif TaskMgr.isKilled():  # 准备过程中被要求杀掉了
                exitCode = TaskError.KILLED_IN_PREPARING
                Logger.info('task killed before run')
            else:  # 执行任务
                exitCode, stdoutCnt, stderrCnt, reportLog = _RunTask(sock, workDir, operation)

            Logger.info("task ended with exit code %d", exitCode)

            ReportTask(sock, TaskMgr.update({
                RequestField.EXIT_CODE: exitCode,
                RequestField.STATUS: TaskStatus.ENDED,
                RequestField.PROCESS_STATUS: None,
                RequestField.END_TIME: time.time(),
                RequestField.STDOUT: stdoutCnt,
                RequestField.STDERR: stderrCnt,
                RequestField.REPORT_LOG: reportLog,
                RequestField.ERROR_MSG: TaskErrorMsg.get(exitCode, None)
            }))

            _CleanEnv(sock, workDir)

        reqSock = Connect(stype=zmq.REQ, ip=config.CONTROLLER_IP, port=config.CONTROLLER_REP_PORT)
        try:
            TaskMgr.fill(FetchTask(reqSock))
            if TaskMgr.isEmpty(): return

            Logger.info("enter busy status")
            SendHeartBeat(reqSock)  # 从 free 进入 busy，立刻报告一下

            while not TaskMgr.isEmpty():
                _Run(reqSock)
                TaskMgr.fill(FetchTask(reqSock))

            Logger.info("enter free status")
            SendHeartBeat(reqSock)  # 从 busy 进入 free，立刻报告一下
        except:
            Logger.exception("enter busy failed")
        finally:
            reqSock.close()

    RunTaskThread = threading.Thread(target=_RunTask)
    RunTaskThread.start()


def TryStopTask(id=None):
    if not TaskMgr.isTask(id):
        return
    TaskMgr.update({RequestField.KILLED: 'TRUE', RequestField.KILL_TIME: time.time()})

    def _KillTask(id):
        count = 0
        while count < config.AGENT_KILL_COUNT:
            ended, pid = TaskMgr.getKillInfo(id)
            Logger.debug('ended: %s, pid: %s', str(ended), str(pid))
            if ended: break;
            if pid is not None:
                if count == 0:
                    Logger.info("will send SIGTERM to %d", -pid)
                    os.kill(-pid, signal.SIGTERM)
                else:
                    Logger.info("will send SIGKILL to %d", -pid)
                    os.kill(-pid, signal.SIGKILL)
                count += 1
            time.sleep(config.AGENT_KILL_INTERVAL / 1000.0)

    thread.start_new_thread(_KillTask, (id,))


def StartHeartBeatThread():
    def _HeartBeatMain():
        reqSock = Connect(stype=zmq.REQ, ip=config.CONTROLLER_IP, port=config.CONTROLLER_REP_PORT)
        while not AgentStopped:
            SendHeartBeat(reqSock)
            task = TaskMgr.check()
            if task is not None:
                ReportTask(reqSock, task)
            time.sleep(config.AGENT_HEARTBEAT_INTERVAL / 1000.0)

    thread.start_new_thread(_HeartBeatMain, ())


def ReportExit():
    reqSock = Connect(stype=zmq.REQ, ip=config.CONTROLLER_IP, port=config.CONTROLLER_REP_PORT)
    SendAndRecv(reqSock, {
        RequestField.TYPE: RequestType.AGENT_EXIT,
        RequestField.AGENT_ID: AGENT_ID,
    }, alwaysWait=False)


def Dispatch():
    global AgentStopped

    Logger.info('agent is ready')
    subSock = Connect(stype=zmq.SUB, ip=config.CONTROLLER_IP, port=config.CONTROLLER_PUB_PORT)
    subSock.set(zmq.SUBSCRIBE, "")

    # 立即尝试获取任务
    TryEnterBusy()

    while not AgentStopped:
        try:
            msg = RecvMsg(subSock, alwaysWait=False)
        except zmq.error.Again:
            continue  # 超时没有内容，应该重试

        try:
            if msg[RequestField.TYPE] == RequestType.AGENT_STOP:
                targetAgent = 'all agents' \
                    if not msg.has_key(RequestField.AGENT_ID) \
                    else ('agent ' + msg[RequestField.AGENT_ID])
                Logger.info("required to stop %s", targetAgent)
                if not msg.has_key(RequestField.AGENT_ID) or msg[RequestField.AGENT_ID] == AGENT_ID:
                    AgentStopped = True
                    TryStopTask()
            elif msg[RequestField.TYPE] == RequestType.TASK_INFORM:
                Logger.info("required to check new task")
                TryEnterBusy()
            elif msg[RequestField.TYPE] == RequestType.TASK_KILL:
                Logger.info("required to kill task %s", msg[RequestField.TASK_ID])
                TryStopTask(msg[RequestField.TASK_ID])
            else:
                Logger.warning('unknown msg type: %s', msg[RequestField.TYPE])
        except:
            Logger.exception('deal request failed: %s', str(msg))

    # 等待任务结束
    global RunTaskThread
    if RunTaskThread is not None:
        RunTaskThread.join()

    # 结束前夕，报告退出
    ReportExit()

    Logger.info('agent exit', AGENT_ID)


def Terminate(sig, extra):
    global AgentStopped
    AgentStopped = True
    TryStopTask()
    Logger.info("signaled by %d", sig)


signal.signal(signal.SIGINT, Terminate)
signal.signal(signal.SIGTERM, Terminate)

if __name__ == '__main__':
    StartHeartBeatThread()
    Dispatch()
