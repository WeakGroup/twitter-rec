import sqlite3
import pickle

path = "/ssd/yisheng/tables/"
con = sqlite3.connect(path + "bigdata.db")
data_path = "../data/follower_dict"

with open(data_path) as f:
  fd = pickle.load(f)

cur = con.cursor()
print "begin interting..."
cur.executemany("INSERT INTO followers VALUES (?, ?)", fd.items())

con.commit()
con.close()
