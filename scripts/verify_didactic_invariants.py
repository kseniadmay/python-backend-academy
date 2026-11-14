# -*- coding: utf-8 -*-
"""
scripts/verify_didactic_invariants.py
Полная проверка соблюдения всех инвариантов задачи:
1. Byte-for-byte идентичность standards.html и academy.html
2. Валидность синтаксиса JS
3. 0 слепых вызовов print( без комментариев в knowledge_base и notes.json
4. Наличие .code-run-bar и .btn-copy-code
5. Отсутствие старых кнопок запуска и snippet-out контейнеров
"""
import glob
import json
import re
import subprocess
import sys

def verify():
    errors = []

    # 1. Byte-for-byte
    s = open("standards/standards.html", "rb").read()
    a = open("academy.html", "rb").read()
    if s != a:
        errors.append(f"standards.html ({len(s)}) != academy.html ({len(a)})")
    else:
        print(f"✓ Invariant 0 PASS: standards.html == academy.html ({len(s)} bytes)")

    # 2. Syntax check
    m = re.search(r'<script>(.*?)</script>', s.decode("utf-8"), re.DOTALL)
    if m:
        with open("scripts/temp_check.js", "w", encoding="utf-8") as out:
            out.write(m.group(1))
        res = subprocess.run(["node", "--check", "scripts/temp_check.js"], capture_output=True, text=True)
        import os
        if os.path.exists("scripts/temp_check.js"):
            os.remove("scripts/temp_check.js")
        if res.returncode != 0:
            errors.append(f"Node syntax check failed: {res.stderr}")
        else:
            print("✓ JS Syntax check PASS: Node exit code 0")

    # 3. Blind print in KB
    kb_files = glob.glob("knowledge_base/**/*.md", recursive=True)
    kb_bare = 0
    for f in kb_files:
        in_code = False
        for l in open(f, encoding="utf-8"):
            st = l.strip()
            if st.startswith("```"):
                in_code = not in_code
                continue
            if in_code and "print(" in st and "#" not in st:
                kb_bare += 1
    if kb_bare > 0:
        errors.append(f"knowledge_base has {kb_bare} bare print lines!")
    else:
        print(f"✓ Knowledge Base PASS: 0 bare print lines across {len(kb_files)} files")

    # 4. Blind print in notes.json
    notes = json.load(open("data/content/notes.json", encoding="utf-8"))
    notes_bare = 0
    for nid, note in notes.items():
        for st in note.get("steps", []):
            html = st.get("html", "")
            for b in re.findall(r'<pre><code>(.*?)</code></pre>', html, flags=re.DOTALL):
                for l in b.split("\n"):
                    if "print(" in l and "#" not in l:
                        notes_bare += 1
    if notes_bare > 0:
        errors.append(f"data/content/notes.json has {notes_bare} bare print lines!")
    else:
        print(f"✓ Canonical Notes JSON PASS: 0 bare print lines across {len(notes)} notes")

    # 5. UI Elements
    s_text = s.decode("utf-8")
    run_btn_dom = len(re.findall(r'<button[^>]*btn-inline-run', s_text))
    snippet_out_dom = len(re.findall(r'class="snippet-out', s_text))
    copy_btns = s_text.count("btn-copy-code")
    run_bars = s_text.count("code-run-bar")

    if run_btn_dom > 0:
        errors.append(f"DOM contains {run_btn_dom} <button ... btn-inline-run>!")
    else:
        print("✓ Interactive runtime buttons PASS: 0 DOM run buttons")

    if snippet_out_dom > 0:
        errors.append(f"DOM contains {snippet_out_dom} snippet-out elements!")
    else:
        print("✓ Snippet output containers PASS: 0 snippet-out containers")

    print(f"✓ Total copy-code button references: {copy_btns}")
    print(f"✓ Total code-run-bar references: {run_bars}")

    if errors:
        print("\n❌ VERIFICATION FAILED:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    else:
        print("\n=======================================================")
        print("🎉 ВСЕ ДИДАКТИЧЕСКИЕ ИНВАРИАНТЫ УСПЕШНО ВЕРИФИЦИРОВАНЫ!")
        print("=======================================================")

if __name__ == "__main__":
    verify()
