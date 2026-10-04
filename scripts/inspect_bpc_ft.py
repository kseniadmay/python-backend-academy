import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

# Посмотрим примеры ремов с bpc
cur.execute("SELECT _id, json_extract(doc, '$.bpc'), json_extract(doc, '$.key') FROM quanta WHERE json_extract(doc, '$.bpc') IS NOT NULL LIMIT 10")
for rid, bpc, key in cur.fetchall():
    print(f"bpc={bpc} | key={key}")

# Посмотрим примеры ремов с ft
cur.execute("SELECT _id, json_extract(doc, '$.ft'), json_extract(doc, '$.key') FROM quanta WHERE json_extract(doc, '$.ft') IS NOT NULL LIMIT 10")
for rid, ft, key in cur.fetchall():
    print(f"ft={ft} | key={key}")

# Посмотрим powerups apu
cur.execute("SELECT _id, json_extract(doc, '$.apu'), json_extract(doc, '$.key') FROM quanta WHERE json_extract(doc, '$.apu') IS NOT NULL LIMIT 10")
for rid, apu, key in cur.fetchall():
    print(f"apu={apu} | key={key}")

con.close()
