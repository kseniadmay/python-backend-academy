import zipfile
import sqlite3
import tempfile
import os

zip_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\remnote_local_sqlite_archive.zip'
with zipfile.ZipFile(zip_path) as z:
    for name in z.namelist():
        if name.endswith('.db'):
            with tempfile.TemporaryDirectory() as tmpdir:
                z.extract(name, tmpdir)
                p = os.path.join(tmpdir, name)
                conn = sqlite3.connect(p)
                cur = conn.cursor()
                try:
                    cur.execute("SELECT count(*) FROM quanta")
                    cnt = cur.fetchone()[0]
                    print(name, 'quanta count:', cnt)
                except Exception as e:
                    print(name, 'error:', e)
                conn.close()
