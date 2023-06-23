#!/bin/bash

# create file
pid_file="/var/pid/flow.pid"

if [ -f $pid_file ]; then
  echo "Found existing .pid file named $pid_file. Checking."

  # check the pid to see if the process exists
  pgrep -F $pid_file
  pid_is_stale=$?
  old_pid=$( cat $pid_file )
  echo "pgrep check on existing .pid file returned exit status: $pid_is_stale"

  if [ $pid_is_stale -eq 1 ]; then
    echo "PID $old_pid is stale. Removing file and continuing."
    rm $pid_file
  else
    echo "PID $old_pid is still running or pgrep check errored. Exiting."
    exit
  fi
else
  /usr/bin/python3 /bolango/water/flow.py > /var/log/flow.log 2>&1 &
  RETVAL=$?
  PID=$!
  [ $RETVAL -eq 0 ] && echo $PID > $pid_file
fi