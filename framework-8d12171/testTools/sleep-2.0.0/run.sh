#!/bin/bash

cd $(dirname $0)
. ../task.info
. ../controller.info

if [ "x$length" == "x" ]; then
	length=100
fi

for i in `seq $length`
do
    echo "llts_tools is running $i / $length" >> report.log 
    sleep 1
done

