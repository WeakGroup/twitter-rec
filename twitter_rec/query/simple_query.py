import numpy as np
import pickle
import sqlite3
import itertools

from twitter_rec import settings
from twitter_rec.util import logger

class SimpleQuery(object):
  def __init__(self):
    self.con = sqlite3.connect(settings.DB_PATH)
    logger.D('Database ready')

  def __del__(self):
    self.con.close()

  def get_all_in_database(self, friends):
    cur = self.con.cursor()
    res = []
    for cname in friends:
      user = cur.execute("SELECT * FROM celebrities WHERE screen_name is ?", (cname,)).fetchone()
      if user is not None:
        res.append(cname)

    return res
    

  # Fetch all similar celebrities of given celebrities.
  def get_all_similar_users(self, celebrities, limit = 20):
    cur = self.con.cursor()
    res = [] 
    for cname in celebrities:
      res.append(cur.execute("SELECT * FROM top_similar WHERE screen_name is ?",
                            (cname,)).fetchall())
    
       
    res = list(itertools.chain.from_iterable(res))

    # Exclude the users who are within query celebrities
    res = [r for r in res if r[1] not in celebrities]
    
    # Sort the users by similarity scores.
    res = sorted(res, key=lambda a:a[2])[::-1]
    return res[:limit]
 
  def get_user(self, screen_name):
    cur = self.con.cursor()
    print screen_name
    res = cur.execute("SELECT * FROM new_celebrities WHERE screen_name = ?", (screen_name,)).fetchone()
    return res

if __name__ == '__main__':
  query_celebrities = ['Yelp', 'Fenng']

  celebrities = SimpleQuery().get_all_in_database(query_celebrities)
  for c in celebrities:
    print c
  similar_users = SimpleQuery().get_all_similar_users(query_celebrities)
  for u in similar_users:
    print u
