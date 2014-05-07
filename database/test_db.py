import sqlite3
import pickle

path = "/ssd/yisheng/tables/"
con = sqlite3.connect(path + "bigdata.db")

cur = con.cursor()

res = cur.execute("SELECT * FROM celebrities")
res = res.fetchall()

for r in res:
  print r

con.commit()
con.close()
