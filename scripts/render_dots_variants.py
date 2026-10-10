import os
import subprocess
import tempfile
from pathlib import Path

html_code = """<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
<meta charset="UTF-8">
<title>Варианты редизайна нити тем Юнита</title>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;600;700;800&family=Golos+Text:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root {
    --paper: #090d13;
    --surface: #121721;
    --surface-2: #18202d;
    --ink: #f8fafc;
    --ink-soft: #94a3b8;
    --ink-muted: #64748b;
    --line: rgba(255, 255, 255, 0.10);
    --moss: #10b981;
    --moss-soft: rgba(16, 185, 129, 0.14);
    --amber: #f59e0b;
    --font-d: 'Unbounded', sans-serif;
    --font-b: 'Golos Text', sans-serif;
    --font-m: 'JetBrains Mono', monospace;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 28px;
    background: #070a0f; color: var(--ink);
    font-family: var(--font-b);
  }
  .variant-section {
    background: #0f141d;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 22px 26px;
    margin-bottom: 26px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
  }
  .variant-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
  }
  .badge-a { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
  .badge-b { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
  .badge-c { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }

  .variant-title {
    font-size: 1.12rem;
    font-weight: 700;
    margin: 0 0 6px;
    color: #f8fafc;
  }
  .variant-desc {
    font-size: 0.84rem;
    color: var(--ink-soft);
    margin-bottom: 18px;
    line-height: 1.45;
  }
  
  /* ВАРИАНТ А: ВСТРОЕННАЯ ШАПКА КАРТОЧКИ */
  .card-integrated {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 18px;
    overflow: hidden;
  }
  .card-head-integrated {
    background: rgba(255, 255, 255, 0.025);
    border-bottom: 1px solid var(--line);
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
  }
  .card-body-integrated {
    padding: 20px 24px;
  }

  .dots-necklace {
    display: flex;
    align-items: center;
    gap: 9px;
    position: relative;
    padding: 4px 6px;
  }
  .dots-necklace-wire {
    position: absolute;
    left: 11px;
    top: 50%;
    transform: translateY(-50%);
    height: 1.5px;
    background: rgba(255, 255, 255, 0.12);
    z-index: 1;
  }
  .dots-necklace-wire-active {
    position: absolute;
    left: 11px;
    top: 50%;
    transform: translateY(-50%);
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
    border: 1.5px solid rgba(255, 255, 255, 0.20);
    position: relative;
    z-index: 3;
    flex-shrink: 0;
  }
  .dot-jewel.done {
    background: #10b981;
    border-color: #34d399;
    box-shadow: 0 0 7px rgba(16, 185, 129, 0.75);
  }
  .dot-jewel.active {
    width: 14px;
    height: 14px;
    margin: -2px;
    background: #34d399;
    border: 2px solid #ffffff;
    box-shadow: 0 0 10px #10b981, 0 0 20px rgba(52, 211, 153, 0.85);
  }
  .dot-jewel.milestone {
    border-color: rgba(245, 158, 11, 0.75);
    background: rgba(245, 158, 11, 0.15);
  }

  /* ВАРИАНТ Б: ГОРИЗОНТАЛЬНАЯ ЛЕНТА ЧИПОВ */
  .chips-track {
    display: flex;
    align-items: center;
    gap: 8px;
    overflow-x: auto;
    padding: 6px 2px;
  }
  .chip-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 0.80rem;
    font-weight: 600;
    white-space: nowrap;
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.04);
    color: var(--ink-soft);
    cursor: pointer;
  }
  .chip-item.done {
    border-color: rgba(16, 185, 129, 0.35);
    background: rgba(16, 185, 129, 0.10);
    color: #34d399;
  }
  .chip-item.active {
    border-color: #10b981;
    background: rgba(16, 185, 129, 0.22);
    color: #ffffff;
    font-weight: 700;
    box-shadow: 0 0 14px rgba(16, 185, 129, 0.35);
  }
  .chip-item.milestone {
    border-color: rgba(245, 158, 11, 0.45);
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.08);
  }

  /* ВАРИАНТ В: BREADCRUMB + СЕГМЕНТИРОВАННЫЙ ТРЕКЕР */
  .dropdown-breadcrumb-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 12px 18px;
  }
  .dropdown-trigger {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--line);
    padding: 7px 14px;
    border-radius: 10px;
    font-size: 0.84rem;
    font-weight: 700;
    color: var(--ink);
    cursor: pointer;
  }
  .segmented-bar {
    display: flex;
    align-items: center;
    gap: 4px;
    width: 240px;
  }
  .segment {
    flex: 1;
    height: 7px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.14);
  }
  .segment.done {
    background: #10b981;
  }
  .segment.active {
    background: #34d399;
    box-shadow: 0 0 8px #10b981;
  }
  .segment.milestone {
    background: #f59e0b;
  }
</style>
</head>
<body>

  <!-- ВАРИАНТ A -->
  <div class="variant-section">
    <span class="variant-badge badge-a">Вариант А</span>
    <h2 class="variant-title">Встроенная шапка карточки урока (Unified Card Shell)</h2>
    <div class="variant-desc">Точки и заголовок юнита перестают «висеть в воздухе» отдельной полоской. Они встроены прямо в аккуратную шапку урока над теорией. Вся карточка выглядит как единое цельное приложение.</div>
    
    <div class="card-integrated">
      <div class="card-head-integrated">
        <div style="display:flex;align-items:center;gap:10px;">
          <span style="font-weight:700;font-size:0.84rem;color:#f8fafc;">Юнит 1.1: Базовый синтаксис</span>
          <span style="color:var(--line);">•</span>
          <span style="background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.32);color:#34d399;padding:2px 9px;border-radius:999px;font-size:0.72rem;font-weight:700;">Тема 3 из 13</span>
        </div>
        <div class="dots-necklace">
          <div class="dots-necklace-wire" style="width:228px;"></div>
          <div class="dots-necklace-wire-active" style="width:38px;"></div>
          <span class="dot-jewel done"></span>
          <span class="dot-jewel done"></span>
          <span class="dot-jewel active"></span>
          <span class="dot-jewel"></span>
          <span class="dot-jewel"></span>
          <span class="dot-jewel"></span>
          <span class="dot-jewel"></span>
          <span class="dot-jewel"></span>
          <span class="dot-jewel"></span>
          <span class="dot-jewel"></span>
          <span class="dot-jewel"></span>
          <span class="dot-jewel"></span>
          <span class="dot-jewel milestone"></span>
          <span style="font-size:0.75rem;font-family:var(--font-m);font-weight:700;color:var(--moss);margin-left:4px;">3/13</span>
        </div>
      </div>
      <div class="card-body-integrated">
        <h3 style="margin:0 0 10px;font-size:1.30rem;font-weight:700;">Срез – это всегда копия</h3>
        <p style="color:var(--ink-soft);font-size:0.92rem;line-height:1.6;margin:0;">Важное отличие от обращения по одному индексу: lst[i] возвращает сам элемент, а lst[i:j] – новый объект...</p>
      </div>
    </div>
  </div>

  <!-- ВАРИАНТ B -->
  <div class="variant-section">
    <span class="variant-badge badge-b">Вариант Б</span>
    <h2 class="variant-title">Лента чипов с названиями тем (Topic Story Pills)</h2>
    <div class="variant-desc">Вместо абстрактных анонимных точек — удобная горизонтальная лента с реальными названиями тем. Сразу видно, что изучено, что сейчас и что ждёт дальше.</div>
    
    <div style="margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;font-size:0.86rem;color:#f8fafc;">Юнит 1.1: Базовый синтаксис</span>
      <span style="font-size:0.75rem;font-family:var(--font-m);font-weight:700;color:var(--moss);">Прогресс: 3 из 13 тем</span>
    </div>
    <div class="chips-track">
      <div class="chip-item done">✓ 1. Память</div>
      <div class="chip-item done">✓ 2. Индексы</div>
      <div class="chip-item active">🟢 3. Срезы (Сейчас)</div>
      <div class="chip-item">4. frozenset</div>
      <div class="chip-item">5. Dict methods</div>
      <div class="chip-item">6. List methods</div>
      <div class="chip-item milestone">👑 13. Тест 1.1</div>
    </div>
  </div>

  <!-- ВАРИАНТ C -->
  <div class="variant-section">
    <span class="variant-badge badge-c">Вариант В</span>
    <h2 class="variant-title">Оглавление юнита + Сегментированный трекер (Menu & Segments)</h2>
    <div class="variant-desc">Лаконичный бейдж с кнопкой «▾ Оглавление», открывающей полный список 13 тем по клику, и современный сегментированный прогресс-бар в стиле Apple/Linear.</div>
    
    <div class="dropdown-breadcrumb-bar">
      <div style="display:flex;align-items:center;gap:12px;">
        <span style="color:var(--ink-muted);font-size:0.82rem;font-weight:600;">Юнит 1.1</span>
        <button class="dropdown-trigger">
          <span>📖 Тема 3 из 13: Срезы в Python</span>
          <span style="color:#38bdf8;font-size:0.74rem;">▾ Все 13 тем</span>
        </button>
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        <div class="segmented-bar">
          <div class="segment done"></div>
          <div class="segment done"></div>
          <div class="segment active"></div>
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment milestone"></div>
        </div>
        <span style="font-size:0.75rem;font-family:var(--font-m);font-weight:700;color:var(--moss);">3/13</span>
      </div>
    </div>
  </div>

</body>
</html>
"""

os.makedirs('design_mockups', exist_ok=True)
mockup_file = os.path.abspath('design_mockups/dots_track_variants.html')
with open(mockup_file, 'w', encoding='utf-8') as f:
    f.write(html_code)

out_dir = r'C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc'
out_png = os.path.join(out_dir, 'dots_redesign_options.png')

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
uri = Path(mockup_file).as_uri()

with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
    cmd = [
        chrome, '--headless=new', '--no-sandbox', '--disable-gpu',
        '--window-size=1080,1050',
        f'--screenshot={out_png}',
        f'--user-data-dir={td}',
        uri
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print('Chrome return code:', res.returncode)
    print('Options screenshot generated:', os.path.isfile(out_png))
