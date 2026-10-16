# -*- coding: utf-8 -*-
import subprocess
import shutil
import os

with open("mockup_skill_1_1_1.html", "r", encoding="utf-8") as f:
    orig = f.read()

# Новые стили для шапки: шкала эшелона + светящиеся изумрудные точки юнита
header_css = """
  /* ================= ЕДИНАЯ ШАПКА: ЭШЕЛОН + ИЗУМРУДНЫЕ ТОЧКИ ЮНИТА ================= */
  .sprint-header-unified {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 18px;
    margin-bottom: 24px;
    border-radius: 20px;
    background: var(--surface);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow: var(--shadow-1);
  }

  .sprint-header-close {
    width: 36px;
    height: 36px;
    border-radius: 11px;
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
  .sprint-header-close:hover {
    color: var(--ink);
    border-color: var(--moss);
    background: rgba(16, 185, 129, 0.12);
  }

  .sprint-header-trackers {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 7px;
  }

  /* 1. Шкала эшелона (сверху) */
  .echelon-track-row {
    display: flex;
    flex-direction: column;
    gap: 3px;
  }
  .echelon-track-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--ink-soft);
  }
  .echelon-track-title {
    display: flex;
    align-items: center;
    gap: 6px;
    color: var(--ink);
    font-weight: 800;
  }
  .echelon-track-val {
    color: var(--amber);
    font-family: var(--font-m);
    font-weight: 700;
  }
  .echelon-progress-bar {
    height: 5px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.04);
  }
  .echelon-progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #be123c, #f59e0b, #10b981);
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.35);
    transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }

  /* 2. Трекер юнита со светящимися изумрудными точками (снизу) */
  .unit-track-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }
  .unit-track-title {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--ink-soft);
    display: flex;
    align-items: center;
    gap: 6px;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .unit-track-title strong {
    color: var(--ink);
  }

  .unit-dots-wrap {
    display: flex;
    align-items: center;
    gap: 7px;
    flex: none;
  }
  .unit-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: all 0.25s ease;
    position: relative;
    cursor: pointer;
  }
  .unit-dot:hover {
    transform: scale(1.2);
  }
  .unit-dot.done {
    background: #10b981;
    border-color: #34d399;
    box-shadow: 0 0 6px rgba(16, 185, 129, 0.6);
  }
  .unit-dot.active {
    width: 11px;
    height: 11px;
    background: #34d399;
    border: 2px solid #ffffff;
    box-shadow: 0 0 10px #10b981, 0 0 18px rgba(16, 185, 129, 0.75);
    animation: emerald-glow-pulse 2s infinite ease-in-out;
  }
  @keyframes emerald-glow-pulse {
    0%, 100% {
      transform: scale(1);
      box-shadow: 0 0 10px #10b981, 0 0 18px rgba(16, 185, 129, 0.65);
    }
    50% {
      transform: scale(1.18);
      box-shadow: 0 0 14px #34d399, 0 0 24px rgba(52, 211, 153, 0.85);
    }
  }

  .unit-dot-label {
    font-size: 0.70rem;
    font-weight: 700;
    color: var(--moss);
    font-family: var(--font-m);
    margin-left: 2px;
  }
"""

header_html = """
        <!-- ЕДИНАЯ ШАПКА: ШКАЛА ЭШЕЛОНА + СВЕТЯЩИЕСЯ ИЗУМРУДНЫЕ ТОЧКИ ЮНИТА -->
        <div class="sprint-header-unified">
          <a href="#/python" class="sprint-header-close" title="Выйти к эшелону">✕</a>

          <div class="sprint-header-trackers">
            
            <!-- 1. Шкала эшелона (сверху) -->
            <div class="echelon-track-row">
              <div class="echelon-track-meta">
                <span class="echelon-track-title">🚨 Эшелон 1 · Скрининг и база</span>
                <span class="echelon-track-val">42% (5/12 юнитов)</span>
              </div>
              <div class="echelon-progress-bar">
                <div class="echelon-progress-fill" style="width: 42%;"></div>
              </div>
            </div>

            <!-- 2. Трекер юнита со светящимися изумрудными точками (снизу) -->
            <div class="unit-track-row">
              <div class="unit-track-title">
                <span>Юнит 1.1:</span>
                <strong>Базовые коллекции и срезы</strong>
                <span style="color:var(--ink-muted);font-weight:500;">· Навык 1.1.1</span>
              </div>

              <!-- Светящиеся изумрудные точки -->
              <div class="unit-dots-wrap" title="Прогресс юнита 1.1">
                <span class="unit-dot done" title="1.1.1 Введение (Завершено)"></span>
                <span class="unit-dot done" title="1.1.2 Индексация (Завершено)"></span>
                <span class="unit-dot active" title="1.1.3 Срезы (Текущий шаг)"></span>
                <span class="unit-dot" title="1.1.4 Slice assignment (Впереди)"></span>
                <span class="unit-dot" title="1.1.5 Рубежный тест (Финал)"></span>
                <span class="unit-dot-label">3/5</span>
              </div>
            </div>

          </div>

          <div style="display:flex;gap:8px;align-items:center;">
            <div class="sprint-xp-pill">⚡ +10 XP</div>
            <a href="#/docs" class="topbar-help-btn" style="padding:6px 12px;border-radius:11px;"><span class="topbar-help-text">📖 Справка</span></a>
          </div>
        </div>
"""

# Assemble page
html_out = orig

# Inject CSS
html_out = html_out.replace("</style>", header_css + "\n</style>", 1)

# Completely remove all tab blocks
html_out = html_out.replace('class="tabs-variant-block"', 'class="tabs-variant-block" style="display:none !important;"')

# Replace topbar
start_tag = '<!-- 1. ВЕРХНИЙ СПРИНТ-ТОПБАР -->'
start_idx = html_out.find(start_tag)
end_tag = '<!-- 2. БЛОК ВКЛАДОК'
end_idx = html_out.find(end_tag)

if start_idx != -1 and end_idx != -1:
    html_out = html_out[:start_idx] + header_html + '\n        ' + html_out[end_idx:]

# Remove any old subtitle inside stage-theory
html_out = html_out.replace('Этап 1 из 3: Теория → Карточки → Код', '')

with open("mockup_unified_echelon_dots.html", "w", encoding="utf-8") as f:
    f.write(html_out)

with open("design_mockups/mockup_unified_echelon_dots.html", "w", encoding="utf-8") as f:
    f.write(html_out)

# Take screenshots: full screen & close-up crop of the header
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\echelon_dots_header.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_unified_echelon_dots.html"
])

from PIL import Image

brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
src_full = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\echelon_dots_header.png"
shutil.copyfile(src_full, os.path.join(brain_dir, "echelon_dots_header.png"))

# Crop header area (x: 260 to 1420, y: 0 to 190)
img = Image.open(src_full)
crop = img.crop((260, 0, 1420, 190))
crop.save(r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\echelon_dots_header_crop.png")
crop.save(os.path.join(brain_dir, "echelon_dots_header_crop.png"))

print("Unified echelon dots mockup and screenshots generated successfully!")
