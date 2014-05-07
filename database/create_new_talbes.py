import sqlite3

con = sqlite3.connect("twitter_db.db")

def create_celebrities_table():
  cur = con.cursor()
  cur.execute("CREATE TABLE celebrities (screen_name text primary key)")

def create_simi_table():
  cur = con.cursor()
  cur.execute("CREATE TABLE top_similar (screen_name text, screen_name_similar text, score real)")

create_celebrities_table()
create_simi_table()

con.commit()
con.close()
