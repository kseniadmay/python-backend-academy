# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

ACADEMY_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"

with open(ACADEMY_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Исправляем дублирование "Юнит 1.1: Юнит 1.1 · ..."
old_tags_block = """    const eyebrowDotsHTML = `
      <div class="topic-eyebrow-track">
        <div class="topic-eyebrow-tags">
          <span class="topic-eyebrow-unit">Юнит ${sk.unitId}: ${escapeHtmlStr(curUnit.title || sk.title || '')}</span>
          <span style="color:var(--line);">•</span>
          <span class="topic-eyebrow-num">Тема ${curNoteNum} из ${totalNotesInUnit}</span>
        </div>"""

new_tags_block = """    const rawUnitTitle = curUnit.title || sk.title || '';
    const cleanUnitTitle = rawUnitTitle.replace(/^Юнит\\s+[\\d.]+\\s*[·•\\-:]\\s*/i, '').trim() || rawUnitTitle;

    const eyebrowDotsHTML = `
      <div class="topic-eyebrow-track">
        <div class="topic-eyebrow-tags">
          <span class="topic-eyebrow-unit">Юнит ${sk.unitId}: ${escapeHtmlStr(cleanUnitTitle)}</span>
          <span style="color:var(--line);">•</span>
          <span class="topic-eyebrow-num">Тема ${curNoteNum} из ${totalNotesInUnit}</span>
        </div>"""

if old_tags_block in code:
    code = code.replace(old_tags_block, new_tags_block, 1)
    print("Fixed unit title duplication")

# 2. Оптимизируем правые контролы в echelon-topbar-clean: убираем дублирующую кнопку переключения конспекта из шапки эшелона
old_right_controls = """      <div style="display:flex;gap:10px;align-items:center;margin-left:14px;">
        <div class="sprint-xp-pill" style="display:inline-flex;align-items:center;gap:4px;padding:5px 11px;border-radius:999px;background:rgba(16,185,129,0.14);border:1px solid rgba(52,211,153,0.35);color:#34d399;font-size:0.75rem;font-weight:700;white-space:nowrap;letter-spacing:0.01em;" title="Заработано за сутки: ${dayXpVal} XP">⚡ ${dayXpVal} XP сегодня</div>
        ${pySkillViewState.tab === 'theory' ? `<button type="button" class="btn btn-ghost" data-py-toggle-fullnote style="padding:6px 12px;font-size:.76rem;border-radius:10px;" title="Переключить режим полного конспекта">${pySkillViewState.fullNoteMode ? '📖 По шагам' : '📄 Весь конспект'}</button>` : ''}
        <a href="#/docs" class="topbar-help-btn" style="padding:6px 14px;border-radius:10px;" title="Справочник синтаксиса и методов Python"><span class="topbar-help-text">📖 Справка</span></a>
      </div>"""

new_right_controls = """      <div style="display:flex;gap:10px;align-items:center;margin-left:14px;flex:none;">
        <div class="sprint-xp-pill" style="display:inline-flex;align-items:center;gap:4px;padding:5px 12px;border-radius:999px;background:rgba(16,185,129,0.14);border:1px solid rgba(52,211,153,0.35);color:#34d399;font-size:0.75rem;font-weight:700;white-space:nowrap;letter-spacing:0.01em;" title="Заработано за сутки: ${dayXpVal} XP">⚡ ${dayXpVal} XP сегодня</div>
        <a href="#/docs" class="topbar-help-btn" style="padding:6px 14px;border-radius:10px;" title="Справочник синтаксиса и методов Python"><span class="topbar-help-text">📖 Справка</span></a>
      </div>"""

if old_right_controls in code:
    code = code.replace(old_right_controls, new_right_controls, 1)
    print("Polished right controls in echelon topbar")

# 3. Добавляем white-space: nowrap в .echelon-clean-meta
code = code.replace(
    ".echelon-clean-meta {\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    font-size: 0.78rem;\n    font-weight: 700;\n  }",
    ".echelon-clean-meta {\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    font-size: 0.76rem;\n    font-weight: 700;\n    white-space: nowrap;\n  }"
)

with open(ACADEMY_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved polished academy.html")

# 4. Скриншот
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
live_png = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\live_skill_111_polished.png"

subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    f"--screenshot={live_png}",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/academy.html#/python/skill/1.1.1"
])

img = Image.open(live_png)
crop = img.crop((260, 0, 1420, 320))
crop_png = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\live_skill_111_polished_crop.png"
crop.save(crop_png)

shutil.copyfile(live_png, os.path.join(brain_dir, "live_skill_111_polished.png"))
shutil.copyfile(crop_png, os.path.join(brain_dir, "live_skill_111_polished_crop.png"))

print("Captured polished live_skill_111 screenshot!")
