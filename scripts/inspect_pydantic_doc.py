import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%Погружение в Pydantic%'")
rows = cur.fetchall()
print('Found:', len(rows))
for rid, d_str in rows:
    d = json.loads(d_str)
    print("ID:", rid, "parent:", d.get('parent'), "key:", d.get('key'))
    
    # Посмотрим детей этого документа
    cur.execute("SELECT _id, doc FROM quanta WHERE json_extract(doc, '$.parent') = ?", (rid,))
    kids = cur.fetchall()
    print(f"Children count: {len(kids)}")
    for k_id, k_doc in kids:
        kd = json.loads(k_doc)
        print(f"  [{k_id}] key={str(kd.get('key'))[:60]} | bpc={kd.get('bpc')} | apu={kd.get('apu')}")

con.close()
