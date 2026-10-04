import sqlite3
import zipfile
import json
import os

zpath = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\remnote_local_sqlite_archive.zip'
with zipfile.ZipFile(zpath, 'r') as z:
    z.extract('browser/remnote.db', r'C:\Users\fury6\.gemini\antigravity\scratch')

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\browser\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

# 1. Посмотрим типы ремов (h - header? type?)
cur.execute("SELECT _id, doc FROM quanta LIMIT 100")
rows = cur.fetchall()

header_samples = []
for rid, d_str in rows:
    d = json.loads(d_str)
    # Check if there is h or type
    if 'h' in d:
        header_samples.append((rid, d.get('h'), d.get('key')))
        
print("Header samples (h field):", len(header_samples))
for s in header_samples[:5]:
    print(" ", s)

# 2. Посмотрим, как устроен документ расписания (HKILo3FLoxkwXggHD) или Карта Мастерства
cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%Карта Мастерства%' OR doc LIKE '%HKILo3FLoxkwXggHD%'")
found = cur.fetchall()
print("Found schedule/map docs:", len(found))
for fid, fdoc in found[:3]:
    d = json.loads(fdoc)
    print("ID:", fid, "key:", d.get('key'))

con.close()
