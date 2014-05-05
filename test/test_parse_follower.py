import pickle
from twitter_rec import crawler
from twitter_rec.Api import Session
import conf
import simplejson as json
from bs4 import BeautifulSoup as BS

s = Session(conf.USERNAME, conf.PASSWD)
s.connect()

has_more = True
cursor = -1

while has_more:
  has_more, cursor, users = s.get_followers("russellpower", cursor)
  for u in users:
    print u['user_id']

