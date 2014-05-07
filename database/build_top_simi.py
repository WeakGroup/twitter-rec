import sqlite3
import pickle

con = sqlite3.connect("twitter_db.db")

with open("/ssd/yisheng/tables/top_20_simi.data") as f:
  simi, indices = pickle.load(f)

with open("../data/celebrity_dict") as f:
  name_to_ind = pickle.load(f)

ind_to_name = dict([(v, k) for k, v in name_to_ind.iteritems()])

cur = con.cursor()

for ind1 in range(simi.shape[0]):
  cname = ind_to_name[ind1]
  simi_users = []

  for t in range(simi.shape[1]):
    ind2 = indices[ind1, t]
    score = simi[ind1, t]
    simi_users.append((cname, ind_to_name[ind2], score))

  cur.executemany("INSERT INTO top_similar VALUES (?, ?, ?)", simi_users)
  
con.commit()
con.close()
