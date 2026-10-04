import sqlite3, json

db_path = r'C:\Users\fury6\.gemini\antigravity\scratch\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute("SELECT _id, doc FROM quanta WHERE json_extract(doc, '$.parent') = 'rbtsQEFIvoHVZxrZc' ORDER BY json_extract(doc, '$.f')")
kids = cur.fetchall()
for rid, d_str in kids:
    d = json.loads(d_str)
    key = str(d.get('key'))[:40]
    apu = d.get('apu')
    ps = d.get('ps')
    f_val = d.get('f')
    print(f'{rid} | f={f_val} | key={key} | apu={apu} | ps={ps}')
con.close()
