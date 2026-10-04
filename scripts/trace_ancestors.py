import sqlite3
import json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%Ваш API всегда возвращает%' LIMIT 1")
row = cur.fetchone()
if row:
    d = json.loads(row[1])
    print('Rem ID:', row[0])
    print('Parent:', d.get('parent'))
    print('bpc:', d.get('bpc'))
    
    # Найдем предков по цепочке
    curr_p = d.get('parent')
    depth = 0
    while curr_p and depth < 6:
        cur.execute('SELECT doc FROM quanta WHERE _id = ?', (curr_p,))
        prow = cur.fetchone()
        if not prow:
            break
        pd = json.loads(prow[0])
        print(f"Ancestor {depth+1} [{curr_p}]: key={pd.get('key')} | bpc={pd.get('bpc')}")
        curr_p = pd.get('parent')
        depth += 1

con.close()
