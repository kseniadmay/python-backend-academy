# -*- coding: utf-8 -*-
"""
Генератор чистой тестовой страницы для навыка 1.1.1 с 4 вариантами вкладок:
- Style 1: Underline (минималистичный Linear / Apple стиль)
- Style 2: Stepper (пошаговый трек Mastery Pipeline с коннекторами)
- Style 3: Milestones (микро-карточки с прогрессбарами)
- Style 4: Capsule (прежняя капсула для сравнения)
"""
import re

with open('academy.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# 1. Извлекаем <head> целиком из academy.html (100% оригинальные цвета и прозрачность)
head_match = re.search(r'<head>([\s\S]*?)</head>', orig)
head_inner = head_match.group(1) if head_match else ''

html_content = f"""<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
{head_inner}
<title>Academy — Python Backend (Навык 1.1.1)</title>
<style>
  /* ================= ВАРИАНТ 1: МИНИМАЛИСТИЧНЫЙ UNDERLINE (LINEAR / APPLE) ================= */
  .tabs-underline {{
    display: flex;
    gap: 24px;
    border-bottom: 1px solid var(--line);
    margin-bottom: 18px;
    padding: 0 4px;
  }}
  .tab-underline-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 0;
    font-size: .88rem;
    font-weight: 500;
    color: var(--ink-muted);
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    cursor: pointer;
    transition: all .18s;
    position: relative;
    margin-bottom: -1px;
    user-select: none;
  }}
  .tab-underline-item:hover {{
    color: var(--ink);
  }}
  .tab-underline-item.active {{
    color: var(--moss-deep);
    font-weight: 700;
    border-bottom: 2px solid var(--moss);
    box-shadow: 0 2px 10px rgba(16, 185, 129, 0.25);
  }}
  .tab-underline-badge {{
    font-size: .72rem;
    font-family: var(--font-m);
    padding: 1px 7px;
    border-radius: 999px;
    background: var(--surface-2);
    color: var(--ink-muted);
    border: 1px solid var(--line);
  }}
  .tab-underline-item.active .tab-underline-badge {{
    background: var(--moss-soft);
    color: var(--moss);
    border-color: var(--moss);
    font-weight: 700;
  }}

  /* ================= ВАРИАНТ 2: ПОШАГОВЫЙ ТРЕК С КОННЕКТОРАМИ (STEPPER PIPELINE) ================= */
  .tabs-stepper {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    padding: 6px 4px;
    position: relative;
  }}
  .stepper-node {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: transparent;
    border: none;
    cursor: pointer;
    user-select: none;
    padding: 4px 6px;
    border-radius: 8px;
    transition: all .15s;
  }}
  .stepper-node:hover {{ background: var(--surface-2); }}
  .stepper-node-circle {{
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: .75rem;
    font-weight: 700;
    font-family: var(--font-m);
    background: var(--surface-2);
    border: 1px solid var(--line);
    color: var(--ink-muted);
    transition: all .2s;
  }}
  .stepper-node.active .stepper-node-circle {{
    background: var(--moss);
    color: #fff;
    border-color: var(--moss);
    box-shadow: 0 0 12px var(--moss-glow);
  }}
  .stepper-node.done .stepper-node-circle {{
    background: var(--moss-soft);
    color: var(--moss);
    border-color: var(--moss);
  }}
  .stepper-node-label {{
    font-size: .84rem;
    font-weight: 600;
    color: var(--ink-muted);
  }}
  .stepper-node.active .stepper-node-label {{
    color: var(--ink);
    font-weight: 700;
  }}
  .stepper-node.done .stepper-node-label {{
    color: var(--ink-soft);
  }}
  .stepper-connector {{
    flex: 1;
    height: 2px;
    background: var(--line-soft);
    margin: 0 10px;
  }}
  .stepper-connector.done {{
    background: var(--moss);
  }}

  /* ================= ВАРИАНТ 3: МИКРО-КАРТОЧКИ С ПРОГРЕССОМ (MILESTONES) ================= */
  .tabs-milestones {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 18px;
  }}
  .milestone-tab {{
    background: var(--surface);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 8px 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    cursor: pointer;
    transition: all .18s;
    text-align: left;
    user-select: none;
  }}
  .milestone-tab:hover {{
    border-color: rgba(255, 255, 255, 0.16);
  }}
  .milestone-tab.active {{
    border-color: var(--moss);
    background: var(--surface-2);
    box-shadow: 0 0 12px var(--moss-glow);
  }}
  .milestone-tab-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: .78rem;
    font-weight: 600;
    color: var(--ink-soft);
  }}
  .milestone-tab.active .milestone-tab-top {{
    color: var(--moss-deep);
    font-weight: 700;
  }}
  .milestone-microbar {{
    height: 3px;
    background: var(--line-soft);
    border-radius: 2px;
    overflow: hidden;
  }}
  .milestone-microbar-fill {{
    height: 100%;
    background: var(--moss);
    border-radius: 2px;
  }}

  /* Переключатель стилей вкладок в шапке (для удобного сравнения) */
  .tab-style-picker {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: var(--surface-2);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 2px 6px;
    font-size: .74rem;
    color: var(--ink-muted);
  }}
  .tab-style-picker select {{
    background: transparent;
    border: none;
    color: var(--ink);
    font-size: .74rem;
    font-family: inherit;
    font-weight: 600;
    cursor: pointer;
    outline: none;
  }}

  /* Улучшения для экранов */
  .tasks-single-row {{
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 6px;
    margin-bottom: 12px;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }}
  .tasks-single-row::-webkit-scrollbar {{ display: none; }}
  .tasks-single-row .btn {{
    flex-shrink: 0;
    white-space: nowrap;
    padding: 6px 12px;
    font-size: .78rem;
  }}
  .ruler-table-compact {{
    width: 100%;
    max-width: 380px;
    margin: 12px auto;
    border-collapse: collapse;
    text-align: center;
    font-family: var(--font-m);
    font-size: .84rem;
    background: var(--surface-2);
    border: 1px solid var(--line-soft);
    border-radius: 10px;
    padding: 8px;
  }}
  .ruler-table-compact td {{ padding: 4px 6px; }}
  .ruler-target {{
    color: var(--amber) !important;
    font-weight: 700;
  }}
  .ruler-cell-target {{
    background: var(--amber-soft) !important;
    border: 1px solid var(--amber) !important;
    color: var(--amber) !important;
    border-radius: 6px;
    font-weight: 700;
  }}
  .fc-chips-container {{
    display: flex;
    gap: 8px;
    justify-content: center;
    margin: 14px 0 6px;
  }}
  .fc-tap-chip {{
    padding: 7px 16px;
    border-radius: 8px;
    background: var(--surface-2);
    border: 1px solid var(--line);
    color: var(--ink);
    font-family: var(--font-m);
    font-size: .90rem;
    font-weight: 700;
    cursor: pointer;
    transition: all .15s;
  }}
  .fc-tap-chip:hover {{ border-color: var(--moss); }}
  .fc-tap-chip.correct {{
    background: var(--moss-soft);
    border-color: var(--moss);
    color: var(--moss);
  }}
  .io-preview-box {{
    background: var(--surface-2);
    border: 1px solid var(--line-soft);
    border-radius: 8px;
    padding: 10px 14px;
    font-family: var(--font-m);
    font-size: .82rem;
    margin: 10px 0;
  }}
  .io-preview-row {{
    display: flex;
    justify-content: space-between;
    padding: 2px 0;
  }}
  .io-preview-row span:first-child {{ color: var(--ink-muted); }}
  .io-preview-row span:last-child {{ color: var(--moss); font-weight: 600; }}
</style>
</head>
<body>

<!-- Аутентичные светящиеся фоновые орбы Obsidian Theme -->
<div class="ambient-orb ambient-orb--burgundy" id="ambient-orb-burgundy"></div>
<div class="ambient-orb ambient-orb--emerald" id="ambient-orb-emerald"></div>

<div id="app">

  <!-- ================= АУТЕНТИЧНЫЙ САЙДБАР ================= -->
  <aside class="sidebar">
    <div class="brand">
      <svg class="icon icon-lg" viewBox="0 0 24 24"><circle cx="6" cy="6" r="2.2"/><circle cx="18" cy="6" r="2.2"/><circle cx="12" cy="18" r="2.2"/><path d="M7.8 7.6 10.5 16M16.2 7.6 13.5 16M8.3 6h7.4"/></svg>
      <span>Academy</span>
    </div>
    <div class="brand-sub">Python Backend</div>

    <div class="nav-section-header">Обучение</div>
    <a href="#/map" class="navlink"><svg class="icon" viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg><span>3D-Тропа</span></a>
    <a href="#/" class="navlink"><svg class="icon" viewBox="0 0 24 24"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg><span>Дашборд</span></a>
    
    <details class="nav-modules-accordion" open>
      <summary class="nav-modules-summary">
        <span>📚 Модули 01–07</span>
        <span class="navlink__pct">14%</span>
      </summary>
      <div class="nav-modules-list">
        <a href="#/python" class="navlink active"><svg class="icon" viewBox="0 0 24 24"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg><span>01 · Python</span><span class="navlink__pct">14%</span></a>
        <a href="#/web" class="navlink"><svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20M2 12h20"/></svg><span>02 · Web</span></a>
        <a href="#/backend" class="navlink"><svg class="icon" viewBox="0 0 24 24"><rect width="20" height="8" x="2" y="2" rx="2" ry="2"/><rect width="20" height="8" x="2" y="14" rx="2" ry="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/></svg><span>03 · Backend</span></a>
      </div>
    </details>

    <div class="nav-section-header">Тренажёры</div>
    <a href="#/practice" class="navlink"><svg class="icon" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg><span>Практика IDE</span></a>
    <a href="#/cards" class="navlink"><svg class="icon" viewBox="0 0 24 24"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="m9 8 6 4-6 4Z"/></svg><span>Карточки</span></a>
    <a href="#/mock" class="navlink"><svg class="icon" viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg><span>Собеседование</span></a>

    <div class="nav-section-header">Инструменты</div>
    <a href="#/docs" class="navlink"><svg class="icon" viewBox="0 0 24 24"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10M6 10h10"/></svg><span>Справочник</span></a>
    <a href="#/sandbox" class="navlink"><svg class="icon" viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg><span>Песочница</span></a>

    <div class="sidebar-foot">
      <button class="btn-quick-start">⚡ Микро-шаг (2 мин)</button>
      <div class="sidebar-pomo-pill">🍅 15:00</div>
      <div class="streak-pill">
        <svg class="icon" viewBox="0 0 24 24"><path d="M12 3c-.5 3-3 4-3 7.5A3.5 3.5 0 0 0 12 14a3.5 3.5 0 0 0 3-5c1.5 1 2 2.7 2 4.2A5 5 0 0 1 12 21a5 5 0 0 1-5-5.2C7 12 9 9 9 7c1 1 1.2 2 1.2 2S11 5 12 3Z"/></svg>
        <span>9 дней подряд</span>
      </div>
      <button class="icon-btn" onclick="toggleTheme()" title="Переключить тему">☀️ / 🌙</button>
      <button class="link-quiet">Сбросить прогресс</button>
      <button class="link-quiet">🔄 Контекст для нового чата</button>
      <button class="link-quiet">🐞 Журнал замечаний</button>
      <button class="link-quiet">⚙️ Настройки</button>
    </div>
  </aside>

  <!-- ================= ОСНОВНАЯ ОБЛАСТЬ (SHELL) ================= -->
  <div class="shell">
    <main>
      <div class="container" style="max-width:880px;">

        <!-- 1. ВЕРХНИЙ СПРИНТ-ТОПБАР -->
        <div class="sprint-focus-topbar sprint-topbar">
          <a href="#/python" class="sprint-close-btn" title="Выйти к юниту">✕</a>
          <div class="sprint-progress-wrap">
            <div class="sprint-progress-meta">
              <span>🚨 Эшелон 1 · Юнит 1.1: Базовые коллекции и срезы (list, tuple, slice) · <strong id="topbar-mode-name">📖 Конспект</strong></span>
              <span id="topbar-step-label">Шаг 1 из 3</span>
            </div>
            <div class="sprint-progress-track">
              <div class="sprint-progress-fill" id="topbar-progress-line" style="width:33%;"></div>
            </div>
          </div>
          <div style="display:flex;gap:6px;align-items:center;">
            <!-- Переключатель формата табов прямо в шапке -->
            <div class="tab-style-picker" title="Формат вкладок">
              <span>Стиль:</span>
              <select id="tab-style-select" onchange="changeTabStyle(this.value)">
                <option value="underline" selected>Линейный (Underline)</option>
                <option value="stepper">Пошаговый трек (Stepper)</option>
                <option value="milestones">Микро-карточки</option>
                <option value="capsule">Капсула (прежняя)</option>
              </select>
            </div>
            <button type="button" class="btn btn-ghost" id="btn-fullnote" style="padding:5px 9px;font-size:.76rem;border-radius:10px;">📄 Весь конспект</button>
            <a href="#/docs" class="topbar-help-btn" style="padding:5px 9px;font-size:.76rem;border-radius:10px;"><span class="topbar-help-text">📖 Справка</span></a>
          </div>
        </div>

        <!-- 2. БЛОК ВКЛАДОК (ПЕРЕКЛЮЧАЕМЫЕ 4 ВАРИАНТА) -->

        <!-- ВАРИАНТ 1: МИНИМАЛИСТИЧНЫЙ UNDERLINE (ПО УМОЛЧАНИЮ) -->
        <div id="tabs-variant-underline" class="tabs-variant-block">
          <div class="tabs-underline">
            <button class="tab-underline-item active" id="u-tab-theory" onclick="switchStage('theory')">
              <span>📖 Конспект</span>
              <span class="tab-underline-badge">✓</span>
            </button>
            <button class="tab-underline-item" id="u-tab-cards" onclick="switchStage('cards')">
              <span>🎴 Карточки</span>
              <span class="tab-underline-badge">1/9</span>
            </button>
            <button class="tab-underline-item" id="u-tab-code" onclick="switchStage('code')">
              <span>💻 Практика</span>
              <span class="tab-underline-badge">0/5</span>
            </button>
            <button class="tab-underline-item" style="color:var(--amber);margin-left:auto;" onclick="alert('Рубежный UnitTest 1.1 разблокируется после практики!')">
              <span>⚡ Тест 1.1</span>
            </button>
          </div>
        </div>

        <!-- ВАРИАНТ 2: ПОШАГОВЫЙ ТРЕК С КОННЕКТОРАМИ -->
        <div id="tabs-variant-stepper" class="tabs-variant-block" style="display:none;">
          <div class="tabs-stepper">
            <button class="stepper-node active" id="s-tab-theory" onclick="switchStage('theory')">
              <span class="stepper-node-circle">1</span>
              <span class="stepper-node-label">Конспект ✓</span>
            </button>
            <div class="stepper-connector done" id="s-conn-1"></div>
            <button class="stepper-node" id="s-tab-cards" onclick="switchStage('cards')">
              <span class="stepper-node-circle">2</span>
              <span class="stepper-node-label">Карточки (1/9)</span>
            </button>
            <div class="stepper-connector" id="s-conn-2"></div>
            <button class="stepper-node" id="s-tab-code" onclick="switchStage('code')">
              <span class="stepper-node-circle">3</span>
              <span class="stepper-node-label">Практика (0/5)</span>
            </button>
            <div class="stepper-connector" id="s-conn-3"></div>
            <button class="stepper-node" style="opacity:0.65;" onclick="alert('Рубежный тест!')">
              <span class="stepper-node-circle" style="color:var(--amber);border-color:var(--amber);">⚡</span>
              <span class="stepper-node-label" style="color:var(--amber);">Тест 1.1</span>
            </button>
          </div>
        </div>

        <!-- ВАРИАНТ 3: МИКРО-КАРТОЧКИ С ПРОГРЕССОМ -->
        <div id="tabs-variant-milestones" class="tabs-variant-block" style="display:none;">
          <div class="tabs-milestones">
            <div class="milestone-tab active" id="m-tab-theory" onclick="switchStage('theory')">
              <div class="milestone-tab-top">
                <span>1 · Конспект</span>
                <span style="color:var(--moss);">✓</span>
              </div>
              <div class="milestone-microbar"><div class="milestone-microbar-fill" style="width:100%;"></div></div>
            </div>
            <div class="milestone-tab" id="m-tab-cards" onclick="switchStage('cards')">
              <div class="milestone-tab-top">
                <span>2 · Карточки</span>
                <span>1/9</span>
              </div>
              <div class="milestone-microbar"><div class="milestone-microbar-fill" style="width:11%;"></div></div>
            </div>
            <div class="milestone-tab" id="m-tab-code" onclick="switchStage('code')">
              <div class="milestone-tab-top">
                <span>3 · Практика</span>
                <span>0/5</span>
              </div>
              <div class="milestone-microbar"><div class="milestone-microbar-fill" style="width:0%;"></div></div>
            </div>
            <div class="milestone-tab" style="border-color:rgba(245,158,11,0.3);" onclick="alert('Рубежный тест!')">
              <div class="milestone-tab-top">
                <span style="color:var(--amber);">⚡ Тест 1.1</span>
                <span style="color:var(--ink-muted);font-size:.70rem;">Финал</span>
              </div>
              <div class="milestone-microbar"><div class="milestone-microbar-fill" style="width:0%;background:var(--amber);"></div></div>
            </div>
          </div>
        </div>

        <!-- ВАРИАНТ 4: ПРЕЖНЯЯ КАПСУЛА -->
        <div id="tabs-variant-capsule" class="tabs-variant-block" style="display:none;">
          <div class="stepper-capsule">
            <button class="stepper-capsule-item active" id="c-tab-theory" onclick="switchStage('theory')">
              <span>📖 Конспект</span>
              <span class="stepper-badge-pill">✓</span>
            </button>
            <button class="stepper-capsule-item" id="c-tab-cards" onclick="switchStage('cards')">
              <span>🎴 Карточки</span>
              <span class="stepper-badge-pill">1/9</span>
            </button>
            <button class="stepper-capsule-item" id="c-tab-code" onclick="switchStage('code')">
              <span>💻 Практика</span>
              <span class="stepper-badge-pill">0/5</span>
            </button>
            <a href="#/python/unittest/1.1" class="stepper-capsule-item">
              <span>⚡ Тест 1.1</span>
            </a>
          </div>
        </div>

        <!-- ================= ЭКРАН 1: КОНСПЕКТ (ТЕОРИЯ) ================= -->
        <div id="stage-theory" class="stage-view">
          <div class="coddy-lesson-card" style="max-width:760px;margin:0 auto;">
            <div class="lesson-theory">
              <h3 style="font-size:1.25rem;font-weight:700;margin-bottom:12px;color:var(--ink);">Срез – это всегда копия</h3>
              <p style="font-size:.95rem;color:var(--ink-soft);line-height:1.6;margin-bottom:18px;">
                Важное отличие от обращения по одному индексу: <code>lst[i]</code> возвращает сам элемент, а <code>lst[i:j]</code> – <b>новый объект</b>, поверхностную копию (<i>shallow copy</i>) части исходного. Изменение среза <b>не затрагивает оригинал</b>.
              </p>

              <!-- Интерактивный код -->
              <div class="code-block-wrap" style="background:#090d13;border:1px solid var(--line);border-radius:12px;overflow:hidden;margin-bottom:16px;">
                <div style="display:flex;justify-content:space-between;align-items:center;padding:7px 14px;background:#121720;border-bottom:1px solid var(--line);font-size:.78rem;font-family:var(--font-m);color:var(--ink-muted);">
                  <span>python</span>
                  <button type="button" class="btn btn-ghost" style="padding:3px 10px;font-size:.76rem;border-color:var(--moss);color:var(--moss);" onclick="runTheoryCode()">▶ Запустить код</button>
                </div>
                <pre style="margin:0;padding:14px 18px;font-family:var(--font-m);font-size:.88rem;line-height:1.65;color:#f8fafc;background:transparent;"><code><span style="color:#ff7b72;font-weight:600;">original</span> = [<span style="color:#79c0ff;">1</span>, <span style="color:#79c0ff;">2</span>, <span style="color:#79c0ff;">3</span>, <span style="color:#79c0ff;">4</span>, <span style="color:#79c0ff;">5</span>]
<span style="color:#ff7b72;font-weight:600;">piece</span> = original<span style="color:#7ee787;font-weight:700;background:rgba(126,231,135,0.12);padding:1px 4px;border-radius:4px;">[1:3]</span>
piece.<span style="color:#d2a8ff;">append</span>(<span style="color:#79c0ff;">99</span>)

<span style="color:#d2a8ff;">print</span>(original)  <span style="color:#8b949e;font-style:italic;"># [1, 2, 3, 4, 5] - не изменился</span>
<span style="color:#d2a8ff;">print</span>(piece)     <span style="color:#8b949e;font-style:italic;"># [2, 3, 99]</span></code></pre>
                <div id="theory-live-out" style="display:none;background:#05070a;border-top:1px dashed var(--line);padding:10px 18px;font-family:var(--font-m);font-size:.84rem;color:#7ee787;">
                  [1, 2, 3, 4, 5]<br>[2, 3, 99]
                </div>
              </div>
            </div>

            <!-- Кнопки перехода -->
            <div style="margin-top:14px;display:flex;gap:8px;align-items:center;">
              <button type="button" class="btn btn-ghost" style="padding:11px 18px;border-radius:14px;font-size:.88rem;">← Назад</button>
              <button class="btn-glass-emerald btn-sprint-cta" style="flex:1;" onclick="switchStage('cards')">
                Понятно, дальше (+10 XP) ➔
              </button>
            </div>
            <div style="display:flex;justify-content:flex-end;margin-top:8px;">
              <span class="meta" style="font-size:.78rem;color:var(--ink-muted);">Этап 1 из 3: Теория → Карточки → Код</span>
            </div>
          </div>
        </div>

        <!-- ================= ЭКРАН 2: КАРТОЧКИ ================= -->
        <div id="stage-cards" class="stage-view" style="display:none;">

          <!-- Сегментированный Stories-прогрессбар -->
          <div style="display:flex;gap:5px;max-width:680px;margin:0 auto 10px;">
            <div style="flex:1;height:4px;border-radius:999px;background:var(--moss);"></div>
            <div style="flex:1;height:4px;border-radius:999px;background:var(--surface-2);border:1px solid var(--line-soft);"></div>
            <div style="flex:1;height:4px;border-radius:999px;background:var(--surface-2);border:1px solid var(--line-soft);"></div>
            <div style="flex:1;height:4px;border-radius:999px;background:var(--surface-2);border:1px solid var(--line-soft);"></div>
            <div style="flex:1;height:4px;border-radius:999px;background:var(--surface-2);border:1px solid var(--line-soft);"></div>
            <div style="flex:1;height:4px;border-radius:999px;background:var(--surface-2);border:1px solid var(--line-soft);"></div>
            <div style="flex:1;height:4px;border-radius:999px;background:var(--surface-2);border:1px solid var(--line-soft);"></div>
            <div style="flex:1;height:4px;border-radius:999px;background:var(--surface-2);border:1px solid var(--line-soft);"></div>
            <div style="flex:1;height:4px;border-radius:999px;background:var(--surface-2);border:1px solid var(--line-soft);"></div>
          </div>

          <div style="display:flex;justify-content:center;margin:6px 0 12px;">
            <div class="deck-mini-track">
              <span>Колода 3 из 9 · <strong>Ф-003: Отрицательные индексы</strong></span>
            </div>
          </div>

          <div class="fc-stage" style="margin:10px auto;max-width:680px;">
            <div class="fc-card" id="fc-main-card" onclick="flipCardAction()">
              <div>
                <div style="display:flex;justify-content:space-between;align-items:center;">
                  <div class="topic-badge" id="fc-badge-label">Вопрос</div>
                  <span class="card-help-badge" onclick="event.stopPropagation();alert('Индекс -1 указывает на последний элемент, -2 — на предпоследний.')">💡 Шпаргалка</span>
                </div>

                <div class="fc-q" style="text-align:center;margin:16px 0;">
                  При <code>a = [1, 2, 3, 4, 5]</code>: Что вернёт <code>a[-2]</code>?
                </div>

                <!-- Лаконичная линейка индексов (заполняет пустую дыру без шума) -->
                <div onclick="event.stopPropagation()">
                  <table class="ruler-table-compact">
                    <tr>
                      <td style="color:var(--moss);font-size:.72rem;">0</td>
                      <td style="color:var(--moss);font-size:.72rem;">1</td>
                      <td style="color:var(--moss);font-size:.72rem;">2</td>
                      <td style="color:var(--moss);font-size:.72rem;">3</td>
                      <td style="color:var(--moss);font-size:.72rem;">4</td>
                    </tr>
                    <tr>
                      <td style="background:var(--surface);border-radius:5px;padding:3px;">1</td>
                      <td style="background:var(--surface);border-radius:5px;padding:3px;">2</td>
                      <td style="background:var(--surface);border-radius:5px;padding:3px;">3</td>
                      <td class="ruler-cell-target" style="padding:3px;">4</td>
                      <td style="background:var(--surface);border-radius:5px;padding:3px;">5</td>
                    </tr>
                    <tr>
                      <td style="color:var(--ink-muted);font-size:.74rem;">-5</td>
                      <td style="color:var(--ink-muted);font-size:.74rem;">-4</td>
                      <td style="color:var(--ink-muted);font-size:.74rem;">-3</td>
                      <td class="ruler-target" style="font-size:.78rem;">-2</td>
                      <td style="color:var(--ink-muted);font-size:.74rem;">-1</td>
                    </tr>
                  </table>
                </div>

                <!-- 4 быстрых чипса ответа -->
                <div class="fc-chips-container" onclick="event.stopPropagation()">
                  <button class="fc-tap-chip" onclick="answerChip(false, this)">3</button>
                  <button class="fc-tap-chip" onclick="answerChip(true, this)">4</button>
                  <button class="fc-tap-chip" onclick="answerChip(false, this)">2</button>
                  <button class="fc-tap-chip" onclick="answerChip(false, this)">IndexError</button>
                </div>

                <!-- Ответ при перевороте -->
                <div class="fc-a" id="fc-answer-content" style="display:none;margin-top:12px;background:var(--moss-soft);border:1px solid var(--moss);border-radius:10px;padding:10px 14px;color:var(--ink);">
                  <strong>✓ Ответ: 4</strong><br>
                  Отрицательный индекс <code>-2</code> указывает на предпоследний элемент списка.
                </div>
              </div>

              <div class="meta" style="margin-top:14px;text-align:center;font-size:.78rem;">Карточка 1 из 9</div>
            </div>

            <!-- Кнопки действий -->
            <div id="fc-unflipped-actions" style="margin-top:10px;display:flex;gap:10px;">
              <button class="btn btn-ghost" onclick="switchStage('theory')">← Назад</button>
              <button class="btn-glass-emerald btn-sprint-cta" style="flex:1;" onclick="flipCardAction()">Показать ответ (Пробел)</button>
              <button class="btn btn-ghost" onclick="flipCardAction()">Дальше →</button>
            </div>

            <div class="fc-rate-row" id="fc-rate-actions" style="display:none;margin-top:10px;">
              <button class="btn btn-ghost" onclick="flipCardAction()">Снова</button>
              <button class="btn btn-burgundy" onclick="flipCardAction()">Трудно (+2 XP)</button>
              <button class="btn btn-clay" onclick="flipCardAction()">Хорошо (+5 XP)</button>
              <button class="btn btn-primary" onclick="flipCardAction()">Легко (+10 XP)</button>
            </div>

            <div style="margin-top:14px;display:flex;justify-content:space-between;align-items:center;">
              <button class="link-quiet" onclick="switchStage('theory')">← Вернуться к конспекту</button>
              <button class="link-quiet" style="font-weight:700;color:var(--moss);" onclick="switchStage('code')">Этап 3: Практика кода в IDE (5 задач) ➔</button>
            </div>
          </div>
        </div>

        <!-- ================= ЭКРАН 3: ПРАКТИКА (IDE) ================= -->
        <div id="stage-code" class="stage-view" style="display:none;">

          <!-- Селектор задач в ОДНУ аккуратную строку без переноса -->
          <div class="tasks-single-row">
            <button class="btn btn-primary">✓ #20 · Разворот срезом [::-1]</button>
            <button class="btn btn-ghost">#19 · Главная диагональ 3x3</button>
            <button class="btn btn-ghost">#39 · Отрицательные индексы</button>
            <button class="btn btn-ghost">#255 · Подсписок первых 3 и последних 2</button>
            <button class="btn btn-ghost">#258 · Кортеж и список</button>
          </div>

          <div class="microstep-card">
            <div class="practice-desktop-grid">

              <!-- Левая колонка: описание задачи и I/O -->
              <div class="practice-left-pane">
                <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:8px;">
                  <span class="topic-badge" style="margin:0;">Задача #20 · <span class="badge" style="background:rgba(217,119,6,0.18);color:var(--amber);padding:1px 7px;border-radius:10px;font-weight:700;">🥚 Уровень 1</span> · Backend &amp; SQL</span>
                  <a href="#/docs" class="link-quiet" style="font-size:.78rem;">📚 Справка</a>
                </div>

                <h2 style="font-size:1.25rem;font-weight:700;margin-bottom:8px;">Разворот списка срезом [::-1]</h2>
                <div class="lesson-theory" style="font-size:.88rem;color:var(--ink-soft);line-height:1.55;margin-bottom:10px;">
                  Создайте исходный список чисел <code>original</code> и получите его инвертированную копию <code>reversed_list</code> с помощью шага среза <code>[::-1]</code>.
                </div>

                <!-- Блок входных и выходных данных -->
                <div class="io-preview-box">
                  <div class="io-preview-row">
                    <span>Вход (original):</span>
                    <span>[1, 2, 3, 4, 5]</span>
                  </div>
                  <div class="io-preview-row">
                    <span>Выход (reversed_list):</span>
                    <span>[5, 4, 3, 2, 1]</span>
                  </div>
                </div>

                <div style="margin-top:auto;">
                  <button class="btn btn-ghost" style="padding:6px 12px;font-size:.78rem;width:100%;" onclick="alert('Шаг -1 выполняет обход последовательности с конца.')">💡 Сократовская наводка (0/4)</button>
                </div>
              </div>

              <!-- Правая колонка: Редактор кода -->
              <div class="practice-right-pane">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;font-size:.78rem;color:var(--ink-muted);">
                  <span>Python 3.13</span>
                  <span style="cursor:pointer;text-decoration:underline;" onclick="resetTaskCode()">Сбросить код</span>
                </div>

                <div class="code-editor-shell" style="border-radius:12px;overflow:hidden;background:#090d13;border:1px solid var(--line);">
                  <textarea id="task-code-editor" class="code-editor" style="min-height:150px;font-family:var(--font-m);font-size:.85rem;line-height:1.6;color:#7ee787;background:transparent;border:none;padding:12px;width:100%;resize:vertical;outline:none;" spellcheck="false"># Задача #20: Сделайте реверс списка срезом
original = [1, 2, 3, 4, 5]
reversed_list = original[::-1]</textarea>
                </div>

                <div style="margin-top:10px;display:flex;gap:8px;align-items:center;">
                  <button class="btn-glass-emerald" style="flex:1;" onclick="runTaskValidation()">▶ Проверить решение (Ctrl+Enter)</button>
                  <button class="btn btn-ghost" onclick="alert('Код выполнен в Brython!')">⚡ Запустить</button>
                </div>

                <!-- Фиксированный терминал вывода тестов -->
                <div id="task-test-logs" style="margin-top:10px;background:#05070a;border:1px solid var(--line);border-radius:10px;padding:10px 14px;font-family:var(--font-m);font-size:.78rem;color:var(--ink-muted);">
                  Нажмите «Проверить решение» для запуска тестов…
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>
    </main>
  </div>

</div>

<script>
  let curStage = 'theory';

  function changeTabStyle(styleName) {{
    document.querySelectorAll('.tabs-variant-block').forEach(el => el.style.display = 'none');
    const targetBlock = document.getElementById('tabs-variant-' + styleName);
    if(targetBlock) targetBlock.style.display = 'block';
    updateAllTabStates(curStage);
  }}

  function switchStage(stageId) {{
    curStage = stageId;
    document.querySelectorAll('.stage-view').forEach(el => el.style.display = 'none');
    const targetStage = document.getElementById('stage-' + stageId);
    if(targetStage) targetStage.style.display = 'block';

    updateAllTabStates(stageId);

    const topTitle = document.getElementById('topbar-mode-name');
    const topCounter = document.getElementById('topbar-step-label');
    const topFill = document.getElementById('topbar-progress-line');
    const fullnoteBtn = document.getElementById('btn-fullnote');

    if(stageId === 'theory') {{
      topTitle.textContent = '📖 Конспект';
      topCounter.textContent = 'Шаг 1 из 3';
      topFill.style.width = '33%';
      if(fullnoteBtn) fullnoteBtn.style.display = 'inline-block';
    }} else if(stageId === 'cards') {{
      topTitle.textContent = '🎴 Карточки';
      topCounter.textContent = 'Карточка 1/9';
      topFill.style.width = '66%';
      if(fullnoteBtn) fullnoteBtn.style.display = 'none';
    }} else if(stageId === 'code') {{
      topTitle.textContent = '💻 Практика';
      topCounter.textContent = 'Задача 1/5';
      topFill.style.width = '100%';
      if(fullnoteBtn) fullnoteBtn.style.display = 'none';
    }}
  }}

  function updateAllTabStates(stageId) {{
    // 1. Underline
    document.querySelectorAll('.tab-underline-item').forEach(el => el.classList.remove('active'));
    const uBtn = document.getElementById('u-tab-' + stageId);
    if(uBtn) uBtn.classList.add('active');

    // 2. Stepper
    document.querySelectorAll('.stepper-node').forEach(el => el.classList.remove('active', 'done'));
    const sBtn = document.getElementById('s-tab-' + stageId);
    if(sBtn) sBtn.classList.add('active');
    if(stageId === 'cards' || stageId === 'code') {{
      const st = document.getElementById('s-tab-theory');
      if(st) st.classList.add('done');
    }}
    if(stageId === 'code') {{
      const sc = document.getElementById('s-tab-cards');
      if(sc) sc.classList.add('done');
    }}

    // 3. Milestones
    document.querySelectorAll('.milestone-tab').forEach(el => el.classList.remove('active'));
    const mBtn = document.getElementById('m-tab-' + stageId);
    if(mBtn) mBtn.classList.add('active');

    // 4. Capsule
    document.querySelectorAll('.stepper-capsule-item').forEach(el => el.classList.remove('active'));
    const cBtn = document.getElementById('c-tab-' + stageId);
    if(cBtn) cBtn.classList.add('active');
  }}

  function toggleTheme() {{
    const html = document.documentElement;
    const isDark = html.getAttribute('data-theme') === 'dark';
    html.setAttribute('data-theme', isDark ? 'light' : 'dark');
  }}

  function runTheoryCode() {{
    const out = document.getElementById('theory-live-out');
    out.style.display = out.style.display === 'none' ? 'block' : 'none';
  }}

  let cardFlipped = false;
  function flipCardAction() {{
    cardFlipped = !cardFlipped;
    const badge = document.getElementById('fc-badge-label');
    const ans = document.getElementById('fc-answer-content');
    const unflippedRow = document.getElementById('fc-unflipped-actions');
    const rateRow = document.getElementById('fc-rate-actions');

    if(cardFlipped) {{
      badge.textContent = 'Ответ';
      badge.style.background = 'var(--moss-soft)';
      badge.style.color = 'var(--moss)';
      ans.style.display = 'block';
      unflippedRow.style.display = 'none';
      rateRow.style.display = 'flex';
    }} else {{
      badge.textContent = 'Вопрос';
      badge.style.background = 'var(--surface-2)';
      badge.style.color = 'var(--ink-soft)';
      ans.style.display = 'none';
      unflippedRow.style.display = 'flex';
      rateRow.style.display = 'none';
    }}
  }}

  function answerChip(isCorrect, btn) {{
    const chips = btn.parentElement.querySelectorAll('.fc-tap-chip');
    chips.forEach(c => c.classList.remove('correct'));
    if(isCorrect) {{
      btn.classList.add('correct');
      if(!cardFlipped) flipCardAction();
    }} else {{
      alert('Попробуйте еще раз или переверните карточку.');
    }}
  }}

  window.addEventListener('keydown', function(e) {{
    if(e.code === 'Space' && e.target.tagName !== 'TEXTAREA') {{
      const cardsStage = document.getElementById('stage-cards');
      if(cardsStage && cardsStage.style.display !== 'none') {{
        e.preventDefault();
        flipCardAction();
      }}
    }}
  }});

  function runTaskValidation() {{
    const logs = document.getElementById('task-test-logs');
    logs.innerHTML = `
      <div style="color:#7ee787;">✓ [AST] Исходный список original объявлен</div>
      <div style="color:#7ee787;">✓ [AST] Использован шаг среза [::-1]</div>
      <div style="color:#7ee787;">✓ [Runtime] reversed_list == [5, 4, 3, 2, 1]</div>
      <div style="color:#7ee787;font-weight:700;margin-top:4px;">🎉 Все тесты пройдены! (+25 XP)</div>
    `;
  }}

  function resetTaskCode() {{
    document.getElementById('task-code-editor').value = `# Задача #20: Сделайте реверс списка срезом\\noriginal = None  # TODO\\nreversed_list = None  # TODO`;
    document.getElementById('task-test-logs').innerHTML = '<div style="color:var(--ink-muted);">Код сброшен к исходному шаблону.</div>';
  }}
</script>
</body>
</html>
"""

# Сохраняем в оба пути
with open('design_mockups/mockup_skill_1_1_1.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('mockup_skill_1_1_1.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Успешно созданы чистые тестовые страницы с 4 вариантами табов!")
