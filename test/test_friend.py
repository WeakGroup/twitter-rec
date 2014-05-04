from twitter_rec import Api 
import time


USERNAME = "liaoyisheng89@sina.com"
PASSWD = "bigdata"

s = Api.Session(USERNAME, PASSWD, debug=False)
s.connect()

s.get_friends()
