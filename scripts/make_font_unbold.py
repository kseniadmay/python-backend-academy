# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

ACADEMY_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"

with open(ACADEMY_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Меняем CSS: убираем font-weight 700/800 на 400/500
code = code.replace(
    """.echelon-clean-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.76rem;
    font-weight: 700;
    white-space: nowrap;
  }""",
    """.echelon-clean-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.76rem;
    font-weight: 400;
    white-space: nowrap;
  }"""
)

code = code.replace(
    """.topic-eyebrow-tags {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.76rem;
    font-weight: 700;
    color: var(--ink-muted);
  }
  .topic-eyebrow-unit {
    color: var(--ink);
    font-weight: 800;
  }
  .topic-eyebrow-num {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.25);
    color: var(--moss);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.70rem;
    font-weight: 700;
  }""",
    """.topic-eyebrow-tags {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.76rem;
    font-weight: 400;
    color: var(--ink-muted);
  }
  .topic-eyebrow-unit {
    color: var(--ink);
    font-weight: 500;
  }
  .topic-eyebrow-num {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.25);
    color: var(--moss);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.70rem;
    font-weight: 500;
  }"""
)

code = code.replace(
    """.dots-necklace-label {
    font-size: 0.72rem;
    font-family: var(--font-m);
    font-weight: 800;
    color: var(--moss);
    margin-left: 2px;
    position: relative;
    z-index: 3;
  }""",
    """.dots-necklace-label {
    font-size: 0.72rem;
    font-family: var(--font-m);
    font-weight: 500;
    color: var(--moss);
    margin-left: 2px;
    position: relative;
    z-index: 3;
  }"""
)

# 2. Меняем HTML в focusTopbarHTML: убираем strong и font-weight 800
old_meta_line = """          <span><strong style="color:var(--ink);">${echMeta.shortLabel}</strong> <span style="color:rgba(255,255,255,0.28);margin:0 4px;">·</span> <span style="color:var(--ink-muted);font-weight:600;">${echMeta.focus}</span></span>
          <span style="color:${echMeta.color || '#34d399'};font-family:var(--font-m);font-weight:800;">
            🎯 ${echPct}% готовности ${echMeta.targetLabel}
          </span>"""

new_meta_line = """          <span><span style="color:var(--ink);font-weight:500;">${echMeta.shortLabel}</span> <span style="color:rgba(255,255,255,0.28);margin:0 4px;">·</span> <span style="color:var(--ink-muted);font-weight:400;">${echMeta.focus}</span></span>
          <span style="color:${echMeta.color || '#34d399'};font-family:var(--font-m);font-weight:500;">
            🎯 ${echPct}% готовности ${echMeta.targetLabel}
          </span>"""

if old_meta_line in code:
    code = code.replace(old_meta_line, new_meta_line, 1)
    print("Replaced meta line: removed strong and 800")
else:
    print("WARNING: old_meta_line not found")

# В pill меняем font-weight 700 на 500
code = code.replace("font-weight:700;white-space:nowrap;letter-spacing:0.01em;", "font-weight:500;white-space:nowrap;letter-spacing:0.01em;")

with open(ACADEMY_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved unbold academy.html")

# 3. Скриншот
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
live_png = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\live_skill_111_unbold.png"

subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    f"--screenshot={live_png}",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/academy.html#/python/skill/1.1.1"
])

img = Image.open(live_png)
crop = img.crop((260, 0, 1420, 320))
crop_png = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\live_skill_111_unbold_crop.png"
crop.save(crop_png)

shutil.copyfile(live_png, os.path.join(brain_dir, "live_skill_111_unbold.png"))
shutil.copyfile(crop_png, os.path.join(brain_dir, "live_skill_111_unbold_crop.png"))

print("Captured unbold screenshot!")
