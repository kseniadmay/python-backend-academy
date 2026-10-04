import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

# Search for rems with header (h)
cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"h\":%' LIMIT 20")
rows = cur.fetchall()
print("Headers found in DB:", len(rows))
for rid, d_str in rows[:10]:
    d = json.loads(d_str)
    print(rid, "h:", d.get('h'), "key:", d.get('key'))

# Search for todo in quanta
cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"status\":%' OR doc LIKE '%\"todo\"%' LIMIT 10")
rows_todo = cur.fetchall()
print("Todo found in DB:", len(rows_todo))
for rid, d_str in rows_todo[:5]:
    d = json.loads(d_str)
    print(rid, "status:", d.get('status'), "key:", d.get('key'))

con.close()
