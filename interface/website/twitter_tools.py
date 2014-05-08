from twitter_rec.Api import Session
from twitter_rec.query.simple_query import SimpleQuery
from twitter_rec import settings

from twitter_rec.util import logger, parse_conf
import os

pass_file = os.path.join(settings.CONF_DIR, 'pass.conf')
credential_file = os.path.join(settings.CONF_DIR, 'credential.conf')

dic = parse_conf(pass_file)
credential = parse_conf(credential_file)
print credential

SESSION = None
API = None
query = None

def get_query():
  global query
  if query is None:
    query = SimpleQuery()
  return query



def get_friends_with_twitterapi(user_name):
  global API
  if API is None:
    import twitter
    API = twitter.Api(consumer_key = credential['consumer_key'],
                    consumer_secret = credential['consumer_secret'],
                    access_token_key = credential['access_token_key'],
                    access_token_secret = credential['access_token_secret'])


  try:
    friends = API.GetFriends(screen_name = user_name)
    return [{'user_id': f.screen_name, 'user_name': f.name} for f in friends]
  except Exception, e:
    global get_friends
    get_friends = get_friends_with_httpapi
    return get_friends(user_name)


def get_friends_with_httpapi(user_name):
  global SESSION
  if SESSION is None:
    SESSION = Session(username = dic['username'], passwd = dic['passwd'])
    SESSION.connect()
    
  friends = SESSION.get_friends(user_name)
  return friends

get_friends = get_friends_with_twitterapi

def get_friend_in_database(friends): 
  Q = get_query() 
  return Q.get_all_in_database(friends)

def get_recommended(friends):
  Q = get_query()
  rec = Q.get_all_similar_users(friends)
  return [x[1] for x in rec]
