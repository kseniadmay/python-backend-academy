import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

# Исследуем все уникальные поля в quanta
cur.execute("SELECT doc FROM quanta LIMIT 500")
rows = cur.fetchall()

keys = set()
for r in rows:
    d = json.loads(r[0])
    keys.update(d.keys())

print("All keys in quanta JSON:", sorted(keys))

# Посмотрим примеры ремов с разными типами
cur.execute("SELECT json_extract(doc, '$.type'), count(*) FROM quanta GROUP BY json_extract(doc, '$.type')")
print("\nTypes distribution:")
for t, cnt in cur.fetchall():
    print(f"  type={t}: {cnt}")

# Посмотрим powerup slots (ps)
cur.execute("SELECT json_extract(doc, '$.ps'), count(*) FROM quanta WHERE json_extract(doc, '$.ps') IS NOT NULL GROUP BY json_extract(doc, '$.ps') LIMIT 15")
print("\nTop ps values:")
for ps, cnt in cur.fetchall():
    print(f"  ps={ps[:60]}: {cnt}")

con.close()
