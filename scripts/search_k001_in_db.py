import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

# Поищем ремы со словами из К-001
cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%Структуры данных Python%'")
rows = cur.fetchall()
print(f"Matching rows for 'Структуры данных Python': {len(rows)}")

for rid, d_str in rows:
    d = json.loads(d_str)
    print(f"ID: {rid} | parent: {d.get('parent')} | key: {str(d.get('key'))[:80]}")

con.close()
