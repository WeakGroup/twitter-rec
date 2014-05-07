import sqlite3
import pickle

path = "/ssd/yisheng/tables/"
con = sqlite3.connect(path + "bigdata.db")
data_path = "../data/celebrity_dict"

with open(data_path) as f:
  cd = pickle.load(f)

cl = [(v,k) for k,v in cd.iteritems()]

for c in cl:
  print c

cur = con.cursor()
print "begin interting celebrity..."
cur.executemany("INSERT INTO celebrities VALUES (?, ?)", cl)

con.commit()
con.close()
