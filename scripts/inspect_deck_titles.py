# -*- coding: utf-8 -*-
with open(r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'("Ф-001"\s*:\s*\{[^}]+})', text)
print("matches count:", len(matches))
if matches:
    print(matches[0][:300])

matches_k = re.findall(r'("К-001"\s*:\s*\{[^}]+})', text)
print("matches_k count:", len(matches_k))
if matches_k:
    print(matches_k[0][:300])
