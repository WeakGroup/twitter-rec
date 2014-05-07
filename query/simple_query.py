import numpy as np
import pickle
import sqlite3
import itertools

con = sqlite3.connect("../database/twitter_db.db")
query_celebrities = ['Yelp', 'Fenng']

# Fetch all similar celebrities of given celebrities.
def get_all_similar_users(celebrities):
  cur = con.cursor()
  res = [] 
  for cname in celebrities:
    res.append(cur.execute("SELECT * FROM top_similar WHERE screen_name is ?",
                          (cname,)).fetchall())
  
     
  res = list(itertools.chain.from_iterable(res))

  # Exclude the users who are within query celebrities
  res = [r for r in res if r[1] not in celebrities]
  
  # Sort the users by similarity scores.
  res = sorted(res, key=lambda a:a[2])[::-1]
  return res


similar_users = get_all_similar_users(query_celebrities)
for u in similar_users:
  print u

con.close()
