import sqlite3
import json

con = sqlite3.connect(r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db')
cur = con.cursor()

cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%Что такое граф%'")
rows = cur.fetchall()
print('Found:', len(rows))
for rid, d_str in rows:
    print('ID:', rid)
    print(d_str)

con.close()
