import sqlite3

con = sqlite3.connect("../data/twitter_db.db")

def create_celebrities_table():
  cur = con.cursor()
  cur.execute("CREATE TABLE celebrities (screen_name text primary key)")

def create_simi_table():
  cur = con.cursor()
  cur.execute("CREATE TABLE top_similar (screen_name text, screen_name_similar text, score real)")

def create_new_celebrities_table():
  cur = con.cursor()
  cur.execute("CREATE TABLE new_celebrities (screen_name text primary key, user_name text, desc text, img_name text)")

create_new_celebrities_table()

con.commit()
con.close()
