import twitter
import util
from util import logger

class Crawler(object):
    CELEBRITY_THRESHOLD = 5000
    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.credential = util.parse_credential_conf(self.conf_file)
        #self.api = twitter.Api(*self.credential)
        self.api = twitter.Api(consumer_key = self.credential['consumer_key'], consumer_secret = self.credential['consumer_secret'],
                access_token_key = self.credential['access_token_key'], access_token_secret = self.credential['access_token_secret'])

        if self.api.VerifyCredentials():
            logger.I('Twitter crawler gets ready')
        else:
            logger.F('Twitter crawler can\'t get credential')

        self.celebrity = set()
        
    
    def crawl(self):
        users = self.api.GetFriends()
        
        for user in users:
            if user.followers_count >= Crawler.CELEBRITY_THRESHOLD:
                logger.D('%s has %d followers, add to the userhouse', user.name, user.followers_count)
                self.celebrity.add(user)
