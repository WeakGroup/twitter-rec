import os
import re
import cookielib
import urllib2
import urllib
import httplib, StringIO
from twitter_rec.debug import VerboseHTTPHandler 
from twitter_rec.util import logger
from twitter_rec.util import unique_order
from bs4 import BeautifulSoup as BS
import simplejson as json

URL = "https://twitter.com"


class Session(object):
  """ Twitter api session """
  def __init__(self, username, passwd, user_agent = None, debug=False):
    self._username = username
    self._passwd = passwd

    if user_agent is None:
      # fake a user agent, some websites (like google) don't like automated exploration
      user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    self._user_agent = user_agent
    self._cj = None
    self._session = None
    self._debug = debug

  def connect(self):
    self._cj = cookielib.CookieJar() 

    if self._debug:
      self._session = urllib2.build_opener(VerboseHTTPHandler,
                                           urllib2.HTTPCookieProcessor(self._cj))
    else:
      self._session = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cj))
    
    _ = dict(self._session.addheaders)
    _['User-Agent'] = self._user_agent
    _['accept-language'] = "zh-CN,zh;q=0.8,en;q=0.6,et;q=0.4,zh-TW;q=0.2" 

    self._session.addheaders = list(_.items())
    
    info = self._session.open(URL)  

    if info.code != 200:
      raise Exception, "Can not access Twitter homepage!"

    content = info.read()
    matched = re.search(r'"authenticity_token" value="([a-zA-Z0-9]*)"', content) 

    assert matched is not None

    # Extract access token from content.
    atoken = matched.group(1)

    form = urllib.urlencode({ "session[username_or_email]" : self._username,
                              "session[password]" : self._passwd,
                              "return_to_ssl" : "true",
                              "scribe_log" : "",
                              "remember_me" : "1",
                              "redirect_after_login" : "/",
                              "authenticity_token" : atoken}
                              )
    
    info = self._session.open(URL+ "/sessions", form) 

    # Check if it's directed to error page.
    if "error" in info.url:
      raise Exception, "Username or password error!"

  def _parse_user(self, source):
    def _convert_string_to_int(number):
      number = number.replace(',', '')
      if number.endswith('K') or number.endswith('k'):
        return int(float(number[:-1]) * 1000)
      if number.endswith('M') or number.endswith('m'):
        return int(float(number[:-1]) * 1000000)
      else:
        return int(number)
    
    soup = BS(source)

    title = soup.find("title").string
    _ = re.search(u'(.*) \((.*)\) on Twitter', title)

    user_name = unicode(_.group(1))
    user_id = unicode(_.group(2))

    try:
      friends = str(soup.find("a", class_ = "js-nav", 
                              attrs={'data-nav':'following', 
                                     "data-element-term" : "following_stats"}).strong.string)
    except AttributeError:
      friends = str(soup.find("a", class_ = "js-nav", 
                              attrs={'data-nav':'following'}).find_all("span")[1].string)
    
    friends = _convert_string_to_int(friends) 
    #print "friends :", friends
    
    try:
      followers = str(soup.find("a", class_ = "js-nav", 
                                attrs={"data-nav" : "followers", 
                                       "data-element-term" : "follower_stats"}).strong.string)
    except AttributeError:
      followers = str(soup.find("a", class_ = "js-nav", 
                                attrs={"data-nav":"followers"}).find_all("span")[1].string)

    followers = _convert_string_to_int(followers)

    return {'user_id':user_id, 
            'user_name':user_name,
            'friends':friends, 
            'followers':followers}


  def _parse_friends(self, source):
    soup = BS(source) 
    divs = soup.find_all("div", class_="stream-item-header")
    users = []

    for i in divs:
      user_name = i.find('strong').string
      user_id = i.find('span', class_ = "username").string
      users.append({'user_id' : user_id, 'user_name' : user_name})
    
    return users
   
  def get_user(self, user_id):
    url = '/%s' % user_id
    logger.D('url=%s', url)
    page = self.read(url)

    return self._parse_user(page)
   

  def get_friends(self, user_id):
    url = '/%s/following' % user_id

    logger.D('url=%s', url)
    page = self.read(url)
    friends = self._parse_friends(page)
    return friends

  # Parse followers style1
  def _try_parse_style1(self, soup):
    usernames = soup.find_all("strong", class_="fullname js-action-profile-name")
    userids = soup.find_all("span", class_="username js-action-profile-name")
    if len(usernames) == 0:
      raise Exception, "style1 error?"
    return usernames, userids

  # Parse followers style2
  def _try_parse_style2(self, soup):
    usernames = soup.find_all("a", class_="js-action-profile-name")
    userids = soup.find_all("a", class_="ProfileCard-screennameLink")
    return usernames, userids

  def _parse_followers(self, html):
    soup = BS(html)
    try:
      usernames, userids = self._try_parse_style1(soup)
    except Exception as e:
      usernames, userids = self._try_parse_style2(soup)

    _ = zip(userids, usernames)
    users = []
    for u in _:
      users.append({'user_id' : u[0].text.strip(), 'user_name' : u[1].text.strip()})
    return users

  def get_followers(self, user_id, cursor = -1):
    """ Get followers of one user. Returns a tuple.
    # t[0] : Whether has more followers to get.
    # t[1] : Updated cursor. Pass to next function call.
    # t[2] : Followers.
    """
    url = '/%s/followers/users?cursor=%s' % (user_id, cursor)
    page = self.read(url)
    js = json.loads(page)
    has_more = js['has_more_items']
    updated_cursor = js['cursor']
    items_html = js['items_html']
    return has_more, updated_cursor, self._parse_followers(items_html) 


  def _save_page(self, page, path):
      with open(path, 'w') as f:
          print >> f, page

  def read(self, url, post_data = None):
    try:
      return self._session.open(URL + url, post_data).read()
    except Exception, e:
      print e
