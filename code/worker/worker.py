import sys
import time
import datetime
import random
import signal
import os
######## to be changed
sys.path.append('/home/jhosan/knobas/code/common/')
from common import *

def sigusr1_handler(signal,frame):
  while task_in_progress:
    time.sleep(0.2)
  write_work_log(id,"worker_interrupted_sigusr1")
  close_work_log(id)
  exit(0)

def sigusr2_handler(signal,frame):
  if not task_in_progress:
    task=set_worker_task_interrupted_in_mongo(task)
  write_work_log(id,"worker_interrupted_sigusr2","task that was in progress: "+str(task))
  close_work_log(id)
  exit(0)

def task_monitoring_test(task):
  f = open(task['data'],'w')
  f.write(task['time_start'])
  f.close()
  task['status']="done"
  task['result']="file created"
  return task

# registring signal handler 
signal.signal(signal.SIGUSR1, sigusr1_handler)
signal.signal(signal.SIGUSR2, sigusr2_handler)

# defining id of worker process: first argument of command line or random number
id=42
if len(sys.argv)>1:
  id=sys.argv[1] 
else:
  id=random.getrandbits(32)

# writing to logs that worker started
write_work_log(id,"worker_started")

task_in_progress=False
task=None
while True:
  currtime=str(datetime.datetime.now())
  task_in_progress=True  
  task=get_worker_task_from_mongo(id,currtime)
  if task == None:
    task_in_progress=False
    ######## To be changed later
    time.sleep(10)
    continue
  task['time_taken']=currtime
  task['status']="in_progress"
  task['worker_id']=id
  if task['type'] == "monitoring_test":
    task=globals()['task_'+task['type']](task)
    task['time_finished']=str(datetime.datetime.now())
    set_worker_task_finished_in_mongo(task)
    task_in_progress=False
    continue
  task_in_progress=False

