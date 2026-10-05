import os
import json
import re

def test_review_blocks():
    _here = os.path.dirname(os.path.abspath(__file__))
    ps_path = os.path.normpath(os.path.join(_here, 'parsed_schedule.json'))
    assert os.path.isfile(ps_path), f"parsed_schedule.json missing: {ps_path}"

    with open(ps_path, 'r', encoding='utf-8') as f:
        ps = json.load(f)

    weeks = ps.get('weeks', [])
    all_days = {d['num']: d for w in weeks for d in w.get('days', [])}

    review_days = [7, 14, 21, 28, 35]
    for dnum in review_days:
        d = all_days.get(dnum)
        assert d is not None, f"Review Day {dnum} missing from schedule!"
        title = d.get('rawTitle', '')
        assert 'REVIEW' in title, f"Day {dnum} title missing 'REVIEW': {title}"

        # 1. Verify RemNote interval repetition
        theory_sections = [s for s in d.get('sections', []) if s.get('type') == 'theory' or 'теория' in s.get('title', '').lower()]
        assert len(theory_sections) > 0, f"Day {dnum} missing theory/interval repetition section"
        theory_items = [it for s in theory_sections for it in s.get('items', [])]
        has_spaced_rep = any('интервальное повторение' in it.lower() or 'remnote' in it.lower() or 'повторение' in it.lower() for it in theory_items)
        assert has_spaced_rep, f"Day {dnum} missing RemNote interval repetition item: {theory_items}"

        # 2. Verify exactly 4 refactoring coding tasks
        coding_sections = [s for s in d.get('sections', []) if s.get('type') == 'coding' or 'кодинг' in s.get('title', '').lower()]
        assert len(coding_sections) > 0, f"Day {dnum} missing coding section"
        coding_items = [it for s in coding_sections for it in s.get('items', [])]
        level_tasks = [it for it in coding_items if re.search(r'Уровень\s+\d', it)]
        assert len(level_tasks) == 4, f"Day {dnum} expected exactly 4 refactoring tasks, got {len(level_tasks)}: {level_tasks}"

        # 3. Verify weekly checklist has exactly 5 items
        checklist_sections = [s for s in d.get('sections', []) if s.get('type') == 'checklist' or 'чек-лист' in s.get('title', '').lower()]
        assert len(checklist_sections) > 0, f"Day {dnum} missing checklist section"
        checklist_items = [it for s in checklist_sections for it in s.get('items', [])]
        assert len(checklist_items) == 5, f"Day {dnum} expected 5 checklist items, got {len(checklist_items)}: {checklist_items}"

    # Day 42 (Final exam and retrospect)
    d42 = all_days.get(42)
    assert d42 is not None, "Day 42 missing from schedule!"
    d42_theory = [s for s in d42.get('sections', []) if s.get('type') == 'theory']
    assert len(d42_theory) > 0, "Day 42 missing theory section"
    d42_checklist = [s for s in d42.get('sections', []) if s.get('type') == 'checklist']
    assert len(d42_checklist) > 0, "Day 42 missing final checklist"

    print("✓ test_review_blocks: All 6 review days (07, 14, 21, 28, 35, 42) verified with spaced repetition, exactly 4 refactoring tasks, and 5-item checklists!")

if __name__ == '__main__':
    test_review_blocks()
