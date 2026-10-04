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
        
        # 1. Документы
        cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%Структуры данных%' LIMIT 3")
        rows = cur.fetchall()
        print('=== Rems with "Структуры данных" ===')
        for rid, doc_str in rows:
            d = json.loads(doc_str)
            print('ID:', rid)
            print('KEY:', d.get('key'))
            print('TYPE:', d.get('type'))
            print('PARENT:', d.get('parent'))
            print('---')
            
        # 2. Ссылки в Карте Мастерства / расписании
        cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"i\":\"q\"%' LIMIT 5")
        rows = cur.fetchall()
        print('=== References (type q) ===')
        for rid, doc_str in rows:
            d = json.loads(doc_str)
            print('ID:', rid)
            print('KEY:', d.get('key'))
            print('---')
            
        conn.close()
