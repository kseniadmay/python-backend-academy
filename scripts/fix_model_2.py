# -*- coding: utf-8 -*-
import subprocess
import shutil
import os

with open("mockup_skill_1_1_1.html", "r", encoding="utf-8") as f:
    orig = f.read()

split_css = """
  .coddy-split-container {
    display: grid;
    grid-template-columns: 460px 1fr;
    gap: 18px;
    align-items: start;
    margin-top: 14px;
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

split_html_body = """
        <!-- ВЕРХНИЙ ЧИСТЫЙ БАР БЕЗ ТАБОВ И БЕЗ ЯРЛЫКОВ -->
        <div class="sprint-focus-topbar sprint-topbar">
          <a href="#/python" class="sprint-close-btn" title="Выйти к юниту">✕</a>
          <div class="sprint-progress-wrap">
            <div class="sprint-progress-meta">
              <span style="font-weight:800;color:var(--ink);">🚨 Юнит 1.1 · Срезы и базовые коллекции</span>
              <span style="color:var(--moss);">Урок 1 из 3 · 33%</span>
            </div>
            <div class="sprint-progress-track">
              <div class="sprint-progress-fill" style="width:33%;"></div>
            </div>
          </div>
          <div style="display:flex;gap:8px;align-items:center;">
            <div class="sprint-xp-pill">⚡ +10 XP</div>
            <a href="#/docs" class="topbar-help-btn" style="padding:5px 10px;font-size:.76rem;border-radius:10px;"><span class="topbar-help-text">📖 Справка</span></a>
          </div>
        </div>

        <!-- 2-КОЛОНОЧНЫЙ СПЛИТ CODDY DESKTOP (ТЕОРИЯ СЛЕВА + IDE СПРАВА) -->
        <div class="coddy-split-container">
          
          <!-- Левая колонка: Теория и челлендж -->
          <div class="coddy-left-col">
            <div class="coddy-theory-card">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span class="badge" style="background:rgba(16,185,129,0.12);color:var(--moss);border:1px solid rgba(16,185,129,0.25);font-size:.70rem;font-weight:800;padding:2px 8px;border-radius:999px;">ТЕОРИЯ</span>
                <span style="font-size:.72rem;color:var(--ink-muted);">2 мин на чтение</span>
              </div>
              <h3 style="margin:0 0 10px;font-size:1.15rem;font-weight:800;color:var(--ink);">Срез — это всегда копия</h3>
              <p style="margin:0 0 12px;font-size:.85rem;line-height:1.55;color:var(--ink-soft);">
                Главное отличие от обращения по одному индексу: <code style="color:var(--moss);background:rgba(16,185,129,0.1);padding:2px 5px;border-radius:5px;">lst[i]</code> возвращает сам элемент, а <code style="color:var(--moss);background:rgba(16,185,129,0.1);padding:2px 5px;border-radius:5px;">lst[i:j]</code> — <strong>новый объект</strong> (поверхностную копию).
              </p>
              <div style="background:#090d13;border:1px solid var(--line);border-radius:12px;padding:12px;font-family:'JetBrains Mono',monospace;font-size:.80rem;line-height:1.55;color:#e2e8f0;margin-bottom:14px;">
                <span style="color:#ff7b72;">original</span> = [1, 2, 3, 4, 5]<br>
                <span style="color:#ff7b72;">piece</span> = original[<span style="color:#7ee787;font-weight:700;">1:3</span>]<br>
                piece.append(<span style="color:#79c0ff;">99</span>)<br>
                <span style="color:#8b949e;"># original остался [1, 2, 3, 4, 5]</span>
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
            <div style="background:#090d13;border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:var(--shadow-1);">
              <!-- Тулбар редактора -->
              <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 16px;background:rgba(255,255,255,0.03);border-bottom:1px solid var(--line);">
                <span style="font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--ink-muted);">solution.py</span>
                <div style="display:flex;gap:8px;">
                  <button type="button" class="btn btn-ghost" style="padding:4px 10px;font-size:.75rem;border-radius:8px;">Сбросить</button>
                  <button type="button" class="btn btn-ghost" style="padding:4px 10px;font-size:.75rem;border-radius:8px;color:var(--amber);">Подсказка</button>
                </div>
              </div>

              <!-- Поле кода -->
              <div style="padding:16px;font-family:'JetBrains Mono',monospace;font-size:.86rem;line-height:1.6;color:#f8fafc;min-height:220px;background:#090d13;">
                <span style="color:#8b949e;"># 1. Создайте список original со значениями 1, 2, 3, 4, 5</span><br>
                original = [1, 2, 3, 4, 5]<br><br>
                <span style="color:#8b949e;"># 2. Получите развернутый список через срез [::-1]</span><br>
                reversed_list = original[::-1]<br><br>
                print(reversed_list)
              </div>

              <!-- Нижняя панель действий -->
              <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:rgba(255,255,255,0.02);border-top:1px solid var(--line);">
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
"""

m2_full = orig
m2_full = m2_full.replace("</style>", split_css + "\n</style>", 1)
m2_full = m2_full.replace('style="max-width:880px;"', 'style="max-width:1160px;margin:0 auto;"')

start_tag = '<!-- 1. ВЕРХНИЙ СПРИНТ-ТОПБАР -->'
start_idx = m2_full.find(start_tag)
end_tag = '<!-- КОНЕЦ СТАДИЙ -->'
end_idx = m2_full.find(end_tag)
if end_idx == -1:
    end_idx = m2_full.find('</div>\n    </main>')

m2_full = m2_full[:start_idx] + split_html_body + '\n      ' + m2_full[end_idx:]

with open("mockup_model_2_split.html", "w", encoding="utf-8") as f:
    f.write(m2_full)

subprocess.run([
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\model_2_split.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_model_2_split.html"
])

brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
shutil.copyfile("design_mockups/model_2_split.png", os.path.join(brain_dir, "model_2_split.png"))
print("Done re-rendering Model 2 split!")
