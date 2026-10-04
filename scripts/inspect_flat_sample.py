import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

# Найдем плоские заголовки
cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"s\":\"H2\"%' OR doc LIKE '%\"s\":\"H3\"%'")
rows = cur.fetchall()

flat_samples = []
for rid, d_str in rows:
    d = json.loads(d_str)
    kids_arr = d.get('children', [])
    cur.execute("SELECT count(*) FROM quanta WHERE json_extract(doc, '$.parent') = ?", (rid,))
    parent_kids = cur.fetchone()[0]
    
    if len(kids_arr) == 0 and parent_kids == 0:
        # Проверим, кто родитель
        pid = d.get('parent')
        if pid:
            cur.execute("SELECT doc FROM quanta WHERE _id = ?", (pid,))
            prow = cur.fetchone()
            if prow:
                pd = json.loads(prow[0])
                flat_samples.append((rid, d.get('key'), pid, pd.get('key'), pd.get('children', [])))
                if len(flat_samples) >= 5:
                    break

print(f"Sample flat headers (without children): {len(flat_samples)}")
for rid, hkey, pid, pkey, pchil in flat_samples:
    print(f"\nHeader [{rid}]: {hkey}")
    print(f"  Parent [{pid}]: {pkey}")
    if rid in pchil:
        idx = pchil.index(rid)
        print(f"  Position in parent children: {idx} of {len(pchil)}")
        if idx + 1 < len(pchil):
            next_id = pchil[idx + 1]
            cur.execute("SELECT doc FROM quanta WHERE _id = ?", (next_id,))
            nrow = cur.fetchone()
            if nrow:
                nd = json.loads(nrow[0])
                print(f"  Next sibling [{next_id}]: {str(nd.get('key'))[:80]}")

con.close()
