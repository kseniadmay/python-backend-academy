import sqlite3
import json

db = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db)
cur = con.cursor()

cur.execute("SELECT _id, doc FROM quanta WHERE json_extract(doc, '$.parent') = ? ORDER BY json_extract(doc, '$.f')", ('rbtsQEFIvoHVZxrZc',))
rows = cur.fetchall()
for rid, dstr in rows:
    d = json.loads(dstr)
    print(f"=== ID: {rid} | f: {d.get('f')} | type: {d.get('type')} ===")
    print('key:', d.get('key'))
    print('children:', d.get('children'))
    print('apu:', d.get('apu'))
    print('ps:', d.get('ps'))
con.close()
