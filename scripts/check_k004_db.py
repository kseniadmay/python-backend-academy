import sqlite3, json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%frozenset_ неизменяемое множество%'")
rows = cur.fetchall()
print(f'Found K-004 rows: {len(rows)}')
for rid, d_str in rows:
    d = json.loads(d_str)
    print('ID:', rid, 'key:', d.get('key'))
    cur.execute("SELECT _id, json_extract(doc, '$.f'), json_extract(doc, '$.key'), json_extract(doc, '$.ps') FROM quanta WHERE json_extract(doc, '$.parent') = ? ORDER BY json_extract(doc, '$.f')", (rid,))
    kids = cur.fetchall()
    print(f'Kids of {rid}: {len(kids)}')
    for k in kids:
        print(f'   {k[0]} | f={k[1]} | ps={k[3]} | key={str(k[2])[:80]}')

con.close()
