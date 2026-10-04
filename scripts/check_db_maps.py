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
        
        # Поищем узел "00 · 🗺️ Карта Мастерства" или "Программа подготовки"
        cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%Карта Мастерства%' OR doc LIKE '%Программа подготовки%'")
        rows = cur.fetchall()
        print('Found maps in DB:', len(rows))
        for rid, doc_str in rows:
            d = json.loads(doc_str)
            print('ID:', rid)
            print('KEY:', d.get('key'))
            print('TYPE:', d.get('type'))
            print('CHILDREN COUNT:', len(d.get('children', [])))
            print('---')
            
        conn.close()
