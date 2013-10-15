#!/bin/bash
cd /home/jhosan/knobas/code/init/ && source ./settings.sh
mongod --fork --port 3333 --bind_ip 127.0.0.1 --logpath "$FILE_MONGO_LOG" --logappend --pidfilepath "$DIR_MONGO_PID" --dbpath "$DIR_MONGO_DATA" --nohttpinterface
memcached -u memcache -l 127.0.0.1 -d -m 64M -p 3334 -U 0 -P "$DIR_MEMC_PID" -t 1
rm $DIR_WORKER_PID/* > /dev/null
for i in `seq $WORKER_NUM`
do
  python $DIR_WORKER_CODE/worker.py $i &
  echo "$!" > $DIR_WORKER_PID/worker.$i.pid
done
