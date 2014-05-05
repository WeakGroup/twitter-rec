import util
from util import logger
from collections import deque
import time
import os
import pickle
import threading
import Queue
from collections import OrderedDict
import random

from .Api import Session


class Checkpointer(threading.Thread):
    INTERVAL = 10
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path
        if os.path.exists(self.path):
            logger.D('Data already exists, load from %s', self.path)
            with open(self.path) as f:
                self._container, user_list = pickle.load(f)
                logger.D('Load %d celebrities', len(self._container))
                self._user_queue = Queue.Queue()
                for user in user_list:
                    self._user_queue.put(user)
        else:
            self._container = None
            self._user_queue = None
            logger.D('Set data path to %s', self.path)
        
        self.daemon = True
        self.start()

    def get_user_queue(self):
        if self._user_queue is None:
            self._user_queue = Queue.Queue()
        return self._user_queue

    def get_container(self):
        if self._container is None:
            self._container = Container(self)
        return self._container

    def flush(self):
        user_list = []
        for elm in list(self._user_queue.queue):
            user_list.append(elm)
        with open(self.path, 'w') as f:
            logger.D('----------------------Flush to checkpoint file %s------------------------', self.path)
            pickle.dump((self._container, user_list), f, protocol = -1)
    
    def run(self):
        while True:
            time.sleep(Checkpointer.INTERVAL)
            self.flush()


class Container(object):
    def __init__(self, checkpoint):
        self._data = OrderedDict()
        self.incr_count = 0
    
    def add(self, user):
      if user['user_id'] in self._data:
        logger.D('user %s in the userhouse, SKIP', user['user_name'])
        return

      self._data[user['user_id']] = user 
      self.incr_count += 1
      logger.D('Now container gets %d users totally.', self.incr_count)
    
    def __len__(self):
      return len(self._data)
    
    def __contains__(self, user):
      return user['user_id'] in self._data


_lock = threading.Lock()

class Crawler(object):
    CELEBRITY_THRESHOLD = 50000
    CELEBRITY_MAX_COUNT = 100 * 1000

    class Worker(threading.Thread):
      def __init__(self, username, password, task_queue, user_queue, celebrity):
        super(Crawler.Worker, self).__init__()
        self.session = Session(username, password, debug=False) 
        self._task_queue = task_queue 
        self._user_queue = user_queue
        self._celebrity = celebrity
        self.daemon = True

      def run(self):
        self.session.connect()
        logger.D("Thread %s is running.", threading.current_thread())

        while True:
          user = self._task_queue.get()
          logger.D('Get user %s from queue', user['user_id'])
          if user in self._celebrity:
              continue
          user_full = self.session.get_user(user_id = user['user_id'])

          if user_full['followers'] >= Crawler.CELEBRITY_THRESHOLD:
            self._user_queue.put(user_full)
            logger.D('%s has %d followers, add to the userhouse', user_full['user_name'], user_full['followers'])

            with _lock:
              self._celebrity.add(user_full)

            if len(self._celebrity) >= Crawler.CELEBRITY_MAX_COUNT:
              return

    def __init__(self, username_or_email, password, checkpoint, n_threads = 10):
        self.session = Session(username_or_email, password, debug = False)
        self.session.connect()
        self.celebrity = checkpoint.get_container()
        self._user_queue = checkpoint.get_user_queue()
        self._task_queue = Queue.Queue() 
        self._workers = [] 

        for i in range(n_threads):
          self._workers.append(Crawler.Worker(username_or_email, password, self._task_queue, self._user_queue, self.celebrity))

        for w in self._workers:
          w.start()


    def crawl(self):
        if self._user_queue.empty():
          logger.D('There is no reserved user in container, Initialize with liao_easion')
          user_seed = self.session.get_user(user_id = "liao_eason") 
          self._user_queue.put(user_seed)

        while True:
          try:
            cur_user = self._user_queue.get() 
          except IndexError:
            return

          logger.D('## Geting friends of user %s', cur_user['user_id'])
          users = self.session.get_friends(user_id = cur_user['user_id'])
          logger.D('Push %d users to task queue', len(users))

          for u in users:
            if u in self._task_queue.queue or u in self.celebrity:
              continue
            self._task_queue.put(u)
