# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

with open("mockup_organic_dots_above_slice.html", "r", encoding="utf-8") as f:
    base_html = f.read()

# Мы создадим 3 варианта бейджа суточного опыта:
# Вариант 1: "⚡ +120 XP сегодня" (классический формат с плюсом и ясным словом сегодня)
# Вариант 2: "⚡ +120 XP за сутки" (буквальная формулировка из запроса пользователя)
# Вариант 3: "⚡ 120 XP сегодня" (минималистичный счетчик без плюса)

options = [
    {
        "id": "opt1_xp_today",
        "label": "Вариант 1: ⚡ +120 XP сегодня",
        "badge_html": '<div class="sprint-xp-pill" style="display:inline-flex;align-items:center;gap:4px;padding:5px 11px;border-radius:999px;background:rgba(245,158,11,0.14);border:1px solid rgba(245,158,11,0.35);color:#fbbf24;font-size:0.75rem;font-weight:700;white-space:nowrap;letter-spacing:0.01em;" title="Заработано за сутки: 120 XP">⚡ +120 XP сегодня</div>'
    },
    {
        "id": "opt2_xp_sutki",
        "label": "Вариант 2: ⚡ +120 XP за сутки",
        "badge_html": '<div class="sprint-xp-pill" style="display:inline-flex;align-items:center;gap:4px;padding:5px 11px;border-radius:999px;background:rgba(245,158,11,0.14);border:1px solid rgba(245,158,11,0.35);color:#fbbf24;font-size:0.75rem;font-weight:700;white-space:nowrap;letter-spacing:0.01em;" title="Заработано за сутки: 120 XP">⚡ +120 XP за сутки</div>'
    },
    {
        "id": "opt3_xp_minimal",
        "label": "Вариант 3: ⚡ 120 XP сегодня",
        "badge_html": '<div class="sprint-xp-pill" style="display:inline-flex;align-items:center;gap:4px;padding:5px 11px;border-radius:999px;background:rgba(16,185,129,0.14);border:1px solid rgba(52,211,153,0.35);color:#34d399;font-size:0.75rem;font-weight:700;white-space:nowrap;letter-spacing:0.01em;" title="Заработано за сутки: 120 XP">⚡ 120 XP сегодня</div>'
    }
]

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
design_dir = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups"

target_replace = """          <div style="display:flex;gap:10px;align-items:center;margin-left:14px;">
            <a href="#/docs" class="topbar-help-btn" style="padding:6px 14px;border-radius:10px;"><span class="topbar-help-text">📖 Справка</span></a>
          </div>"""

for opt in options:
    new_controls = f"""          <div style="display:flex;gap:10px;align-items:center;margin-left:14px;">
            {opt["badge_html"]}
            <a href="#/docs" class="topbar-help-btn" style="padding:6px 14px;border-radius:10px;"><span class="topbar-help-text">📖 Справка</span></a>
          </div>"""
    
    html = base_html.replace(target_replace, new_controls)
    html_path = os.path.join(design_dir, f"{opt['id']}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    full_png = os.path.join(design_dir, f"{opt['id']}.png")
    subprocess.run([
        chrome_path,
        "--headless=new", "--disable-gpu", "--window-size=1440,900",
        f"--screenshot={full_png}",
        f"file:///{html_path.replace(os.sep, '/')}"
    ])
    
    # Crop
    img = Image.open(full_png)
    crop = img.crop((260, 0, 1420, 240))
    crop_path = os.path.join(design_dir, f"{opt['id']}_crop.png")
    crop.save(crop_path)
    
    # Copy to brain
    shutil.copyfile(full_png, os.path.join(brain_dir, f"{opt['id']}.png"))
    shutil.copyfile(crop_path, os.path.join(brain_dir, f"{opt['id']}_crop.png"))
    print(f"Rendered {opt['id']}")

print("All rendered!")
