import sqlite3

path = "/ssd/yisheng/tables/"
con = sqlite3.connect(path + "bigdata.db")

def create_followers_table():
  cur = con.cursor()
  cur.execute("CREATE TABLE followers (screen_name text primary key, user_idx int)")

def create_celebrities_table():
  cur = con.cursor()
  cur.execute("CREATE TABLE celebrities (celebrity_idx int primary key, screen_name text)")

def create_following_table():
  cur = con.cursor()
  cur.execute("CREATE TABLE following (user_idx int, celebrity_idx int)")

create_followers_table()
create_celebrities_table()
create_following_table()

con.commit()
con.close()
