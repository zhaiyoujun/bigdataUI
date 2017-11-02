#!/bin/sh

cd $(dirname $0)

. ../controller.info
. ../task.info

export CONTROLLER_ADDRESS
export AGENT_IP
export __TASK_ID__
export __OPERATION__
export __OPERATION_VERSION__
export __VISITOR__
export __VISITOR_TOKEN__

export CalcCount
export WorkerCount
export Port
export MasterAddr

python main.py > report.log 2>&1

RET=$?

if [ "x" != "x$Wait" ]; then
    sleep $Wait
fi

exit $RET