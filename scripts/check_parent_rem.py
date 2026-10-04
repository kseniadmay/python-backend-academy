import zipfile
import sqlite3
import tempfile
import os
import json

zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\remnote_local_sqlite_archive.zip'
with zipfile.ZipFile(zip_path) as z:
    with tempfile.TemporaryDirectory() as tmpdir:
        entry = 'remnote-69d8425df107d8b00ed6ddb9/remnote.db'
        z.extract(entry, tmpdir)
        db_path = os.path.join(tmpdir, entry)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        cur.execute("SELECT _id, doc FROM quanta WHERE _id = 'YGAQC5yDHhkPb7145'")
        row = cur.fetchone()
        if row:
            d = json.loads(row[1])
            print('ID:', row[0])
            print('KEY:', d.get('key'))
            print('PARENT:', d.get('parent'))
            print('TYPE:', d.get('type'))
            print('FULL DOC:', d)
            
        conn.close()
