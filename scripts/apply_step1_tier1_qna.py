# -*- coding: utf-8 -*-
import os
import sys
import re
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..'))

from tier1_qna_enrichment_map import TIER1_REPLACEMENTS, ANSWER_REPLACEMENTS

def apply_step1():
    print("=== STEP 1: APPLYING TIER 1 Q&A ENRICHMENTS ===")
    
    # 1. Update data/content/cards.json
    cards_json_path = os.path.join(_ROOT, 'data', 'content', 'cards.json')
    with open(cards_json_path, 'r', encoding='utf-8') as f:
        cards_data = json.load(f)
        
    q_updated = 0
    a_updated = 0
    
    for deck_id, deck in cards_data.items():
        cards = deck.get('cards', [])
        for idx, c in enumerate(cards):
            q = c.get('q', '').strip()
            # Check question replacements
            if q in TIER1_REPLACEMENTS:
                c['q'] = TIER1_REPLACEMENTS[q]
                q_updated += 1
            # Check answer replacements
            if (deck_id, idx) in ANSWER_REPLACEMENTS:
                c['a'] = ANSWER_REPLACEMENTS[(deck_id, idx)]
                a_updated += 1
                
    with open(cards_json_path, 'w', encoding='utf-8') as f:
        json.dump(cards_data, f, ensure_ascii=False, indent=2)
    print(f"1. Updated cards.json: {q_updated} questions, {a_updated} answers")

    # 2. Update knowledge_base markdown files
    def html_to_md(text):
        s = text
        s = s.replace('<code>', '`').replace('</code>', '`')
        s = s.replace('&quot;', '"').replace('&#x27;', "'")
        s = s.replace('&gt;', '>').replace('&lt;', '<')
        s = s.replace('&amp;', '&')
        return s

    kb_dir = os.path.join(_ROOT, 'knowledge_base')
    kb_files_updated = 0
    
    # build deck_id to target replacements
    decks_to_patch = set(k[0] for k in ANSWER_REPLACEMENTS.keys())
    
    for root, dirs, files in os.walk(kb_dir):
        for fname in files:
            if fname.endswith('.md') and fname.startswith('Ф-'):
                fid = re.match(r'(Ф-\d+)', fname).group(1)
                fpath = os.path.join(root, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                lines = content.splitlines()
                changed = False
                new_lines = []
                
                # Each card is line: N. Question >> Answer
                card_idx = 0
                for line in lines:
                    m = re.match(r'^(\d+\.\s+)(.*?)\s*(>>\s*.*)$', line)
                    if m:
                        num_pfx = m.group(1)
                        q_part = m.group(2).strip()
                        raw_ans = m.group(3)
                        ans_part = re.sub(r'^>>\s*', '', raw_ans).strip()
                        
                        # Match Q
                        for orig_q, repl_q in TIER1_REPLACEMENTS.items():
                            orig_md = html_to_md(orig_q).strip()
                            if q_part == orig_md or q_part.replace('`', '') == orig_md.replace('`', ''):
                                q_part = html_to_md(repl_q).strip()
                                changed = True
                                break
                                
                        # Match A
                        if (fid, card_idx) in ANSWER_REPLACEMENTS:
                            ans_part = html_to_md(ANSWER_REPLACEMENTS[(fid, card_idx)]).strip()
                            changed = True
                            
                        new_lines.append(f"{num_pfx}{q_part} >> {ans_part}")
                        card_idx += 1
                    else:
                        new_lines.append(line)
                        
                if changed:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines) + '\n')
                    kb_files_updated += 1
                    
    print(f"2. Updated {kb_files_updated} markdown files in knowledge_base")

    # 3. Update standards/standards.html
    standards_path = os.path.join(_ROOT, 'standards', 'standards.html')
    academy_path = os.path.join(_ROOT, 'academy.html')
    
    with open(standards_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    tracks = ['PY_MASTERY', 'WEB_MASTERY', 'BACKEND_MASTERY', 'ALGO_MASTERY', 'DB_MASTERY', 'ARCH_MASTERY', 'INFRA_MASTERY']
    std_q_updated = 0
    std_a_updated = 0
    
    for tr in tracks:
        m = re.search(rf'(const\s+{tr}\s*=\s*)(\{{.*?\}})(;\s*(?:const|window))', html, re.DOTALL)
        if m:
            prefix = m.group(1)
            raw_json = m.group(2)
            suffix = m.group(3)
            data = json.loads(raw_json)
            
            decks = data.get('decks', {})
            track_changed = False
            for did, d in decks.items():
                for idx, c in enumerate(d.get('cards', [])):
                    q = c.get('q', '').strip()
                    if q in TIER1_REPLACEMENTS:
                        c['q'] = TIER1_REPLACEMENTS[q]
                        std_q_updated += 1
                        track_changed = True
                    if (did, idx) in ANSWER_REPLACEMENTS:
                        c['a'] = ANSWER_REPLACEMENTS[(did, idx)]
                        std_a_updated += 1
                        track_changed = True
                        
            if track_changed:
                new_raw_json = json.dumps(data, ensure_ascii=False)
                old_block = m.group(0)
                new_block = prefix + new_raw_json + suffix
                html = html.replace(old_block, new_block, 1)

    print(f"3. Updated standards/standards.html: {std_q_updated} questions, {std_a_updated} answers")

    with open(standards_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    with open(academy_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"4. Synced academy.html (100% byte-for-byte identical to standards.html)")

if __name__ == '__main__':
    apply_step1()
