#!/bin/bash
MONGODB="knobas"
mongo --port 3333 --host 127.0.0.1 $MONGODB --eval "db.dropDatabase()"
mongo --port 3333 --host 127.0.0.1 $MONGODB --eval "db.createCollection('worker_queue')"
mongo --port 3333 --host 127.0.0.1 $MONGODB --eval "db.createCollection('worker_queue_log',{'capped':'true','autoIndexId':'false','size':5242880})"
