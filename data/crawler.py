import twitter
import util
from util import logger
from collections import deque
import time

class Crawler(object):
    CELEBRITY_THRESHOLD = 5000
    CELEBRITY_MAX_COUNT = 100 * 1000
    REQUEST_INTERVAL = 10

    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.credential = util.parse_credential_conf(self.conf_file)
        self.api = twitter.Api(consumer_key = self.credential['consumer_key'], consumer_secret = self.credential['consumer_secret'],
                access_token_key = self.credential['access_token_key'], access_token_secret = self.credential['access_token_secret'])

        self.myself = self.api.VerifyCredentials()
        if self.myself:
            logger.I('Twitter crawler gets ready')
        else:
            logger.F('Twitter crawler can\'t get credential')

        self.celebrity = set()
        
    
    def crawl(self):
        queue = deque()
        queue.append(self.myself)
        last_req_time = time.time()
        while True:
            try:
                cur_user = queue.popleft()
            except IndexError:
                return
            logger.D('Geting friends of user %s', cur_user.name)
            now = time.time()
            interval = now - last_req_time
            if interval < Crawler.REQUEST_INTERVAL:
              logger.D('sleep %fs', Crawler.REQUEST_INTERVAL - interval)
              time.sleep(Crawler.REQUEST_INTERVAL - interval)
            last_req_time = time.time()
            users = self.api.GetFriends(user_id = cur_user.id)
            logger.D('Get %d users', len(users))
 
            for user in users:
                if user.followers_count >= Crawler.CELEBRITY_THRESHOLD:
                    if user in queue:
                        continue
                    queue.append(user)
                    self.celebrity.add(user)
                    logger.D('%s has %d followers, add to the userhouse', user.name, user.followers_count)
                    if len(self.celebrity) >= Crawler.CELEBRITY_MAX_COUNT:
                        return
            logger.D('Finish dealing with user %s', cur_user.name)
