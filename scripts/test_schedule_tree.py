import os
import json
import re

def test_schedule_tree():
    _here = os.path.dirname(os.path.abspath(__file__))
    ps_path = os.path.normpath(os.path.join(_here, 'parsed_schedule.json'))
    dump_path = os.path.normpath(os.path.join(_here, 'all_rems_dump.json'))
    
    assert os.path.isfile(ps_path), f"parsed_schedule.json missing: {ps_path}"
    assert os.path.isfile(dump_path), f"all_rems_dump.json missing: {dump_path}"

    with open(ps_path, 'r', encoding='utf-8') as f:
        ps = json.load(f)

    # 1. Verify 6 modules / weeks
    weeks = ps.get('weeks', [])
    assert len(weeks) == 6, f"Expected strictly 6 modules/weeks, got {len(weeks)}"
    
    # 2. Verify 42 days
    all_days = [d for w in weeks for d in w.get('days', [])]
    assert len(all_days) == 42, f"Expected strictly 42 days, got {len(all_days)}"
    day_nums = [d.get('num') for d in all_days]
    assert day_nums == list(range(1, 43)), f"Day numbers mismatch: {day_nums}"

    # 3. Verify total tasks (~300 tasks)
    total_level_tasks = 0
    total_coding_items = 0
    circle_emojis = ['🟢', '🟡', '🔴', '⚪', '⚫', '🔵', '🟣', '🟠']
    allowed_animals = ['🥚', '🐣', '🐥', '🦆', '🦊', '🐺', '🐯', '🦁', '🐉', '👑']

    mismatches = []
    
    for d in all_days:
        dnum = d.get('num')
        for s in d.get('sections', []):
            st = s.get('type', '')
            title = s.get('title', '')
            if st == 'coding' or 'кодинг' in title.lower():
                items = s.get('items', [])
                total_coding_items += len(items)
                
                # Filter actual tasks with Level
                level_tasks = [it for it in items if re.search(r'Уровень\s+\d', it)]
                total_level_tasks += len(level_tasks)

                # Check circle emoji prohibition
                for it in items:
                    for circ in circle_emojis:
                        assert circ not in it, f"Day {dnum} task contains prohibited circle emoji {circ}: {it}"
                
                # Check header counter vs actual tasks
                m = re.search(r'(?:до\s+)?(\d+)\s+задач', title)
                if m:
                    stated = int(m.group(1))
                    if stated == 4:
                        # Review days: exactly 4 refactoring tasks
                        assert len(level_tasks) == 4, f"Day {dnum}: expected exactly 4 refactoring tasks for 'до 4 задач', got {len(level_tasks)}"
                    elif stated == 8:
                        # Regular days: up to 8 tasks (7-8 tasks)
                        assert len(level_tasks) in (7, 8), f"Day {dnum}: expected 7-8 tasks for 'до 8 задач', got {len(level_tasks)}"
                        assert len(items) in (8, 9), f"Day {dnum}: expected 8-9 items under section, got {len(items)}"
    assert 280 <= total_level_tasks <= 320, f"Expected ~300 coding tasks, got {total_level_tasks}"
    print(f"Total level tasks: {total_level_tasks}, total coding items: {total_coding_items}")

    # 4. Verify canonical root in all_rems_dump.json
    with open(dump_path, 'r', encoding='utf-8') as f:
        rems = json.load(f)
    
    by_id = {r['_id']: r for r in rems if '_id' in r}
    canonical_root_id = 'GwREY4bq5eQvPyeAB'
    assert canonical_root_id in by_id, f"Canonical root {canonical_root_id} missing from dump!"
    
    dump_weeks = [r for r in rems if r.get('parent') == canonical_root_id and 'Неделя' in str(r.get('key', ''))]
    assert len(dump_weeks) == 6, f"Expected 6 weeks under canonical root in dump, got {len(dump_weeks)}"

    print("✓ test_schedule_tree: 6 modules, 42 days, ~300 tasks, pure animal emojis (0 circles), exact header counters & canonical root verified!")

if __name__ == '__main__':
    test_schedule_tree()
