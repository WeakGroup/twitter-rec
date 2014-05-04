import util
from util import logger
from collections import deque
import time
import os
import pickle

from .Api import Session

class Container(object):
    def __init__(self, path):
        self.path = path
        self.max_incr = 500
        self.incr_count = 0
        if os.path.exists(self.path):
            logger.D('Data already exists, load from %s', self.path)
            with open(self.path) as f:
                self.data = pickle.load(f)
                logger.D('Load %d celebrities', len(self.data))
        else:
            logger.D('Set data path to %s', self.path)
        
    def add(self, user):
        if user in self.data:
            return
        self.incr_count += 1
        if self.incr_count == self.max_incr:
            self._flush()
            self.incr_count = 0

    def _flush(self):
        with open(self.path, 'w') as f:
            pickle.dump(self.data, f, protocol = -1)

    def __len__(self):
        return len(self.data)
            

class Crawler(object):
    CELEBRITY_THRESHOLD = 5000
    CELEBRITY_MAX_COUNT = 100 * 1000

    def __init__(self, username_or_email, password, checkpoint_path):
        self.session = Session(username_or_email, password, debug = False)
        self.myself = self.session.connect()
        if self.myself:
            logger.I('Twitter crawler gets ready')
        else:
            logger.F('Twitter crawler can\'t get credential')

        self.celebrity = Container(checkpoint_path)
    
    def crawl(self):
        queue = deque()
        queue.append(self.myself)
        while True:
            try:
                cur_user = queue.popleft()
            except IndexError:
                return
            logger.D('Geting friends of user %s', cur_user['user_name'])
            users = self.session.get_friends(user_name= cur_user['user_name'])
            logger.D('Get %d users', len(users))
 
            for user in users:
                user_full = self.session.get_user(user_name = user['user_name'])
                if user_full['followers'] >= Crawler.CELEBRITY_THRESHOLD:
                    if user_full in queue:
                        continue
                    queue.append(user_full)
                    self.celebrity.add(user_full)
                    logger.D('%s has %d followers, add to the userhouse', user_full['user_name'], user_full['followers'])
                    if len(self.celebrity) >= Crawler.CELEBRITY_MAX_COUNT:
                        return
            logger.D('Finish dealing with user %s', cur_user[ 'user_name'])
