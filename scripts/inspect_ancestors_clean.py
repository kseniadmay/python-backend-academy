import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute('SELECT doc FROM quanta WHERE _id = ?', ('2bHnWDHJbIjrNfugH',))
row = cur.fetchone()
d = json.loads(row[0])
print('2bHnWDHJbIjrNfugH parent:', d.get('parent'))
print('children count:', len(d.get('children', [])))

p = d.get('parent')
while p:
    cur.execute('SELECT doc FROM quanta WHERE _id = ?', (p,))
    pr = cur.fetchone()
    if not pr:
        break
    pd = json.loads(pr[0])
    print('  Ancestor:', p, 'key:', pd.get('key'))
    p = pd.get('parent')

for cid in d.get('children', [])[:20]:
    cur.execute('SELECT doc FROM quanta WHERE _id = ?', (cid,))
    cr = cur.fetchone()
    if cr:
        cd = json.loads(cr[0])
        bpc = str(cd.get('bpc', ''))
        h = 'H2' if 'H2' in bpc else ('H3' if 'H3' in bpc else '')
        print(f"    [{cid}] ({h}) {str(cd.get('key'))[:60]}")

con.close()
