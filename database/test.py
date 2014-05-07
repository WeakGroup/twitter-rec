import sqlite3
import pickle

path = "/ssd/yisheng/tables/"
con = sqlite3.connect(path + "bigdata.db")

cur = con.cursor()
cur.execute("SELECT count(*) FROM celebrities")
print cur.fetchone()

con.commit()
con.close()
