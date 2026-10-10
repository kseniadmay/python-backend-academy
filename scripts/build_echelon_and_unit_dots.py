# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

with open("mockup_skill_1_1_1.html", "r", encoding="utf-8") as f:
    orig = f.read()

# 1. Стили: Шкала эшелона в шапке + Отдельная нить 13 изумрудных точек над уроком
css_tracker = """
  /* ================= 1. ШАПКА: ТОЛЬКО ШКАЛА ЭШЕЛОНА ================= */
  .echelon-topbar-only {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 10px 18px;
    margin-bottom: 18px;
    border-radius: 18px;
    background: var(--surface);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow: var(--shadow-1);
  }
  .echelon-close-btn {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--surface-2);
    border: 1px solid var(--line);
    color: var(--ink-soft);
    text-decoration: none;
    font-size: 1rem;
    font-weight: 800;
    flex: none;
    transition: all 0.2s ease;
  }
  .echelon-close-btn:hover {
    color: var(--ink);
    border-color: var(--moss);
    background: rgba(16, 185, 129, 0.12);
  }
  .echelon-bar-wrap {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  .echelon-meta-line {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--ink-soft);
  }
  .echelon-bar-track {
    height: 6px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.04);
  }
  .echelon-bar-fill {
    height: 100%;
    width: 42%;
    border-radius: 999px;
    background: linear-gradient(90deg, #be123c, #f59e0b, #10b981);
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
    transition: width 0.4s ease;
  }

  /* ================= 2. ТРЕКЕР ЮНИТА: СВЕТЯЩИЕСЯ ИЗУМРУДНЫЕ ТОЧКИ НАД СРЕЗОМ ================= */
  .unit-dots-standalone-strip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 10px 18px;
    margin-bottom: 20px;
    border-radius: 14px;
    background: rgba(22, 27, 36, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(16px);
  }
  .unit-strip-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--ink-soft);
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
  }
  .unit-strip-title strong {
    color: var(--ink);
  }

  .unit-dots-thread {
    display: flex;
    align-items: center;
    gap: 8px;
    flex: none;
  }
  .unit-dot-pip {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.25s ease;
    cursor: pointer;
    position: relative;
  }
  .unit-dot-pip:hover {
    transform: scale(1.3);
  }
  .unit-dot-pip.done {
    background: #10b981;
    border-color: #34d399;
    box-shadow: 0 0 7px rgba(16, 185, 129, 0.7);
  }
  .unit-dot-pip.active {
    width: 13px;
    height: 13px;
    background: #34d399;
    border: 2px solid #ffffff;
    box-shadow: 0 0 12px #10b981, 0 0 22px rgba(52, 211, 153, 0.85);
    animation: pip-emerald-pulse 2s infinite ease-in-out;
  }
  .unit-dot-pip.milestone {
    border-color: rgba(245, 158, 11, 0.5);
    background: rgba(245, 158, 11, 0.15);
  }
  .unit-dot-pip.milestone.active {
    border-color: #f59e0b;
    background: #f59e0b;
    box-shadow: 0 0 14px rgba(245, 158, 11, 0.8);
  }

  @keyframes pip-emerald-pulse {
    0%, 100% {
      transform: scale(1);
      box-shadow: 0 0 10px #10b981, 0 0 18px rgba(16, 185, 129, 0.65);
    }
    50% {
      transform: scale(1.22);
      box-shadow: 0 0 16px #34d399, 0 0 26px rgba(52, 211, 153, 0.9);
    }
  }

  .unit-thread-counter {
    font-size: 0.74rem;
    font-weight: 800;
    color: var(--moss);
    font-family: var(--font-m);
    margin-left: 4px;
  }
"""

# HTML новой шапки и трекера
echelon_topbar_html = """
        <!-- 1. ВЕРХНИЙ БАР: ШКАЛА ЭШЕЛОНА -->
        <div class="echelon-topbar-only">
          <a href="#/python" class="echelon-close-btn" title="Выйти к карте">✕</a>
          <div class="echelon-bar-wrap">
            <div class="echelon-meta-line">
              <span style="font-weight:800;color:var(--ink);">🚨 Эшелон 1 · Скрининг и база</span>
              <span style="color:var(--amber);font-family:var(--font-m);font-weight:700;">42% (5/12 юнитов)</span>
            </div>
            <div class="echelon-bar-track">
              <div class="echelon-bar-fill" style="width: 42%;"></div>
            </div>
          </div>
          <div style="display:flex;gap:8px;align-items:center;">
            <div class="sprint-xp-pill">⚡ +10 XP</div>
            <a href="#/docs" class="topbar-help-btn" style="padding:6px 12px;border-radius:11px;"><span class="topbar-help-text">📖 Справка</span></a>
          </div>
        </div>

        <!-- 2. СВЕТЯЩИЕСЯ ИЗУМРУДНЫЕ ТОЧКИ ЮНИТА НАД СРЕЗОМ (13 ТЕМ ЮНИТА 1.1) -->
        <div class="unit-dots-standalone-strip">
          <div class="unit-strip-title">
            <span>Юнит 1.1 · <strong>Базовые коллекции и срезы</strong></span>
            <span style="color:var(--ink-muted);">• Тема 3 из 13: Срезы</span>
          </div>

          <div class="unit-dots-thread" title="13 тем Юнита 1.1">
            <span class="unit-dot-pip done" title="1. К-001 Память и структуры (Пройдено)"></span>
            <span class="unit-dot-pip done" title="2. К-002 Индексы списков (Пройдено)"></span>
            <span class="unit-dot-pip active" title="3. К-003 Срезы list/tuple (Текущая тема)"></span>
            <span class="unit-dot-pip" title="4. К-004 Множества set/frozenset"></span>
            <span class="unit-dot-pip" title="5. К-005 Аргументы *args/**kwargs"></span>
            <span class="unit-dot-pip" title="6. К-006 Методы dict (get, keys, values)"></span>
            <span class="unit-dot-pip" title="7. К-007 Методы списков (append, extend)"></span>
            <span class="unit-dot-pip" title="8. К-008 Модуль collections (namedtuple)"></span>
            <span class="unit-dot-pip" title="9. К-009 collections (deque, Counter)"></span>
            <span class="unit-dot-pip" title="10. К-010 Pass by assignment"></span>
            <span class="unit-dot-pip" title="11. К-011 Работа с файлами (open)"></span>
            <span class="unit-dot-pip" title="12. К-012 Служебные zip, id"></span>
            <span class="unit-dot-pip milestone" title="13. Рубежный тест 1.1 (Финал)"></span>
            <span class="unit-thread-counter">3/13</span>
          </div>
        </div>
"""

html_page = orig
# Inject CSS
html_page = html_page.replace("</style>", css_tracker + "\n</style>", 1)

# Completely remove all tab blocks
html_page = html_page.replace('class="tabs-variant-block"', 'class="tabs-variant-block" style="display:none !important;"')

# Replace topbar
start_tag = '<!-- 1. ВЕРХНИЙ СПРИНТ-ТОПБАР -->'
start_idx = html_page.find(start_tag)
end_tag = '<!-- 2. БЛОК ВКЛАДОК'
end_idx = html_page.find(end_tag)

if start_idx != -1 and end_idx != -1:
    html_page = html_page[:start_idx] + echelon_topbar_html + '\n        ' + html_page[end_idx:]

# Remove any old subtitle inside stage-theory
html_page = html_page.replace('Этап 1 из 3: Теория → Карточки → Код', '')

with open("mockup_echelon_and_13_dots.html", "w", encoding="utf-8") as f:
    f.write(html_page)

with open("design_mockups/mockup_echelon_and_13_dots.html", "w", encoding="utf-8") as f:
    f.write(html_page)

# Capture screenshots via Chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\echelon_13_dots.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_echelon_and_13_dots.html"
])

brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
src_full = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\echelon_13_dots.png"
shutil.copyfile(src_full, os.path.join(brain_dir, "echelon_13_dots.png"))

# Crop top area including topbar + dots strip (x: 260 to 1420, y: 0 to 220)
img = Image.open(src_full)
crop = img.crop((260, 0, 1420, 220))
crop.save(r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\echelon_13_dots_crop.png")
crop.save(os.path.join(brain_dir, "echelon_13_dots_crop.png"))

print("Captured 13 dots mockup and crops successfully!")
