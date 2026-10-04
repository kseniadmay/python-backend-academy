import sqlite3
import json

con = sqlite3.connect(r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db')
cur = con.cursor()
cur.execute("SELECT _id, json_extract(doc, '$.f'), json_extract(doc, '$.key'), json_extract(doc, '$.bpc') FROM quanta WHERE json_extract(doc, '$.parent') = '2bHnWDHJbIjrNfugH' ORDER BY json_extract(doc, '$.f')")
rows = cur.fetchall()
print('Total children of 2bHnWDHJbIjrNfugH:', len(rows))
for r in rows:
    bpc = str(r[3])
    h = ' [H2]' if 'H2' in bpc else (' [H3]' if 'H3' in bpc else '')
    print(f"  {r[1]} | {r[0]} | {str(r[2])[:60]}{h}")
con.close()
