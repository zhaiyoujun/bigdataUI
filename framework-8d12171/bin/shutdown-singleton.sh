#!/bin/sh

cd $(dirname $0)

./shutdown-agents.sh
./shutdown-controller.sh
