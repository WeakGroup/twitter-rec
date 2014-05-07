import sqlite3
import pickle

con = sqlite3.connect("twitter_db.db")

cur = con.cursor()

cur.execute("SELECT * FROM top_similar")

res = cur.fetchall()

for r in res:
  if r[0] == u"Fenng":
    print r

print len(res)

con.commit()
con.close()
