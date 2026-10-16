# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

# Создаем HTML страницу, сравнивающую варианты, объединяющие ступени найма и педагогическую ясность:
# Вариант 1: Воронка найма (Первичный скрининг -> Технический раунд -> Практический раунд -> Финал и Оффер)
# Вариант 2: Раунды отбора с фокусом (Скрининг: База -> Тех-раунд: Стек -> Лайвкодинг: Сервисы -> Финал: Архитектура)
# Вариант 3: Прагматичные этапы кандидата (1. Скрининг HR/Лид -> 2. Глубокое тех-интервью -> 3. Боевой лайвкодинг -> 4. Защита оффера)

html_content = """<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
<meta charset="utf-8">
<title>Hiring Stages Pedagogical Synthesis</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0d1016;
  --surface: rgba(18, 24, 38, 0.74);
  --line: rgba(255, 255, 255, 0.09);
  --ink: #f8fafc;
  --ink-muted: #94a3b8;
  --ink-soft: #cbd5e1;
  --emerald: #10b981;
  --moss: #34d399;
  --amber: #fbbf24;
  --bordeaux: #f43f5e;
  --purple: #a855f7;
  --font-s: 'Plus Jakarta Sans', system-ui, sans-serif;
  --font-m: 'JetBrains Mono', monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-s);
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  align-items: center;
}
.wrap { width: 100%; max-width: 920px; }
h2 { font-size: 1.15rem; font-weight: 800; margin-bottom: 6px; color: var(--ink); display: flex; align-items: center; gap: 8px; }
.sub { font-size: 0.82rem; color: var(--ink-muted); margin-bottom: 16px; font-weight: 500; }

.section-box {
  background: rgba(18, 24, 38, 0.45);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 24px;
}

.echelon-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: rgba(18, 24, 38, 0.74);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 10px 18px;
  backdrop-filter: blur(20px);
  margin-bottom: 10px;
}
.e-wrap { flex: 1; display: flex; flex-direction: column; gap: 4px; min-width: 0; }
.e-meta { display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; }
.e-track { height: 5px; border-radius: 999px; background: rgba(255,255,255,0.06); overflow: hidden; }
.e-fill { height: 100%; border-radius: 999px; }

.pill-xp {
  display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: 999px;
  background: rgba(16,185,129,0.14); border: 1px solid rgba(52,211,153,0.35);
  color: #34d399; font-size: 0.73rem; font-weight: 700; white-space: nowrap;
}
.btn-help {
  padding: 5px 12px; border-radius: 8px; border: 1px solid var(--line); background: rgba(255,255,255,0.04);
  color: var(--ink-soft); font-size: 0.75rem; font-weight: 600; text-decoration: none;
}
</style>
</head>
<body>

<div class="wrap">
  <!-- ВАРИАНТ 1 -->
  <div class="section-box">
    <h2>Вариант 1: Каноническая воронка отбора (Понятные раунды найма)</h2>
    <div class="sub">Чётко отражает путь соискателя: от первого сита до финального получения оффера.</div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">🚨 Эшелон 1: Первичный скрининг</span>
          <span style="color:#34d399;font-family:var(--font-m);font-weight:800;">🎯 35% готовности к скринингу</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:35%;background:linear-gradient(90deg,#f43f5e,#34d399);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">🎯 Эшелон 2: Технический раунд</span>
          <span style="color:#fbbf24;font-family:var(--font-m);font-weight:800;">🎯 52% готовности к тех-раунду</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:52%;background:linear-gradient(90deg,#f59e0b,#10b981);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">⚡ Эшелон 3: Практический раунд</span>
          <span style="color:#34d399;font-family:var(--font-m);font-weight:800;">🎯 20% готовности к лайвкодингу</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:20%;background:linear-gradient(90deg,#10b981,#06b6d4);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">👑 Эшелон 4: Финал и Оффер</span>
          <span style="color:#c084fc;font-family:var(--font-m);font-weight:800;">🎯 10% готовности к офферу</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:10%;background:linear-gradient(90deg,#a855f7,#ec4899);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>
  </div>

  <!-- ВАРИАНТ 2 -->
  <div class="section-box">
    <h2>Вариант 2: Этап найма + Педагогический фокус (Двойная ясность)</h2>
    <div class="sub">Связывает конкретный раунд собеседования с тем, какие именно знания там тестируют.</div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">🚨 Эшелон 1: Скрининг · База языка</span>
          <span style="color:#34d399;font-family:var(--font-m);font-weight:800;">🎯 35% готовности</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:35%;background:linear-gradient(90deg,#f43f5e,#34d399);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">🎯 Эшелон 2: Тех-раунд · Стек и БД</span>
          <span style="color:#fbbf24;font-family:var(--font-m);font-weight:800;">🎯 52% готовности</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:52%;background:linear-gradient(90deg,#f59e0b,#10b981);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">⚡ Эшелон 3: Лайвкодинг · Сервисы</span>
          <span style="color:#34d399;font-family:var(--font-m);font-weight:800;">🎯 20% готовности</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:20%;background:linear-gradient(90deg,#10b981,#06b6d4);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">👑 Эшелон 4: Финал · Архитектура</span>
          <span style="color:#c084fc;font-family:var(--font-m);font-weight:800;">🎯 10% готовности</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:10%;background:linear-gradient(90deg,#a855f7,#ec4899);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>
  </div>

  <!-- ВАРИАНТ 3 -->
  <div class="section-box">
    <h2>Вариант 3: Прагматичные барьеры отбора (От сита до контракта)</h2>
    <div class="sub">Короткие реалистичные названия этапов в IT-компаниях:</div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">🚨 Эшелон 1: Тех-скрининг</span>
          <span style="color:#34d399;font-family:var(--font-m);font-weight:800;">🎯 35% готовности</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:35%;background:linear-gradient(90deg,#f43f5e,#34d399);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">🎯 Эшелон 2: Собеседование по стеку</span>
          <span style="color:#fbbf24;font-family:var(--font-m);font-weight:800;">🎯 52% готовности</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:52%;background:linear-gradient(90deg,#f59e0b,#10b981);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">⚡ Эшелон 3: Боевой лайвкодинг</span>
          <span style="color:#34d399;font-family:var(--font-m);font-weight:800;">🎯 20% готовности</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:20%;background:linear-gradient(90deg,#10b981,#06b6d4);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>

    <div class="echelon-row">
      <div class="e-wrap">
        <div class="e-meta">
          <span style="font-weight:800;color:var(--ink);">👑 Эшелон 4: Защита оффера</span>
          <span style="color:#c084fc;font-family:var(--font-m);font-weight:800;">🎯 10% готовности</span>
        </div>
        <div class="e-track"><div class="e-fill" style="width:10%;background:linear-gradient(90deg,#a855f7,#ec4899);"></div></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <div class="pill-xp">⚡ 120 XP сегодня</div>
        <a href="#" class="btn-help">📖 Справка</a>
      </div>
    </div>
  </div>
</div>

</body>
</html>
"""

html_path = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\hiring_stages_options.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
full_png = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\hiring_stages_options.png"

subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1200,1260",
    f"--screenshot={full_png}",
    f"file:///{html_path.replace(os.sep, '/')}"
])

brain_png = os.path.join(brain_dir, "hiring_stages_options.png")
shutil.copyfile(full_png, brain_png)

print("Hiring stages preview rendered successfully!")
