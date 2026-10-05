import os
import json
import sqlite3

_here = os.path.dirname(os.path.abspath(__file__))
dump_path = os.path.normpath(os.path.join(_here, 'all_rems_dump.json'))

db_path = r'C:\Users\fury6\remnote\remnote-69d8425df107d8b00ed6ddb9\remnote.db'
if os.path.exists(db_path):
    print("DB exists! Size:", os.path.getsize(db_path))
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT count(*) FROM quanta")
    print("Quanta count:", cur.fetchone()[0])
    cur.execute("SELECT count(*) FROM cards")
    print("Cards count:", cur.fetchone()[0])
    con.close()
elif os.path.exists(dump_path):
    print("RemNote database dump verified at:", dump_path)
    with open(dump_path, 'r', encoding='utf-8') as f:
        rems = json.load(f)
    print("Total Rems in dump:", len(rems))
    canonical_root = [r for r in rems if r.get('_id') == 'GwREY4bq5eQvPyeAB' or (r.get('_id') == 'HKILo3FLoxkwXggHD')]
    if not canonical_root:
        canonical_root = [r for r in rems if '42 дня' in str(r.get('key', ''))]
    assert len(canonical_root) >= 1, "Canonical 42-day schedule root missing from dump!"
    c_root_id = canonical_root[0]['_id']
    weeks = [r for r in rems if r.get('parent') == c_root_id and 'Неделя' in str(r.get('key', ''))]
    print(f"Schedule Root: {c_root_id}")
    print(f"Found {len(weeks)} weeks under canonical schedule root")
    assert len(rems) > 1000, f"Expected >1000 rems, got {len(rems)}"
    assert len(weeks) == 6, f"Expected 6 weeks under canonical root, got {len(weeks)}"
    print("✓ RemNote JSON dump integrity verified successfully (6 weeks found)!")
else:
    print("[WARN] Neither remnote.db nor all_rems_dump.json found.")

