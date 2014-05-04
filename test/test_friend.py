from twitter_rec import Api 
import time


USERNAME = "liaoyisheng89@sina.com"
PASSWD = "bigdata"

s = Api.Session(USERNAME, PASSWD, debug=False)
s.connect()


info = s.read("/")
print info

"""
users = s.get_friends()
for user in users:
    print user['user_name'], user['user_id']
"""
