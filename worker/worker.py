import sys, time, datetime, random, signal, pymongo

id=random.getrandbits(32)
if len(sys.argv)>1:
  id=sys.argv[1] 

def_path="/home/jhosan/knobas/"
log_path=def_path+"logs/worker."+id+".log"
log_file=open(log_path,'a')
log_file.write(str(datetime.datetime.now())+" worker "+id+" started.")
task_in_progress=False
task=None
dbname="knobas"
db=pymongo.Connection("127.0.0.1:3333")[dbname]

def sigusr1_handler(signal,frame):
  while task_in_progress:
    time.sleep(0.2) 
  log_file.write(str(datetime.datetime.now())+" worker "+id+" stopped by SIGUSR1\n")
  log_file.close()
  exit(0)
def sigusr2_handler(signal,frame):
  if not task_in_progress:
    task['status']="new"
    task['result']="interrupted by SIGUSR2"
    db.worker_queue.save(task) 
  log_file.write(str(datetime.datetime.now())+" worker "+id+" stopped by SIGUSR2\n")
  log_file.write("task that was in progress: "+str(task)+"\n")
  log_file.close()
  exit(0)
   
signal.signal(signal.SIGUSR1, sigusr1_handler)
signal.signal(signal.SIGUSR2, sigusr2_handler)

id=random.getrandbits(32)
if len(sys.argv)>1:
  id=sys.argv[1] 

while True:
  currtime=str(datetime.datetime.now())
  task_in_progress=True  
  task=db.worker_queue.find_and_modify(
    query={"status":"new"},
    update={"$set":{"status":"in_progress","time_taken":currtime,"worker_id":id}},
    upsert=False,
    sort={"priority":1,"time_start":1})
  if task == None:
    task_in_progress=False
    time.sleep(10)
    continue
  task['time_taken']=currtime
  task['status']="in_progress"
  task['worker_id']=id
  if task['type'] == "monitoring_test":
    f = open(task['data'],'w')
    f.write(task['time_start'])
    f.close() 
    task['status']="done"
    task['result']="file created"
    task['time_finished']=str(datetime.datetime.now())
    db.worker_queue.remove({"_id":task["_id"]})
    db.worker_queue_log.insert(task)
    task_in_progress=False
    continue
