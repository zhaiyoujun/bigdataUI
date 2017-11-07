# coding: utf8

import json
import os
import random
import sys
import time
import traceback

import zmq


def Connect(stype, addr):
    ctx = zmq.Context.instance()
    sock = ctx.socket(stype)
    sock.setsockopt(zmq.RCVTIMEO, 3000)
    sock.connect(addr)
    return sock


def Bind(stype, port):
    ctx = zmq.Context.instance()
    sock = ctx.socket(stype)
    sock.setsockopt(zmq.RCVTIMEO, 3000)
    address = 'tcp://*:%d' % port
    sock.bind(address)
    return sock


def RecvMsg(sock):
    data = sock.recv_string()
    msg = json.loads(data)
    return msg


def SendMsg(sock, msg):
    data = json.dumps(msg)
    sock.send(data)


def SendAndRecv(sock, msg):
    SendMsg(sock, msg)
    return RecvMsg(sock)


def WaitTask(mgrSock, id):
    print 'waiting task:', id
    while True:
        msg = SendAndRecv(mgrSock, {
            '__TYPE__': 'TASK/QUERY',
            '__TASK_ID__': id,
        })
        if msg['__CODE__'] == 0 and msg['__STATUS__'] in ['FINISHED', 'ENDED']:
            return
        time.sleep(0.1)


def MasterMain():
    port = int(os.getenv('Port', 30000))
    workerCount = int(os.getenv('WorkerCount', 2))
    calcCount = int(os.getenv('CalcCount', 100000))
    controllerAddr = os.getenv('CONTROLLER_ADDRESS')

    mgrSock = Connect(zmq.REQ, controllerAddr)
    dataSock = Bind(zmq.REP, port)
    tasks = []

    for i in xrange(workerCount):
        req = {
            '__TYPE__': 'TASK/SUBMIT',
            '__FATHER_ID__': os.getenv('__TASK_ID__'),
            '__OPERATION__': os.getenv('__OPERATION__'),
            '__OPERATION_VERSION__': os.getenv('__OPERATION_VERSION__'),
            '__VISITOR__': os.getenv('__VISITOR__'),
            '__VISITOR_TOKEN__': os.getenv('__VISITOR_TOKEN__'),
            'MasterAddr': 'tcp://%s:%d' % (os.getenv('AGENT_IP'), port),
            'CalcCount': calcCount
        }
        if req['__VISITOR__'] is None:
            req.pop('__VISITOR__')
            req.pop('__VISITOR_TOKEN__')
        reply = SendAndRecv(mgrSock, req)
        if reply['__CODE__'] == 0:
            tasks.append(reply['__TASK_ID__'])
        else:
            print 'submit task failed:', reply
            sys.exit(1)

    cin = 0
    for i in xrange(len(tasks)):
        while True:
            try:
                msg = RecvMsg(dataSock)
                break
            except:
                traceback.print_exc()
                continue
        SendMsg(dataSock, {'code': 0})
        cin += msg['cin']

    [WaitTask(mgrSock, id) for id in tasks]

    print 'in =', cin
    print 'all =', calcCount, '*', workerCount
    print 'pi =', (cin * 4.0) / (calcCount * workerCount)


def WorkerMain():
    masterAddr = os.getenv('MasterAddr')
    calcCount = int(os.getenv('CalcCount'))

    cin = 0
    for i in xrange(calcCount):
        x = random.random() * 2 - 1
        y = random.random() * 2 - 1
        if x * x + y * y <= 1:
            cin += 1

    sock = Connect(zmq.REQ, masterAddr)
    reply = SendAndRecv(sock, {'cin': cin})

    print 'in =', cin
    print 'all =', calcCount
    print 'reply =', reply


if __name__ == '__main__':
    if os.getenv('MasterAddr') is None:
        MasterMain()
    else:
        WorkerMain()
