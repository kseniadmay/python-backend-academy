# -*- coding: utf-8 -*-
import json
import re
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..'))

def apply_step2():
    print("=== STEP 2: INJECTING 26 DECKS (425 CARDS) INTO PY_MASTERY ===")
    
    cards_json_path = os.path.join(_ROOT, 'data', 'content', 'cards.json')
    with open(cards_json_path, 'r', encoding='utf-8') as f:
        cards_json = json.load(f)

    standards_path = os.path.join(_ROOT, 'standards', 'standards.html')
    academy_path = os.path.join(_ROOT, 'academy.html')
    with open(standards_path, 'r', encoding='utf-8') as f:
        html = f.read()

    new_deck_ids = [
        'Ф-226', 'Ф-227', 'Ф-228', 'Ф-229', 'Ф-230', 'Ф-231',
        'Ф-232', 'Ф-233', 'Ф-234', 'Ф-235', 'Ф-236', 'Ф-237',
        'Ф-239', 'Ф-240', 'Ф-241', 'Ф-242', 'Ф-245', 'Ф-246',
        'Ф-247', 'Ф-248', 'Ф-249', 'Ф-252', 'Ф-253', 'Ф-254',
        'Ф-255', 'Ф-256'
    ]

    deck_to_skill = {
        'Ф-226': '1.1.3',
        'Ф-227': '1.1.2',
        'Ф-228': '1.1.2',
        'Ф-229': '1.1.1',
        'Ф-230': '1.1.2',
        'Ф-231': '1.1.1',
        'Ф-232': '1.2.1',
        'Ф-233': '1.2.3',
        'Ф-234': '1.2.1',
        'Ф-235': '1.3.2',
        'Ф-236': '1.3.1',
        'Ф-237': '1.3.3',
        'Ф-239': '1.4.3',
        'Ф-240': '1.4.1',
        'Ф-241': '1.5.1',
        'Ф-242': '1.5.1',
        'Ф-245': '1.6.1',
        'Ф-246': '1.7.1',
        'Ф-247': '1.7.1',
        'Ф-248': '1.7.1',
        'Ф-249': '1.8.3',
        'Ф-252': '1.9.1',
        'Ф-253': '1.9.1',
        'Ф-254': '1.9.2',
        'Ф-255': '1.9.1',
        'Ф-256': '1.9.3',
    }

    m = re.search(r'(const\s+PY_MASTERY\s*=\s*)(\{.*?\})(;\s*(?:const|window))', html, re.DOTALL)
    if not m:
        raise ValueError("Could not find const PY_MASTERY in standards.html")

    prefix = m.group(1)
    py_data = json.loads(m.group(2))
    suffix = m.group(3)

    # 1. Inject decks into py_data['decks']
    injected_decks_count = 0
    injected_cards_count = 0
    if 'decks' not in py_data:
        py_data['decks'] = {}

    for did in new_deck_ids:
        if did in cards_json:
            deck_obj = cards_json[did]
            py_data['decks'][did] = {
                'id': did,
                'title': deck_obj.get('title', did),
                'cards': deck_obj.get('cards', []),
                'unitId': deck_to_skill[did].rsplit('.', 1)[0]
            }
            injected_decks_count += 1
            injected_cards_count += len(deck_obj.get('cards', []))

    print(f"1. Injected {injected_decks_count} decks ({injected_cards_count} cards) into PY_MASTERY.decks")

    # 2. Add deck IDs into fIds and decks of corresponding skills
    skills_updated = 0
    for u in py_data.get('units', []):
        for s in u.get('skills', []):
            sid = s.get('id')
            decks_for_this_skill = [did for did, target_sid in deck_to_skill.items() if target_sid == sid]
            if decks_for_this_skill:
                fids = s.get('fIds', [])
                decks = s.get('decks', [])
                for did in decks_for_this_skill:
                    if did not in fids:
                        fids.append(did)
                    if did not in decks:
                        decks.append(did)
                s['fIds'] = fids
                s['decks'] = decks
                skills_updated += 1

    print(f"2. Updated {skills_updated} skills in PY_MASTERY with new deck fIds")

    # Re-serialize PY_MASTERY
    new_raw_json = json.dumps(py_data, ensure_ascii=False)
    old_block = m.group(0)
    new_block = prefix + new_raw_json + suffix
    html = html.replace(old_block, new_block, 1)

    with open(standards_path, 'w', encoding='utf-8') as f:
        f.write(html)

    with open(academy_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print("3. Successfully saved standards.html and academy.html (100% match)")

if __name__ == '__main__':
    apply_step2()
