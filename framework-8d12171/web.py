# coding: utf8

import json
import os
import sys

import zmq

import config
from const import RequestField, RequestType
from flask import Flask, jsonify
from flask import redirect
from flask import render_template
from flask import request
from log import InitLogging
from net import Connect, SendAndRecv
from toolPool import splitToolname

InitLogging(config.WEB_LOG_FILE)
app = Flask(__name__)

reqSock = Connect(stype=zmq.REQ, ip=config.CONTROLLER_IP, port=config.CONTROLLER_REP_PORT)


@app.route('/')
def index():
    return redirect("/task", code=302)


@app.route('/agent')
def agentPage():
    return render_template('agent.html')


@app.route('/tool')
def toolPage():
    return render_template('tool.html')


@app.route('/task')
def taskPage():
    return render_template('task.html')


@app.route('/api/task/submit', methods=['POST'])
def taskSubmit():
    operation, version = splitToolname(request.form.get('operation'))
    tags = request.form.getlist('agentTag')
    names = request.form.getlist('paramName')
    values = request.form.getlist('paramValue')
    req = {
        RequestField.TYPE: RequestType.TASK_SUBMIT,
        RequestField.AGENT_TAG: tags,
        RequestField.OPERATION: operation,
        RequestField.OPERATION_VERSION: version
    }
    for i in xrange(len(names)):
        name = names[i].strip()
        if name == '': continue
        req[name] = values[i]
    reply = SendAndRecv(reqSock, req)
    return jsonify(reply)


@app.route('/api/task/stat', methods=['GET'])
def taskStat():
    response = SendAndRecv(reqSock, {RequestField.TYPE: RequestType.TASK_STATISTIC})
    return jsonify(response)


@app.route('/api/task', methods=['GET'])
def tasks():
    response = SendAndRecv(reqSock, {
        RequestField.TYPE: RequestType.TASK_DETAILS,
        RequestField.OFFSET: request.args.get('offset', 0),
        RequestField.LIMIT: request.args.get('limit', 50),
        RequestField.FATHER_ID: request.args.get('fatherId', None),
        RequestField.DEEP: 1
    })
    return jsonify({'data': {'rows': response['tasks'], 'total': response['total']}})


@app.route('/api/task/kill', methods=['POST'])
def taskKill():
    taskId = request.form.get('taskId')
    reply = SendAndRecv(reqSock, {RequestField.TYPE: RequestType.TASK_KILL, RequestField.TASK_ID: taskId})
    return jsonify(reply)


@app.route('/api/agent/stat', methods=['GET'])
def agentStat():
    response = SendAndRecv(reqSock, {RequestField.TYPE: RequestType.AGENT_STATISTIC})
    return jsonify(response)


@app.route('/api/agent', methods=['GET'])
def agents():
    response = SendAndRecv(reqSock, {RequestField.TYPE: RequestType.AGENT_DETAILS})
    code = response.pop(RequestField.CODE)
    for agentId, agent in response.items():
        agent[RequestField.AGENT_ID] = agentId
    agents = response.values()
    agents.sort(key=lambda t: t[RequestField.AGENT_ID])
    return jsonify({'data': agents})


@app.route('/api/tool', methods=['GET'])
def tools():
    response = SendAndRecv(reqSock, {RequestField.TYPE: RequestType.TOOL_DETAILS})
    code = response.pop(RequestField.CODE)
    tools = sum(response.values(), [])
    return jsonify({'data': tools})


def makeToolPath(operation, version):
    filename = operation + (('-' + version) if version else '') + '.tar.gz'
    return os.path.join(config.TOOLS_DIR, filename)


@app.route('/api/tool', methods=['POST'])
def addTool():
    operation = request.form.get('operation')
    version = request.form.get('version')
    file = request.files['tar']
    if not operation or not version or not file:
        return jsonify({RequestField.CODE: -1})  # 缺少必要参数
    path = makeToolPath(operation, version)
    if os.path.exists(path):
        return jsonify({RequestField.CODE: -2})  # 已经存在了，不允许覆盖
    file.save(path)
    return jsonify({RequestField.CODE: 0})


@app.route('/api/tool/del', methods=['POST'])
def delTool():
    operation = request.form.get('operation')
    version = request.form.get('version')
    path = makeToolPath(operation, version)
    try:
        if os.path.exists(path):
            os.remove(path)
        return jsonify({RequestField.CODE: 0})
    except:
        return jsonify({RequestField.CODE: -1})  # 删除出错了


@app.route('/api', methods=['POST'])
def common():
    req = json.loads(request.form.get('request'))
    res = SendAndRecv(reqSock, req)
    return jsonify(res)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '-H', '--help'):
        print 'Usage: python web.py <host> <port>'
        sys.exit(1)

    host = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    app.run(host=host, port=port, debug=True, use_reloader=False)
