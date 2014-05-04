import util
from util import logger
from collections import deque
import time
import os
import pickle
import threading
import Queue
from collections import OrderedDict

from .Api import Session

class Container(object):
    def __init__(self, path):
        self.path = path
        self.max_incr = 10
        self.incr_count = 0
        self._data = OrderedDict()
        self._last_user = None
        if os.path.exists(self.path):
          logger.D('Data already exists, load from %s', self.path)
          with open(self.path) as f:
            self._data, self._last_user = pickle.load(f)
            logger.D('Load %d celebrities', len(self._data))
        else:
          logger.D('Set data path to %s', self.path)

    def add(self, user):
      if user['user_id'] in self._data:
        return

      self._data[user['user_id']] = user 
      self._last_user = user
      self.incr_count += 1
      logger.D('Now container gets %d users totally.', self.incr_count)

      if self.incr_count % self.max_incr == 0:
        self._flush()

    def _flush(self):
      with open(self.path, 'w') as f:
        logger.D('Flush to checkpoint file %s.', self.path)
        pickle.dump((self._data, self._last_user), f, protocol = -1)
    
    def __len__(self):
      return len(self._data)

    @property
    def last_user(self):
      return self._last_user
    


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

      def run(self):
        self.session.connect()
        logger.D("Thread %s is running.", threading.current_thread())

        while True:
          user = self._task_queue.get()
          user_full = self.session.get_user(user_id = user['user_id'])

          if user_full['followers'] >= Crawler.CELEBRITY_THRESHOLD:
            self._user_queue.put(user_full)
            logger.D('%s has %d followers, add to the userhouse', user_full['user_name'], user_full['followers'])

            with _lock:
              self._celebrity.add(user_full)

            if len(self._celebrity) >= Crawler.CELEBRITY_MAX_COUNT:
              return

    def __init__(self, username_or_email, password, checkpoint_path, n_threads = 10):
        self.session = Session(username_or_email, password, debug = False)
        self.session.connect()
        self.celebrity = Container(checkpoint_path)
        self._user_queue = Queue.Queue() 
        self._task_queue = Queue.Queue() 
        self._workers = [] 

        for i in range(n_threads):
          self._workers.append(Crawler.Worker(username_or_email, password, self._task_queue, self._user_queue, self.celebrity))

        for w in self._workers:
          w.start()


    def crawl(self):
        user_seed = self.celebrity.last_user
        if user_seed is None:
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
          for u in users:
            self._task_queue.put(u)
