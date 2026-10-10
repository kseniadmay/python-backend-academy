# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

with open("mockup_skill_1_1_1.html", "r", encoding="utf-8") as f:
    orig = f.read()

# ==========================================================
# 1. МОДЕЛЬ 1: Duolingo / Coddy Flow (Единый урок без ярлыков)
# В шапке: только плавная полоса прогресса (Шаг 1 из 5) и название темы.
# Никаких слов "Конспект", "Карточки", "Практика", никаких блоков или вкладок!
# ==========================================================

m1_css = """
  .duo-topbar {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 16px;
    margin-bottom: 24px;
    border-radius: 18px;
    background: var(--surface);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(20px);
    box-shadow: var(--shadow-1);
  }
  .duo-close {
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
  }
  .duo-progress-box {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .duo-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--ink-soft);
  }
  .duo-track {
    height: 9px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }
  .duo-fill {
    height: 100%;
    width: 25%;
    border-radius: 999px;
    background: linear-gradient(90deg, #10b981, #34d399);
    box-shadow: 0 0 12px rgba(16, 185, 129, 0.5);
    transition: width 0.3s ease;
  }
  .duo-xp {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 12px;
    border-radius: 999px;
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.25);
    color: var(--amber);
    font-size: 0.76rem;
    font-weight: 800;
  }
"""

m1_html = orig

# Hide all tabs completely
m1_html = m1_html.replace('class="tabs-variant-block"', 'class="tabs-variant-block" style="display:none !important;"')

# Replace topbar with clean Duo topbar
old_topbar_regex = r'<div class="sprint-focus-topbar sprint-topbar">.*?</div>\s*</div>'
new_duo_topbar = """
        <div class="duo-topbar">
          <a href="#/python" class="duo-close" title="Выйти">✕</a>
          <div class="duo-progress-box">
            <div class="duo-meta">
              <span style="color:var(--ink);font-weight:800;">🚨 Юнит 1.1 · Срезы и базовые коллекции</span>
              <span style="color:var(--moss);">Шаг 1 из 5</span>
            </div>
            <div class="duo-track">
              <div class="duo-fill" style="width:20%;"></div>
            </div>
          </div>
          <div class="duo-xp">⚡ +10 XP</div>
          <a href="#/docs" class="topbar-help-btn" style="padding:6px 12px;border-radius:10px;"><span class="topbar-help-text">📖 Справка</span></a>
        </div>
"""

# Inject CSS and HTML for Model 1
import re
m1_ready = m1_html.replace('</style>', m1_css + '\n</style>', 1)
# Replace topbar
m1_ready = re.sub(r'<div class="sprint-focus-topbar sprint-topbar">.*?<!-- 2\. БЛОК ВКЛАДОК', new_duo_topbar + '\n        <!-- 2. БЛОК ВКЛАДОК', m1_ready, flags=re.DOTALL)

with open("mockup_model_1_duoflow.html", "w", encoding="utf-8") as f:
    f.write(m1_ready)

subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\model_1_duoflow.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_model_1_duoflow.html"
])


# ==========================================================
# 2. МОДЕЛЬ 2: 2-Колоночный сплит Coddy Desktop (как в референсе SQL/Python)
# Слева: теория и микро-задание.
# Справа: редактор кода, тесты и вывод.
# ==========================================================

m2_css = """
  .coddy-split-container {
    display: grid;
    grid-template-columns: 440px 1fr;
    gap: 18px;
    align-items: start;
  }
  .coddy-left-col {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .coddy-right-col {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .coddy-theory-card {
    background: var(--surface);
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 20px;
    backdrop-filter: blur(20px);
    box-shadow: var(--shadow-1);
  }
  .coddy-challenge-card {
    background: rgba(16, 185, 129, 0.05);
    border: 1px solid rgba(16, 185, 129, 0.20);
    border-radius: 18px;
    padding: 16px 20px;
  }
"""

m2_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Academy · Срезы (Coddy Split)</title>
  <style>
    {orig[orig.find('<style>')+7:orig.find('</style>')]}
    {m1_css}
    {m2_css}
  </style>
</head>
<body class="theme-obsidian">
  <div id="ambient-orb-burgundy"></div>
  <div id="ambient-orb-emerald"></div>
  
  <div class="shell">
    <!-- Сайдбар -->
    {orig[orig.find('<aside class="sidebar"'):orig.find('</aside>')+8]}

    <main>
      <div class="container" style="max-width:1160px;margin:0 auto;padding:16px;">
        
        <!-- Шапка: чистый прогресс урока без табов -->
        <div class="duo-topbar">
          <a href="#/python" class="duo-close" title="Выйти к урокам">✕</a>
          <div class="duo-progress-box">
            <div class="duo-meta">
              <span style="color:var(--ink);font-weight:800;">🚨 Юнит 1.1 · Срезы (list, tuple, slice)</span>
              <span style="color:var(--moss);">Урок 1 из 3 · 33%</span>
            </div>
            <div class="duo-track">
              <div class="duo-fill" style="width:33%;"></div>
            </div>
          </div>
          <div class="duo-xp">⚡ +10 XP</div>
          <a href="#/docs" class="topbar-help-btn" style="padding:6px 12px;border-radius:10px;"><span class="topbar-help-text">📖 Справка</span></a>
        </div>

        <!-- 2-Колоночный сплит -->
        <div class="coddy-split-container">
          
          <!-- Левая колонка: Теория и челлендж -->
          <div class="coddy-left-col">
            <div class="coddy-theory-card">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span class="badge" style="background:rgba(16,185,129,0.12);color:var(--moss);border:1px solid rgba(16,185,129,0.25);font-size:.70rem;font-weight:800;">ТЕОРИЯ</span>
                <span style="font-size:.72rem;color:var(--ink-muted);">2 мин на чтение</span>
              </div>
              <h3 style="margin:0 0 10px;font-size:1.15rem;font-weight:800;color:var(--ink);">Срез — это всегда копия</h3>
              <p style="margin:0 0 12px;font-size:.85rem;line-height:1.55;color:var(--ink-soft);">
                Главное отличие от индекса: <code style="color:var(--moss);background:rgba(16,185,129,0.1);padding:2px 5px;border-radius:5px;">lst[i]</code> возвращает ссылку на сам элемент, а <code style="color:var(--moss);background:rgba(16,185,129,0.1);padding:2px 5px;border-radius:5px;">lst[i:j]</code> — <strong>новый объект</strong> (поверхностную копию).
              </p>
              <div style="background:var(--code-surface);border:1px solid var(--code-border);border-radius:12px;padding:12px;font-family:'JetBrains Mono',monospace;font-size:.80rem;line-height:1.5;color:#e2e8f0;margin-bottom:14px;">
                <span style="color:#f43f5e;">original</span> = [1, 2, 3, 4, 5]<br>
                <span style="color:#f43f5e;">piece</span> = original[<span style="color:#10b981;">1:3</span>]<br>
                piece.append(<span style="color:#a855f7;">99</span>)<br>
                <span style="color:#64748b;"># original остался [1, 2, 3, 4, 5]!</span>
              </div>
            </div>

            <!-- Блок задания (челлендж) -->
            <div class="coddy-challenge-card">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-size:1.1rem;">💡</span>
                <strong style="color:var(--moss);font-size:.88rem;">Челлендж #20</strong>
                <span style="margin-left:auto;font-size:.70rem;color:var(--amber);background:rgba(245,158,11,0.12);padding:2px 8px;border-radius:999px;font-weight:700;">Легко</span>
              </div>
              <p style="margin:0 0 10px;font-size:.83rem;color:var(--ink-soft);line-height:1.5;">
                Разверните список задом наперёд с помощью шага среза <code style="color:var(--amber);">[::-1]</code> и запишите результат в <code style="color:var(--ink);">reversed_list</code>.
              </p>
              <div style="font-size:.78rem;color:var(--ink-muted);background:rgba(0,0,0,0.25);padding:8px 12px;border-radius:9px;border:1px solid rgba(255,255,255,0.06);">
                <strong>Ожидается:</strong> <code style="color:#34d399;">reversed_list == [5, 4, 3, 2, 1]</code>
              </div>
            </div>
          </div>

          <!-- Правая колонка: IDE редактор, кнопки и консоль тестов -->
          <div class="coddy-right-col">
            <div style="background:var(--code-surface);border:1px solid var(--code-border);border-radius:18px;overflow:hidden;box-shadow:var(--shadow-1);">
              <!-- Тулбар редактора -->
              <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 16px;background:rgba(0,0,0,0.25);border-bottom:1px solid var(--line);">
                <span style="font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--ink-muted);">solution.py</span>
                <div style="display:flex;gap:8px;">
                  <button type="button" class="btn btn-ghost" style="padding:4px 10px;font-size:.75rem;border-radius:8px;">Сбросить</button>
                  <button type="button" class="btn btn-ghost" style="padding:4px 10px;font-size:.75rem;border-radius:8px;color:var(--amber);">Подсказка</button>
                </div>
              </div>

              <!-- Поле кода -->
              <div style="padding:16px;font-family:'JetBrains Mono',monospace;font-size:.86rem;line-height:1.6;color:#f8fafc;min-height:220px;background:#090d13;">
                <span style="color:#64748b;"># 1. Создайте список original со значениями 1, 2, 3, 4, 5</span><br>
                original = [1, 2, 3, 4, 5]<br><br>
                <span style="color:#64748b;"># 2. Получите развернутый список через срез [::-1]</span><br>
                reversed_list = original[::-1]<br><br>
                print(reversed_list)
              </div>

              <!-- Нижняя панель действий -->
              <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:rgba(0,0,0,0.35);border-top:1px solid var(--line);">
                <button type="button" class="btn btn-ghost" style="padding:7px 14px;border-radius:10px;font-size:.80rem;">▶ Запустить</button>
                <button type="button" class="btn btn-primary" style="padding:7px 20px;border-radius:10px;font-size:.82rem;background:var(--moss-gradient);box-shadow:var(--shadow-moss);">✓ Проверить решение (+10 XP)</button>
              </div>

              <!-- Консоль тестов под редактором -->
              <div style="padding:12px 16px;background:#05070a;border-top:1px solid rgba(255,255,255,0.06);font-family:'JetBrains Mono',monospace;font-size:.78rem;">
                <div style="color:var(--moss);display:flex;align-items:center;gap:6px;margin-bottom:4px;">
                  <span>✓</span> <span>Тест 1: original создан со значениями [1, 2, 3, 4, 5]</span>
                </div>
                <div style="color:var(--moss);display:flex;align-items:center;gap:6px;">
                  <span>✓</span> <span>Тест 2: reversed_list равен [5, 4, 3, 2, 1]</span>
                </div>
              </div>
            </div>
          </div>

        </div>

      </div>
    </main>
  </div>
</body>
</html>"""

with open("mockup_model_2_split.html", "w", encoding="utf-8") as f:
    f.write(m2_html)

subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\model_2_split.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_model_2_split.html"
])

# Copy to brain dir
for name in ["model_1_duoflow", "model_2_split"]:
    src = f"design_mockups/{name}.png"
    if os.path.exists(src):
        shutil.copyfile(src, os.path.join(brain_dir, f"{name}.png"))

print("Captured Model 1 (Duolingo flow) and Model 2 (Coddy Split) successfully!")
