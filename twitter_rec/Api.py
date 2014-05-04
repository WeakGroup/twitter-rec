import os
import re
import cookielib
import urllib2
import urllib
import httplib, StringIO
from .debug import VerboseHTTPHandler 
from .util import logger
from .util import unique_order

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

    self.myself = self._parse_user(info.read())
    return self.myself

  
  def _parse_user(self, source):
    user_id = re.search('data-user-id="([0-9]+)"', source).group(1)
    user_name = re.search('data-screen-name="(\w+)"', source).group(1)
    friends = re.search(r'<span [^>]+>Following</span>\s+<span [^>]+>([0-9]+)</span>', source).group(1)
    followers = re.search(r'<span [^>]+>Followers</span>\s+<span [^>]+>([0-9]+)</span>', source).group(1)

    return {'user_id':user_id, 'user_name':user_name, 'friends':friends, 'followers':followers}

  def _parse_friends(self, source):
    user_ids = unique_order(re.findall('(?<=data-user-id=")[0-9]+"', source))
    user_names = unique_order(re.findall('(?<=data-screen-name=")\w+"', source))
    users = []
    for id, name in zip(user_ids, user_names):
      users.append({'user_id':id, 'user_name': name})
    return users[1:]
   
  def get_user(self. user_id = None, user_name = None):
     if user_id is not None:
      url = '/?id=%s' % user_id
    else:
      if user_name is None:
        user_name = self.myself['user_name']
      url = '/%s' % user_name

    logger.D('url=%s', url)
    page = self.read(url)

    return self._parse_user(page)
   
  def get_friends(self, user_id = None, user_name = None):
    if user_id is not None:
      url = '/?id=%s/following' % user_id
    else:
      if user_name is None:
        user_name = self.myself['user_name']
      url = '/%s/following' % user_name

    logger.D('url=%s', url)
    page = self.read(url)
    
    friends = self._parse_friends(page)
    return friends
    
  
  def _save_page(self, page, path):
      with open(path, 'w') as f:
          print >> f, page

  def read(self, url, post_data = None):
    try:
      return self._session.open(URL + url, post_data).read()
    except Exception, e:
      print e
