#!/bin/bash

echo -e "stopping ble_daemon..."

PID=`ps aux | grep ble_daemon | grep -v grep | grep -v nano | sed 's/miro\ *//' | sed 's/\ .*//'`
if [[ "$PID" != "" ]];
then
	echo "send SIGINT to $PID..."
	kill -SIGINT $PID
	echo "wait for stop..."
	sleep 0.5
	PID=`ps aux | grep ble_daemon | grep -v grep | grep -v nano | sed 's/miro\ *//' | sed 's/\ .*//'`
	[[ "$PID" != "" ]] && {
		echo "send KILL to PID=$PID..."
		kill $PID
		echo "wait for stop..."
		sleep 0.5
		PID=`ps aux | grep ble_daemon | grep -v grep | grep -v nano | sed 's/miro\ *//' | sed 's/\ .*//'`
		[[ "$PID" != "" ]] && { echo -e "unable to stop process $PID"; exit 1; }
	}
	echo -e "...OK"
else
	echo "(not running)"
fi
