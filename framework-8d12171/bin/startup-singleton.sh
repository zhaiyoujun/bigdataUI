#!/bin/sh

cd $(dirname $0)

./startup-agents.sh "$@"
./startup-controller.sh "$@"
