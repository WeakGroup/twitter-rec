from twitter_rec import Api 
import time


USERNAME = "liaoyisheng89@sina.com"
PASSWD = "bigdata"

s = Api.Session(USERNAME, PASSWD, debug=False)
s.connect()

counter = 0

while True:
  _ = s.read("https://twitter.com/AllenboChina/followers")
  if "eason" in _:
    print counter 
    counter += 1
  else:
    assert False
