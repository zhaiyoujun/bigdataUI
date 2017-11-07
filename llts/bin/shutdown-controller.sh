#!/bin/sh

function KillAll() {
	ps aux | grep -i "$1" | grep -i "$2" | grep -v grep | awk '{print $2}' | xargs kill > /dev/null 2>&1
	while true
	do
		ps aux | grep -i "$1" | grep -i "$2" | grep -v grep > /dev/null 2>&1
		if [ $? -ne 0 ]; then
			return
		fi
		sleep 1
		echo "waiting for: $1"
	done
}

cd $(dirname $0)/..
ID=$(pwd)

KillAll 'python web.py'        "$ID"
KillAll 'python controller.py' "$ID"
