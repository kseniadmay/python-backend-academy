#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
_ROOT = os.path.normpath(os.path.join(_HERE, '..'))

from question_replacements_map import REPLACEMENTS_MAP

def apply_improvements():
    print(f"Applying {len(REPLACEMENTS_MAP)} question improvements across the academy...")
    
    # 1. Update data/content/cards.json
    cards_json_path = os.path.join(_ROOT, 'data', 'content', 'cards.json')
    cards_json_updated = 0
    if os.path.isfile(cards_json_path):
        with open(cards_json_path, 'r', encoding='utf-8') as f:
            cards_data = json.load(f)
        for deck_id, deck in cards_data.items():
            for card in deck.get('cards', []):
                q = card.get('q', '').strip()
                if q in REPLACEMENTS_MAP:
                    card['q'] = REPLACEMENTS_MAP[q]
                    cards_json_updated += 1
        with open(cards_json_path, 'w', encoding='utf-8') as f:
            json.dump(cards_data, f, ensure_ascii=False, indent=2)
        print(f"1. Updated {cards_json_updated} cards in {cards_json_path}")

    # 2. Update knowledge_base markdown files
    kb_dir = os.path.join(_ROOT, 'knowledge_base')
    kb_updated_files = 0
    kb_updated_questions = 0
    
    # Helper to convert HTML-formatted replacement to markdown format
    def html_to_md(text):
        s = text
        s = s.replace('<code>', '`').replace('</code>', '`')
        s = s.replace('&quot;', '"').replace('&#x27;', "'")
        s = s.replace('&gt;', '>').replace('&lt;', '<')
        s = s.replace('&amp;', '&')
        s = re.sub(r'<span class="math-formula">(.*?)</span>', r'\1', s)
        return s

    md_replacements = {}
    for orig_html_q, new_html_q in REPLACEMENTS_MAP.items():
        orig_md = html_to_md(orig_html_q).strip()
        new_md = html_to_md(new_html_q).strip()
        md_replacements[orig_md] = new_md

    for root, dirs, files in os.walk(kb_dir):
        for fname in files:
            if fname.endswith('.md') and 'Карточки' in root:
                fpath = os.path.join(root, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                file_changed = False
                
                # Check line by line: lines usually start with "N. Question? >> Answer"
                lines = content.splitlines()
                new_lines = []
                for line in lines:
                    m = re.match(r'^(\d+\.\s+)(.*?)\s*(>>\s*.*)$', line)
                    if m:
                        num_prefix = m.group(1)
                        line_q = m.group(2).strip()
                        ans_suffix = m.group(3)
                        
                        # Match with md_replacements
                        matched = False
                        if line_q in md_replacements:
                            line_q = md_replacements[line_q]
                            matched = True
                        else:
                            # Try normalizing backticks or quotes
                            norm_line_q = line_q.replace('"', "'").replace('`', '')
                            for orig_k, repl_v in md_replacements.items():
                                if orig_k.replace('"', "'").replace('`', '') == norm_line_q:
                                    line_q = repl_v
                                    matched = True
                                    break
                        if matched:
                            file_changed = True
                            kb_updated_questions += 1
                            new_lines.append(f"{num_prefix}{line_q} {ans_suffix}")
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)
                        
                if file_changed:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines) + '\n')
                    kb_updated_files += 1

    print(f"2. Updated {kb_updated_questions} questions across {kb_updated_files} markdown files in knowledge_base")

    # 3. Update standards/standards.html
    standards_path = os.path.join(_ROOT, 'standards', 'standards.html')
    academy_path = os.path.join(_ROOT, 'academy.html')
    
    with open(standards_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    html_replaced_count = 0
    tracks = ['PY_MASTERY', 'WEB_MASTERY', 'BACKEND_MASTERY', 'ALGO_MASTERY', 'DB_MASTERY', 'ARCH_MASTERY', 'INFRA_MASTERY']
    
    # We will update the JSON objects inside each track
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
                for card in d.get('cards', []):
                    q = card.get('q', '').strip()
                    if q in REPLACEMENTS_MAP:
                        card['q'] = REPLACEMENTS_MAP[q]
                        html_replaced_count += 1
                        track_changed = True
                        
            if track_changed:
                new_raw_json = json.dumps(data, ensure_ascii=False)
                # replace in html
                old_block = m.group(0)
                new_block = prefix + new_raw_json + suffix
                html = html.replace(old_block, new_block, 1)

    print(f"3. Updated {html_replaced_count} cards in standards/standards.html")

    # Save to standards/standards.html
    with open(standards_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # Save identical content to academy.html (Canonical Benchmark Invariant)
    with open(academy_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"4. Synced academy.html (strictly identical to standards/standards.html)")

if __name__ == '__main__':
    apply_improvements()
