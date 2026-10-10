# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

with open("mockup_organic_dots_above_slice.html", "r", encoding="utf-8") as f:
    html = f.read()

# Убираем бейдж +10 XP из шапки полностью
old_right_controls = """          <div style="display:flex;gap:10px;align-items:center;margin-left:14px;">
            <div class="sprint-xp-pill" title="Очки опыта за завершение шага">⚡ +10 XP</div>
            <a href="#/docs" class="topbar-help-btn" style="padding:6px 12px;border-radius:10px;"><span class="topbar-help-text">📖 Справка</span></a>
          </div>"""

new_right_controls = """          <div style="display:flex;gap:10px;align-items:center;margin-left:14px;">
            <a href="#/docs" class="topbar-help-btn" style="padding:6px 14px;border-radius:10px;"><span class="topbar-help-text">📖 Справка</span></a>
          </div>"""

if old_right_controls in html:
    html = html.replace(old_right_controls, new_right_controls, 1)
else:
    # fallback removal
    html = html.replace('<div class="sprint-xp-pill" title="Очки опыта за завершение шага">⚡ +10 XP</div>', '')
    html = html.replace('<div class="sprint-xp-pill">⚡ +10 XP</div>', '')

with open("mockup_organic_dots_above_slice.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("design_mockups/mockup_organic_dots_above_slice.html", "w", encoding="utf-8") as f:
    f.write(html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\clean_header_no_xp_badge.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_organic_dots_above_slice.html"
])

brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
src_full = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\clean_header_no_xp_badge.png"
shutil.copyfile(src_full, os.path.join(brain_dir, "clean_header_no_xp_badge.png"))

img = Image.open(src_full)
crop = img.crop((260, 0, 1420, 240))
crop.save(r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\clean_header_no_xp_badge_crop.png")
crop.save(os.path.join(brain_dir, "clean_header_no_xp_badge_crop.png"))

print("Captured clean header without XP badge successfully!")
