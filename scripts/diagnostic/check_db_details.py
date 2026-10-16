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
        
        # Поищем все ремы, где parent = 'Yh3mV60cdYnjhNTx6'
        cur.execute("SELECT _id, doc FROM quanta WHERE json_extract(doc, '$.parent') = 'Yh3mV60cdYnjhNTx6'")
        rows = cur.fetchall()
        print('Children of Program:', len(rows))
        for rid, doc_str in rows[:10]:
            d = json.loads(doc_str)
            print('ID:', rid, 'KEY:', d.get('key'))
            
        # Поищем, где лежат конспекты
        cur.execute("SELECT _id, doc FROM quanta WHERE doc LIKE '%Структуры данных Python%'")
        rows = cur.fetchall()
        print('\nQuanta with \"Структуры данных Python\":', len(rows))
        for rid, doc_str in rows:
            d = json.loads(doc_str)
            print('ID:', rid)
            print('KEY:', d.get('key'))
            print('PARENT:', d.get('parent'))
            print('DOC FLAG (type):', d.get('type'))
            print('---')
            
        conn.close()
