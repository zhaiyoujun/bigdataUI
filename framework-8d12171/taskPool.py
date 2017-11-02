# coding: utf8

import copy
import logging
import random
import string
import time

import config
from const import RequestField, TaskStatus, TaskStatusLevel

Logger = logging.getLogger('')


def _cmp(a, b, cmp):
    if a is None:
        return b
    if b is None:
        return a
    return cmp(a, b)


def _min(a, b):
    return _cmp(a, b, min)


def _max(a, b):
    return _cmp(a, b, max)


class TaskPool(object):
    _tasks = {}
    _status = {
        TaskStatus.WAITING: [],
        TaskStatus.DISPATCHED: [],
        TaskStatus.PREPARING: [],
        TaskStatus.RUNNING: [],
        TaskStatus.ENDED: [],
        TaskStatus.FINISHED: []
    }
    _lastClean = None  # 上次检查清理过期任务的时间

    # 记录每个id的子id
    _childTasks = {}

    @classmethod
    def query(cls, msg):
        for id, task in cls._tasks.items():
            matched = True
            for field, value in msg.items():
                if field == RequestField.TYPE:
                    continue
                if field not in task or value != task[field]:
                    matched = False
                    break
            if matched:
                return task
        return None

    @classmethod
    def queryClan(cls, msg):
        tasks = cls.getClan(msg[RequestField.TASK_ID])
        if len(tasks) == 0:
            return None

        result = {
            RequestField.SUBMIT_TIME: None,
            RequestField.FINISH_TIME: None,
            RequestField.CLAN_TASKS: {},
            RequestField.CLAN_STATISTIC: {
                TaskStatus.WAITING: 0,
                TaskStatus.DISPATCHED: 0,
                TaskStatus.PREPARING: 0,
                TaskStatus.RUNNING: 0,
                TaskStatus.ENDED: 0,
                TaskStatus.FINISHED: 0
            }
        }

        allFinished = True
        for task in tasks:
            result[RequestField.SUBMIT_TIME] = _min(result[RequestField.SUBMIT_TIME], task[RequestField.SUBMIT_TIME])
            result[RequestField.CLAN_TASKS][task[RequestField.TASK_ID]] = task
            result[RequestField.CLAN_STATISTIC][task[RequestField.STATUS]] += 1

            if not allFinished or RequestField.FINISH_TIME not in task:
                allFinished = False
                continue
            result[RequestField.FINISH_TIME] = _max(result[RequestField.FINISH_TIME], task[RequestField.FINISH_TIME])

        if not allFinished:
            result[RequestField.FINISH_TIME] = None

        return result

    @classmethod
    def kill(cls, id):
        task = cls._tasks[id]
        Logger.info('task %s change status %s => %s', id, task[RequestField.STATUS], TaskStatus.FINISHED)
        task[RequestField.STATUS] = TaskStatus.FINISHED
        task[RequestField.KILLED] = 'TRUE'
        task[RequestField.FINISH_TIME] = time.time()
        cls._status[TaskStatus.WAITING].remove(id)
        cls._status[TaskStatus.FINISHED].append(id)
        cls._tasks[id] = task
        Logger.info('task %s updated: %s', id, str(task))
        return task

    @classmethod
    def report(cls, task):
        id = task[RequestField.TASK_ID]
        old = cls._tasks[id]
        if TaskStatusLevel[old[RequestField.STATUS]] > TaskStatusLevel[task[RequestField.STATUS]]:
            Logger.warning('task %s cannot change status %s => %s', id, old[RequestField.STATUS],
                           task[RequestField.STATUS])
            raise Exception('status level cannot be reduced')
        if old[RequestField.STATUS] != task[RequestField.STATUS]:
            Logger.info('task %s change status %s => %s', id, old[RequestField.STATUS], task[RequestField.STATUS])
        cls._status[old[RequestField.STATUS]].remove(id)
        cls._status[task[RequestField.STATUS]].append(id)
        cls._tasks[id] = copy.deepcopy(task)
        cls._tasks[id].pop(RequestField.TYPE, None)
        cls._tasks[id].pop(RequestField.CODE, None)
        Logger.debug('task %s updated: %s', id, str(task))
        return task

    @classmethod
    def new(cls, task):
        id = 'TASK_' + str(time.time()) + '_' + ''.join(random.choice(string.letters) for x in range(5))
        task[RequestField.TASK_ID] = id
        task[RequestField.STATUS] = TaskStatus.WAITING
        task[RequestField.SUBMIT_TIME] = time.time()
        cls._status[TaskStatus.WAITING].append(id)
        cls._tasks[id] = copy.deepcopy(task)
        cls._tasks[id].pop(RequestField.TYPE, None)
        cls._tasks[id].pop(RequestField.CODE, None)
        Logger.info('new task %s: %s', id, str(task))
        # childTask
        if RequestField.FATHER_ID in task:
            fid = task[RequestField.FATHER_ID]
            if fid not in cls._tasks:
                Logger.warning("unknown father task '%s' for new task '%s'", fid, id)
                cls._tasks[id].pop(RequestField.FATHER_ID)
            else:
                if fid not in cls._childTasks:
                    cls._childTasks[fid] = []
                cls._childTasks[fid].append(id)
                Logger.info("%s has new child task %s", fid, id)
        return task, len(cls._status[TaskStatus.WAITING]) == 1

    @classmethod
    def hasWaiting(cls):
        return len(cls._status[TaskStatus.WAITING]) > 0

    @classmethod
    def findWaiting(cls, agentId, agentTags):
        for id in cls._status[TaskStatus.WAITING]:
            taskTags = cls._tasks[id].get(RequestField.AGENT_TAG)
            if type(taskTags) != list and type(taskTags) != tuple:
                taskTags = []
            if sum([1 if t in agentTags else 0 for t in taskTags], 0) == len(taskTags):
                return id
        return None

    @classmethod
    def fetchWaiting(cls, agentId, agentTags):
        id = cls.findWaiting(agentId, agentTags)
        if id is None:
            return None
        task = cls._tasks[id]
        cls._status[TaskStatus.WAITING].remove(id)
        cls._status[TaskStatus.DISPATCHED].append(id)
        task[RequestField.STATUS] = TaskStatus.DISPATCHED
        task[RequestField.AGENT_ID] = agentId
        Logger.info('task %s change status %s => %s', id, TaskStatus.WAITING, TaskStatus.DISPATCHED)
        Logger.info('agent %s fetch task %s', agentId, id)
        return task

    @classmethod
    def getChildren(cls, id):
        if id not in cls._childTasks:
            return []
        tasks = []
        for cid in cls._childTasks[id]:
            child = cls._tasks[cid]
            childStatus = child[RequestField.STATUS]
            if childStatus != TaskStatus.ENDED and childStatus != TaskStatus.FINISHED:
                tasks.append(cid)
        return tasks

    @classmethod
    def getClan(cls, id):
        result = []

        def _getClan(r):
            if r not in cls._tasks:
                return
            result.append(cls._tasks[r])
            if r not in cls._childTasks:
                return
            for cid in cls._childTasks[r]:
                _getClan(cid)

        _getClan(id)
        return result

    @classmethod
    def getTaskFamily(cls, id):
        result = [id, ]
        if id in cls._childTasks:
            for cid in cls._childTasks[id]:
                result += cls.getTaskFamily(cid)
        return result

    @classmethod
    def cleanTaskFamily(cls, id):
        family = cls.getTaskFamily(id)
        for cid in family:
            if cls._tasks[cid][RequestField.STATUS] != TaskStatus.FINISHED:
                return False
        Logger.info("will clean task family '%s'", id)
        for cid in family:
            cls._status[TaskStatus.FINISHED].remove(cid)
            task = cls._tasks.pop(cid)
            cls._childTasks.pop(cid, None)
            Logger.info('task %s is removed %s' % (id, task))
        return True

    @classmethod
    def cleanTasks(cls):
        now = time.time()
        if cls._lastClean is not None and now - cls._lastClean < 60 * 60:
            return  # 上次检查还没过去一个小时，不用检查的这么频繁
        taskKeepSeconds = config.TASK_KEEP_HOURS * 60 * 60
        for id in cls._status[TaskStatus.FINISHED]:
            task = cls._tasks[id]
            if RequestField.FATHER_ID not in task and time.time() - task[RequestField.FINISH_TIME] > taskKeepSeconds:
                cls.cleanTaskFamily(id)
        cls._lastClean = now

    @classmethod
    def statistic(cls):
        report = {}
        for status in cls._status.keys():
            report[status] = len(cls._status[status])
        return report

    @classmethod
    def details(cls, offset, limit, fatherId, deep):
        Logger.debug('query tasks, offset=%d, limit=%d, fatherId=%s, deep=%d', offset, limit, fatherId, deep)

        def _family(task, deep):
            fids = []
            while RequestField.FATHER_ID in task and len(fids) < deep:
                fids.append(task[RequestField.FATHER_ID])
                task = cls._tasks[task[RequestField.FATHER_ID]]
            return fids

        def _filter(task, fatherId, deep):
            if deep == 0:
                return task[RequestField.TASK_ID] == fatherId
            if fatherId is None:
                return len(_family(task, deep)) < deep
            return fatherId in _family(task, deep)

        result = []
        for task in cls._tasks.values():
            if _filter(task, fatherId, deep):
                result.append(copy.deepcopy(task))

        result.sort(key=lambda t: t[RequestField.SUBMIT_TIME], reverse=True)
        return {'tasks': result[offset:offset + limit], 'total': len(result)}
