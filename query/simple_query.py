import numpy as np
import pickle
import sqlite3
import itertools

fpath = "/ssd/yisheng/tables/top_20_simi.data"
path = "/ssd/yisheng/tables/"
username = "@shervin"

con = sqlite3.connect(path + "bigdata.db")

with open(fpath) as f:
  top_k_simi, top_k_indices = pickle.load(f)


def get_indices_of_followees(username):
  cur = con.cursor()
  result = cur.execute("SELECT c.celebrity_idx FROM celebrities AS c, followers AS fl,\
                        following AS f WHERE \
                        f.user_idx = fl.user_idx and c.celebrity_idx = f.celebrity_idx and \
                        fl.screen_name = ?", (username,))
  
  return list(itertools.chain.from_iterable(result.fetchall()))

def get_top_k_similarities(indices, k=20):
  assert len(indices) > 0
  first_idx = indices[0]
  local_simi = top_k_simi[first_idx] 
  local_indices = top_k_indices[first_idx]
  
  for i in range(1, len(indices)):
    idx = indices[i]
    local_simi = np.concatenate((local_simi, top_k_simi[idx]), axis=1)
    local_indices = np.concatenate((local_indices, top_k_indices[idx]), axis=1)
  
  si = np.argsort(local_simi)[::-1][:k]
  return local_indices[si]

def get_corresponding_celebrities(c_indices):
  cur = con.cursor()
  result = [] 
  for i in c_indices:
    result.append(cur.execute("SELECT * FROM celebrities WHERE celebrity_idx = ?", (i,)).fetchone())
  return result

  
c_indices = get_indices_of_followees(username)
c_indices = get_top_k_similarities(c_indices)
print get_corresponding_celebrities(c_indices)

con.close()
