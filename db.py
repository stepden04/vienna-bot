import sqlite3
con = sqlite3.connect("old-listings.db")

cur = con.cursor()

try:
    cur.execute("CREATE TABLE listings(title, uri, posted)")
except:
    print('Cant create table or it alreready exists')

def append_db(data):
    cur.executemany("INSERT INTO listings VALUES(?, ?, ?)",data)
    con.commit()
    
def is_listed(id):
    r = cur.execute("SELECT uri FROM listings")
    return (id in r.fetchall())

def close_db():
    con.close()
    