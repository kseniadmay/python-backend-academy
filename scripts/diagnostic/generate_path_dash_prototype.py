import os

base_dir = r"C:\Users\fury6\OneDrive\Python_Backend_Academy"
proto_path = os.path.join(base_dir, "design_mockups", "zen_path_and_dashboard_prototype.html")

html_content = """<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<title>Дистилляция главного экрана: Тропа (#/path) и Дашборд (#/)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Onest:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  :root, :root[data-theme="light"] {
    --zen-bg: #faf8f5;
    --zen-bg-subtle: #f4efe8;
    --zen-surface: rgba(255, 255, 255, 0.88);
    --zen-surface-card: rgba(255, 255, 255, 0.72);
    --zen-surface-subtle: rgba(15, 23, 42, 0.04);
    --zen-surface-hover: rgba(15, 23, 42, 0.06);
    --zen-hairline: rgba(0, 0, 0, 0.07);
    --zen-hairline-subtle: rgba(0, 0, 0, 0.04);
    --zen-glass-blur: 24px;
    --zen-text-main: #0f172a;
    --zen-text-soft: #334155;
    --zen-text-muted: #64748b;
    --zen-text-dim: #94a3b8;
    --zen-emerald: #145a46;
    --zen-emerald-light: #10b981;
    --zen-emerald-glow: rgba(20, 90, 70, 0.16);
    --zen-emerald-soft: rgba(20, 90, 70, 0.09);
    --zen-emerald-border: rgba(20, 90, 70, 0.28);
    --zen-amber: #d97706;
    --zen-amber-light: #f59e0b;
    --zen-amber-soft: rgba(217, 119, 6, 0.10);
    --zen-amber-border: rgba(217, 119, 6, 0.30);
    --zen-bordeaux: #6b1d2f;
    --zen-bordeaux-light: #be123c;
    --zen-bordeaux-soft: rgba(107, 29, 47, 0.09);
    --zen-bordeaux-border: rgba(107, 29, 47, 0.28);
    --zen-orb-burgundy: rgba(107, 29, 47, 0.07);
    --zen-orb-emerald: rgba(20, 90, 70, 0.07);
    --zen-shadow-island: 0 20px 48px -12px rgba(15, 23, 42, 0.08), 0 1px 2px rgba(15, 23, 42, 0.04);
    --zen-shadow-lift: 0 12px 28px -8px rgba(15, 23, 42, 0.07);
    --zen-font-sans: 'Onest', -apple-system, BlinkMacSystemFont, sans-serif;
    --zen-font-mono: 'JetBrains Mono', monospace;
  }

  :root[data-theme="dark"] {
    --zen-bg: #0b0f15;
    --zen-bg-subtle: #10151f;
    --zen-surface: rgba(18, 23, 33, 0.82);
    --zen-surface-card: rgba(22, 28, 40, 0.65);
    --zen-surface-subtle: rgba(255, 255, 255, 0.035);
    --zen-surface-hover: rgba(255, 255, 255, 0.07);
    --zen-hairline: rgba(255, 255, 255, 0.08);
    --zen-hairline-subtle: rgba(255, 255, 255, 0.045);
    --zen-glass-blur: 24px;
    --zen-text-main: #f8fafc;
    --zen-text-soft: #cbd5e1;
    --zen-text-muted: #8b9bb4;
    --zen-text-dim: #55657e;
    --zen-emerald: #10b981;
    --zen-emerald-light: #34d399;
    --zen-emerald-glow: rgba(16, 185, 129, 0.22);
    --zen-emerald-soft: rgba(16, 185, 129, 0.12);
    --zen-emerald-border: rgba(52, 211, 153, 0.35);
    --zen-amber: #f59e0b;
    --zen-amber-light: #fbbf24;
    --zen-amber-soft: rgba(245, 158, 11, 0.14);
    --zen-amber-border: rgba(251, 191, 36, 0.35);
    --zen-bordeaux: #fb7185;
    --zen-bordeaux-light: #f43f5e;
    --zen-bordeaux-soft: rgba(225, 29, 72, 0.16);
    --zen-bordeaux-border: rgba(251, 113, 133, 0.45);
    --zen-orb-burgundy: rgba(190, 18, 60, 0.16);
    --zen-orb-emerald: rgba(16, 185, 129, 0.14);
    --zen-shadow-island: 0 24px 64px -12px rgba(0, 0, 0, 0.65), 0 0 0 1px var(--zen-hairline);
    --zen-shadow-lift: 0 16px 36px -8px rgba(0, 0, 0, 0.55);
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--zen-bg);
    color: var(--zen-text-main);
    font-family: var(--zen-font-sans);
    line-height: 1.55;
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
    transition: background 0.25s ease, color 0.25s ease;
  }

  .zen-ambient-top {
    position: fixed; width: 480px; height: 480px;
    top: -140px; left: -100px;
    background: var(--zen-orb-burgundy);
    filter: blur(100px); border-radius: 50%;
    pointer-events: none; z-index: 0;
  }
  .zen-ambient-bottom {
    position: fixed; width: 460px; height: 460px;
    bottom: -120px; right: -90px;
    background: var(--zen-orb-emerald);
    filter: blur(100px); border-radius: 50%;
    pointer-events: none; z-index: 0;
  }

  .zen-topbar {
    position: sticky; top: 0; z-index: 100;
    background: var(--zen-surface);
    backdrop-filter: blur(var(--zen-glass-blur));
    -webkit-backdrop-filter: blur(var(--zen-glass-blur));
    border-bottom: 1px solid var(--zen-hairline);
    padding: 12px 24px;
    display: flex; justify-content: space-between; align-items: center; gap: 16px;
  }
  .zen-brand {
    display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--zen-text-main);
  }
  .zen-brand-badge {
    width: 32px; height: 32px; border-radius: 9px;
    background: linear-gradient(135deg, var(--zen-emerald), var(--zen-bordeaux));
    color: #ffffff; display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 0.92rem; box-shadow: 0 2px 8px var(--zen-emerald-glow);
  }
  .zen-brand-title { font-size: 1.05rem; font-weight: 800; letter-spacing: -0.01em; }
  .zen-brand-sub { font-size: 0.72rem; color: var(--zen-text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }

  .zen-btn-toggle {
    background: var(--zen-surface-subtle); border: 1px solid var(--zen-hairline);
    color: var(--zen-text-soft); padding: 8px 14px; border-radius: 10px;
    font-size: 0.82rem; font-weight: 600; cursor: pointer; display: inline-flex;
    align-items: center; gap: 6px; transition: all 0.15s ease;
  }
  .zen-btn-toggle:hover {
    background: var(--zen-surface-hover); color: var(--zen-text-main); border-color: var(--zen-emerald-border);
  }

  .zen-layout {
    position: relative; z-index: 1; max-width: 1240px; margin: 0 auto; padding: 24px 20px 80px;
  }

  .zen-tab-nav {
    display: flex; gap: 8px; background: var(--zen-surface);
    border: 1px solid var(--zen-hairline); padding: 6px; border-radius: 16px;
    margin-bottom: 24px; backdrop-filter: blur(var(--zen-glass-blur));
    box-shadow: var(--zen-shadow-island);
  }
  .zen-tab-btn {
    flex: 1; padding: 10px 18px; border-radius: 11px; border: none;
    background: transparent; color: var(--zen-text-muted); font-family: var(--zen-font-sans);
    font-size: 0.88rem; font-weight: 600; cursor: pointer; display: flex;
    align-items: center; justify-content: center; gap: 8px; transition: all 0.15s ease;
  }
  .zen-tab-btn:hover { color: var(--zen-text-main); background: var(--zen-surface-hover); }
  .zen-tab-btn.active {
    background: var(--zen-emerald-soft); color: var(--zen-emerald);
    border: 1px solid var(--zen-emerald-border); font-weight: 700;
  }
  :root[data-theme="dark"] .zen-tab-btn.active { color: var(--zen-emerald-light); }

  .tab-pane { display: none; }
  .tab-pane.active { display: block; }

  /* Card primitives */
  .zen-card {
    background: var(--zen-surface); border: 1px solid var(--zen-hairline);
    border-radius: 24px; padding: 26px 28px; backdrop-filter: blur(var(--zen-glass-blur));
    -webkit-backdrop-filter: blur(var(--zen-glass-blur)); box-shadow: var(--zen-shadow-island);
    margin-bottom: 24px;
  }
  .zen-card-subtle {
    background: var(--zen-surface-card); border: 1px solid var(--zen-hairline-subtle);
    border-radius: 18px; padding: 20px 22px; transition: transform .2s ease, border-color .2s ease;
  }
  .zen-card-subtle:hover {
    border-color: var(--zen-hairline);
  }

  .zen-header {
    display: flex; justify-content: space-between; align-items: center; gap: 16px;
    padding-bottom: 16px; margin-bottom: 20px; border-bottom: 1px solid var(--zen-hairline);
    flex-wrap: wrap;
  }
  .zen-eyebrow {
    font-size: 0.74rem; font-weight: 700; color: var(--zen-text-muted);
    letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 4px;
  }
  .zen-title {
    font-size: 1.28rem; font-weight: 800; letter-spacing: -0.01em; color: var(--zen-text-main);
  }

  .dots-necklace {
    display: inline-flex; align-items: center; gap: 7px; padding: 6px 14px;
    border-radius: 999px; background: var(--zen-surface-subtle); border: 1px solid var(--zen-hairline);
    font-size: 0.78rem; font-weight: 600;
  }

  /* Two Column Layout for Coddy Path */
  .zen-split-grid {
    display: grid; grid-template-columns: 1fr 340px; gap: 24px; align-items: start;
  }
  @media (max-width: 992px) {
    .zen-split-grid { grid-template-columns: 1fr; }
  }

  /* 3D Tactile CTA Button */
  .btn-dominant-cta {
    display: inline-flex; align-items: center; justify-content: center; gap: 8px;
    background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
    color: #ffffff; border: none; border-radius: 14px; padding: 13px 26px;
    font-family: var(--zen-font-sans); font-size: 0.95rem; font-weight: 800;
    cursor: pointer; text-decoration: none;
    box-shadow: 0 4px 0 #c2410c, 0 10px 20px rgba(234, 88, 12, 0.35);
    transition: all 0.15s ease;
  }
  .btn-dominant-cta:hover {
    transform: translateY(-2px); box-shadow: 0 6px 0 #c2410c, 0 14px 24px rgba(234, 88, 12, 0.45);
  }
  .btn-dominant-cta:active {
    transform: translateY(2px); box-shadow: 0 2px 0 #c2410c, 0 6px 12px rgba(234, 88, 12, 0.25);
  }

  /* Tiles Grid (Dashboard) */
  .zen-tiles-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 24px;
  }
  @media (max-width: 768px) {
    .zen-tiles-grid { grid-template-columns: repeat(2, 1fr); }
  }
  .zen-tile {
    background: var(--zen-surface-card); border: 1px solid var(--zen-hairline);
    border-radius: 18px; padding: 18px; text-align: left;
  }
  .zen-tile-num {
    font-size: 1.65rem; font-weight: 800; letter-spacing: -0.02em; margin: 4px 0 2px;
  }
  .zen-tile-sub {
    font-size: 0.74rem; color: var(--zen-text-muted); font-weight: 500;
  }

  /* Matrix rows (Dashboard) */
  .zen-track-row {
    display: flex; align-items: center; justify-content: space-between; gap: 14px;
    padding: 12px 14px; border-radius: 12px; background: var(--zen-surface-subtle);
    border: 1px solid var(--zen-hairline-subtle); margin-bottom: 8px;
    transition: background 0.15s ease;
  }
  .zen-track-row:hover { background: var(--zen-surface-hover); }

  .m-sq-grid {
    display: flex; gap: 4px; align-items: center; flex-wrap: wrap;
  }
  .m-sq-dot {
    width: 14px; height: 14px; border-radius: 4px; background: var(--zen-hairline);
    transition: all 0.15s ease;
  }
  .m-sq-dot.done { background: var(--zen-emerald); box-shadow: 0 0 6px var(--zen-emerald-glow); }
  .m-sq-dot.partial { background: var(--zen-amber); }
</style>
</head>
<body>

<div class="zen-ambient-top"></div>
<div class="zen-ambient-bottom"></div>

<header class="zen-topbar">
  <a href="#" class="zen-brand">
    <div class="zen-brand-badge">⚡</div>
    <div>
      <div class="zen-brand-title">Python Backend Academy</div>
      <div class="zen-brand-sub">Эссенция главного экрана</div>
    </div>
  </a>

  <div style="display:flex;gap:10px;align-items:center;">
    <button type="button" class="zen-btn-toggle" onclick="toggleTheme()">🌓 Переключить тему</button>
  </div>
</header>

<main class="zen-layout">

  <!-- Nav switcher between Path and Dashboard -->
  <nav class="zen-tab-nav">
    <button class="zen-tab-btn active" onclick="switchTab('tab-path')">🗺️ Экран «Путь» (#/path)</button>
    <button class="zen-tab-btn" onclick="switchTab('tab-dashboard')">📊 Дашборд результатов (#/)</button>
  </nav>

  <!-- ==================== 1. ЭКРАН ПУТЬ (#/path) ==================== -->
  <section id="tab-path" class="tab-pane active">
    
    <div class="zen-split-grid">
      
      <!-- Main Column: Hero CTA + Chapters list -->
      <div>
        
        <!-- Hero Card (Coddy Dominant CTA) -->
        <div class="zen-card" style="border-left: 4px solid var(--zen-amber);">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap;margin-bottom:16px;">
            <div>
              <div class="zen-eyebrow" style="color:var(--zen-amber);">ПРОГРАММА › РАЗДЕЛ 1 · ГЛАВА 1</div>
              <h1 class="zen-title" style="font-size:1.5rem;margin-bottom:4px;">Юнит 1.1 · Базовые коллекции и срезы</h1>
              <div style="font-size:0.82rem;color:var(--zen-text-muted);">
                Глава 1: Python Core · 2/9 уроков сдано · 22%
              </div>
            </div>

            <a href="#/python/skill/1.1.1" class="btn-dominant-cta">
              ПРОДОЛЖИТЬ ➔
            </a>
          </div>

          <!-- Progress bar -->
          <div style="margin-top:14px;">
            <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:var(--zen-text-muted);margin-bottom:6px;">
              <span>Прогресс главы</span>
              <span style="font-weight:700;color:var(--zen-amber);">22%</span>
            </div>
            <div style="height:7px;border-radius:99px;background:var(--zen-hairline);overflow:hidden;">
              <div style="height:100%;width:22%;background:linear-gradient(90deg, var(--zen-amber), #ea580c);border-radius:99px;"></div>
            </div>
          </div>
        </div>

        <!-- Chapters List in Clean Style -->
        <div class="zen-card">
          <div class="zen-header">
            <div>
              <div class="zen-eyebrow">Структура курса</div>
              <div class="zen-title">7 Глав подготовки к Junior+</div>
            </div>
            <span class="dots-necklace">45 юнитов всего</span>
          </div>

          <!-- Chapter 1 Box -->
          <div class="zen-card-subtle" style="margin-bottom:12px;border-left:3px solid var(--zen-emerald);">
            <div style="display:flex;justify-content:space-between;align-items:center;cursor:pointer;">
              <div>
                <div style="font-weight:800;font-size:1.05rem;">Глава 1: Python Core</div>
                <div style="font-size:0.78rem;color:var(--zen-text-muted);">9 юнитов: Синтаксис, память, ООП, дескрипторы, асинхронность</div>
              </div>
              <span style="font-weight:700;color:var(--zen-emerald);font-size:0.88rem;">2 / 9 · 22%</span>
            </div>
          </div>

          <!-- Chapter 2 Box -->
          <div class="zen-card-subtle" style="margin-bottom:12px;opacity:0.9;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div>
                <div style="font-weight:700;font-size:1.02rem;">Глава 2: Сети и Web-протоколы</div>
                <div style="font-size:0.78rem;color:var(--zen-text-muted);">4 юнита: HTTP/2, REST, WebSockets, Аутентификация</div>
              </div>
              <span style="font-size:0.82rem;color:var(--zen-text-muted);">0 / 4 · 0%</span>
            </div>
          </div>

          <!-- Chapter 3 Box -->
          <div class="zen-card-subtle" style="margin-bottom:12px;opacity:0.85;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div>
                <div style="font-weight:700;font-size:1.02rem;">Глава 3: Серверные фреймворки (FastAPI & Django)</div>
                <div style="font-size:0.78rem;color:var(--zen-text-muted);">8 частей: Pydantic v2, DI, SQLAlchemy 2.0, DRF</div>
              </div>
              <span style="font-size:0.82rem;color:var(--zen-text-muted);">0 / 8 · 0%</span>
            </div>
          </div>

          <!-- Chapter 4 Box -->
          <div class="zen-card-subtle" style="opacity:0.8;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div>
                <div style="font-weight:700;font-size:1.02rem;">Глава 4: Алгоритмы и структуры данных</div>
                <div style="font-size:0.78rem;color:var(--zen-text-muted);">6 юнитов: Big O, Списки, Деревья, Графы, Сортировки</div>
              </div>
              <span style="font-size:0.82rem;color:var(--zen-text-muted);">0 / 6 · 0%</span>
            </div>
          </div>

        </div>

      </div>

      <!-- Right Rail (Coddy Radar) -->
      <div>
        
        <!-- Rail Card 1: Readiness Echelon 1 -->
        <div class="zen-card-subtle" style="margin-bottom:16px;">
          <div class="zen-eyebrow" style="color:var(--zen-bordeaux);">🎯 До 1-го скрининга</div>
          <div style="display:flex;justify-content:space-between;align-items:baseline;margin:8px 0 6px;">
            <span style="font-size:1.8rem;font-weight:900;color:var(--zen-emerald);">35%</span>
            <span style="font-size:0.75rem;color:var(--zen-text-muted);">Осталось 9 тем</span>
          </div>
          <div style="height:6px;border-radius:99px;background:var(--zen-hairline);overflow:hidden;margin-bottom:10px;">
            <div style="height:100%;width:35%;background:linear-gradient(90deg, var(--zen-bordeaux), var(--zen-emerald));border-radius:99px;"></div>
          </div>
          <a href="#/mock" style="font-size:0.78rem;color:var(--zen-emerald);text-decoration:none;font-weight:600;">Симулятор собеседования →</a>
        </div>

        <!-- Rail Card 2: Radar Themes -->
        <div class="zen-card-subtle" style="margin-bottom:16px;">
          <div class="zen-eyebrow">🎯 Радар скрининга</div>
          <div style="font-size:0.78rem;color:var(--zen-text-muted);margin-bottom:12px;">14 ключевых тем тех-фильтра</div>

          <div style="display:flex;flex-direction:column;gap:10px;">
            <div>
              <div style="display:flex;justify-content:space-between;font-size:0.78rem;margin-bottom:4px;">
                <span>Сложность O(n) & срезы</span>
                <span style="font-weight:700;color:var(--zen-emerald);">85%</span>
              </div>
              <div style="height:4px;border-radius:99px;background:var(--zen-hairline);overflow:hidden;">
                <div style="height:100%;width:85%;background:var(--zen-emerald);border-radius:99px;"></div>
              </div>
            </div>

            <div>
              <div style="display:flex;justify-content:space-between;font-size:0.78rem;margin-bottom:4px;">
                <span>Хеш-таблицы dict/set</span>
                <span style="font-weight:700;color:var(--zen-amber);">40%</span>
              </div>
              <div style="height:4px;border-radius:99px;background:var(--zen-hairline);overflow:hidden;">
                <div style="height:100%;width:40%;background:var(--zen-amber);border-radius:99px;"></div>
              </div>
            </div>

            <div>
              <div style="display:flex;justify-content:space-between;font-size:0.78rem;margin-bottom:4px;">
                <span>SQL JOIN & индексы B-Tree</span>
                <span style="font-weight:600;color:var(--zen-text-dim);">0%</span>
              </div>
              <div style="height:4px;border-radius:99px;background:var(--zen-hairline);overflow:hidden;">
                <div style="height:100%;width:0%;background:var(--zen-text-dim);border-radius:99px;"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Rail Card 3: SRS Flashcards Queue -->
        <div class="zen-card-subtle">
          <div class="zen-eyebrow">🧠 Очередь повторения SRS</div>
          <div style="font-size:0.82rem;font-weight:700;margin:6px 0 4px;">12 карточек на сегодня</div>
          <p style="font-size:0.76rem;color:var(--zen-text-muted);line-height:1.45;margin-bottom:10px;">
            Интервальное повторение ключевых определений: GIL, MRO, Дескрипторы.
          </p>
          <a href="#/cards" style="font-size:0.78rem;color:var(--zen-emerald);text-decoration:none;font-weight:600;">Перейти в колоду →</a>
        </div>

      </div>

    </div>

  </section>

  <!-- ==================== 2. ДАШБОРД РЕЗУЛЬТАТОВ (#/) ==================== -->
  <section id="tab-dashboard" class="tab-pane">

    <!-- 4 Stats Tiles -->
    <div class="zen-tiles-grid">
      <div class="zen-tile">
        <div class="zen-eyebrow" style="color:var(--zen-emerald);">💎 Опыт всего</div>
        <div class="zen-tile-num" style="color:var(--zen-emerald);">520</div>
        <div class="zen-tile-sub">⚡ +55 XP заработано за сегодня</div>
      </div>

      <div class="zen-tile">
        <div class="zen-eyebrow" style="color:var(--zen-amber);">💻 Задачи IDE</div>
        <div class="zen-tile-num" style="color:var(--zen-amber);">18 <span style="font-size:1rem;color:var(--zen-text-muted);font-weight:500;">/ 401</span></div>
        <div class="zen-tile-sub">Браузерная среда Brython 3.13</div>
      </div>

      <div class="zen-tile">
        <div class="zen-eyebrow" style="color:var(--zen-bordeaux);">🧠 Навыков 👑</div>
        <div class="zen-tile-num" style="color:var(--zen-bordeaux);">14 <span style="font-size:1rem;color:var(--zen-text-muted);font-weight:500;">/ 126</span></div>
        <div class="zen-tile-sub">Подтвержденное Mastery Learning</div>
      </div>

      <div class="zen-tile">
        <div class="zen-eyebrow">🏆 Юнитов сдано</div>
        <div class="zen-tile-num">3 <span style="font-size:1rem;color:var(--zen-text-muted);font-weight:500;">/ 45</span></div>
        <div class="zen-tile-sub">Рубежные Unit Tests 100% PASS</div>
      </div>
    </div>

    <!-- Skill Matrix across 7 Tracks -->
    <div class="zen-card">
      <div class="zen-header">
        <div>
          <div class="zen-eyebrow">Матрица компетенций платформы</div>
          <div class="zen-title">126 Инженерных навыков по 7 модулям</div>
        </div>
        <span class="dots-necklace">Mastery ≥ 80%</span>
      </div>

      <!-- Track 1: Python -->
      <div class="zen-track-row">
        <div style="min-width:180px;">
          <div style="font-weight:800;font-size:0.95rem;">🐍 Python Core</div>
          <div style="font-size:0.75rem;color:var(--zen-text-muted);">28 навыков · 2800 MP</div>
        </div>
        <div class="m-sq-grid">
          <div class="m-sq-dot done"></div><div class="m-sq-dot done"></div><div class="m-sq-dot done"></div>
          <div class="m-sq-dot partial"></div><div class="m-sq-dot"></div><div class="m-sq-dot"></div>
          <div class="m-sq-dot"></div><div class="m-sq-dot"></div><div class="m-sq-dot"></div>
          <div class="m-sq-dot"></div><div class="m-sq-dot"></div><div class="m-sq-dot"></div>
        </div>
        <div style="font-weight:700;color:var(--zen-emerald);font-size:0.85rem;min-width:60px;text-align:right;">
          24%
        </div>
      </div>

      <!-- Track 2: Web -->
      <div class="zen-track-row">
        <div style="min-width:180px;">
          <div style="font-weight:800;font-size:0.95rem;">🌐 Web-протоколы</div>
          <div style="font-size:0.75rem;color:var(--zen-text-muted);">10 навыков · 1000 MP</div>
        </div>
        <div class="m-sq-grid">
          <div class="m-sq-dot done"></div><div class="m-sq-dot"></div><div class="m-sq-dot"></div>
          <div class="m-sq-dot"></div><div class="m-sq-dot"></div><div class="m-sq-dot"></div>
        </div>
        <div style="font-weight:700;color:var(--zen-text-muted);font-size:0.85rem;min-width:60px;text-align:right;">
          10%
        </div>
      </div>

      <!-- Track 3: Backend -->
      <div class="zen-track-row">
        <div style="min-width:180px;">
          <div style="font-weight:800;font-size:0.95rem;">⚙️ Backend Core</div>
          <div style="font-size:0.75rem;color:var(--zen-text-muted);">24 навыка · 2400 MP</div>
        </div>
        <div class="m-sq-grid">
          <div class="m-sq-dot"></div><div class="m-sq-dot"></div><div class="m-sq-dot"></div>
          <div class="m-sq-dot"></div><div class="m-sq-dot"></div><div class="m-sq-dot"></div>
        </div>
        <div style="font-weight:700;color:var(--zen-text-muted);font-size:0.85rem;min-width:60px;text-align:right;">
          0%
        </div>
      </div>

      <!-- Track 4: Algorithms -->
      <div class="zen-track-row">
        <div style="min-width:180px;">
          <div style="font-weight:800;font-size:0.95rem;">⚡ Алгоритмы</div>
          <div style="font-size:0.75rem;color:var(--zen-text-muted);">12 навыков · 1200 MP</div>
        </div>
        <div class="m-sq-grid">
          <div class="m-sq-dot"></div><div class="m-sq-dot"></div><div class="m-sq-dot"></div>
          <div class="m-sq-dot"></div><div class="m-sq-dot"></div><div class="m-sq-dot"></div>
        </div>
        <div style="font-weight:700;color:var(--zen-text-muted);font-size:0.85rem;min-width:60px;text-align:right;">
          0%
        </div>
      </div>

    </div>

  </section>

</main>

<script>
  function switchTab(tabId) {
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.zen-tab-btn').forEach(el => el.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
  }

  function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    html.setAttribute('data-theme', current === 'dark' ? 'light' : 'dark');
  }
</script>

</body>
</html>
"""

with open(proto_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Created prototype: {proto_path} ({len(html_content)} bytes)")
