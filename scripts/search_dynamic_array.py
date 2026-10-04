import sqlite3
import json

con = sqlite3.connect(r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db')
cur = con.cursor()

cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%динамический массив%'")
rows = cur.fetchall()
print('Found:', len(rows))
for rid, d_str in rows[:5]:
    d = json.loads(d_str)
    print('ID:', rid)
    print('parent:', d.get('parent'))
    print('key:', d.get('key'))
    print('h:', d.get('h'))
    print('children count:', len(d.get('children', [])))

con.close()
