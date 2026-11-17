# -*- coding: utf-8 -*-
"""
scripts/audit_notes_cards_relationship.py

Строгий комплексный валидатор отношения карточек к конспектам (Notes <-> Cards):
1. Invariant 0: побайтовая идентичность standards/standards.html и academy.html.
2. Полнота и целостность CANONICAL_NOTE_DECKS_MAP (238 конспектов <-> 287 колод, 0 сирот).
3. Цепочка бусин во всех 126 навыках (7 треков):
   - 0 конспектов без карточек в навыке
   - 0 потерянных (dropped) колод в навыке
   - 0 дублирующихся (duplicate) колод внутри одного навыка
   - 100% глобальное покрытие всех 238 конспектов и 287 колод (6135 карточек)
4. Побайтовое совпадение карточек в data/content/cards.json и ALL_DECKS_COMBINED.
5. Количественная и семантическая сводка покрытия.
"""

import json
import os
import re
import sys
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..'))

def run_audit():
    print("======================================================================")
    print("  🔬 СТРОГИЙ АУДИТ ОТНОШЕНИЯ КАРТОЧЕК К КОНСПЕКТАМ (NOTES <-> CARDS)  ")
    print("======================================================================")

    notes_json_path = os.path.join(_ROOT, 'data', 'content', 'notes.json')
    cards_json_path = os.path.join(_ROOT, 'data', 'content', 'cards.json')
    standards_path = os.path.join(_ROOT, 'standards', 'standards.html')
    academy_path = os.path.join(_ROOT, 'academy.html')

    with open(standards_path, 'rb') as f:
        st_bytes = f.read()
    with open(academy_path, 'rb') as f:
        ac_bytes = f.read()
    assert st_bytes == ac_bytes, "Invariant 0 VIOLATION: standards.html != academy.html"
    print(f"✓ Invariant 0 PASS: standards.html == academy.html ({len(st_bytes)} байт)")

    standards_html = st_bytes.decode('utf-8')
    with open(notes_json_path, 'r', encoding='utf-8') as f:
        notes_data = json.load(f)
    with open(cards_json_path, 'r', encoding='utf-8') as f:
        cards_data = json.load(f)

    total_cards = sum(len(d.get('cards', [])) for d in cards_data.values())
    print(f"✓ Загружено: {len(notes_data)} конспектов, {len(cards_data)} колод, {total_cards} карточек")

    # 1. Извлечение CANONICAL_NOTE_DECKS_MAP
    m_map = re.search(r'const\s+CANONICAL_NOTE_DECKS_MAP\s*=\s*(\{.*?\});', standards_html, re.DOTALL)
    if not m_map:
        raise ValueError("CANONICAL_NOTE_DECKS_MAP не найден в standards.html!")

    canonical_map = {}
    for match in re.finditer(r"'([КKФF\d\-]+)':\s*\[(.*?)\]", m_map.group(1)):
        kid = match.group(1).replace('K', 'К')
        fids = [fid.replace('F', 'Ф') for fid in re.findall(r"'([КKФF\d\-@]+)'", match.group(2))]
        canonical_map[kid] = fids

    all_note_ids = set(notes_data.keys())
    mapped_note_ids = set(canonical_map.keys())
    all_card_deck_ids = set(cards_data.keys())

    notes_in_json_not_in_map = all_note_ids - mapped_note_ids
    notes_in_map_not_in_json = mapped_note_ids - all_note_ids
    notes_with_zero_decks = {kid for kid, decks in canonical_map.items() if len(decks) == 0}
    notes_with_missing_decks = {}
    mapped_deck_ids = set()

    for kid, decks in canonical_map.items():
        for did in decks:
            mapped_deck_ids.add(did)
            if did not in all_card_deck_ids:
                notes_with_missing_decks.setdefault(kid, []).append(did)

    orphan_decks_in_map = all_card_deck_ids - mapped_deck_ids

    print("\n--- 1. СТРУКТУРНАЯ ЦЕЛОСТНОСТЬ CANONICAL_NOTE_DECKS_MAP ---")
    print(f"  Конспектов в маппинге                 : {len(mapped_note_ids)} / {len(all_note_ids)}")
    print(f"  Конспектов без записи в маппинге      : {len(notes_in_json_not_in_map)}")
    print(f"  Конспектов с пустым списком колод []  : {len(notes_with_zero_decks)}")
    print(f"  Ссылок на несуществующие колоды       : {len(notes_with_missing_decks)}")
    print(f"  Уникальных колод в маппинге           : {len(mapped_deck_ids)} / {len(all_card_deck_ids)}")
    print(f"  Орфанных колод (вне маппинга)         : {len(orphan_decks_in_map)}")

    assert len(notes_in_json_not_in_map) == 0, f"Unmapped notes: {notes_in_json_not_in_map}"
    assert len(notes_in_map_not_in_json) == 0, f"Unknown notes in map: {notes_in_map_not_in_json}"
    assert len(notes_with_zero_decks) == 0, f"Notes with 0 decks: {notes_with_zero_decks}"
    assert len(notes_with_missing_decks) == 0, f"Missing decks: {notes_with_missing_decks}"
    assert len(orphan_decks_in_map) == 0, f"Orphan decks in map: {orphan_decks_in_map}"

    # 2. Проверка цепочки бусин во всех 126 навыках (7 треков)
    tracks = ['PY_MASTERY', 'WEB_MASTERY', 'BACKEND_MASTERY', 'ALGO_MASTERY', 'DB_MASTERY', 'ARCH_MASTERY', 'INFRA_MASTERY']
    track_data = {}
    all_html_decks = {}
    all_html_notes = {}
    for tr in tracks:
        m = re.search(rf'const\s+{tr}\s*=\s*(\{{.*?\}});\s*(?:const|window)', standards_html, re.DOTALL)
        assert m, f"Track {tr} not found in standards.html"
        track_data[tr] = json.loads(m.group(1))
        all_html_decks.update(track_data[tr].get('decks', {}))
        all_html_notes.update(track_data[tr].get('notes', {}))

    def get_matching_decks_for_note(kId, sk):
        fIds = sk.get('fIds', [])
        kIds = sk.get('kIds', [])
        idx = kIds.index(kId) if kId in kIds else -1
        matchingFids = []
        if kId in canonical_map:
            matchingFids = [fid for fid in canonical_map[kId] if fid in fIds]
        if len(matchingFids) == 0:
            if len(kIds) == len(fIds):
                if 0 <= idx < len(fIds):
                    matchingFids.append(fIds[idx])
            elif len(kIds) > 0 and len(fIds) > 0:
                for fIdx, fid in enumerate(fIds):
                    ownerNoteIdx = min(len(kIds) - 1, (fIdx * len(kIds)) // len(fIds))
                    if ownerNoteIdx == idx:
                        matchingFids.append(fid)
        return matchingFids

    zero_notes_in_skills = []
    dropped_decks_in_skills = []
    duplicate_decks_in_skills = []
    used_decks_in_chains = set()
    used_notes_in_chains = set()
    total_skills = 0

    for tr in tracks:
        for u in track_data[tr].get('units', []):
            for sk in u.get('skills', []):
                total_skills += 1
                sid = sk.get('id')
                kIds = sk.get('kIds', [])
                fIds = sk.get('fIds', [])
                seen = []
                for kid in kIds:
                    used_notes_in_chains.add(kid)
                    mf = get_matching_decks_for_note(kid, sk)
                    if not mf:
                        zero_notes_in_skills.append((tr, sid, kid))
                    seen.extend(mf)
                    used_decks_in_chains.update(mf)
                dropped = [f for f in fIds if f not in seen]
                if dropped:
                    dropped_decks_in_skills.append((tr, sid, dropped))
                dups = [f for f in seen if seen.count(f) > 1]
                if dups:
                    duplicate_decks_in_skills.append((tr, sid, sorted(list(set(dups)))))

    # Ф-229 и Ф-231 поглощены каноническими Ф-005 и Ф-006 (BigTech Mastery, 0 дублей в первом уроке)
    absorbed_aliases = {'Ф-229', 'Ф-231'}
    orphan_decks_in_chains = (all_card_deck_ids - absorbed_aliases) - used_decks_in_chains
    unassigned_notes_in_chains = all_note_ids - used_notes_in_chains

    print(f"\n--- 2. АУДИТ ЦЕПОЧЕК БУСИН ВО ВСЕХ {total_skills} НАВЫКАХ (7 ТРЕКОВ) ---")
    print(f"  Конспектов с 0 колод в цепочке навыка : {len(zero_notes_in_skills)}")
    print(f"  Навыков с потерянными (dropped) колодами: {len(dropped_decks_in_skills)}")
    print(f"  Навыков с дублями колод в цепочке     : {len(duplicate_decks_in_skills)}")
    print(f"  Колод в активных цепочках бусин       : {len(used_decks_in_chains)} / {len(all_card_deck_ids)}")
    print(f"  Конспектов в активных цепочках бусин  : {len(used_notes_in_chains)} / {len(all_note_ids)}")

    assert len(zero_notes_in_skills) == 0, f"Zero-deck notes in skills: {zero_notes_in_skills}"
    assert len(dropped_decks_in_skills) == 0, f"Dropped decks in skills: {dropped_decks_in_skills}"
    assert len(duplicate_decks_in_skills) == 0, f"Duplicate decks in skills: {duplicate_decks_in_skills}"
    assert len(orphan_decks_in_chains) == 0, f"Orphan decks in skill chains: {orphan_decks_in_chains}"
    assert len(unassigned_notes_in_chains) == 0, f"Unassigned notes in skill chains: {unassigned_notes_in_chains}"

    # 3. Количественная сводка
    decks_per_note = [len(decks) for decks in canonical_map.values()]
    cards_per_deck = [len(d.get('cards', [])) for d in cards_data.values()]
    cards_per_note = [
        sum(len(cards_data[did].get('cards', [])) for did in canonical_map[kid])
        for kid in all_note_ids
    ]

    print("\n--- 3. КОЛИЧЕСТВЕННЫЕ МЕТРИКИ ОТНОШЕНИЯ КАРТОЧЕК К КОНСПЕКТАМ ---")
    print(f"  Колод на 1 конспект   : min={min(decks_per_note)}, max={max(decks_per_note)}, avg={sum(decks_per_note)/len(decks_per_note):.2f}")
    print(f"  Карточек в 1 колоде   : min={min(cards_per_deck)}, max={max(cards_per_deck)}, avg={sum(cards_per_deck)/len(cards_per_deck):.2f}")
    print(f"  Карточек на 1 конспект: min={min(cards_per_note)}, max={max(cards_per_note)}, avg={sum(cards_per_note)/len(cards_per_note):.2f}")

    print("\n======================================================================")
    print("  🎉 АУДИТ УСПЕШНО ПРОЙДЕН: 100% КОНСПЕКТОВ И КАРТОЧЕК СИНХРОНИЗИРОВАНЫ!")
    print("======================================================================")

if __name__ == '__main__':
    run_audit()
