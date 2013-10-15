#!/bin/bash
source ./settings.sh
for f in `ls -1 $DIR_WORKER_PID*`
do
  kill -USR1 `cat $f`
  sleep 1
done
for f in `ls -1 $DIR_WORKER_PID*`
do
  if ps -p `cat $f` > /dev/null
  then
    echo "$f not yet exited" 
    sleep 1
  else
    echo "removing $f"
    rm $f
  fi
done
if [ -f $DIR_WORKER_PIDworker.*.pid ]
then
  for f in `ls -1 $DIR_WORKER_PID*`
  do
    if ps -p `cat $f` > /dev/null
    then
      kill -USR2 `cat $f`
    else
      echo "removing $f"
      rm $f
    fi
  done
  if [ -f $DIR_WORKER_PIDworker.*.pid ]
  then
    sleep 10
    for f in `ls -1 $DIR_WORKER_PID*`
    do
      if ps -p `cat $f` > /dev/null
      then
        kill `cat $f`
      else
        rm $f
        echo "removing $f"
      fi
    done
    if [ -f $DIR_WORKER_PIDworker.*.pid ]
    then
      sleep 10
      for f in `ls -1 $DIR_WORKER_PID*`
      do
        kill -9 `cat $f`
        rm $f
        echo "removing $f"
      done
    fi
  fi
fi
mongod --shutdown --dbpath "$DIR_MONGO_DATA" 