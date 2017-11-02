# coding: utf8

import json
import logging

import zmq

import config
from const import RequestField, RequestType
from log import InitLogging
from net import SendAndRecv, Connect

Logger = logging.getLogger('')

InitLogging(config.CLIENT_LOG_FILE)

if __name__ == '__main__':
    reqSock = Connect(stype=zmq.REQ, ip=config.CONTROLLER_IP, port=config.CONTROLLER_REP_PORT)

    while True:
        cmd = str(raw_input(">>> ")).strip()
        if len(cmd) == 0: continue

        cmds = cmd.split(" ")
        if len(cmds) < 1: continue

        if cmds[0] == RequestType.TASK_SUBMIT:
            request = {RequestField.TYPE: RequestType.TASK_SUBMIT, RequestField.OPERATION: cmds[1]}
            for i in range(2, len(cmds)):
                k, v = cmds[i].split('=', 1)
                request[k] = v
            reply = SendAndRecv(reqSock, request)
            if reply[RequestField.CODE] == 0:
                Logger.info("request accepted, id=%s, request=%s", reply[RequestField.TASK_ID], json.dumps(request, indent=4))
            else:
                Logger.warning("request rejected, code=%s", reply[RequestField.CODE])

        elif cmds[0] == RequestType.TASK_KILL:
            id = cmds[1]
            reply = SendAndRecv(reqSock, {RequestField.TYPE: RequestType.TASK_KILL, RequestField.TASK_ID: id})
            if reply[RequestField.CODE] == 0:
                Logger.info("request accepted, id=%s", id)
            else:
                Logger.warning("request rejected, id=%s, code=%s", id, reply[RequestField.CODE])

        elif cmds[0] == RequestType.TASK_QUERY:
            id = cmds[1]
            request = {RequestField.TYPE: RequestType.TASK_QUERY, RequestField.TASK_ID: id}
            for i in range(2, len(cmds)):
                k, v = cmds[i].split('=', 1)
                request[k] = v
            reply = SendAndRecv(reqSock, request)

            if reply[RequestField.CODE] == 0:
                Logger.info("request accepted, id=%s, task=%s", id, json.dumps(reply, indent=4))
            else:
                Logger.warning("request rejected, id=%s, code=%s", id, reply[RequestField.CODE])

        elif cmds[0] == RequestType.TASK_QUERY_CLAN:
            id = cmds[1]
            request = {RequestField.TYPE: RequestType.TASK_QUERY_CLAN, RequestField.TASK_ID: id}
            reply = SendAndRecv(reqSock, request)

            if reply[RequestField.CODE] == 0:
                Logger.info("request accepted, id=%s, result=%s", id, json.dumps(reply, indent=4))
            else:
                Logger.warning("request rejected, id=%s, code=%s", id, reply[RequestField.CODE])

        elif cmds[0] == RequestType.AGENT_STATISTIC:
            reply = SendAndRecv(reqSock, {RequestField.TYPE: RequestType.AGENT_STATISTIC})
            if reply[RequestField.CODE] == 0:
                Logger.info("request accepted, statistic=%s", json.dumps(reply, indent=4))
            else:
                Logger.warning("request rejected, code=%s", reply[RequestField.CODE])

        elif cmds[0] == RequestType.TASK_STATISTIC:
            reply = SendAndRecv(reqSock, {RequestField.TYPE: RequestType.TASK_STATISTIC})
            if reply[RequestField.CODE] == 0:
                Logger.info("request accepted, statistic=%s", json.dumps(reply, indent=4))
            else:
                Logger.warning("request rejected, code=%s", reply[RequestField.CODE])

        elif cmds[0] == RequestType.TASK_DETAILS:
            reply = SendAndRecv(reqSock, {RequestField.TYPE: RequestType.TASK_DETAILS})
            if reply[RequestField.CODE] == 0:
                Logger.info("request accepted, tasks=%s", json.dumps(reply, indent=4))
            else:
                Logger.warning("request rejected, code=%s", reply[RequestField.CODE])

        elif cmds[0] == 'QUIT':
            break

        else:
            reply = SendAndRecv(reqSock, {RequestField.TYPE: cmds[0]})
            if reply[RequestField.CODE] == 0:
                Logger.info("request accepted, statistic=%s", json.dumps(reply, indent=4))
            else:
                Logger.warning("request rejected, code=%s", reply[RequestField.CODE])
