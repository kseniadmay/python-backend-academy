# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\2b320042-cd74-466b-b716-1ee73a7ff7f2"
mockup_dir = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups"
proto_html = os.path.join(mockup_dir, "active_topic_title_placement.html")

full_png = os.path.join(brain_dir, "topic_titles_full_overview.png")

# 1. Full page overview
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1280,2200",
    f"--screenshot={full_png}",
    f"file:///{proto_html.replace(os.sep, '/')}"
], check=True)
print("Saved full overview screenshot")

# 2. Individual crops for variants
# We can create mini HTMLs for crisp individual captures
v_list = [
    {
        "id": "vA",
        "name": "topic_var_A_top_centered",
        "hud": """
  <div style="display:flex;flex-direction:column;align-items:center;gap:12px;margin:22px 0 20px;">
    <div class="dynamic-unit-title">
      <span class="unit-name-part">Базовый синтаксис</span>
      <span class="dot-sep-part">·</span>
      <span class="active-sub-part">list comprehension, dict comprehension и set</span>
    </div>
    <div class="dots-necklace">
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span>
      <span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel active"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel milestone"></span>
    </div>
  </div>
"""
    },
    {
        "id": "vB",
        "name": "topic_var_B_bottom_centered",
        "hud": """
  <div style="display:flex;flex-direction:column;align-items:center;gap:12px;margin:22px 0 20px;">
    <div class="dots-necklace">
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span>
      <span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel active"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel milestone"></span>
    </div>
    <div class="dynamic-unit-title">
      <span class="unit-name-part">Базовый синтаксис</span>
      <span class="dot-sep-part">·</span>
      <span class="active-sub-part">list comprehension, dict comprehension и set</span>
    </div>
  </div>
"""
    },
    {
        "id": "vC",
        "name": "topic_var_C_bottom_left",
        "hud": """
  <div style="display:flex;flex-direction:column;gap:12px;margin:22px 0 20px;">
    <div class="dots-necklace">
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span>
      <span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel active"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel milestone"></span>
    </div>
    <div style="display:flex;align-items:center;justify-content:flex-start;padding-left:4px;">
      <div class="dynamic-unit-title">
        <span class="unit-name-part">Базовый синтаксис</span>
        <span class="dot-sep-part">·</span>
        <span class="active-sub-part">list comprehension, dict comprehension и set</span>
      </div>
    </div>
  </div>
"""
    },
    {
        "id": "vD",
        "name": "topic_var_D_top_left",
        "hud": """
  <div style="display:flex;flex-direction:column;gap:12px;margin:22px 0 20px;">
    <div style="display:flex;align-items:center;justify-content:flex-start;padding-left:4px;">
      <div class="dynamic-unit-title">
        <span class="unit-name-part">Базовый синтаксис</span>
        <span class="dot-sep-part">·</span>
        <span class="active-sub-part">list comprehension, dict comprehension и set</span>
      </div>
    </div>
    <div class="dots-necklace">
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span>
      <span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span><span class="dot-jewel"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel active"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel done"></span><span class="dot-jewel"></span>
      <span class="dots-stage-divider"></span>
      <span class="dot-jewel milestone"></span>
    </div>
  </div>
"""
    }
]

mini_template = """<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Preview</title>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700;800&family=Golos+Text:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --paper: #0e100a;
    --surface-card: #181c12;
    --ink: #eceddf;
    --ink-soft: #9da18f;
    --ink-muted: #6b6f5e;
    --line: rgba(255, 255, 255, 0.08);
    --font-d: 'Unbounded', sans-serif;
    --font-b: 'Golos Text', sans-serif;
    --font-m: 'JetBrains Mono', monospace;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--paper);
    color: var(--ink);
    font-family: var(--font-b);
    padding: 24px 20px;
    display: flex;
    justify-content: center;
    -webkit-font-smoothing: antialiased;
  }
  .stage-wrap {
    width: 100%;
    max-width: 780px;
  }
  .dynamic-unit-title {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.98rem;
    letter-spacing: -0.01em;
  }
  .unit-name-part {
    font-family: var(--font-d);
    font-weight: 700;
    color: var(--ink);
  }
  .dot-sep-part {
    color: var(--ink-muted);
    font-weight: 700;
    opacity: 0.45;
    font-size: 1.1rem;
    line-height: 1;
  }
  .active-sub-part {
    font-family: var(--font-b);
    font-weight: 500;
    color: var(--ink-soft);
  }
  .dots-necklace {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    position: relative;
    padding: 6px 0;
  }
  .dots-stage-divider {
    width: 2px;
    height: 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.18);
    margin: 0 5px;
  }
  .dot-jewel {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.16);
    position: relative;
    cursor: pointer;
  }
  .dot-jewel.done {
    background: #10b981;
    box-shadow: 0 0 8px #10b981, 0 0 16px rgba(16, 185, 129, 0.65), 0 0 26px rgba(16, 185, 129, 0.35);
  }
  .dot-jewel.active {
    width: 9px;
    height: 9px;
    background: #ffffff;
    box-shadow: 0 0 10px #ffffff, 0 0 22px rgba(255, 255, 255, 0.95), 0 0 38px rgba(255, 255, 255, 0.6);
  }
  .dot-jewel.milestone {
    border-radius: 2px;
    transform: rotate(45deg);
    background: rgba(245, 158, 11, 0.3);
    border: 1px solid rgba(245, 158, 11, 0.7);
  }
  .fc-card {
    background: var(--surface-card);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 26px 28px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
  }
  .fc-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }
  .badge-question {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.06);
    color: var(--ink-soft);
  }
  .badge-cheat {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 4px 11px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: var(--ink-soft);
  }
  .fc-question-text {
    font-size: 1.05rem;
    font-weight: 600;
    line-height: 1.5;
    margin-bottom: 24px;
    color: var(--ink);
  }
  .fc-inline-code {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 6px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.25);
    color: #34d399;
    font-family: var(--font-m);
    font-size: 0.92rem;
  }
  .fc-inline-kw {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.08);
    color: #38bdf8;
    font-family: var(--font-m);
    font-size: 0.92rem;
  }
  .fc-meta {
    font-size: 0.78rem;
    color: var(--ink-muted);
    text-align: center;
    margin-bottom: 20px;
  }
  .fc-actions {
    display: flex;
    gap: 12px;
    align-items: center;
  }
  .btn-ghost {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--ink);
    padding: 12px 20px;
    border-radius: 14px;
    font-size: 0.88rem;
    font-weight: 600;
  }
  .btn-primary {
    background: rgba(16, 185, 129, 0.16);
    border: 1px solid rgba(16, 185, 129, 0.45);
    color: #34d399;
    padding: 12px 24px;
    border-radius: 14px;
    font-size: 0.92rem;
    font-weight: 700;
    flex: 1;
    text-align: center;
    box-shadow: 0 0 16px rgba(16, 185, 129, 0.15);
  }
</style>
</head>
<body>
<div class="stage-wrap">
  __HUD__
  <div class="fc-card">
    <div class="fc-card-header">
      <span class="badge-question">Вопрос</span>
      <span class="badge-cheat">💡 Шпаргалка</span>
    </div>
    <div class="fc-question-text">
      Каковы главные преимущества list comprehension перед классическим циклом <span class="fc-inline-kw">for</span> с <span class="fc-inline-code">list.append()</span> ?
    </div>
    <div class="fc-meta">Карточка 1 из 19</div>
    <div class="fc-actions">
      <button class="btn-ghost">← Назад</button>
      <button class="btn-primary">Показать ответ (Пробел)</button>
      <button class="btn-ghost">Дальше →</button>
    </div>
  </div>
</div>
</body>
</html>
"""

for v in v_list:
    tmp_path = os.path.join(mockup_dir, f"tmp_{v['id']}.html")
    full_html = mini_template.replace("__HUD__", v["hud"])
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    png_path = os.path.join(brain_dir, f"{v['name']}.png")
    subprocess.run([
        chrome_path,
        "--headless=new", "--disable-gpu", "--window-size=1080,580",
        f"--screenshot={png_path}",
        f"file:///{tmp_path.replace(os.sep, '/')}"
    ], check=True)
    
    if os.path.exists(png_path):
        img = Image.open(png_path)
        crop = img.crop((40, 0, 1040, 490))
        crop.save(png_path)
        print(f"Captured {v['name']}.png")
    
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

print("All topic placement screenshots done!")
