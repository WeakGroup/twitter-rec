from mpi4py import MPI
import pickle
import threading
import time
from util import logger
import socket
import os
from Api import Session

USERNAME = "liaoyisheng89@sina.com"
PASSWD = "bigdata"
data_file = "./data/data"


class Container(threading.Thread):
  INTERVAL = 200

  def __init__(self, checkpath):
    super(Container, self).__init__()
    self.checkpath = checkpath
    self.daemon = True
    self._lock = threading.Lock()

    if os.path.exists(self.checkpath):
      logger.D("Loading checkpoint file %s.", self.checkpath)
      with open(self.checkpath) as f:
        self._table = pickle.load(f)
      logger.D("Finish loading checkpoint file %s.", self.checkpath)
    else:
      self._table = {}

  def run(self):
    logger.D("Container checkpoint thread is running")
    
    while True:
      time.sleep(Container.INTERVAL)
      self.flush()
  
  def flush(self):
    with self._lock:
      logger.D("------------ Flush to checkpoint file %s --------------", self.checkpath)
      with open(self.checkpath, "w") as f:
        pickle.dump(self._table, f, protocol = -1)
    
  def is_exist(self, user_id):
    return user_id in self._table

  def add(self, user_id, followers_list):
    if user_id not in self._table:
      self._table[user_id] = []
    with self._lock:
      self._table[user_id].extend(followers_list)


def crawl(target, container, rank):
  session = Session(USERNAME, PASSWD, debug = False)
  session.connect()
  
  for idx, user in enumerate(target):
    if container.is_exist(user):
      logger.D("%s has been cralwed, SKIP.", user)
      continue
    
    has_more = True
    cursor = -1
    count = 0
    round = 0

    try:
      while has_more:
        has_more, cursor, users = session.get_followers(user, cursor)
        count += len(users)
        round += 1

        # Log every 20 rounds.
        if round % 20 == 0:
          logger.D("rank %s adds %d followers to user %s[%s/%s]", rank, count, user, idx, len(target))

        container.add(user, users)
    except Exception as e:
      logger.D("Catched exceptions %s", e)

    logger.D("###### Finished User [%s] ########", user)

  logger.D("Worker Finish")

def main():
  with open(data_file) as f:
    followees = pickle.load(f)
  
  num = len(followees)
  size = MPI.COMM_WORLD.Get_size()
  rank = MPI.COMM_WORLD.Get_rank()
  
  num_per_worker = num / size
  start_idx = num_per_worker * rank

  if rank == size - 1:
    end_idx = num
  else:
    end_idx = start_idx + num_per_worker

  # Path for checkpoint
  checkpath = "checkpt_%s_%s" % (size, rank)

  # The follwees this worker needs to crawl.
  local_followees = followees[start_idx : end_idx]
  
  container = Container(checkpath)
  container.start()
  crawl(local_followees, container, rank)
  MPI.COMM_WORLD.Barrier()


if __name__ == "__main__":
  main()
