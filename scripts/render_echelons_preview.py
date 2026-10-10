# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

# Создаем HTML страницу, демонстрирующую как все 4 эшелона смотрятся:
# 1) В верхнем топбаре темы (для каждого эшелона)
# 2) В дорожной карте (Roadmap 4 карточки)

html_content = """<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
<meta charset="utf-8">
<title>Echelons Naming Preview</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0d1016;
  --surface: rgba(18, 24, 38, 0.74);
  --surface-2: rgba(26, 34, 52, 0.85);
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
  gap: 30px;
  align-items: center;
}
.wrap { width: 100%; max-width: 900px; }
h2 { font-size: 1.15rem; font-weight: 800; margin-bottom: 14px; color: var(--ink); display: flex; align-items: center; gap: 8px; }
.sub { font-size: 0.82rem; color: var(--ink-muted); margin-bottom: 20px; font-weight: 500; }

.echelon-topbar-clean {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: rgba(18, 24, 38, 0.74);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 12px 20px;
  backdrop-filter: blur(20px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.28);
  margin-bottom: 12px;
}
.echelon-clean-wrap { flex: 1; display: flex; flex-direction: column; gap: 5px; min-width: 0; }
.echelon-clean-meta { display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; }
.echelon-clean-track { height: 6px; border-radius: 999px; background: rgba(255,255,255,0.06); overflow: hidden; }
.echelon-clean-fill { height: 100%; border-radius: 999px; transition: width .35s; }

.pill-xp {
  display: inline-flex; align-items: center; gap: 4px; padding: 5px 11px; border-radius: 999px;
  background: rgba(16,185,129,0.14); border: 1px solid rgba(52,211,153,0.35);
  color: #34d399; font-size: 0.75rem; font-weight: 700; white-space: nowrap;
}
.btn-help {
  padding: 6px 14px; border-radius: 10px; border: 1px solid var(--line); background: rgba(255,255,255,0.04);
  color: var(--ink-soft); font-size: 0.78rem; font-weight: 600; text-decoration: none; display: flex; align-items: center; gap: 4px;
}

/* Roadmap 4 cards grid */
.grid-4 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.card {
  background: var(--surface); border: 1px solid var(--line); border-radius: 16px; padding: 14px 16px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 10px;
}
.card-head { display: flex; justify-content: space-between; align-items: center; }
.badge {
  font-size: 0.75rem; font-weight: 800; padding: 4px 10px; border-radius: 999px; display: inline-flex; align-items: center; gap: 5px;
}
.chip { font-family: var(--font-m); font-size: 0.78rem; font-weight: 800; color: var(--moss); background: rgba(16,185,129,0.12); padding: 2px 8px; border-radius: 8px; }
.desc { font-size: 0.76rem; color: var(--ink-muted); line-height: 1.4; }
.track { height: 6px; border-radius: 999px; background: rgba(255,255,255,0.06); overflow: hidden; margin: 4px 0; }
.foot { display: flex; justify-content: space-between; font-size: 0.74rem; color: var(--ink-muted); }

.b1 { background: rgba(244,63,94,0.15); border: 1px solid rgba(244,63,94,0.35); color: #fb7185; }
.b2 { background: rgba(251,191,36,0.15); border: 1px solid rgba(251,191,36,0.35); color: #fbbf24; }
.b3 { background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.35); color: #34d399; }
.b4 { background: rgba(168,85,247,0.15); border: 1px solid rgba(168,85,247,0.35); color: #c084fc; }

</style>
</head>
<body>

<div class="wrap">
  <h2>🎯 Основной стандарт: Названия по этапам собеседования</h2>
  <div class="sub">В шапке урока студент сразу видит, к какому рубежу отбора приближается текущая тема:</div>

  <!-- Эшелон 1 -->
  <div class="echelon-topbar-clean">
    <div class="echelon-clean-wrap">
      <div class="echelon-clean-meta">
        <span style="font-weight:800;color:var(--ink);">🚨 Эшелон 1: Скрининг</span>
        <span style="color:#34d399;font-family:var(--font-m);font-weight:800;">🎯 35% готовности к скринингу</span>
      </div>
      <div class="echelon-clean-track">
        <div class="echelon-clean-fill" style="width: 35%; background: linear-gradient(90deg, #f43f5e, #34d399);"></div>
      </div>
    </div>
    <div style="display:flex;gap:10px;align-items:center;">
      <div class="pill-xp">⚡ 120 XP сегодня</div>
      <a href="#" class="btn-help">📖 Справка</a>
    </div>
  </div>

  <!-- Эшелон 2 -->
  <div class="echelon-topbar-clean">
    <div class="echelon-clean-wrap">
      <div class="echelon-clean-meta">
        <span style="font-weight:800;color:var(--ink);">🎯 Эшелон 2: Тех-интервью</span>
        <span style="color:#fbbf24;font-family:var(--font-m);font-weight:800;">🎯 52% готовности к тех-интервью</span>
      </div>
      <div class="echelon-clean-track">
        <div class="echelon-clean-fill" style="width: 52%; background: linear-gradient(90deg, #f59e0b, #10b981);"></div>
      </div>
    </div>
    <div style="display:flex;gap:10px;align-items:center;">
      <div class="pill-xp">⚡ 120 XP сегодня</div>
      <a href="#" class="btn-help">📖 Справка</a>
    </div>
  </div>

  <!-- Эшелон 3 -->
  <div class="echelon-topbar-clean">
    <div class="echelon-clean-wrap">
      <div class="echelon-clean-meta">
        <span style="font-weight:800;color:var(--ink);">⚡ Эшелон 3: Продакшен</span>
        <span style="color:#34d399;font-family:var(--font-m);font-weight:800;">🎯 20% готовности к продакшену</span>
      </div>
      <div class="echelon-clean-track">
        <div class="echelon-clean-fill" style="width: 20%; background: linear-gradient(90deg, #10b981, #06b6d4);"></div>
      </div>
    </div>
    <div style="display:flex;gap:10px;align-items:center;">
      <div class="pill-xp">⚡ 120 XP сегодня</div>
      <a href="#" class="btn-help">📖 Справка</a>
    </div>
  </div>

  <!-- Эшелон 4 -->
  <div class="echelon-topbar-clean">
    <div class="echelon-clean-wrap">
      <div class="echelon-clean-meta">
        <span style="font-weight:800;color:var(--ink);">👑 Эшелон 4: Архитектура</span>
        <span style="color:#c084fc;font-family:var(--font-m);font-weight:800;">🎯 10% готовности к офферу</span>
      </div>
      <div class="echelon-clean-track">
        <div class="echelon-clean-fill" style="width: 10%; background: linear-gradient(90deg, #a855f7, #ec4899);"></div>
      </div>
    </div>
    <div style="display:flex;gap:10px;align-items:center;">
      <div class="pill-xp">⚡ 120 XP сегодня</div>
      <a href="#" class="btn-help">📖 Справка</a>
    </div>
  </div>

  <h2 style="margin-top:28px;">🗺️ Как это выглядит в обзорной сетке (Roadmap)</h2>
  <div class="grid-4">
    <!-- Card 1 -->
    <div class="card">
      <div>
        <div class="card-head">
          <span class="badge b1">🚨 Эшелон 1: Скрининг</span>
          <span class="chip">35%</span>
        </div>
        <div class="desc" style="margin-top:8px;">Первичный отсев на HR и тех-скрининге (Python Core, сложность O(n), два указателя, SQL JOIN, HTTP/REST, Git).</div>
      </div>
      <div>
        <div class="track"><div style="width:35%;height:100%;background:#f43f5e;"></div></div>
        <div class="foot"><span>42 / 120 MP</span><span style="color:#34d399;font-weight:700;">Изучать →</span></div>
      </div>
    </div>

    <!-- Card 2 -->
    <div class="card">
      <div>
        <div class="card-head">
          <span class="badge b2">🎯 Эшелон 2: Тех-интервью</span>
          <span class="chip" style="color:#fbbf24;background:rgba(251,191,36,0.12);">52%</span>
        </div>
        <div class="desc" style="margin-top:8px;">Основная техническая секция по стеку (ООП, Asyncio/GIL, FastAPI/Django, транзакции и индексы БД, Docker).</div>
      </div>
      <div>
        <div class="track"><div style="width:52%;height:100%;background:#fbbf24;"></div></div>
        <div class="foot"><span>88 / 170 MP</span><span style="color:#34d399;font-weight:700;">Изучать →</span></div>
      </div>
    </div>

    <!-- Card 3 -->
    <div class="card">
      <div>
        <div class="card-head">
          <span class="badge b3">⚡ Эшелон 3: Продакшен</span>
          <span class="chip">20%</span>
        </div>
        <div class="desc" style="margin-top:8px;">Инженерия уровня Strong Junior (Redis, очереди Celery/Kafka, CI/CD, Nginx, микросервисы, Observability).</div>
      </div>
      <div>
        <div class="track"><div style="width:20%;height:100%;background:#34d399;"></div></div>
        <div class="foot"><span>24 / 120 MP</span><span style="color:#34d399;font-weight:700;">Изучать →</span></div>
      </div>
    </div>

    <!-- Card 4 -->
    <div class="card">
      <div>
        <div class="card-head">
          <span class="badge b4">👑 Эшелон 4: Архитектура</span>
          <span class="chip" style="color:#c084fc;background:rgba(168,85,247,0.12);">10%</span>
        </div>
        <div class="desc" style="margin-top:8px;">Конкурентное преимущество на оффер (Highload, System Design, паттерны проектирования, второй фреймворк).</div>
      </div>
      <div>
        <div class="track"><div style="width:10%;height:100%;background:#a855f7;"></div></div>
        <div class="foot"><span>12 / 120 MP</span><span style="color:#34d399;font-weight:700;">Изучать →</span></div>
      </div>
    </div>
  </div>
</div>

</body>
</html>
"""

html_path = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\echelons_preview.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
full_png = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\echelons_preview.png"

subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1200,980",
    f"--screenshot={full_png}",
    f"file:///{html_path.replace(os.sep, '/')}"
])

brain_png = os.path.join(brain_dir, "echelons_preview.png")
shutil.copyfile(full_png, brain_png)

print("Echelons preview rendered successfully!")
