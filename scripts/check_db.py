import os
import sqlite3

db_path = r'C:\Users\fury6\remnote\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
if os.path.exists(db_path):
    print("DB exists! Size:", os.path.getsize(db_path))
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT count(*) FROM quanta")
    print("Quanta count:", cur.fetchone()[0])
    cur.execute("SELECT count(*) FROM cards")
    print("Cards count:", cur.fetchone()[0])
    cur.execute("SELECT _id, json_extract(doc, '$.key') FROM quanta WHERE doc LIKE '%Ф-011%'")
    rows = cur.fetchall()
    print("Found Ф-011 in DB:", len(rows), rows)
    cur.execute("SELECT _id, json_extract(doc, '$.key') FROM quanta WHERE doc LIKE '%Переменные args и kwargs%'")
    rows2 = cur.fetchall()
    print("Found Переменные args и kwargs:", len(rows2), rows2[:5])
    con.close()
else:
    print("DB does not exist at:", db_path)
    p = r'C:\Users\fury6\remnote'
    if os.path.exists(p):
        print("Contents of", p, os.listdir(p))
