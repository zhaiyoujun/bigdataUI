# coding: utf8

import json
import logging
import socket

import zmq

import config

Logger = logging.getLogger('')


def GetMyIP(subnet, port=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect((subnet, port))
        IP = s.getsockname()[0]
    except:
        Logger.warning("connect failed while fetch self IP, will use 127.0.0.1")
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


MyIP = GetMyIP(config.SELF_SUBNET)


def RecvMsg(sock, alwaysWait=True):
    while True:
        try:
            msg = sock.recv_json()
            Logger.debug('RecvMsg: %s', str(msg))
            return msg
        except zmq.error.Again, e:
            if not alwaysWait:
                raise e
            Logger.warn("waiting for data to receive")


def SendMsg(sock, msg):
    sock.send_json(msg)
    Logger.debug('SendMsg: %s', str(msg))


def SendAndRecv(sock, msg, alwaysWait=True):
    SendMsg(sock, msg)
    return RecvMsg(sock, alwaysWait)


def Connect(stype=None, ip=None, port=None, address=None):
    ctx = zmq.Context.instance()
    sock = ctx.socket(stype)
    sock.setsockopt(zmq.RCVTIMEO, config.ZMQ_RECV_TIMEOUT)
    if address is None:
        address = 'tcp://%s:%d' % (ip, port)
    sock.connect(address)
    return sock


def Bind(stype=None, port=None, address=None):
    ctx = zmq.Context.instance()
    sock = ctx.socket(stype)
    sock.setsockopt(zmq.RCVTIMEO, config.ZMQ_RECV_TIMEOUT)
    if address is None:
        address = 'tcp://*:%d' % port
    sock.bind(address)
    return sock
