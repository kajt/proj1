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
  log_file.write(str(datetime.datetime.now())+" worker "+str(id)+" stopped by SIGUSR1\n")
  log_file.close()
  exit(0)

def sigusr2_handler(signal,frame):
  if not task_in_progress:
    task=set_worker_task_interrupted_in_mongo(task)
  log_file.write(str(datetime.datetime.now())+" worker "+str(id)+" stopped by SIGUSR2\n")
  log_file.write("task that was in progress: "+str(task)+"\n")
  log_file.close()
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

######## TO BE REDEFINED LATER ########
# log path
def_path="/home/jhosan/knobas/data/"
log_path=def_path+"logs/worker."+str(id)+".log"

# writing start note 
log_file=open(log_path,'a')
log_file.write(str(datetime.datetime.now())+" worker "+str(id)+" started.")

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

