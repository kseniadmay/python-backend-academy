import os
import json

def test_rem_links():
    _here = os.path.dirname(os.path.abspath(__file__))
    dump_path = os.path.normpath(os.path.join(_here, 'all_rems_dump.json'))
    assert os.path.isfile(dump_path), f"Dump file missing: {dump_path}"
    
    with open(dump_path, 'r', encoding='utf-8') as f:
        rems = json.load(f)
    
    by_id = {r['_id']: r for r in rems if '_id' in r}
    root_id = 'GwREY4bq5eQvPyeAB'
    weeks = [r for r in rems if r.get('parent') == root_id and 'Неделя' in str(r.get('key', ''))]
    week_ids = set(w['_id'] for w in weeks)
    days = [r for r in rems if r.get('parent') in week_ids]
    day_ids = set(d['_id'] for d in days)

    schedule_ids = set([root_id]) | week_ids | day_ids
    frontier = list(day_ids)
    while frontier:
        curr = frontier.pop()
        kids = [r['_id'] for r in rems if r.get('parent') == curr]
        for kid in kids:
            if kid not in schedule_ids:
                schedule_ids.add(kid)
                frontier.append(kid)

    def extract_text(val):
        if isinstance(val, str): return val
        if isinstance(val, list): return ' '.join(extract_text(x) for x in val)
        if isinstance(val, dict):
            if 'text' in val: return val['text']
            if 'textOfDeletedRem' in val: return extract_text(val['textOfDeletedRem'])
        return ''

    loading_glitches = []
    broken_q_refs = []
    total_q_refs = 0

    for rid in schedule_ids:
        r = by_id[rid]
        key = r.get('key', [])
        if isinstance(key, list):
            for part in key:
                if isinstance(part, dict):
                    if part.get('i') == 'q':
                        total_q_refs += 1
                        target_id = part.get('_id')
                        target = by_id.get(target_id)
                        deleted_text = part.get('textOfDeletedRem')
                        if not target and not deleted_text:
                            broken_q_refs.append((rid, target_id, 'No target and no textOfDeletedRem'))
                        if deleted_text:
                            s = extract_text(deleted_text).strip()
                            if s in ('Загрузка...', 'Loading...', 'Loading', 'Загрузка') or s.startswith('Загрузка...') or s.startswith('Loading...'):
                                loading_glitches.append((rid, target_id, s))
                    if 'text' in part:
                        t = str(part['text']).strip()
                        if t in ('Загрузка...', 'Loading...', 'Loading', 'Загрузка') or t.startswith('Загрузка...') or t.startswith('Loading...'):
                            loading_glitches.append((rid, part, t))

    assert len(loading_glitches) == 0, f"Found {len(loading_glitches)} loading placeholders in schedule links: {loading_glitches}"
    assert len(broken_q_refs) == 0, f"Found {len(broken_q_refs)} broken q-references without fallback text: {broken_q_refs}"

    # Also verify parsed_schedule.json if present
    ps_path = os.path.normpath(os.path.join(_here, 'parsed_schedule.json'))
    if os.path.isfile(ps_path):
        with open(ps_path, 'r', encoding='utf-8') as f:
            ps = json.load(f)
        ps_str = json.dumps(ps, ensure_ascii=False)
        assert 'Загрузка...' not in ps_str, "Found 'Загрузка...' in parsed_schedule.json"
        assert 'Loading...' not in ps_str, "Found 'Loading...' in parsed_schedule.json"

    print(f"✓ test_rem_links: {total_q_refs} schedule references verified clean (0 loading placeholders, 0 broken links)!")

if __name__ == '__main__':
    test_rem_links()
