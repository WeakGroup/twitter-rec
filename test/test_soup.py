from twitter_rec import Api 
import time
from bs4 import BeautifulSoup as BS 


USERNAME = "liaoyisheng89@sina.com"
PASSWD = "bigdata"

s = Api.Session(USERNAME, PASSWD, debug=False)
s.connect()

def test_get_followers():
  _ = s.read("https://twitter.com/AllenboChina/followers")
  soup = BS(_) 
  
  divs = soup.find_all("div", class_="stream-item-header")
  print len(divs) 
  
  for i in divs:
    name = i.find('strong').string
    id = i.find('span').string
    print name, id


test_get_followers()
