#!/bin/bash

cd $(dirname $0)/..
ID=$(pwd)

COUNT=$1
if [ "x$COUNT" == "x" ]; then
	COUNT=30
fi

for i in `seq $COUNT`
do
	python agent.py "$ID" > /dev/null 2>&1 &
done