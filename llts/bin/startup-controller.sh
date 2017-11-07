#!/bin/bash

cd $(dirname $0)/..
ID=$(pwd)

python controller.py       "$ID" > /dev/null 2>&1 &
python web.py 0.0.0.0 5000 "$ID" > /dev/null 2>&1 &
