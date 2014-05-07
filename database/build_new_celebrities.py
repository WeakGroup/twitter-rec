import sqlite3
import pickle

con = sqlite3.connect("twitter_db.db")
data_path = "../data/celebrity_dict"

with open(data_path) as f:
  cd = pickle.load(f)

cl = [(k,) for k,v in cd.iteritems()]

cur = con.cursor()
print "begin interting celebrity..."
cur.executemany("INSERT INTO celebrities VALUES (?)", cl)

con.commit()
con.close()
