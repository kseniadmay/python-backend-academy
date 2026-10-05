#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, sys, os, re, json

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)

res = subprocess.run(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'], capture_output=True, text=True)
if res.returncode != 0:
    sys.exit(0)

files = [f.strip() for f in res.stdout.splitlines() if f.strip()]

for f in files:
    if f.endswith('.js') and os.path.isfile(f):
        c = subprocess.run(['node', '--check', f], capture_output=True, text=True)
        if c.returncode != 0:
            print(f"[HOOK ERROR] Ошибка синтаксиса JS в {f}:\n{c.stderr}")
            sys.exit(1)
    elif f.endswith('.py') and os.path.isfile(f):
        c = subprocess.run([sys.executable, '-m', 'py_compile', f], capture_output=True, text=True)
        if c.returncode != 0:
            print(f"[HOOK ERROR] Ошибка синтаксиса Python в {f}:\n{c.stderr}")
            sys.exit(1)
    elif f.endswith('.json') and os.path.isfile(f):
        try:
            with open(f, encoding='utf-8') as jf:
                json.load(jf)
        except Exception as e:
            print(f"[HOOK ERROR] Ошибка синтаксиса JSON в {f}:\n{e}")
            sys.exit(1)
    elif f == 'academy.html' and os.path.isfile(f):
        with open(f, encoding='utf-8') as hf:
            html = hf.read()
        scripts = re.findall(r'<script>([\s\S]*?)</script>', html)
        if scripts:
            tmp = os.path.join(root, 'scripts', 'tmp_hook_check.js')
            with open(tmp, 'w', encoding='utf-8') as tf:
                tf.write(scripts[0])
            c = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
            if os.path.exists(tmp):
                try: os.remove(tmp)
                except Exception: pass
            if c.returncode != 0:
                print(f"[HOOK ERROR] Ошибка синтаксиса inline JS в academy.html:\n{c.stderr}")
                sys.exit(1)

print("✓ [Pre-Commit] Синтаксическая проверка пройдена (JS, Python, JSON в норме).")
sys.exit(0)
