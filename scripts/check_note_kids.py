import sqlite3
import json

con = sqlite3.connect(r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db')
cur = con.cursor()

doc_id = 'b9Aqkdxfsegfd0O0Q'
cur.execute("SELECT _id, doc FROM quanta WHERE json_extract(doc, '$.parent') = ?", (doc_id,))
root_kids = cur.fetchall()
print(f"Direct children of document {doc_id}: {len(root_kids)}")
for rid, d_str in root_kids:
    d = json.loads(d_str)
    print(f"  [{rid}] key={d.get('key')} | ps={d.get('ps')}")
    # Дети этого ребенка
    cur.execute("SELECT _id, doc FROM quanta WHERE json_extract(doc, '$.parent') = ?", (rid,))
    subkids = cur.fetchall()
    print(f"    Subchildren count: {len(subkids)}")
    for srid, sd_str in subkids:
        sd = json.loads(sd_str)
        print(f"      [{srid}] key={str(sd.get('key'))[:60]}")

con.close()
