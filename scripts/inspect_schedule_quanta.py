import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

# 1. Посмотрим на документ расписания HKILo3FLoxkwXggHD
cur.execute("SELECT doc FROM quanta WHERE _id = 'HKILo3FLoxkwXggHD'")
row = cur.fetchone()
if row:
    d = json.loads(row[0])
    print("Schedule root doc keys:", list(d.keys()))
    print("Children count:", len(d.get('children', [])))
    print("Key:", d.get('key'))

# 2. Посмотрим первые 10 дочерних элементов расписания
if row and d.get('children'):
    cids = d['children'][:10]
    placeholders = ','.join(['?'] * len(cids))
    cur.execute(f"SELECT _id, doc FROM quanta WHERE _id IN ({placeholders})", cids)
    for cid, cdoc in cur.fetchall():
        cd = json.loads(cdoc)
        print(f"Child {cid}: key={cd.get('key')}, type={cd.get('type')}, h={cd.get('h')}, cr={cd.get('cr')}")

# 3. Поищем ремы с '---' или divider
cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%divider%' OR doc LIKE '%---%' LIMIT 5")
for r in cur.fetchall():
    d = json.loads(r[1])
    print("Divider candidate:", r[0], "key:", d.get('key'), "type:", d.get('type'))

con.close()
