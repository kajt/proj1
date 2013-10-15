#!/bin/bash
DEF_DIR="/home/jhosan/knobas"
WORKER_NUM=3
mongod --fork --port 3333 --bind_ip 127.0.0.1 --logpath "$DEF_DIR/logs/mongodb.log" --logappend --pidfilepath "$DEF_DIR/pids/mongodb/" --dbpath "$DEF_DIR/db/mongodb/" --nohttpinterface
rm $DEF_DIR/pids/worker/* > /dev/null
for i in `seq $WORKER_NUM`
do
  python $DEF_DIR/worker/worker.py $i &
  echo "$!" > $DEF_DIR/pids/worker/worker.$i.pid
done
