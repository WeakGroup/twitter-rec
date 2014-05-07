import sqlite3
import pickle

path = "/ssd/yisheng/tables/"
con = sqlite3.connect(path + "bigdata.db")
data_path = "../data/following_tuple"

with open(data_path) as f:
  ft = pickle.load(f)

cur = con.cursor()
print "begin interting following table..."
cur.executemany("INSERT INTO following VALUES (?, ?)", ft)

con.commit()
con.close()
