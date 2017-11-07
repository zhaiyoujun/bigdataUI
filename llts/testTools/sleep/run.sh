#!/bin/bash

cd $(dirname $0)
. ../task.info
. ../controller.info

if [ "x$length" == "x" ]; then
	length=100
fi

sleep $length

