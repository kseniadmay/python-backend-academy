# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

with open("mockup_echelon_and_13_dots.html", "r", encoding="utf-8") as f:
    html = f.read()

# Обновляем мета-текст шкалы на целевую формулировку готовности к собеседованию
old_meta = """<div class="echelon-meta-line">
              <span style="font-weight:800;color:var(--ink);">🚨 Эшелон 1 · Скрининг и база</span>
              <span style="color:var(--amber);font-family:var(--font-m);font-weight:700;">42% (5/12 юнитов)</span>
            </div>
            <div class="echelon-bar-track">
              <div class="echelon-bar-fill" style="width: 42%;"></div>
            </div>"""

new_meta = """<div class="echelon-meta-line">
              <span style="font-weight:800;color:var(--ink);display:flex;align-items:center;gap:6px;">
                <span>🚨 Эшелон 1: Скрининг и база</span>
              </span>
              <span style="color:#34d399;font-family:var(--font-m);font-weight:800;display:flex;align-items:center;gap:5px;">
                <span style="color:var(--amber);">🎯</span> 35% готовности к тех-скринингу
              </span>
            </div>
            <div class="echelon-bar-track">
              <div class="echelon-bar-fill" style="width: 35%;"></div>
            </div>"""

if old_meta in html:
    html = html.replace(old_meta, new_meta, 1)
else:
    # fallback replace
    html = html.replace("42% (5/12 юнитов)", "🎯 35% готовности к тех-скринингу")
    html = html.replace("style=\"width: 42%;\"", "style=\"width: 35%;\"")

with open("mockup_echelon_and_13_dots.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("design_mockups/mockup_echelon_and_13_dots.html", "w", encoding="utf-8") as f:
    f.write(html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\echelon_interview_readiness.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_echelon_and_13_dots.html"
])

brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
src_full = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\echelon_interview_readiness.png"
shutil.copyfile(src_full, os.path.join(brain_dir, "echelon_interview_readiness.png"))

img = Image.open(src_full)
crop = img.crop((260, 0, 1420, 220))
crop.save(r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\echelon_interview_readiness_crop.png")
crop.save(os.path.join(brain_dir, "echelon_interview_readiness_crop.png"))

print("Captured interview readiness bar successfully!")
