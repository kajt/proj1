#!/bin/bash
DEF_DIR="/home/jhosan/knobas"
for f in `ls -1 $DEF_DIR/pids/worker/*`
do
  kill -USR1 `cat $f`
  sleep 1
done
for f in `ls -1 $DEF_DIR/pids/worker/*`
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
if [ -f $DEF_DIR/pids/worker/worker.*.pid ]
then
  for f in `ls -1 $DEF_DIR/pids/worker/*`
  do
    if ps -p `cat $f` > /dev/null
    then
      kill -USR2 `cat $f`
    else
      echo "removing $f"
      rm $f
    fi
  done
  if [ -f $DEF_DIR/pids/worker/worker.*.pid ]
  then
    sleep 10
    for f in `ls -1 $DEF_DIR/pids/worker/*`
    do
      if ps -p `cat $f` > /dev/null
      then
        kill `cat $f`
      else
        rm $f
        echo "removing $f"
      fi
    done
    if [ -f $DEF_DIR/pids/worker/worker.*.pid ]
    then
      sleep 10
      for f in `ls -1 $DEF_DIR/pids/worker/*`
      do
        kill -9 `cat $f`
        rm $f
        echo "removing $f"
      done
    fi
  fi
fi
mongod --shutdown --dbpath "$DEF_DIR/db/mongodb" 
