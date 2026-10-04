import sqlite3
import json

con = sqlite3.connect(r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db')
cur = con.cursor()

# Найдем документы
cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%document%' LIMIT 10")
rows = cur.fetchall()
print('Sample docs:', len(rows))
for rid, d_str in rows[:5]:
    d = json.loads(d_str)
    print(rid, d.get('key'), 'keys:', list(d.keys())[:8])

con.close()
