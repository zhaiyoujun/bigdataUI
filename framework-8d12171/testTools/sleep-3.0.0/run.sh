#!/bin/bash

cd $(dirname $0)
. ../task.info
. ../controller.info

if [ "x$length" == "x" ]; then
	length=100
fi

for i in `seq $length`
do
    echo "REPORT llts_tools is running $i / $length" >> report.log
    echo "STDOUT llts_tools is running $i / $length"
    echo "STDERR llts_tools is running $i / $length" 1>&2
    sleep 1
done

if [ "x$code" == "x" ]; then
    code=0
fi

exit $code
