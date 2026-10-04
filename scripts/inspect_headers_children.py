import sqlite3
import json

con = sqlite3.connect(r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db')
cur = con.cursor()

# Найдем любой рем с h != None (заголовок H1/H2/H3)
cur.execute("SELECT _id, doc FROM quanta WHERE json_extract(doc, '$.h') IS NOT NULL LIMIT 20")
rows = cur.fetchall()
print(f"Total headers with $.h: {len(rows)}")

for rid, d_str in rows[:10]:
    d = json.loads(d_str)
    pid = d.get('parent')
    h = d.get('h')
    key = str(d.get('key'))[:60]
    
    # Посмотрим, есть ли у этого заголовка дети (WHERE parent = rid)
    cur.execute("SELECT count(*) FROM quanta WHERE json_extract(doc, '$.parent') = ?", (rid,))
    kids_cnt = cur.fetchone()[0]
    
    # Посмотрим, кто его родитель
    cur.execute("SELECT doc FROM quanta WHERE _id = ?", (pid,))
    prow = cur.fetchone()
    pkey = 'None'
    if prow:
        pkey = str(json.loads(prow[0]).get('key'))[:40]
        
    print(f"Header [{rid}] (H{h}): key={key} | kids={kids_cnt} | parent={pid} ({pkey})")

con.close()
