# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

with open("mockup_skill_1_1_1.html", "r", encoding="utf-8") as f:
    orig = f.read()

# Стили для ультра-чистого Варианта А:
# 1. Топбар содержит ТОЛЬКО шкалу эшелона (35% готовности к тех-скринингу).
# 2. Точки юнита расположены ПРЯМО НАД СРЕЗОМ органично, без громоздкой серой рамки!
organic_css = """
  /* ================= ТОПБАР: ТОЛЬКО ЭШЕЛОН И ГОТОВНОСТЬ ================= */
  .echelon-topbar-clean {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 18px;
    margin-bottom: 24px;
    border-radius: 18px;
    background: var(--surface);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow: var(--shadow-1);
  }
  .echelon-clean-close {
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
  }
  .echelon-clean-wrap {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  .echelon-clean-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.74rem;
    font-weight: 700;
  }
  .echelon-clean-track {
    height: 6px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.04);
  }
  .echelon-clean-fill {
    height: 100%;
    width: 35%;
    border-radius: 999px;
    background: linear-gradient(90deg, #be123c, #f59e0b 50%, #10b981 100%);
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.45);
  }

  /* ================= ТОЧКИ ПРЯМО НАД СРЕЗОМ (БЕЗ РАМОК И ПЛАШЕК) ================= */
  .topic-eyebrow-track {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 12px;
    padding: 0 2px;
  }
  .topic-eyebrow-tags {
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
  }

  /* Нить светящихся точек */
  .dots-necklace {
    display: flex;
    align-items: center;
    gap: 9px;
    position: relative;
    padding: 4px 6px;
  }
  .dots-necklace-wire {
    position: absolute;
    left: 8px;
    right: 20px;
    height: 1.5px;
    background: rgba(255, 255, 255, 0.10);
    z-index: 1;
  }
  .dots-necklace-wire-active {
    position: absolute;
    left: 8px;
    width: 36px;
    height: 1.5px;
    background: #10b981;
    box-shadow: 0 0 6px #10b981;
    z-index: 2;
  }

  .dot-jewel {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #0d1016;
    border: 1.5px solid rgba(255, 255, 255, 0.18);
    position: relative;
    z-index: 3;
    transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
  }
  .dot-jewel:hover {
    transform: scale(1.4);
  }
  .dot-jewel.done {
    background: #10b981;
    border-color: #34d399;
    box-shadow: 0 0 7px rgba(16, 185, 129, 0.75);
  }
  .dot-jewel.active {
    width: 14px;
    height: 14px;
    background: #34d399;
    border: 2px solid #ffffff;
    box-shadow: 0 0 12px #10b981, 0 0 24px rgba(52, 211, 153, 0.9);
    animation: jewel-pulse 2s infinite ease-in-out;
  }
  .dot-jewel.milestone {
    border-color: rgba(245, 158, 11, 0.6);
    background: rgba(245, 158, 11, 0.15);
  }
  @keyframes jewel-pulse {
    0%, 100% {
      transform: scale(1);
      box-shadow: 0 0 10px #10b981, 0 0 18px rgba(16, 185, 129, 0.65);
    }
    50% {
      transform: scale(1.2);
      box-shadow: 0 0 16px #34d399, 0 0 28px rgba(52, 211, 153, 0.95);
    }
  }

  .dots-necklace-label {
    font-size: 0.72rem;
    font-family: var(--font-m);
    font-weight: 800;
    color: var(--moss);
    margin-left: 2px;
    position: relative;
    z-index: 3;
  }
"""

organic_topbar = """
        <!-- 1. ТОПБАР: ТОЛЬКО ЭШЕЛОН И ГОТОВНОСТЬ К СКРИНИНГУ -->
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
        </div>
"""

organic_card_top = """
        <!-- 2. ЭКРАН УРОКА: ТОЧКИ ОРГАНИЧНО НАД ЗАГОЛОВКОМ (БЕЗ РАМОК) -->
        <div id="stage-theory" class="stage-view">
          <div class="coddy-lesson-card" style="max-width:780px;margin:0 auto;">
            
            <!-- ОРГАНИЧЕСКАЯ НИТЬ ТОЧЕК НАД СРЕЗОМ -->
            <div class="topic-eyebrow-track">
              <div class="topic-eyebrow-tags">
                <span class="topic-eyebrow-unit">Юнит 1.1: Базовые коллекции</span>
                <span style="color:var(--line);">•</span>
                <span class="topic-eyebrow-num">Тема 3 из 13</span>
              </div>

              <div class="dots-necklace" title="13 тем Юнита 1.1">
                <div class="dots-necklace-wire"></div>
                <div class="dots-necklace-wire-active"></div>
                <span class="dot-jewel done" title="1. К-001 Память (Пройдено)"></span>
                <span class="dot-jewel done" title="2. К-002 Индексы (Пройдено)"></span>
                <span class="dot-jewel active" title="3. К-003 Срезы (Текущая тема)"></span>
                <span class="dot-jewel" title="4. К-004 Множества"></span>
                <span class="dot-jewel" title="5. К-005 Аргументы"></span>
                <span class="dot-jewel" title="6. К-006 Методы dict"></span>
                <span class="dot-jewel" title="7. К-007 Методы list"></span>
                <span class="dot-jewel" title="8. К-008 namedtuple"></span>
                <span class="dot-jewel" title="9. К-009 deque, Counter"></span>
                <span class="dot-jewel" title="10. К-010 Pass by assignment"></span>
                <span class="dot-jewel" title="11. К-011 Файлы"></span>
                <span class="dot-jewel" title="12. К-012 zip, id"></span>
                <span class="dot-jewel milestone" title="13. Рубежный тест 1.1 👑"></span>
                <span class="dots-necklace-label">3/13</span>
              </div>
            </div>

            <div class="lesson-theory">
              <h1 style="font-size:1.45rem;font-weight:800;margin:0 0 12px;color:var(--ink);letter-spacing:-0.02em;">Срез – это всегда копия</h1>
"""

html_page = orig
html_page = html_page.replace("</style>", organic_css + "\n</style>", 1)
html_page = html_page.replace('class="tabs-variant-block"', 'class="tabs-variant-block" style="display:none !important;"')

start_topbar = '<!-- 1. ВЕРХНИЙ СПРИНТ-ТОПБАР -->'
start_idx = html_page.find(start_topbar)
end_stage_h3 = html_page.find('<h3 style="font-size:1.25rem;font-weight:700;margin-bottom:12px;color:var(--ink);">Срез – это всегда копия</h3>')

if start_idx != -1 and end_stage_h3 != -1:
    html_page = html_page[:start_idx] + organic_topbar + '\n' + organic_card_top + html_page[end_stage_h3 + len('<h3 style="font-size:1.25rem;font-weight:700;margin-bottom:12px;color:var(--ink);">Срез – это всегда копия</h3>'):]

# Remove old subtitle
html_page = html_page.replace('Этап 1 из 3: Теория → Карточки → Код', '')

with open("mockup_organic_dots_above_slice.html", "w", encoding="utf-8") as f:
    f.write(html_page)

with open("design_mockups/mockup_organic_dots_above_slice.html", "w", encoding="utf-8") as f:
    f.write(html_page)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\organic_dots_above_slice.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_organic_dots_above_slice.html"
])

brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
src_full = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\organic_dots_above_slice.png"
shutil.copyfile(src_full, os.path.join(brain_dir, "organic_dots_above_slice.png"))

img = Image.open(src_full)
crop = img.crop((260, 0, 1420, 240))
crop.save(r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\organic_dots_above_slice_crop.png")
crop.save(os.path.join(brain_dir, "organic_dots_above_slice_crop.png"))

print("Captured organic dots above slice successfully!")
