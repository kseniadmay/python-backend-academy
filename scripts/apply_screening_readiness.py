# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

with open("mockup_organic_dots_above_slice.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Убираем крестик [✕] и меняем текст на точную формулировку
# "🚨 Эшелон 1: Скрининг" и "35% готовности"

old_topbar = """        <!-- 1. ТОПБАР: ТОЛЬКО ЭШЕЛОН И ГОТОВНОСТЬ К СКРИНИНГУ -->
        <div class="echelon-topbar-clean">
          <a href="#/python" class="echelon-clean-close" title="Выйти к карте">✕</a>
          <div class="echelon-clean-wrap">
            <div class="echelon-clean-meta">
              <span style="font-weight:800;color:var(--ink);">🚨 Эшелон 1: Скрининг и база</span>
              <span style="color:#34d399;font-family:var(--font-m);font-weight:800;">
                <span style="color:var(--amber);">🎯</span> 35% готовности к тех-скринингу
              </span>
            </div>
            <div class="echelon-clean-track">
              <div class="echelon-clean-fill"></div>
            </div>
          </div>
          <div style="display:flex;gap:8px;align-items:center;">
            <div class="sprint-xp-pill">⚡ +10 XP</div>
            <a href="#/docs" class="topbar-help-btn" style="padding:6px 12px;border-radius:10px;"><span class="topbar-help-text">📖 Справка</span></a>
          </div>
        </div>"""

new_topbar = """        <!-- 1. ТОПБАР: БЕЗ КРЕСТИКА, С ЧЕТКОЙ ШКАЛОЙ ГОТОВНОСТИ -->
        <div class="echelon-topbar-clean" style="padding: 12px 20px;">
          <div class="echelon-clean-wrap">
            <div class="echelon-clean-meta" style="font-size: 0.78rem;">
              <span style="font-weight:800;color:var(--ink);">🚨 Эшелон 1: Скрининг</span>
              <span style="color:#34d399;font-family:var(--font-m);font-weight:800;">
                <span style="color:var(--amber);">🎯</span> 35% готовности
              </span>
            </div>
            <div class="echelon-clean-track" style="height: 6px; margin-top: 3px;">
              <div class="echelon-clean-fill" style="width: 35%;"></div>
            </div>
          </div>
          <div style="display:flex;gap:10px;align-items:center;margin-left:14px;">
            <div class="sprint-xp-pill" title="Очки опыта за завершение шага">⚡ +10 XP</div>
            <a href="#/docs" class="topbar-help-btn" style="padding:6px 12px;border-radius:10px;"><span class="topbar-help-text">📖 Справка</span></a>
          </div>
        </div>"""

if old_topbar in html:
    html = html.replace(old_topbar, new_topbar, 1)
else:
    # generic replace
    html = html.replace('<a href="#/python" class="echelon-clean-close" title="Выйти к карте">✕</a>', '')
    html = html.replace('🚨 Эшелон 1: Скрининг и база', '🚨 Эшелон 1: Скрининг')
    html = html.replace('35% готовности к тех-скринингу', '35% готовности')

with open("mockup_organic_dots_above_slice.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("design_mockups/mockup_organic_dots_above_slice.html", "w", encoding="utf-8") as f:
    f.write(html)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\no_cross_screening_ready.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_organic_dots_above_slice.html"
])

brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
src_full = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\no_cross_screening_ready.png"
shutil.copyfile(src_full, os.path.join(brain_dir, "no_cross_screening_ready.png"))

img = Image.open(src_full)
crop = img.crop((260, 0, 1420, 240))
crop.save(r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\no_cross_screening_ready_crop.png")
crop.save(os.path.join(brain_dir, "no_cross_screening_ready_crop.png"))

print("Updated without cross and rendered successfully!")
