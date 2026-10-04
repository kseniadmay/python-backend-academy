import sqlite3
import json

conn = sqlite3.connect(r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db')
c = conn.cursor()
rows = c.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"parent\":\"rbtsQEFIvoHVZxrZc\"%'").fetchall()
print('Total children with parent=rbtsQEFIvoHVZxrZc:', len(rows))
for _id, doc in rows:
    robj = json.loads(doc)
    t = 'DIVIDER' if robj.get('apu', {}).get('dv') else ('H2' if 'H2' in str(robj.get('ps')) else ('CODE' if 'cd_b' in str(robj.get('ps')) else 'TEXT'))
    print(f'{_id} | {t:7s} | key: {robj.get("key", [])[:2]}')
