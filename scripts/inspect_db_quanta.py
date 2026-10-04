import zipfile
import sqlite3
import tempfile
import os
import json

zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\remnote_local_sqlite_archive.zip'
with zipfile.ZipFile(zip_path) as z:
    with tempfile.TemporaryDirectory() as tmpdir:
        z.extract('browser/remnote.db', tmpdir)
        db_path = os.path.join(tmpdir, 'browser/remnote.db')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # 1. Посмотрим на документы расписания и конспектов
        cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%Структуры данных%' LIMIT 3")
        rows = cur.fetchall()
        print('=== Rems with \"Структуры данных\" ===')
        for rid, doc_str in rows:
            d = json.loads(doc_str)
            print('ID:', rid)
            print('KEY:', d.get('key'))
            print('TYPE:', d.get('type'))
            print('PARENT:', d.get('parent'))
            print('---')
            
        # 2. Посмотрим на Rem References (type q)
        cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"i\":\"q\"%' LIMIT 3")
        rows = cur.fetchall()
        print('=== References ===')
        for rid, doc_str in rows:
            d = json.loads(doc_str)
            print('ID:', rid)
            print('KEY:', d.get('key'))
            print('---')
            
        # 3. Посмотрим на пустые строки / разделители
        cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%\"key\":[]%' OR doc LIKE '%\"key\":[\"\"]%' LIMIT 3")
        rows = cur.fetchall()
        print('=== Empty rems ===')
        for rid, doc_str in rows:
            d = json.loads(doc_str)
            print('ID:', rid)
            print('KEY:', d.get('key'))
            print('---')
            
        conn.close()
