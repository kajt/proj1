import pymongo
import datetime
import time
import os.path
import os

dbname="knobas"
checkstr=str(datetime.datetime.now())
filepath="/home/jhosan/knobas/data/monitoring/test.txt"

db=pymongo.Connection("127.0.0.1:3333")[dbname]
db.worker_queue.insert({
  "type":"monitoring_test",
  "data":filepath,
  "status":"new",
  "worker_id":"",
  "priority":"normal",
  "time_start":checkstr,
  "time_taken":"",
  "time_finished":"",
  "result":""})
for i in range(5):
  time.sleep(10)
  if os.path.exists(filepath):
    f=open(filepath,'r')
    readline=f.readline()
    if readline == checkstr:
      print "check OK"    
    else:
      print "check failed"
    f.close()
    os.remove(filepath) 
    break
print "finishing"
