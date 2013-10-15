import pymongo
import datetime
import time
import os.path
import os
import sys
sys.path.append('/home/jhosan/knobas/code/common/')
from common import *

checkstr=str(datetime.datetime.now())
filepath="/home/jhosan/knobas/data/monitoring/test.txt"

set_worker_task_to_mongo("monitoring_test",filepath,ttime_start=checkstr)

# db.worker_queue.insert({
#  "type":"monitoring_test",
#  "data":filepath,
#  "status":"new",
#  "worker_id":"",
#  "priority":"normal",
#  "time_start":checkstr,
#  "time_taken":"",
#  "time_finished":"",
#  "result":""})
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
