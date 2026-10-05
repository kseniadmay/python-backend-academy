import os
import json

def test_rems_dump():
    _here = os.path.dirname(os.path.abspath(__file__))
    dump_path = os.path.normpath(os.path.join(_here, 'all_rems_dump.json'))
    assert os.path.isfile(dump_path), f"Dump file missing: {dump_path}"
    
    with open(dump_path, 'r', encoding='utf-8') as f:
        rems = json.load(f)
    
    assert isinstance(rems, list), "Expected list of rems in dump"
    assert len(rems) > 10000, f"Expected >10,000 rems, got {len(rems)}"
    
    by_id = {r['_id']: r for r in rems if '_id' in r}
    assert len(by_id) == len(rems), "Found duplicate _id entries in dump!"
    
    # Verify schedule root
    root_id = 'GwREY4bq5eQvPyeAB'
    assert root_id in by_id, f"Canonical schedule root {root_id} missing!"
    root_rem = by_id[root_id]
    assert '42 дня' in str(root_rem.get('key', '')), "Root rem title does not mention 42 дня"
    
    # Verify 6 canonical weeks
    weeks = [r for r in rems if r.get('parent') == root_id and 'Неделя' in str(r.get('key', ''))]
    assert len(weeks) == 6, f"Expected 6 weeks under root, got {len(weeks)}"
    week_ids = set(w['_id'] for w in weeks)
    
    # Verify 42 canonical days
    days = [r for r in rems if r.get('parent') in week_ids]
    assert len(days) == 42, f"Expected 42 days under 6 weeks, got {len(days)}"
    
    # Verify acyclicity and valid parent chain
    for d in days:
        curr = d
        visited = set()
        while curr and curr.get('parent'):
            pid = curr['parent']
            assert pid not in visited, f"Cycle detected in parent chain at {pid}!"
            visited.add(pid)
            curr = by_id.get(pid)
    
    print(f"✓ test_rems_dump: {len(rems)} rems, canonical root {root_id}, 6 weeks, 42 days verified acyclic!")

if __name__ == '__main__':
    test_rems_dump()
