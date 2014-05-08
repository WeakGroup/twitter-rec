import sqlite3
import pickle

con = sqlite3.connect("../data/twitter_db.db")

cur = con.cursor()

cur.execute("SELECT * FROM celebrities")

res = cur.fetchall()


print len(res)

con.commit()
con.close()
