import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

doc_id = 'MkMzFB2C7CcFVmWBM'
cur.execute('SELECT doc FROM quanta WHERE _id = ?', (doc_id,))
row = cur.fetchone()
d = json.loads(row[0])

print(f"Document {doc_id} key: {d.get('key')}")
print(f"Children in array: {len(d.get('children', []))}")

# Посмотрим всех потомков через parent = doc_id
cur.execute("SELECT _id, json_extract(doc, '$.f'), json_extract(doc, '$.key'), json_extract(doc, '$.bpc'), json_extract(doc, '$.ps') FROM quanta WHERE json_extract(doc, '$.parent') = ? ORDER BY json_extract(doc, '$.f')", (doc_id,))
kids = cur.fetchall()
print(f"Total direct children in DB: {len(kids)}")

for kid in kids:
    print(f"  [{kid[0]}] f={kid[1]} | ps={kid[4]} | key={str(kid[2])[:80]}")
    # Посмотрим детей этого ребенка (второй уровень)
    cur.execute("SELECT _id, json_extract(doc, '$.f'), json_extract(doc, '$.key') FROM quanta WHERE json_extract(doc, '$.parent') = ?", (kid[0],))
    subkids = cur.fetchall()
    if subkids:
        print(f"    Subchildren count: {len(subkids)}")
        for sk in subkids[:3]:
            print(f"      [{sk[0]}] key={str(sk[2])[:60]}")

con.close()
