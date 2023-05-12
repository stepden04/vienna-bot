import sqlite3
con = sqlite3.connect("old-listings.db")

cur = con.cursor()

try:
    cur.execute("CREATE TABLE listings(title, uri, posted)")
except:
    print('Cant create table or it alreready exists')

def append_db(title,uri,posted):
    cur.execute(f"INSERT INTO listings VALUES('{str(title)}', '{str(uri)}', {posted})")
    con.commit()
    
def is_listed(id):
    r = cur.execute("SELECT uri FROM listings")
    return (id in r.fetchall())

def update_value(name,new,cond):
    cur.execute(f'UPDATE listings SET {name} = {new} WHERE {cond}')

def close_db():
    con.close()
    