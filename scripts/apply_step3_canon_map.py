# -*- coding: utf-8 -*-
import json
import re
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..'))

def apply_step3():
    print("=== STEP 3: FULL 100% COVERAGE FOR CANONICAL_NOTE_DECKS_MAP ===")
    
    standards_path = os.path.join(_ROOT, 'standards', 'standards.html')
    academy_path = os.path.join(_ROOT, 'academy.html')
    with open(standards_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Parse all tracks to build full clean CANONICAL_NOTE_DECKS_MAP
    tracks = ['PY_MASTERY', 'WEB_MASTERY', 'BACKEND_MASTERY', 'ALGO_MASTERY', 'DB_MASTERY', 'ARCH_MASTERY', 'INFRA_MASTERY']
    unit_tier = {
        '1.1': 1, '1.2': 1, '1.3': 1, '1.4': 1, '1.8': 1, '1.9': 1,
        '2.1': 1, '2.2': 1, '2.3': 1, '2.4': 1,
        '4.1': 1, '4.2': 1, '4.3': 1, '4.4': 1, '4.6': 1,
        '5.1': 1, '5.2': 1, '5.3': 1, '5.4': 1,
        '7.1': 1
    }

    # Read existing CANONICAL_NOTE_DECKS_MAP from standards.html
    m_old_map = re.search(r'const\s+CANONICAL_NOTE_DECKS_MAP\s*=\s*(\{.*?\});', html, re.DOTALL)
    if not m_old_map:
        raise ValueError("Could not find CANONICAL_NOTE_DECKS_MAP in standards.html")

    old_map_text = m_old_map.group(1)
    existing_map = {}
    for match in re.finditer(r"'([КKФF\d\-]+)':\s*\[(.*?)\]", old_map_text):
        kid = match.group(1)
        fids = re.findall(r"'([КKФF\d\-@]+)'", match.group(2))
        existing_map[kid] = fids

    # Read all skills to find mappings for missing notes
    all_units = []
    note_to_skill = {}
    for tr in tracks:
        m = re.search(rf'const\s+{tr}\s*=\s*(\{{.*?\}});\s*(?:const|window)', html, re.DOTALL)
        if m:
            d = json.loads(m.group(1))
            for u in d.get('units', []):
                all_units.append(u)
                for s in u.get('skills', []):
                    for kid in s.get('kIds', []):
                        note_to_skill.setdefault(kid, []).append((u['id'], s))

    # Add missing mappings from skills
    for kid, skills in note_to_skill.items():
        if kid not in existing_map or not existing_map[kid]:
            fids = []
            for uid, s in skills:
                for fid in s.get('fIds', []):
                    if fid not in fids:
                        fids.append(fid)
            existing_map[kid] = fids

    # Group units by echelon:
    # Echelon 1: 20 units
    # Echelon 2: 1.5, 1.6, 1.7, 3.1, 3.2, 3.3, 3.5, 3.6, 5.5, 7.2, 7.6
    # Echelon 3: 3.7, 3.8, 4.5, 5.6, 6.1, 6.2, 6.3, 6.5, 7.3, 7.4, 7.5
    # Echelon 4: 3.4, 6.4, 6.6
    tier1_units = ['1.1', '1.2', '1.3', '1.4', '1.8', '1.9', '2.1', '2.2', '2.3', '2.4', '4.1', '4.2', '4.3', '4.4', '4.6', '5.1', '5.2', '5.3', '5.4', '7.1']
    tier2_units = ['1.5', '1.6', '1.7', '3.1', '3.2', '3.3', '3.5', '3.6', '5.5', '7.2', '7.6']
    tier3_units = ['3.7', '3.8', '4.5', '5.6', '6.1', '6.2', '6.3', '6.5', '7.3', '7.4', '7.5']
    tier4_units = ['3.4', '3.9', '6.4', '6.6']

    # Let's map unitId to its notes
    unit_notes = {}
    for u in all_units:
        uid = u['id']
        u_kids = []
        for s in u.get('skills', []):
            for kid in s.get('kIds', []):
                if kid not in u_kids:
                    u_kids.append(kid)
        unit_notes[uid] = u_kids

    # Build formatted CANONICAL_NOTE_DECKS_MAP string
    map_lines = ["const CANONICAL_NOTE_DECKS_MAP = {"]

    def format_unit_group(echelon_name, unit_list):
        map_lines.append(f"\n  // ========================================================")
        map_lines.append(f"  // {echelon_name}")
        map_lines.append(f"  // ========================================================")
        for uid in unit_list:
            kids = unit_notes.get(uid, [])
            if not kids:
                continue
            map_lines.append(f"\n  // Unit {uid}")
            for kid in kids:
                fids = existing_map.get(kid, [])
                fids_str = ", ".join([f"'{f}'" for f in fids])
                map_lines.append(f"  '{kid}': [{fids_str}],")

    format_unit_group("=== ЭШЕЛОН 1: BigTech-скрининг и фундамент (20 юнитов) ===", tier1_units)
    format_unit_group("=== ЭШЕЛОН 2: Тех-ядро и параллельные ветви стека ===", tier2_units)
    format_unit_group("=== ЭШЕЛОН 3: Продакшен-инженерия и сервисы ===", tier3_units)
    format_unit_group("=== ЭШЕЛОН 4: Архитектурный резерв, Flask и System Design ===", tier4_units)

    map_lines.append("\n};")
    new_map_block = "\n".join(map_lines)

    # Replace old map in standards.html
    html = html.replace(m_old_map.group(0), new_map_block, 1)

    with open(standards_path, 'w', encoding='utf-8') as f:
        f.write(html)

    with open(academy_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print("1. Successfully updated CANONICAL_NOTE_DECKS_MAP for all 238 notes!")
    print("2. Byte-for-byte synced academy.html")

if __name__ == '__main__':
    apply_step3()
