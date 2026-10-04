import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

# Search by title in key
cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%01 · %' LIMIT 20")
for r in cur.fetchall():
    d = json.loads(r[1])
    key = d.get('key')
    print(r[0], "key:", key)
    # Check parent and children
    print("  type:", d.get('type'), "h:", d.get('h'), "children:", len(d.get('children', [])))

con.close()
