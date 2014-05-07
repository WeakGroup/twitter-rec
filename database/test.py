import sqlite3
import pickle

path = "/ssd/yisheng/tables/"
con = sqlite3.connect(path + "bigdata.db")

cur = con.cursor()

cur.execute("""SELECT c.screen_name FROM celebrities as c, followers as fl, following as f WHERE c.celebrity_idx = f.celebrity_idx and fl.user_idx = f.user_idx and fl.screen_name='@Liao_Eason' """)

print cur.fetchall()

con.commit()
con.close()
