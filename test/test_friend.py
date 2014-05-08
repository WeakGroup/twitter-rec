from twitter_rec import Api 
import time


USERNAME = "liaoyisheng89@sina.com"
PASSWD = "bigdata"

s = Api.Session(USERNAME, PASSWD, debug=False)
s.connect()
has_more = True
cursor = -1

while has_more:
  has_more, cursor, users = s.get_friends('Dropbox', cursor)
  for u in users:
    print u
