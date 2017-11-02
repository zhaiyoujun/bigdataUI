# coding: utf8

import copy
import logging
import time

import config
from const import RequestField, AgentStatus

Logger = logging.getLogger('')


class AgentPool(object):
    _agents = {}
    _lastCheck = None  # 上次检查 agent 丢失的时间

    @classmethod
    def update(cls, msg):
        agentId = msg[RequestField.AGENT_ID]
        ip = msg[RequestField.AGENT_IP]
        tag = msg[RequestField.AGENT_TAG]
        status = msg[RequestField.AGENT_STATUS]
        if not cls._agents.has_key(agentId):
            Logger.info("new agent %s connected", agentId)
        else:
            oldStatus = cls._agents[agentId][RequestField.STATUS]
            if oldStatus != status:
                Logger.info("agent %s change status %s => %s", agentId, oldStatus, status)

        cls._agents[agentId] = {
            RequestField.STATUS: status,
            RequestField.AGENT_IP: ip,
            RequestField.AGENT_TAG: tag,
            RequestField.TIME: time.time()
        }

    @classmethod
    def exit(cls, agentId):
        if agentId not in cls._agents:
            Logger.warning('unknown agent %s exited', agentId)
        else:
            cls._agents.pop(agentId)
            Logger.info("agent %s exited", agentId)

    @classmethod
    def getTags(cls, agentId):
        if agentId not in cls._agents:
            return None
        return cls._agents[agentId][RequestField.AGENT_TAG]

    @classmethod
    def checkLost(cls):
        now = time.time()
        if cls._lastCheck is not None and (now - cls._lastCheck) * 1000 < config.AGENT_HEARTBEAT_INTERVAL:
            return  # 上次检查还没过去一次心跳周期，不用检查的这么频繁
        # 超过两倍心跳间隔未收到心跳，则认为丢失连接
        isLost = lambda ts: (now - ts) * 1000 > 2 * config.AGENT_HEARTBEAT_INTERVAL
        for agentId, agent in cls._agents.items():
            if agent[RequestField.STATUS] != AgentStatus.LOST and isLost(agent[RequestField.TIME]):
                Logger.info("agent %s change status %s => %s", agentId, agent[RequestField.STATUS], AgentStatus.LOST)
                agent[RequestField.STATUS] = AgentStatus.LOST
        cls._lastCheck = now

    @classmethod
    def statistic(cls):
        report = {
            '__TOTAL__': len(cls._agents),
            AgentStatus.BUSY: 0,
            AgentStatus.FREE: 0,
            AgentStatus.LOST: 0
        }
        for agent in cls._agents.values():
            report[agent[RequestField.STATUS]] += 1
        return report

    @classmethod
    def details(cls):
        return copy.deepcopy(cls._agents)
