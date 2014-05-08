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

def get_query():
  return SimpleQuery()

def get_friends_with_twitterapi(user_name):
  global API
  if API is None:
    import twitter
    API = twitter.Api(consumer_key = credential['consumer_key'],
                    consumer_secret = credential['consumer_secret'],
                    access_token_key = credential['access_token_key'],
                    access_token_secret = credential['access_token_secret'])


  try:
    if API.GetUser(screen_name = user_name).friends > 200:
      raise Exception
    friends = API.GetFriends(screen_name = user_name)
    return [{'user_id': f.screen_name, 'user_name': f.name} for f in friends]
  except Exception, e:
    global get_friends
    get_friends = get_friends_with_httpapi
    try:
      res = get_friends(user_name)
    except Exception as e:
      return None
    return res


def get_friends_with_httpapi(user_name):
  global SESSION
  if SESSION is None:
    SESSION = Session(username = dic['username'], passwd = dic['passwd'])
    SESSION.connect()
  
  has_more = True
  cursor = -1
  friends_list = []
  count = 0

  while has_more and count < 200:
    has_more, cursor, friends = SESSION.get_friends(user_name, cursor)
    count += len(friends)
    friends_list.extend(friends)

  for f in friends_list:
    f['user_id'] = f['user_id'][1:]
    print "#", f

  return friends_list

get_friends = get_friends_with_twitterapi

def get_friend_in_database(friends): 
  Q = get_query() 
  return Q.get_all_in_database(friends)

def get_recommended(friends):
  Q = get_query()
  rec = Q.get_all_similar_users(friends)
  return [x[1] for x in rec]

def filter_user(user):
  return {'description':user.description,
          'followers': user.followers_count,
          'friends': user.friends_count,
          'name': user.name,
          'image_url': user.profile_image_url,
          'user_name': user.screen_name,
          }

def try_get_from_database(screen_name):
  logger.D('using database')
  Q = get_query()
  res = Q.get_user(screen_name)
  if res is not None and res[3] is not None:
    return {'description' : res[2],
            'name' : res[1],
            'user_name' : res[0],
            'image_url' : "../images/images/" + res[3]}
  return None 
  
def get_users(user_list):
  rst = []
  for user in user_list:
    res = try_get_from_database(user)

    if res is None:
      try:
        logger.D('using twitter API')
        rst.append(filter_user(API.GetUser(screen_name = user)))
      except Exception as e:
        print e
    else:
      rst.append(res)
  return rst
