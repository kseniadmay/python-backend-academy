import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

# Найдем все ремы с заголовками H1, H2, H3
cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"s\":\"H2\"%' OR doc LIKE '%\"s\":\"H3\"%'")
rows = cur.fetchall()
print(f"Total H2/H3 rems in DB: {len(rows)}")

headers_with_kids = 0
headers_without_kids = 0

for rid, d_str in rows:
    d = json.loads(d_str)
    # Проверим, есть ли у этого заголовка дети (через children или WHERE parent = rid)
    kids_arr = d.get('children', [])
    cur.execute("SELECT count(*) FROM quanta WHERE json_extract(doc, '$.parent') = ?", (rid,))
    parent_kids = cur.fetchone()[0]
    
    if len(kids_arr) > 0 or parent_kids > 0:
        headers_with_kids += 1
    else:
        headers_without_kids += 1

print(f"Headers WITH children (collapsible ▾): {headers_with_kids}")
print(f"Headers WITHOUT children (flat): {headers_without_kids}")

con.close()
