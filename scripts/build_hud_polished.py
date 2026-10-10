# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

with open("mockup_skill_1_1_1.html", "r", encoding="utf-8") as f:
    orig = f.read()

# Продвинутые стили для ультра-чистого и глубокого HUD-интерфейса
hud_css = """
  /* ================= 1. ЕДИНЫЙ ЦЕЛЬНЫЙ ПУЛЬТ УПРАВЛЕНИЯ (HUD) ================= */
  .sprint-hud-master {
    background: var(--surface);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 14px 20px 12px;
    margin-bottom: 22px;
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45);
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  /* Верхний ярус: Эшелон, шкала готовности, XP, Справка */
  .hud-top-tier {
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .hud-close-btn {
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
  .hud-close-btn:hover {
    color: var(--ink);
    border-color: var(--moss);
    background: rgba(16, 185, 129, 0.12);
  }

  .hud-echelon-bar-wrap {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  .hud-echelon-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--ink-soft);
  }
  .hud-echelon-title {
    display: flex;
    align-items: center;
    gap: 6px;
    color: var(--ink);
    font-weight: 800;
  }
  .hud-target-readiness {
    color: #34d399;
    font-family: var(--font-m);
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .hud-laser-track {
    height: 6px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.04);
  }
  .hud-laser-fill {
    height: 100%;
    width: 35%;
    border-radius: 999px;
    background: linear-gradient(90deg, #be123c 0%, #f59e0b 50%, #10b981 100%);
    box-shadow: 0 0 12px rgba(16, 185, 129, 0.5);
    position: relative;
    transition: width 0.4s ease;
  }
  /* Бегущий световой блик по шкале */
  .hud-laser-fill::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.6) 50%, transparent 100%);
    animation: laser-shimmer 2.5s infinite linear;
  }
  @keyframes laser-shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(200%); }
  }

  /* Разделитель между ярусами */
  .hud-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.08) 20%, rgba(255, 255, 255, 0.08) 80%, transparent);
  }

  /* Нижний ярус: Тема юнита + Нить из 13 изумрудных жемчужин на рельсе */
  .hud-bottom-tier {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 2px 4px 4px;
  }
  .hud-unit-info {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.78rem;
    color: var(--ink-soft);
    min-width: 0;
  }
  .hud-unit-info strong {
    color: var(--ink);
  }
  .hud-topic-badge {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.25);
    color: var(--moss);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.70rem;
    font-weight: 700;
  }

  /* Рельс световода с 13 точками */
  .hud-rail-container {
    display: flex;
    align-items: center;
    position: relative;
    padding: 4px 0;
    flex: none;
  }
  .hud-rail-line {
    position: absolute;
    left: 6px;
    right: 14px;
    height: 2px;
    background: rgba(255, 255, 255, 0.10);
    z-index: 1;
  }
  .hud-rail-line-active {
    position: absolute;
    left: 6px;
    width: 48px;
    height: 2px;
    background: linear-gradient(90deg, #10b981, #34d399);
    box-shadow: 0 0 6px rgba(16, 185, 129, 0.8);
    z-index: 2;
  }
  .hud-dots-beads {
    display: flex;
    align-items: center;
    gap: 10px;
    position: relative;
    z-index: 3;
  }

  /* Каждая точка как светящаяся жемчужина */
  .hud-bead {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(20, 27, 36, 0.95);
    border: 1.5px solid rgba(255, 255, 255, 0.16);
    transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
    position: relative;
  }
  .hud-bead:hover {
    transform: scale(1.35);
  }
  .hud-bead.done {
    background: #10b981;
    border-color: #34d399;
    box-shadow: 0 0 8px rgba(16, 185, 129, 0.7);
  }
  .hud-bead.active {
    width: 14px;
    height: 14px;
    background: #34d399;
    border: 2px solid #ffffff;
    box-shadow: 0 0 12px #10b981, 0 0 24px rgba(52, 211, 153, 0.85);
    animation: bead-pulse 2.2s infinite ease-in-out;
  }
  .hud-bead.milestone {
    border-color: rgba(245, 158, 11, 0.6);
    background: rgba(245, 158, 11, 0.15);
  }
  .hud-bead.milestone:hover {
    background: #f59e0b;
  }
  @keyframes bead-pulse {
    0%, 100% {
      transform: scale(1);
      box-shadow: 0 0 10px #10b981, 0 0 20px rgba(16, 185, 129, 0.65);
    }
    50% {
      transform: scale(1.2);
      box-shadow: 0 0 16px #34d399, 0 0 28px rgba(52, 211, 153, 0.9);
    }
  }

  .hud-counter-pill {
    margin-left: 6px;
    font-size: 0.74rem;
    font-family: var(--font-m);
    font-weight: 800;
    color: var(--moss);
    background: rgba(16, 185, 129, 0.1);
    padding: 2px 7px;
    border-radius: 999px;
    border: 1px solid rgba(16, 185, 129, 0.2);
  }

  /* ================= 2. СХЕМА ПАМЯТИ ВНУТРИ КАРТОЧКИ ================= */
  .memory-schema-box {
    margin: 16px 0;
    padding: 14px 18px;
    border-radius: 14px;
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.08);
  }
  .memory-schema-title {
    font-size: 0.74rem;
    font-weight: 800;
    color: var(--ink-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .memory-diagram-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }
  .memory-card-obj {
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.02);
    font-family: var(--font-m);
    font-size: 0.80rem;
  }
  .memory-card-obj.orig {
    border-left: 3px solid #f43f5e;
  }
  .memory-card-obj.slice {
    border-left: 3px solid #10b981;
    background: rgba(16, 185, 129, 0.04);
  }
  .memory-obj-id {
    font-size: 0.68rem;
    color: var(--ink-muted);
    margin-bottom: 4px;
  }
  .memory-cells-row {
    display: flex;
    gap: 4px;
    margin-top: 6px;
  }
  .memory-cell {
    padding: 3px 8px;
    border-radius: 5px;
    background: var(--surface-2);
    border: 1px solid var(--line);
    font-weight: 700;
    font-size: 0.78rem;
  }
  .memory-cell.highlight {
    background: rgba(16, 185, 129, 0.18);
    border-color: var(--moss);
    color: #34d399;
  }

  /* Интерактивный микро-квиз для проверки интуиции */
  .quick-check-wrap {
    margin-top: 14px;
    padding: 12px 16px;
    border-radius: 12px;
    background: rgba(245, 158, 11, 0.06);
    border: 1px solid rgba(245, 158, 11, 0.22);
  }
  .quick-check-question {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .quick-check-chips {
    display: flex;
    gap: 8px;
  }
  .quick-check-chip {
    padding: 6px 14px;
    border-radius: 8px;
    background: var(--surface-2);
    border: 1px solid var(--line);
    color: var(--ink-soft);
    font-size: 0.78rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
  }
  .quick-check-chip:hover {
    border-color: var(--moss);
    color: var(--ink);
  }
  .quick-check-chip.correct {
    background: rgba(16, 185, 129, 0.18);
    border-color: var(--moss);
    color: #34d399;
  }
"""

hud_markup = """
        <!-- ЕДИНЫЙ ЦЕЛЬНЫЙ ПУЛЬТ УПРАВЛЕНИЯ (HUD): ЭШЕЛОН + СВЕТЯЩАЯСЯ НИТЬ 13 ТОЧЕК НА РЕЛЬСЕ -->
        <div class="sprint-hud-master">
          
          <!-- 1. Верхний ярус: Эшелон и шкала готовности к собеседованию -->
          <div class="hud-top-tier">
            <a href="#/python" class="hud-close-btn" title="Выйти к карте">✕</a>
            
            <div class="hud-echelon-bar-wrap">
              <div class="hud-echelon-meta">
                <span class="hud-echelon-title">
                  <span>🚨 Эшелон 1: Скрининг и база</span>
                </span>
                <span class="hud-target-readiness">
                  <span>🎯</span> <strong>35% готовности к тех-скринингу</strong>
                </span>
              </div>
              <div class="hud-laser-track">
                <div class="hud-laser-fill" style="width: 35%;"></div>
              </div>
            </div>

            <div style="display:flex;gap:8px;align-items:center;">
              <div class="sprint-xp-pill">⚡ +10 XP</div>
              <a href="#/docs" class="topbar-help-btn" style="padding:5px 11px;border-radius:10px;"><span class="topbar-help-text">📖 Справка</span></a>
            </div>
          </div>

          <!-- Тонкий оптический разделитель -->
          <div class="hud-divider"></div>

          <!-- 2. Нижний ярус: Текущий юнит + нить из 13 светящихся точек на рельсе -->
          <div class="hud-bottom-tier">
            <div class="hud-unit-info">
              <span>Юнит 1.1: <strong>Базовые коллекции и срезы</strong></span>
              <span class="hud-topic-badge">Тема 3 из 13 · Срезы</span>
            </div>

            <!-- Рельс с 13 точками-жемчужинами -->
            <div class="hud-rail-container" title="13 тем Юнита 1.1">
              <div class="hud-rail-line"></div>
              <div class="hud-rail-line-active" style="width: 44px;"></div>
              
              <div class="hud-dots-beads">
                <span class="hud-bead done" title="1. Память и структуры (Пройдено)"></span>
                <span class="hud-bead done" title="2. Индексация (Пройдено)"></span>
                <span class="hud-bead active" title="3. Срезы (Текущая тема)"></span>
                <span class="hud-bead" title="4. Множества set/frozenset"></span>
                <span class="hud-bead" title="5. Аргументы *args/**kwargs"></span>
                <span class="hud-bead" title="6. Методы dict"></span>
                <span class="hud-bead" title="7. Методы списков"></span>
                <span class="hud-bead" title="8. collections.namedtuple"></span>
                <span class="hud-bead" title="9. collections.deque, Counter"></span>
                <span class="hud-bead" title="10. Pass by assignment"></span>
                <span class="hud-bead" title="11. Файлы (open)"></span>
                <span class="hud-bead" title="12. Служебные zip, id"></span>
                <span class="hud-bead milestone" title="13. Рубежный тест Юнита 1.1 👑"></span>
                <span class="hud-counter-pill">3 / 13</span>
              </div>
            </div>
          </div>

        </div>
"""

theory_card_enriched = """
        <!-- ЭКРАН УРОКА: ОБОГАЩЁННЫЙ КОНСПЕКТ СО СХЕМОЙ ПАМЯТИ -->
        <div id="stage-theory" class="stage-view">
          <div class="coddy-lesson-card" style="max-width:800px;margin:0 auto;">
            <div class="lesson-theory">
              <h3 style="font-size:1.30rem;font-weight:800;margin-bottom:12px;color:var(--ink);letter-spacing:-0.02em;">Срез – это всегда копия</h3>
              <p style="font-size:.95rem;color:var(--ink-soft);line-height:1.6;margin-bottom:14px;">
                Важное отличие от обращения по одному индексу: <code>lst[i]</code> возвращает ссылку на сам элемент, а <code>lst[i:j]</code> – <b>новый объект</b>, поверхностную копию (<i>shallow copy</i>). Изменение среза <b>не затрагивает оригинал</b>.
              </p>

              <!-- Схема памяти CPython (Mental Model) -->
              <div class="memory-schema-box">
                <div class="memory-schema-title">
                  <span>🧠 Модель памяти CPython (Heap Allocation)</span>
                </div>
                <div class="memory-diagram-grid">
                  <div class="memory-card-obj orig">
                    <div class="memory-obj-id">id: 0x7fa1 · original (list)</div>
                    <div class="memory-cells-row">
                      <span class="memory-cell">1</span>
                      <span class="memory-cell">2</span>
                      <span class="memory-cell">3</span>
                      <span class="memory-cell">4</span>
                      <span class="memory-cell">5</span>
                    </div>
                  </div>
                  <div class="memory-card-obj slice">
                    <div class="memory-obj-id" style="color:#34d399;">id: 0x8be4 · piece = original[1:3] (новый объект!)</div>
                    <div class="memory-cells-row">
                      <span class="memory-cell">2</span>
                      <span class="memory-cell">3</span>
                      <span class="memory-cell highlight">+99</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Интерактивный код -->
              <div class="code-block-wrap" style="background:#090d13;border:1px solid var(--line);border-radius:12px;overflow:hidden;margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 16px;background:#121720;border-bottom:1px solid var(--line);font-size:.78rem;font-family:var(--font-m);color:var(--ink-muted);">
                  <span>python 3.13</span>
                  <button type="button" class="btn btn-ghost" style="padding:3px 10px;font-size:.76rem;border-color:var(--moss);color:var(--moss);" onclick="runTheoryCode()">▶ Запустить код</button>
                </div>
                <pre style="margin:0;padding:14px 18px;font-family:var(--font-m);font-size:.88rem;line-height:1.65;color:#f8fafc;background:transparent;"><code><span style="color:#ff7b72;font-weight:600;">original</span> = [<span style="color:#79c0ff;">1</span>, <span style="color:#79c0ff;">2</span>, <span style="color:#79c0ff;">3</span>, <span style="color:#79c0ff;">4</span>, <span style="color:#79c0ff;">5</span>]
<span style="color:#ff7b72;font-weight:600;">piece</span> = original<span style="color:#7ee787;font-weight:700;background:rgba(126,231,135,0.12);padding:1px 4px;border-radius:4px;">[1:3]</span>
piece.<span style="color:#d2a8ff;">append</span>(<span style="color:#79c0ff;">99</span>)

<span style="color:#d2a8ff;">print</span>(original)  <span style="color:#8b949e;font-style:italic;"># [1, 2, 3, 4, 5] — не изменился!</span>
<span style="color:#d2a8ff;">print</span>(piece)     <span style="color:#8b949e;font-style:italic;"># [2, 3, 99]</span></code></pre>
                <div id="theory-live-out" style="display:none;background:#05070a;border-top:1px dashed var(--line);padding:10px 18px;font-family:var(--font-m);font-size:.84rem;color:#7ee787;">
                  [1, 2, 3, 4, 5]<br>[2, 3, 99]
                </div>
              </div>

              <!-- 1-клик микро-проверка для закрепления интуиции -->
              <div class="quick-check-wrap">
                <div class="quick-check-question">
                  <span>⚡ Экспресс-проверка: изменится ли original после <code>piece.append(99)</code>?</span>
                </div>
                <div class="quick-check-chips">
                  <button type="button" class="quick-check-chip correct" onclick="alert('Верно! Срез создает независимый список в куче. +5 XP')">✓ Нет, останется прежним</button>
                  <button type="button" class="quick-check-chip" onclick="alert('Неверно. Срез lst[1:3] — это копия, оригинал защищен!')">Да, добавится 99</button>
                </div>
              </div>
            </div>

            <!-- Доминирующая кнопка действия -->
            <div style="margin-top:20px;display:flex;gap:10px;align-items:center;">
              <button type="button" class="btn btn-ghost" style="padding:12px 20px;border-radius:14px;font-size:.88rem;">← Назад</button>
              <button class="btn-glass-emerald btn-sprint-cta" style="flex:1;padding:12px 24px;border-radius:14px;font-size:.95rem;font-weight:800;background:var(--moss-gradient);box-shadow:var(--shadow-moss);">
                Понятно, дальше (+10 XP) ➔
              </button>
            </div>
          </div>
        </div>
"""

html_final = orig
html_final = html_final.replace("</style>", hud_css + "\n</style>", 1)
html_final = html_final.replace('class="tabs-variant-block"', 'class="tabs-variant-block" style="display:none !important;"')

start_topbar = '<!-- 1. ВЕРХНИЙ СПРИНТ-ТОПБАР -->'
start_idx = html_final.find(start_topbar)
end_stage_theory = '<!-- ================= ЭКРАН 2: КАРТОЧКИ ================= -->'
end_idx = html_final.find(end_stage_theory)

if start_idx != -1 and end_idx != -1:
    html_final = html_final[:start_idx] + hud_markup + '\n        ' + theory_card_enriched + '\n        ' + html_final[end_idx:]

with open("mockup_unified_hud_polished.html", "w", encoding="utf-8") as f:
    f.write(html_final)

with open("design_mockups/mockup_unified_hud_polished.html", "w", encoding="utf-8") as f:
    f.write(html_final)

# Chrome screenshots
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\hud_polished_full.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_unified_hud_polished.html"
])

brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
src_full = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\hud_polished_full.png"
shutil.copyfile(src_full, os.path.join(brain_dir, "hud_polished_full.png"))

img = Image.open(src_full)
crop = img.crop((260, 0, 1420, 240))
crop.save(r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\hud_polished_crop.png")
crop.save(os.path.join(brain_dir, "hud_polished_crop.png"))

# Also crop the memory schema and quick check area (x: 260 to 1420, y: 220 to 560)
crop_card = img.crop((260, 220, 1420, 680))
crop_card.save(r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\card_enriched_crop.png")
crop_card.save(os.path.join(brain_dir, "card_enriched_crop.png"))

print("Captured polished HUD and enriched card successfully!")
