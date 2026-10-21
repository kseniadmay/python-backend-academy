import os
import re

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_path = os.path.join(root, 'academy.html')

with open(academy_path, 'r', encoding='utf-8') as f:
    content = f.read()

print('Original academy.html size:', len(content))

# ---------------------------------------------------------------------------
# 1. CSS styles for Echelon Selector, Quick Tabs, Modal & Bottom Sheet
# ---------------------------------------------------------------------------
target_css_anchor = """.path-echelon-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    font-size: 0.72rem;
    font-weight: 800;
    border-radius: 999px;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    white-space: nowrap;
    flex-shrink: 0;
  }"""

new_css = """.path-echelon-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    font-size: 0.72rem;
    font-weight: 800;
    border-radius: 999px;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .path-echelon-pill-btn {
    border: none;
    font: inherit;
    cursor: pointer;
    transition: all 0.18s ease;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
  }
  .path-echelon-pill-btn:hover {
    filter: brightness(1.15);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
  }
  .path-echelon-pill-btn:active {
    transform: translateY(1px);
    filter: brightness(0.95);
  }
  .path-echelon-pill-btn:focus-visible {
    outline: 2px solid var(--amber, #f59e0b);
    outline-offset: 2px;
  }
  .pep-chevron {
    font-size: 0.65rem;
    margin-left: 2px;
    opacity: 0.8;
    transition: transform 0.2s ease;
  }
  .path-echelon-pill-btn:hover .pep-chevron {
    opacity: 1;
    transform: translateY(1px);
  }

  /* Desktop / Tablet Quick-switch Tabs for Echelons */
  .path-echelon-quick-tabs {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
    margin-bottom: 12px;
    padding: 4px;
    border-radius: 14px;
    background: rgba(22, 27, 36, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }
  html:not([data-theme="dark"]) .path-echelon-quick-tabs {
    background: rgba(241, 245, 249, 0.88);
    border: 1px solid rgba(0, 0, 0, 0.06);
  }
  .path-eq-tab {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 11px;
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--ink-muted, #94a3b8);
    background: transparent;
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.18s ease;
    white-space: nowrap;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
  }
  .path-eq-tab:hover {
    color: var(--ink, #f8fafc);
    background: rgba(255, 255, 255, 0.06);
  }
  html:not([data-theme="dark"]) .path-eq-tab:hover {
    color: #0f172a;
    background: rgba(0, 0, 0, 0.05);
  }
  .path-eq-tab.active {
    color: #f8fafc;
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.18);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
  }
  html:not([data-theme="dark"]) .path-eq-tab.active {
    color: #0f172a;
    background: #ffffff;
    border-color: rgba(0, 0, 0, 0.12);
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
  }
  .path-eq-tab.active.path-eq-tab--t1 { border-color: rgba(244, 63, 94, 0.45); color: #fecdd3; }
  .path-eq-tab.active.path-eq-tab--t2 { border-color: rgba(245, 158, 11, 0.45); color: #fde68a; }
  .path-eq-tab.active.path-eq-tab--t3 { border-color: rgba(59, 130, 246, 0.45); color: #bfdbfe; }
  .path-eq-tab.active.path-eq-tab--t4 { border-color: rgba(168, 85, 247, 0.45); color: #e9d5ff; }
  @media (max-width: 640px) {
    .path-echelon-quick-tabs {
      display: none; /* On smartphones, selection is accessed via the header echelon pill */
    }
  }

  /* Echelon / Program Selector Modal & Bottom Sheet (Zen Glassmorphism) */
  .path-echelon-modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    z-index: 100010;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.24s ease;
  }
  .path-echelon-modal-backdrop.is-open {
    opacity: 1;
    pointer-events: auto;
  }
  .path-echelon-modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0.96);
    width: 92%;
    max-width: 580px;
    max-height: 85vh;
    overflow-y: auto;
    background: rgba(18, 23, 32, 0.96);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 24px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.75);
    z-index: 100011;
    padding: 24px 26px;
    opacity: 0;
    pointer-events: none;
    transition: all 0.24s cubic-bezier(0.16, 1, 0.3, 1);
  }
  html:not([data-theme="dark"]) .path-echelon-modal {
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(0, 0, 0, 0.12);
    box-shadow: 0 24px 60px rgba(15, 23, 42, 0.2);
  }
  .path-echelon-modal.is-open {
    opacity: 1;
    pointer-events: auto;
    transform: translate(-50%, -50%) scale(1);
  }
  @media (max-width: 640px) {
    .path-echelon-modal {
      top: auto;
      bottom: 0;
      left: 0;
      right: 0;
      transform: translateY(100%);
      width: 100%;
      max-width: 100%;
      border-radius: 24px 24px 0 0;
      padding: 18px 18px calc(24px + env(safe-area-inset-bottom, 16px));
      max-height: 88vh;
      border-bottom: none;
    }
    .path-echelon-modal.is-open {
      transform: translateY(0);
    }
  }
  .path-echelon-modal-handle {
    display: none;
    width: 38px;
    height: 4px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.22);
    margin: 0 auto 12px;
  }
  @media (max-width: 640px) {
    .path-echelon-modal-handle { display: block; }
  }
  .path-echelon-modal-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 16px;
  }
  .path-echelon-modal-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #f8fafc;
    margin: 0 0 4px;
    letter-spacing: -0.01em;
  }
  html:not([data-theme="dark"]) .path-echelon-modal-title { color: #0f172a; }
  .path-echelon-modal-sub {
    font-size: 0.8rem;
    color: var(--ink-muted, #94a3b8);
    margin: 0;
    line-height: 1.4;
  }
  .path-echelon-modal-close {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: var(--ink-muted, #94a3b8);
    cursor: pointer;
    font-size: 0.95rem;
    transition: all 0.16s ease;
    flex-shrink: 0;
  }
  .path-echelon-modal-close:hover {
    background: rgba(255, 255, 255, 0.12);
    color: #f8fafc;
  }
  .path-echelon-cards-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .echelon-prog-card {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 14px 16px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.03);
    border: 1.5px solid rgba(255, 255, 255, 0.08);
    cursor: pointer;
    transition: all 0.18s ease;
    text-align: left;
    position: relative;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
  }
  html:not([data-theme="dark"]) .echelon-prog-card {
    background: rgba(248, 250, 252, 0.92);
    border-color: rgba(0, 0, 0, 0.08);
  }
  .echelon-prog-card:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.22);
    transform: translateY(-1px);
  }
  html:not([data-theme="dark"]) .echelon-prog-card:hover {
    background: #ffffff;
    border-color: rgba(0, 0, 0, 0.16);
  }
  .echelon-prog-card.is-active {
    background: rgba(255, 255, 255, 0.07);
    border-color: rgba(52, 211, 153, 0.65);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
  }
  html:not([data-theme="dark"]) .echelon-prog-card.is-active {
    background: #ffffff;
    border-color: rgba(16, 185, 129, 0.6);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.12);
  }
  .echelon-prog-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
  }
  .echelon-prog-card-title-wrap {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 0;
  }
  .echelon-prog-card-icon {
    font-size: 1.25rem;
    line-height: 1;
    flex-shrink: 0;
  }
  .echelon-prog-card-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.01em;
  }
  html:not([data-theme="dark"]) .echelon-prog-card-title { color: #0f172a; }
  .echelon-prog-card-badge {
    font-size: 0.72rem;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 999px;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .echelon-prog-card-desc {
    font-size: 0.78rem;
    line-height: 1.42;
    color: var(--ink-soft, #cbd5e1);
  }
  html:not([data-theme="dark"]) .echelon-prog-card-desc { color: #475569; }
  .echelon-prog-card-meta-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-top: 2px;
  }
  .echelon-prog-card-stats {
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--ink-muted, #94a3b8);
  }
  .echelon-prog-card-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 10px;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    cursor: pointer;
    border: none;
    transition: all 0.16s ease;
  }
  .echelon-prog-card-btn--active {
    background: rgba(52, 211, 153, 0.2);
    color: #6ee7b7;
    border: 1px solid rgba(52, 211, 153, 0.4);
    pointer-events: none;
  }
  .echelon-prog-card-btn--select {
    background: linear-gradient(180deg, #fbbf24, #d97706);
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.35);
  }
  .echelon-prog-card-btn--select:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
  }"""

assert target_css_anchor in content, 'target_css_anchor not found'
content = content.replace(target_css_anchor, new_css, 1)
print('1. CSS for Echelon Selector & Modal injected successfully!')

# ---------------------------------------------------------------------------
# 1b. Add responsive pcl-short and pcl-full to CSS for Bug 142
# ---------------------------------------------------------------------------
target_crumbs_css = """.path-echelon-pill .pep-short,
  .path-screening-badge .psb-short {"""

new_crumbs_css = """.path-echelon-pill .pep-short,
  .path-screening-badge .psb-short,
  .path-chapter-crumb-label .pcl-short {
    display: none;
  }
  @media (max-width: 768px) {
    .path-chapter-crumb-label .pcl-full { display: none !important; }
    .path-chapter-crumb-label .pcl-short { display: inline !important; }
  }
  .path-echelon-pill .pep-short,
  .path-screening-badge .psb-short {"""

assert target_crumbs_css in content, 'target_crumbs_css not found'
content = content.replace(target_crumbs_css, new_crumbs_css, 1)
print('1b. Responsive .path-chapter-crumb-label .pcl-short injected!')

assert target_css_anchor in content, 'target_css_anchor not found'
content = content.replace(target_css_anchor, new_css, 1)
print('1. CSS for Echelon Selector & Modal injected successfully!')

# ---------------------------------------------------------------------------
# 2. ensureExtendedState: initialize state.selectedEchelon
# ---------------------------------------------------------------------------
target_state_anchor = "if(!s.pathViewMode || !['game','pro'].includes(s.pathViewMode)) s.pathViewMode = 'game';"
new_state_anchor = """if(!s.pathViewMode || !['game','pro'].includes(s.pathViewMode)) s.pathViewMode = 'game';
  if(s.selectedEchelon !== 'all' && (typeof s.selectedEchelon !== 'number' || s.selectedEchelon < 1 || s.selectedEchelon > 4)) s.selectedEchelon = 1;"""

assert target_state_anchor in content, 'target_state_anchor not found'
content = content.replace(target_state_anchor, new_state_anchor, 1)
print('2. state.selectedEchelon initialized in ensureExtendedState!')

# ---------------------------------------------------------------------------
# 3. Helpers: getEchelonUnitsAndChapters & renderEchelonCardsModalHTML
# ---------------------------------------------------------------------------
helpers_code = """
function getEchelonUnitsAndChapters(echelonTier, allUnits){
  const sourceUnits = allUnits || ALL_UNITS_COMBINED;
  let units = [];
  if(echelonTier === 'all'){
    units = sourceUnits.slice();
  } else {
    const t = Number(echelonTier) || 1;
    units = sourceUnits.filter(u => getEffectiveUnitTier(u.id) === t);
  }
  if(!units.length) units = sourceUnits.slice();

  const chaptersMeta = [
    { num: 1, title: 'Python Core', track: 'python', shortTitle: 'Python Core' },
    { num: 2, title: 'Web & HTTP', track: 'web', shortTitle: 'Web & HTTP' },
    { num: 3, title: 'Backend & Архитектура', track: 'backend', shortTitle: 'Backend & Архитектура' },
    { num: 4, title: 'Алгоритмы и структуры данных', track: 'algorithms', shortTitle: 'Алгоритмы и структуры' },
    { num: 5, title: 'Базы данных и SQL', track: 'databases', shortTitle: 'Базы данных и SQL' },
    { num: 6, title: 'Системный дизайн', track: 'architecture', shortTitle: 'Системный дизайн' },
    { num: 7, title: 'Инфраструктура и DevOps', track: 'infra', shortTitle: 'Инфраструктура и DevOps' }
  ];

  const chapters = [];
  let currentChapter = null;
  units.forEach((u, idx) => {
    const tr = getTrackForUnit(u.id);
    const meta = chaptersMeta.find(c => c.track === tr.routePrefix) || { num: 1, title: tr.title, track: tr.routePrefix, shortTitle: tr.title };
    if(!currentChapter || currentChapter.track !== meta.track){
      currentChapter = {
        startIdx: idx,
        num: meta.num,
        chapterNum: meta.num,
        title: `Глава ${meta.num}: ${meta.title}`,
        shortTitle: meta.shortTitle,
        track: meta.track,
        unitsCount: 0,
        units: []
      };
      chapters.push(currentChapter);
    }
    currentChapter.units.push(u);
  });
  chapters.forEach(c => {
    c.unitsCount = c.units.length;
  });
  return { units, chapters };
}
window.getEchelonUnitsAndChapters = getEchelonUnitsAndChapters;

function renderEchelonCardsModalHTML(curEchelon){
  const curTier = (curEchelon === 'all') ? 'all' : (Number(curEchelon) || 1);
  const tiers = [1, 2, 3, 4];
  const cards = tiers.map(t => {
    const em = INTERVIEW_ECHELONS[t] || INTERVIEW_ECHELONS[1];
    const prog = (typeof getEchelonProgress === 'function') ? getEchelonProgress(t) : { units: [], skills: [], pct: 0 };
    const tUnits = prog.units || [];
    const tCompletedUnits = tUnits.filter(isUnitCompleted).length;
    const tTotalUnits = tUnits.length;
    const tPct = prog.pct || 0;
    const isActive = (curTier === t);

    return `
      <div class="echelon-prog-card ${isActive ? 'is-active' : ''}" data-select-echelon="${t}" role="button" tabindex="0" aria-label="${escapeHtmlStr(em.label)}. ${tCompletedUnits} из ${tTotalUnits} уроков сдано.">
        <div class="echelon-prog-card-top">
          <div class="echelon-prog-card-title-wrap">
            <span class="echelon-prog-card-icon">${em.icon}</span>
            <span class="echelon-prog-card-title">${escapeHtmlStr(em.label.split(':')[0])} · ${escapeHtmlStr(em.focus)}</span>
          </div>
          <span class="echelon-prog-card-badge ${em.badgeClass}">${tPct}%</span>
        </div>
        <div class="echelon-prog-card-desc">${escapeHtmlStr(em.desc)}</div>
        <div class="cd-bar cd-bar-track" style="height:5px;margin:2px 0;"><div class="cd-fill cd-bar-fill" style="width:${Math.max(5, tPct)}%;background:${em.gradient || em.color};"></div></div>
        <div class="echelon-prog-card-meta-row">
          <span class="echelon-prog-card-stats">${tCompletedUnits} из ${tTotalUnits} ${pluralizeRu(tTotalUnits, 'урока', 'уроков', 'уроков')} сдано</span>
          ${isActive
            ? '<span class="echelon-prog-card-btn echelon-prog-card-btn--active">ТЕКУЩАЯ ПРОГРАММА ✓</span>'
            : `<button type="button" class="echelon-prog-card-btn echelon-prog-card-btn--select" data-select-echelon="${t}">ВЫБРАТЬ ПРОГРАММУ ➔</button>`}
        </div>
      </div>
    `;
  }).join('');

  const isAllActive = (curTier === 'all');
  const allUnitsTotal = ALL_UNITS_COMBINED.length;
  const allUnitsDone = ALL_UNITS_COMBINED.filter(isUnitCompleted).length;
  const allPct = Math.round(allUnitsDone / allUnitsTotal * 100);

  const allCard = `
    <div class="echelon-prog-card ${isAllActive ? 'is-active' : ''}" data-select-echelon="all" role="button" tabindex="0" style="margin-top:4px;" aria-label="Сквозной курс, все 45 уроков.">
      <div class="echelon-prog-card-top">
        <div class="echelon-prog-card-title-wrap">
          <span class="echelon-prog-card-icon">🌐</span>
          <span class="echelon-prog-card-title">Сквозной курс · Все 7 глав программы</span>
        </div>
        <span class="echelon-prog-card-badge" style="background:rgba(255,255,255,0.08);color:#f8fafc;">${allPct}%</span>
      </div>
      <div class="echelon-prog-card-desc">Единый непрерывный маршрут через все 45 уроков от синтаксиса Python до системного дизайна и DevOps.</div>
      <div class="cd-bar cd-bar-track" style="height:5px;margin:2px 0;"><div class="cd-fill cd-bar-fill" style="width:${Math.max(5, allPct)}%;"></div></div>
      <div class="echelon-prog-card-meta-row">
        <span class="echelon-prog-card-stats">${allUnitsDone} из ${allUnitsTotal} уроков сдано</span>
        ${isAllActive
          ? '<span class="echelon-prog-card-btn echelon-prog-card-btn--active">ТЕКУЩИЙ МАРШРУТ ✓</span>'
          : '<button type="button" class="echelon-prog-card-btn echelon-prog-card-btn--select" data-select-echelon="all">ВЫБРАТЬ ВСЕ ➔</button>'}
      </div>
    </div>
  `;

  return cards + allCard;
}
window.renderEchelonCardsModalHTML = renderEchelonCardsModalHTML;
"""

target_helpers_anchor = "function isUnitCompleted(u){"
assert target_helpers_anchor in content, 'target_helpers_anchor not found'
content = content.replace(target_helpers_anchor, helpers_code + "\n" + target_helpers_anchor, 1)
print('3. Helpers getEchelonUnitsAndChapters & renderEchelonCardsModalHTML injected!')

# ---------------------------------------------------------------------------
# 4. Update renderPathMobileStatsHTML to include echelon switch trigger
# ---------------------------------------------------------------------------
target_pms = """function renderPathMobileStatsHTML(totalCompletedUnits, streakText, curTier, activeChapterNum, chapterCompleted, chapterTotal){
  const chNum = activeChapterNum || 1;
  const chDone = (typeof chapterCompleted === 'number') ? chapterCompleted : 0;
  const chTot = (typeof chapterTotal === 'number') ? chapterTotal : 9;
  const tierNum = curTier || 1;
  return `
    <div class="path-mobile-stats" role="status" aria-label="Статистика обучения">
      <span class="pms-item pms-echelon" title="Текущий эшелон подготовки">${(typeof INTERVIEW_ECHELONS !== 'undefined' && INTERVIEW_ECHELONS[tierNum] && INTERVIEW_ECHELONS[tierNum].icon) || '🛡️'} <b>Эшелон ${tierNum}</b></span>
      <span class="pms-item" title="Пройдено в главе ${chNum}">📘 <b>Гл. ${chNum}: ${chDone}/${chTot}</b></span>
      <span class="pms-item" title="Стрик активности">🔥 <b>${state.streak || 0}</b> ${streakText}</span>
      <span class="pms-item" title="Накопленный опыт">⚡ <b>${state.xp || 0} XP</b></span>
    </div>`;
}"""

new_pms = """function renderPathMobileStatsHTML(totalCompletedUnits, streakText, curTier, activeChapterNum, chapterCompleted, chapterTotal){
  const chNum = activeChapterNum || 1;
  const chDone = (typeof chapterCompleted === 'number') ? chapterCompleted : 0;
  const chTot = (typeof chapterTotal === 'number') ? chapterTotal : 9;
  const tierNum = (curTier === 'all') ? 1 : (Number(curTier) || 1);
  const tierIcon = (typeof INTERVIEW_ECHELONS !== 'undefined' && INTERVIEW_ECHELONS[tierNum] && INTERVIEW_ECHELONS[tierNum].icon) || '🛡️';
  const tierLabel = (curTier === 'all') ? 'Все' : tierNum;
  return `
    <div class="path-mobile-stats" role="status" aria-label="Статистика обучения">
      <span class="pms-item pms-echelon" data-open-echelon-modal="1" role="button" tabindex="0" title="Нажмите, чтобы сменить программу / эшелон">${tierIcon} <b>Эшелон ${tierLabel}</b> <span style="font-size:0.68rem;opacity:0.8;">▾</span></span>
      <span class="pms-item" title="Пройдено в главе ${chNum}">📘 <b>Гл. ${chNum}: ${chDone}/${chTot}</b></span>
      <span class="pms-item" title="Стрик активности">🔥 <b>${state.streak || 0}</b> ${streakText}</span>
      <span class="pms-item" title="Накопленный опыт">⚡ <b>${state.xp || 0} XP</b></span>
    </div>`;
}"""

assert target_pms in content, 'target_pms not found'
content = content.replace(target_pms, new_pms, 1)
print('4. renderPathMobileStatsHTML updated!')

# ---------------------------------------------------------------------------
# 5. Update renderCoddyRightRail to dynamically reflect curEchelon
# ---------------------------------------------------------------------------
target_rail = """function renderCoddyRightRail(totalCompletedUnits, streakText, activeChapterNum){"""
new_rail = """function renderCoddyRightRail(totalCompletedUnits, streakText, activeChapterNum, selectedEchelonOverride){
  const curEchNum = (selectedEchelonOverride !== undefined) ? selectedEchelonOverride : ((state && state.selectedEchelon) || 1);"""

assert target_rail in content, 'target_rail not found'
content = content.replace(target_rail, new_rail, 1)

# Inside renderCoddyRightRail, make Widget 1 dynamic to the selected echelon
target_rail_w1 = """      <!-- Widget 1: Screening Readiness — мотивирующая графа «До 1-го скрининга %» (по ТЗ) -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-card-head">
          <div class="coddy-rail-badge">🎯 До 1-го скрининга</div>
          <a href="#/mock" class="coddy-rail-link">Симулятор</a>
        </div>
        <div class="coddy-rail-meter">
          ${e1Pct > 0
            ? `<span class="coddy-rail-meter-value">${e1Pct}%</span><span class="meta">готовности к тех-скринингу</span>`
            : `<span class="coddy-rail-meter-value" style="font-size:1.35rem;color:var(--amber,#fbbf24);">СТАРТ</span><span class="meta">базовый тех-скрининг</span>`}
        </div>
        <div class="cd-bar cd-bar-track" role="progressbar" aria-label="Готовность к техническому скринингу" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${e1Pct}"><div class="cd-fill cd-bar-fill" style="width:${Math.max(8, e1Pct)}%;"></div></div>
        <div class="meta" style="font-size:.75rem;margin-top:7px;">${e1Pct > 0 ? `⏳ Освоено ${e1 ? e1.skills.filter(s => getSkillMP(s.id) >= 80).length : 0} из ${e1 ? e1.skills.length : 32} навыков Эшелона 1` : `• Фундамент тех-скрининга · Глава ${activeChapterNum}`}</div>
      </div>"""

new_rail_w1 = """      <!-- Widget 1: Screening Readiness — мотивирующая графа с динамическим эшелоном -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-card-head">
          <div class="coddy-rail-badge" data-open-echelon-modal="1" role="button" tabindex="0" style="cursor:pointer;" title="Нажмите, чтобы сменить эшелон">${(typeof INTERVIEW_ECHELONS !== 'undefined' && INTERVIEW_ECHELONS[curEchNum] && INTERVIEW_ECHELONS[curEchNum].icon) || '🎯'} До ${(typeof INTERVIEW_ECHELONS !== 'undefined' && INTERVIEW_ECHELONS[curEchNum] && INTERVIEW_ECHELONS[curEchNum].targetLabel) || 'скрининга'} ▾</div>
          <a href="#/mock" class="coddy-rail-link">Симулятор</a>
        </div>
        <div class="coddy-rail-meter">
          ${e1Pct > 0
            ? `<span class="coddy-rail-meter-value">${e1Pct}%</span><span class="meta">готовности к тех-скринингу</span>`
            : `<span class="coddy-rail-meter-value" style="font-size:1.35rem;color:var(--amber,#fbbf24);">СТАРТ</span><span class="meta">базовый тех-скрининг</span>`}
        </div>
        <div class="cd-bar cd-bar-track" role="progressbar" aria-label="Готовность к техническому скринингу" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${e1Pct}"><div class="cd-fill cd-bar-fill" style="width:${Math.max(8, e1Pct)}%;"></div></div>
        <div class="meta" style="font-size:.75rem;margin-top:7px;">${e1Pct > 0 ? `⏳ Освоено ${e1 ? e1.skills.filter(s => getSkillMP(s.id) >= 80).length : 0} из ${e1 ? e1.skills.length : 32} навыков Эшелона 1` : `• Фундамент тех-скрининга · Глава ${activeChapterNum}`}</div>
      </div>"""

assert target_rail_w1 in content, 'target_rail_w1 not found'
content = content.replace(target_rail_w1, new_rail_w1, 1)

target_rail_w3 = """          ${totalCompletedUnits === 0
            ? 'Очередь повторения пуста. Освойте первый урок, чтобы активировать карточки интервального повторения к скринингу.'
            : 'Интервальное повторение ключевых определений перед собеседованием: <span style="color:#f8fafc;font-weight:600;">Синтаксис, структуры данных</span>.'}"""

new_rail_w3 = """          ${totalCompletedUnits === 0
            ? 'Очередь пуста. Пройдите первый урок, чтобы открыть карточки к скринингу.'
            : 'Интервальное повторение ключевых определений перед собеседованием: <span style="color:#f8fafc;font-weight:600;">Синтаксис, структуры данных</span>.'}"""

assert target_rail_w3 in content, 'target_rail_w3 not found'
content = content.replace(target_rail_w3, new_rail_w3, 1)
print('5. renderCoddyRightRail updated!')

# ---------------------------------------------------------------------------
# 6. Rewrite viewPathSerpentine to filter by selected echelon & render program switcher
# ---------------------------------------------------------------------------
# We find viewPathSerpentine and replace it with the echelon-driven version.
serpentine_start = content.find('function viewPathSerpentine(options){')
serpentine_end = content.find('let proCollapsedChapters = new Set();')
assert serpentine_start != -1 and serpentine_end != -1, 'viewPathSerpentine bounds not found'

new_viewPathSerpentine = """function viewPathSerpentine(options){
  options = options || {};
  ensureExtendedState();
  const curEchelon = (options.echelon !== undefined) ? options.echelon : ((state && state.selectedEchelon) || 1);
  const { units: allUnits, chapters: chapterBreakpoints } = getEchelonUnitsAndChapters(curEchelon, ALL_UNITS_COMBINED);
  const usePawNodes = state.pathNodeStyle !== 'button';
  
  // Find which units are completed vs active vs locked
  let activeUnitIndex = -1;
  allUnits.forEach((u, idx) => {
    const isUnitTestPassed = (state.passedUnitTests || []).includes(u.id);
    const allSkillsMastered = (u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80);
    const isCompleted = isUnitTestPassed || allSkillsMastered;
    if(!isCompleted && activeUnitIndex === -1){
      activeUnitIndex = idx;
    }
  });
  if(activeUnitIndex === -1) activeUnitIndex = Math.max(0, allUnits.length - 1);

  // Track coordinates for each node in this echelon
  const chapterStartSet = new Set(chapterBreakpoints.slice(1).map(cb => cb.startIdx));
  let curY = 90;
  const coords = allUnits.map((u, i) => {
    if(i > 0){
      curY += 115;
      if(chapterStartSet.has(i)){
        curY += 240; // Dedicated gap (+240px) for Mastery Challenge branch and Chapter Gate Card
      }
    }
    const x = Math.round(210 + 110 * Math.sin((i * Math.PI) / 2.2));
    return { x, y: curY };
  });

  const totalH = coords.length ? (coords[coords.length - 1].y + 120) : 400;

  // Build smooth Bezier path
  let dPath = coords.length ? `M ${coords[0].x} ${coords[0].y}` : '';
  for(let i = 0; i < coords.length - 1; i++){
    const p1 = coords[i];
    const p2 = coords[i+1];
    const midY = (p1.y + p2.y) / 2;
    dPath += ` C ${p1.x} ${midY}, ${p2.x} ${midY}, ${p2.x} ${p2.y}`;
  }

  // Build progress sub-path up to active unit
  let dProgress = '';
  if(activeUnitIndex > 0 && coords.length > 0){
    dProgress = `M ${coords[0].x} ${coords[0].y}`;
    for(let i = 0; i < Math.min(activeUnitIndex, coords.length - 1); i++){
      const p1 = coords[i];
      const p2 = coords[i+1];
      const midY = (p1.y + p2.y) / 2;
      dProgress += ` C ${p1.x} ${midY}, ${p2.x} ${midY}, ${p2.x} ${p2.y}`;
    }
  }

  // Dotted "path ahead" overlay from active unit to end
  let dFuture = '';
  if(activeUnitIndex < coords.length - 1 && coords.length > 0){
    dFuture = `M ${coords[activeUnitIndex].x} ${coords[activeUnitIndex].y}`;
    for(let i = activeUnitIndex; i < coords.length - 1; i++){
      const p1 = coords[i];
      const p2 = coords[i+1];
      const midY = (p1.y + p2.y) / 2;
      dFuture += ` C ${p1.x} ${midY}, ${p2.x} ${midY}, ${p2.x} ${p2.y}`;
    }
  }

  // Active unit metadata for top chapter banner
  const curActiveUnit = allUnits[activeUnitIndex] || allUnits[0] || ALL_UNITS_COMBINED[0];
  const curChapter = chapterBreakpoints.find(cb => cb.units.some(u => u.id === curActiveUnit.id)) || chapterBreakpoints[0] || { num: 1, chapterNum: 1, shortTitle: 'Python Core', units: allUnits };
  const activeChapterNum = curChapter.chapterNum || curChapter.num || 1;
  const chapterUnits = curChapter.units || allUnits;
  const totalInChapter = chapterUnits.length;
  const completedInChapter = chapterUnits.filter(isUnitCompleted).length;
  const chapterSegmentsHTML = chapterUnits.map((u, uIdx) => {
    const isPassed = isUnitCompleted(u);
    const isActive = u.id === curActiveUnit.id;
    return `<div class="path-seg-bar ${isPassed ? 'done' : (isActive ? 'active' : '')}" title="Урок ${uIdx + 1}: ${escapeHtmlStr(cleanUnitTitle(u.id, u.title))}"></div>`;
  }).join('');
  const activeLessonNumInChap = Math.max(1, chapterUnits.findIndex(u => u.id === curActiveUnit.id) + 1);
  const chapterProgressLabel = completedInChapter === 0
    ? `<span class="pcc-full">Начало · ${totalInChapter} ${pluralizeRu(totalInChapter, 'урок', 'урока', 'уроков')}</span><span class="pcc-short">0 / ${totalInChapter}</span>`
    : `<span class="pcc-full">${completedInChapter} из ${totalInChapter} сдано</span><span class="pcc-short">${completedInChapter} / ${totalInChapter}</span>`;

  // Chapter gate cards between chapters in this echelon
  let markersSVG = '';
  chapterBreakpoints.forEach((cb, ci) => {
    if(ci > 0 && coords[cb.startIdx]){
      const prevCb = chapterBreakpoints[ci - 1];
      const isPrevChapterDone = prevCb.units.length > 0 && prevCb.units.every(isUnitCompleted);
      const curCompletedCount = cb.units.filter(isUnitCompleted).length;
      const isCurChapterDone = cb.units.length > 0 && curCompletedCount === cb.units.length;
      const gateStatus = !isPrevChapterDone ? 'locked' : (isCurChapterDone ? 'completed' : 'active');
      const isLocked = (gateStatus === 'locked');

      const prevY = coords[cb.startIdx - 1].y;
      const cy = prevY + 180;

      let hexFill = 'url(#pathButtonActive)';
      let hexStroke = 'rgba(251, 191, 36, 0.95)';
      let hexGlow = 'filter="drop-shadow(0 0 10px rgba(245, 158, 11, 0.65))"';
      let hexText = `<text x="0" y="-48" text-anchor="middle" font-size="14" font-weight="900" fill="#ffffff">${cb.chapterNum}</text>`;

      if(isLocked){
        hexFill = 'url(#pathButtonLocked)';
        hexStroke = 'rgba(190, 18, 60, 0.60)';
        hexGlow = '';
        hexText = `<text x="0" y="-49" text-anchor="middle" font-size="12" font-weight="900" fill="#fda4af">🔒</text>`;
      } else if(isCurChapterDone){
        hexFill = 'url(#pathButtonCompleted)';
        hexStroke = 'rgba(52, 211, 153, 0.85)';
        hexGlow = 'filter="drop-shadow(0 0 10px rgba(16, 185, 129, 0.55))"';
        hexText = `<text x="0" y="-48" text-anchor="middle" font-size="15" font-weight="900" fill="#ffffff">✓</text>`;
      }

      const hexBadge = `
        <g class="path-gate-hex-badge" ${hexGlow}>
          <polygon points="0,-72 16,-63 16,-44 0,-35 -16,-44 -16,-63" fill="${hexFill}" stroke="${hexStroke}" stroke-width="1.8" stroke-linejoin="round"/>
          <polygon points="0,-68 13,-60 13,-46 0,-38 -13,-46 -13,-60" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="1" stroke-linejoin="round"/>
          ${hexText}
        </g>`;

      let subText = '';
      if(isLocked){
        subText = `<text class="path-gate-sub" x="0" y="5" text-anchor="middle" font-size="10.5" font-weight="600" fill="#fda4af">${cb.unitsCount} ${pluralizeRu(cb.unitsCount, 'урок', 'урока', 'уроков')} · Откроется после «${escapeHtmlStr(prevCb.shortTitle)}»</text>`;
      } else if(isCurChapterDone){
        subText = `<text class="path-gate-sub" x="0" y="5" text-anchor="middle" font-size="10.5" font-weight="600" fill="#6ee7b7">✓ Все ${cb.unitsCount} из ${cb.unitsCount} уроков сданы · 100%</text>`;
      } else {
        const pct = Math.round(curCompletedCount / cb.unitsCount * 100);
        subText = `<text class="path-gate-sub" x="0" y="5" text-anchor="middle" font-size="10.5" font-weight="600" fill="#fcd34d">${curCompletedCount} из ${cb.unitsCount} ${pluralizeRu(cb.unitsCount, 'урока', 'уроков', 'уроков')} сдано · ${pct}%</text>`;
      }

      let btnContent = '';
      if(isLocked){
        btnContent = `
          <g class="path-gate-btn path-gate-btn--locked" data-gate-track="${cb.track}" data-gate-locked="1" data-gate-prev-title="${escapeHtmlStr(prevCb.shortTitle)}" role="button" tabindex="0" aria-label="Глава ${cb.chapterNum} заблокирована. Завершите темы «${escapeHtmlStr(prevCb.shortTitle)}»." aria-disabled="true">
            <rect x="-110" y="18" width="220" height="28" rx="14" fill="rgba(65, 12, 26, 0.75)" stroke="rgba(190, 18, 60, 0.55)" stroke-width="1.2"/>
            <text x="0" y="36" text-anchor="middle" font-size="10.5" font-weight="800" fill="#fda4af" letter-spacing="0.06em">🔒 ГЛАВА ЗАКРЫТА</text>
          </g>`;
      } else {
        const btnLabel = isCurChapterDone ? 'ОБЗОР ГЛАВЫ ➔' : 'ПЕРЕЙТИ К ГЛАВЕ ➔';
        btnContent = `
          <g class="path-gate-btn path-gate-btn--unlocked" data-gate-track="${cb.track}" data-gate-locked="0" role="button" tabindex="0" aria-label="Перейти к главе ${cb.chapterNum}: ${escapeHtmlStr(cb.shortTitle)}" aria-keyshortcuts="Enter Space">
            <rect class="path-gate-btn-rect" x="-110" y="18" width="220" height="28" rx="14" fill="url(#hexGradCompleted)" stroke="rgba(52, 211, 153, 0.60)" stroke-width="1.2" filter="drop-shadow(0 4px 12px rgba(16,185,129,0.40))"/>
            <text x="0" y="36" text-anchor="middle" font-size="10.5" font-weight="900" fill="#ffffff" letter-spacing="0.06em">${btnLabel}</text>
          </g>`;
      }

      markersSVG += `
        <g class="path-section-gate path-chapter-ribbon path-section-gate--${gateStatus}" transform="translate(210, ${cy})">
          <line x1="-195" y1="0" x2="-160" y2="0" stroke="rgba(190, 18, 60, 0.40)" stroke-width="1.5" stroke-dasharray="4 4"/>
          <line x1="160" y1="0" x2="195" y2="0" stroke="rgba(190, 18, 60, 0.40)" stroke-width="1.5" stroke-dasharray="4 4"/>
          <rect class="path-section-gate-bg" x="-155" y="-53" width="310" height="112" rx="18" fill="rgba(19, 24, 34, 0.94)" stroke="${isLocked ? 'rgba(190, 18, 60, 0.45)' : (isCurChapterDone ? 'rgba(16, 185, 129, 0.50)' : 'rgba(245, 158, 11, 0.60)')}" stroke-width="1.5" filter="drop-shadow(0 12px 28px rgba(0,0,0,0.65))"/>
          ${hexBadge}
          <text class="path-gate-title" x="0" y="-14" text-anchor="middle" font-size="12" font-weight="900" fill="#f8fafc" letter-spacing="0.08em">ГЛАВА ${cb.chapterNum}: ${escapeHtmlStr(cb.shortTitle.toUpperCase())}</text>
          ${subText}
          ${btnContent}
        </g>`;
    }
  });

  // Flat-topped hexagon SVG points calculation
  let nodesSVG = '';
  allUnits.forEach((u, i) => {
    const { x, y } = coords[i];
    let status = 'locked';
    if(i < activeUnitIndex || isUnitCompleted(u)){
      status = 'completed';
    } else if(i === activeUnitIndex){
      status = 'active';
    }

    const isCompleted = (status === 'completed');
    const isActive = (status === 'active');

    const topGrad = isCompleted ? 'url(#hexGradCompleted)' : (isActive ? 'url(#hexGradActive)' : 'url(#hexGradLocked)');
    const buttonGrad = isCompleted ? 'url(#pathButtonCompleted)' : (isActive ? 'url(#pathButtonActive)' : 'url(#pathButtonLocked)');
    const strokeColor = isCompleted ? 'rgba(255,255,255,0.3)' : (isActive ? '#fef08a' : 'rgba(148,163,184,0.28)');
    const strokeWidth = isActive ? 2 : 1.5;

    let centerIcon = '';
    let pulseHalo = '';
    let activeBubble = '';
    let radialProgressRing = '';
    const iconName = getSemanticTrailIcon(u, i, false);

    let unitProgPct = 0;
    let unitSkillsMastered = 0;
    const unitTotalSkills = (u.skills && u.skills.length > 0) ? u.skills.length : 1;
    if(u.skills && u.skills.length > 0){
      unitSkillsMastered = u.skills.filter(s => getSkillMP(s.id) >= 80).length;
      unitProgPct = Math.round((unitSkillsMastered / unitTotalSkills) * 100);
    }
    if(isCompleted) unitProgPct = 100;

    if(isCompleted){
      centerIcon = `<text x="${x}" y="${y+(usePawNodes?10:7)}" text-anchor="middle" font-size="${usePawNodes?18:22}" font-weight="900" fill="#ffffff">✓</text>`;
    } else if(isActive){
      pulseHalo = `<circle class="hex-pulse-halo" cx="${x}" cy="${y}" r="40" fill="none" stroke="rgba(245, 158, 11, 0.6)"/>`;
      centerIcon = trailIconCenter(x, y + (usePawNodes ? 5 : 1), iconName, usePawNodes ? 20 : 26, '#ffffff');
      const unitStarted = (u.skills || []).some(s => (getSkillMP(s.id) || 0) > 0);
      if(unitStarted && unitProgPct > 0 && unitProgPct < 100){
        const circ = 238.7;
        const dashOffset = (circ * (1 - unitProgPct / 100)).toFixed(1);
        radialProgressRing = `<circle class="hex-progress-ring" cx="${x}" cy="${y}" r="38" fill="none" stroke="#fbbf24" stroke-width="3.5" stroke-dasharray="${circ}" stroke-dashoffset="${dashOffset}" stroke-linecap="round" transform="rotate(-90 ${x} ${y})" filter="drop-shadow(0 0 6px rgba(251,191,36,0.6))"/>`;
      }
      const bubbleTxt = unitStarted ? (unitProgPct > 0 ? `ПРОДОЛЖИТЬ ➔ · ${unitSkillsMastered}/${unitTotalSkills}` : 'ПРОДОЛЖИТЬ ➔') : 'НАЧАТЬ ➔';
      const bubbleW = unitStarted ? (unitProgPct > 0 ? 152 : 118) : 96;
      const bubbleY = y - 44;
      activeBubble = `
        <g class="hex-active-tooltip hex-active-tooltip--direct" data-direct-unit="${u.id}" transform="translate(${x}, ${bubbleY})" role="button" tabindex="0" aria-label="${bubbleTxt}" title="Нажмите, чтобы сразу перейти к обучению">
          <g class="hex-active-tooltip__inner">
            <rect x="${-bubbleW/2}" y="-16" width="${bubbleW}" height="22" rx="11" fill="#ff7a00" filter="drop-shadow(0 4px 10px rgba(255,122,0,0.45))"/>
            <polygon points="-5,6 5,6 0,11" fill="#ff7a00"/>
            <text x="0" y="-1" text-anchor="middle" font-size="10" font-weight="900" fill="#ffffff" letter-spacing="0.06em">${bubbleTxt}</text>
          </g>
        </g>`;
    } else {
      centerIcon = trailIconCenter(x, y + (usePawNodes ? 5 : 0), iconName, usePawNodes ? 18 : 24, '#a9b3c3');
    }

    const nodeShape = usePawNodes
      ? trailPawShape(x, y, topGrad, strokeColor, strokeWidth)
      : trailIsometricButton(x, y, buttonGrad, isActive ? 'rgba(255,230,160,0.95)' : (isCompleted ? 'rgba(167,243,208,0.75)' : 'rgba(203,213,225,0.42)'), isActive ? 1.8 : 1.3);

    const buttonContent = usePawNodes ? centerIcon : `<g class="path-button-icon">${centerIcon}</g>`;
    const underTitleFull = cleanUnitTitle(u.id, u.title);
    const shortTitle = (underTitleFull.length > 24) ? underTitleFull.slice(0, 22) + '…' : underTitleFull;
    const underLabelX = x;
    const underLabelAnchor = 'middle';
    const nodeStateLabel = isCompleted ? 'Пройден' : (isActive ? 'Текущий урок, доступен для продолжения' : 'Заблокирован: сначала пройдите предыдущие уроки');
    const lessonNumInChap = (chapterUnits.findIndex(x => x.id === u.id) >= 0) ? (chapterUnits.findIndex(x => x.id === u.id) + 1) : (i + 1);
    const nodeAccessibleLabel = `Урок ${lessonNumInChap}: ${cleanUnitTitle(u.id, u.title)}. ${nodeStateLabel}. Нажмите Enter или пробел, чтобы открыть.`;

    nodesSVG += `
      <g class="hex-3d-node hex-node--${status}" data-unit-id="${u.id}" data-node-idx="${i}" data-cx="${x}" data-cy="${y}" role="button" tabindex="0" aria-label="${escapeHtmlStr(nodeAccessibleLabel)}" aria-keyshortcuts="Enter Space ArrowUp ArrowDown Home End" title="${escapeHtmlStr(nodeAccessibleLabel)}">
        ${pulseHalo}
        ${radialProgressRing}
        <circle cx="${x}" cy="${y}" r="34" fill="transparent" pointer-events="all"/>
        ${nodeShape}
        ${buttonContent}
        <text class="hex-node-underlabel hex-node-underlabel--${status}" x="${underLabelX}" y="${y + 52}" text-anchor="${underLabelAnchor}">${escapeHtmlStr(shortTitle)}</text>
        ${activeBubble}
      </g>`;
  });

  // «Челлендж мастерства» side branches for each chapter in this echelon
  let branchesSVG = '';
  chapterBreakpoints.forEach((cb, cIdx) => {
    const endIdx = (cIdx < chapterBreakpoints.length - 1) ? (chapterBreakpoints[cIdx + 1].startIdx - 1) : (allUnits.length - 1);
    const u = allUnits[endIdx];
    if(!u || !coords[endIdx]) return;
    const { x, y } = coords[endIdx];
    const track = getTrackForUnit(u.id);
    const chDone = (state.passedUnitTests || []).includes(u.id);
    const chUnlocked = endIdx <= activeUnitIndex;
    const chStatus = chDone ? 'done' : (chUnlocked ? 'open' : 'locked');
    const bx = Math.max(68, Math.min(352, x + (x >= 210 ? 70 : -70)));
    const by = y + 36;
    const chGrad = chDone ? 'url(#hexGradCompleted)' : (chStatus === 'open' ? 'url(#hexGradChallenge)' : 'url(#hexGradLocked)');
    const chButtonGrad = chDone ? 'url(#pathButtonCompleted)' : (chStatus === 'open' ? 'url(#pathButtonChallenge)' : 'url(#pathButtonLocked)');
    const chStroke = chDone ? 'rgba(255,255,255,0.3)' : (chStatus === 'open' ? 'rgba(251,113,133,0.6)' : 'rgba(148,163,184,0.28)');
    let chIcon = '';
    let chHalo = '';
    if(chDone){
      chIcon = `<text x="${bx}" y="${by+(usePawNodes?8:6)}" text-anchor="middle" font-size="${usePawNodes?15:16}" font-weight="900" fill="#ffffff">✓</text>`;
    } else if(chStatus === 'open'){
      chHalo = `<circle class="hex-challenge-pulse" cx="${bx}" cy="${by}" r="28" fill="none" stroke="rgba(190,18,60,0.55)"/>`;
      chIcon = trailIconCenter(bx, by + (usePawNodes?4:1), 'trophy', usePawNodes?17:22, '#ffffff');
    } else {
      chIcon = trailIconCenter(bx, by + (usePawNodes?4:0), 'trophy', usePawNodes?16:20, '#a9b3c3');
    }
    const challengeShape = usePawNodes
      ? trailPawShape(bx, by, chGrad, chStroke, chStatus === 'open' ? 1.8 : 1.3)
      : trailIsometricButton(bx, by, chButtonGrad, chStatus === 'open' ? 'rgba(253,164,175,0.9)' : 'rgba(203,213,225,0.42)', chStatus === 'open' ? 1.7 : 1.2);
    const challengeContent = usePawNodes ? chIcon : `<g class="path-button-icon">${chIcon}</g>`;
    const connectorStroke = chDone ? 'rgba(52,211,153,0.80)' : (chStatus === 'open' ? 'rgba(251,113,133,0.85)' : 'rgba(148,163,184,0.48)');

    branchesSVG += `
      <g class="hex-challenge-branch">
        <path d="M ${x},${y + 24} Q ${x},${(y + by) / 2} ${bx},${by - 20}" fill="none" stroke="${connectorStroke}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="3 4"/>
        <g class="hex-challenge-node hex-challenge-node--${chStatus}" data-challenge-route="#${track.routePrefix}/unittest/${u.id}" data-challenge-status="${chStatus}" data-cx="${bx}" data-cy="${by}" role="button" tabindex="0" aria-label="Челлендж мастерства, проверка урока ${u.id}. ${chDone ? 'Пройдено' : (chUnlocked ? 'Доступно' : 'Заблокировано до прохождения предыдущих уроков')}. Нажмите Enter или пробел, чтобы открыть." aria-keyshortcuts="Enter Space" aria-disabled="${chStatus === 'locked' ? 'true' : 'false'}">
          ${chHalo}
          <circle cx="${bx}" cy="${by}" r="24" fill="transparent" pointer-events="all"/>
          ${challengeShape}
          ${challengeContent}
          <text class="hex-branch-label" x="${bx}" y="${by + 36}" text-anchor="middle">ЧЕЛЛЕНДЖ<tspan x="${bx}" dy="12">МАСТЕРСТВА</tspan></text>
        </g>
      </g>`;
  });

  const totalCompletedUnits = ALL_UNITS_COMBINED.filter(isUnitCompleted).length;
  const streakText = (typeof pluralizeRu === 'function') ? pluralizeRu(state.streak || 0, 'день', 'дня', 'дней') : 'дн.';

  // Echelon metadata
  const curTierNum = (curEchelon === 'all') ? (curActiveUnit.tier || 1) : (Number(curEchelon) || 1);
  const curEchelonMeta = (typeof INTERVIEW_ECHELONS !== 'undefined' && INTERVIEW_ECHELONS[curTierNum]) ? INTERVIEW_ECHELONS[curTierNum] : { shortLabel: `Эшелон ${curTierNum}`, icon: '🛡️', targetLabel: 'к скринингу' };
  const e1Top = (typeof getEchelonProgress === 'function') ? getEchelonProgress(1) : null;
  const e1PctTop = e1Top ? e1Top.pct : 0;
  const echProg = (typeof getEchelonProgress === 'function') ? getEchelonProgress(curTierNum) : null;
  const echPct = echProg ? echProg.pct : 0;

  const echelonFull = (curEchelon === 'all') ? '🌐 Все эшелоны' : curEchelonMeta.shortLabel;
  const echelonShort = (curEchelon === 'all') ? '🌐 Все' : `${curEchelonMeta.icon} Эшелон ${curTierNum}`;

  let screeningFull = '';
  let screeningShort = '';
  if(curTierNum === 1 || curEchelon === 'all'){
    screeningFull = e1PctTop > 0 ? `⚡ Готовность к тех-скринингу: ${e1PctTop}%` : '⚡ Старт тех-скрининга · База';
    screeningShort = e1PctTop > 0 ? `⚡ ${e1PctTop}% к скринингу` : '⚡ Старт · База';
  } else if(curTierNum === 2){
    screeningFull = echPct > 0 ? `🎯 Готовность к тех-интервью: ${echPct}%` : '🎯 Старт тех-интервью · Стек';
    screeningShort = echPct > 0 ? `🎯 ${echPct}% к интервью` : '🎯 Старт · Стек';
  } else if(curTierNum === 3){
    screeningFull = echPct > 0 ? `⚡ Готовность к лайвкодингу: ${echPct}%` : '⚡ Старт лайвкодинга · Сервисы';
    screeningShort = echPct > 0 ? `⚡ ${echPct}% к лайвкодингу` : '⚡ Старт · Сервисы';
  } else {
    screeningFull = echPct > 0 ? `👑 Готовность к офферу: ${echPct}%` : '👑 Старт архитектуры';
    screeningShort = echPct > 0 ? `👑 ${echPct}% к офферу` : '👑 Старт · Оффер';
  }

  return `
    <div class="coddy-path-layout">
      <div class="container path-serpentine-wrap">
        <!-- Desktop Quick Echelon Switcher Tabs (Direct 1-click program selection) -->
        <div class="path-echelon-quick-tabs" role="tablist" aria-label="Быстрый выбор эшелона программы">
          <button type="button" class="path-eq-tab path-eq-tab--t1 ${curEchelon===1?'active':''}" data-select-echelon="1" title="Эшелон 1: Скрининг · Фундамент (14 уроков)">🛡️ 1. Скрининг</button>
          <button type="button" class="path-eq-tab path-eq-tab--t2 ${curEchelon===2?'active':''}" data-select-echelon="2" title="Эшелон 2: Тех-интервью · Стек и БД (17 уроков)">🎯 2. Стек и БД</button>
          <button type="button" class="path-eq-tab path-eq-tab--t3 ${curEchelon===3?'active':''}" data-select-echelon="3" title="Эшелон 3: Лайвкодинг · Сервисы (11 уроков)">⚡ 3. Продакшен</button>
          <button type="button" class="path-eq-tab path-eq-tab--t4 ${curEchelon===4?'active':''}" data-select-echelon="4" title="Эшелон 4: Финал · Системный дизайн (3 урока)">👑 4. Системный дизайн</button>
          <button type="button" class="path-eq-tab ${curEchelon==='all'?'active':''}" data-select-echelon="all" title="Сквозной курс (все 45 уроков)">🌐 Все 45</button>
        </div>

        <!-- Mobile compact stats strip -->
        ${renderPathMobileStatsHTML(totalCompletedUnits, streakText, curEchelon, activeChapterNum, completedInChapter, totalInChapter)}

        <!-- Top Chapter Banner (Three-tier layout with Interactive Echelon Program Trigger) -->
        <div class="path-chapter-banner">
          <div class="path-chapter-banner-top">
            <div class="path-chapter-breadcrumb">
              <button type="button" class="path-echelon-pill path-echelon-pill-btn echelon-pill--t${curTierNum}" data-open-echelon-modal="1" title="Нажмите, чтобы выбрать программу / эшелон подготовки" aria-haspopup="dialog">
                <span class="pep-full">${echelonFull} <span class="pep-chevron">▾</span></span>
                <span class="pep-short">${echelonShort} <span class="pep-chevron">▾</span></span>
              </button>
              <span class="path-crumb-sep">›</span>
              <span class="path-chapter-crumb-label"><span class="pcl-full">ГЛАВА ${activeChapterNum}</span><span class="pcl-short">ГЛ. ${activeChapterNum}</span></span>
            </div>
            <span class="path-screening-badge" title="${escapeHtmlStr(screeningFull)}"><span class="psb-full">${screeningFull}</span><span class="psb-short">${screeningShort}</span></span>
          </div>
          <div class="path-chapter-title">Урок ${activeLessonNumInChap} · ${escapeHtmlStr(cleanUnitTitle(curActiveUnit.id, curActiveUnit.title))}</div>
          <div class="path-chapter-progress-row">
            <div class="path-chapter-segments">
              ${chapterSegmentsHTML}
            </div>
            <span class="path-chapter-count" title="${completedInChapter === 0 ? `Начни главу: в ней ${totalInChapter} ${pluralizeRu(totalInChapter, 'урок', 'урока', 'уроков')}` : `Завершено уроков: ${completedInChapter} из ${totalInChapter}`}" aria-label="${completedInChapter === 0 ? `Начни главу: ${totalInChapter} ${pluralizeRu(totalInChapter, 'урок', 'урока', 'уроков')}` : `Завершено уроков: ${completedInChapter} из ${totalInChapter}`}">${chapterProgressLabel}</span>
          </div>
        </div>

        <!-- S-Curve SVG Trail -->
        <div class="path-serpentine" style="position:relative;">
          <svg class="path-serpentine-svg" viewBox="0 0 420 ${totalH}" xmlns="http://www.w3.org/2000/svg" role="group" aria-label="Путь обучения: ${allUnits.length} уроков и челленджи">
            <defs>
              <linearGradient id="hexGradCompleted" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#34d399"/>
                <stop offset="100%" stop-color="#059669"/>
              </linearGradient>
              <linearGradient id="hexGradActive" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#fbbf24"/>
                <stop offset="100%" stop-color="#d97706"/>
              </linearGradient>
              <linearGradient id="hexGradLocked" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#3a4150"/>
                <stop offset="100%" stop-color="#15181f"/>
              </linearGradient>
              <linearGradient id="hexGradChallenge" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#fb7185"/>
                <stop offset="100%" stop-color="#be123c"/>
              </linearGradient>
              <linearGradient id="pathButtonActive" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffd166"/><stop offset="0.52" stop-color="#f59e0b"/><stop offset="1" stop-color="#c65a08"/></linearGradient>
              <linearGradient id="pathButtonCompleted" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#6ee7b7"/><stop offset="0.52" stop-color="#10b981"/><stop offset="1" stop-color="#047857"/></linearGradient>
              <linearGradient id="pathButtonLocked" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#566174"/><stop offset="0.55" stop-color="#303949"/><stop offset="1" stop-color="#1b2230"/></linearGradient>
              <linearGradient id="pathButtonSide" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#303a4b"/><stop offset="1" stop-color="#111722"/></linearGradient>
              <linearGradient id="pathButtonChallenge" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fda4af"/><stop offset="0.55" stop-color="#e11d48"/><stop offset="1" stop-color="#9f1239"/></linearGradient>
              <linearGradient id="pathProgressGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#10b981"/>
                <stop offset="100%" stop-color="#f59e0b"/>
              </linearGradient>
            </defs>

            <!-- Outer cyber conduit trail shadow -->
            <path d="${dPath}" fill="none" stroke="rgba(0,0,0,0.4)" stroke-width="18" stroke-linecap="round"/>
            <!-- Background cyber conduit track -->
            <path class="path-track-bg" d="${dPath}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="8" stroke-linecap="round"/>
            ${dProgress ? `<path class="path-track-progress" d="${dProgress}" fill="none" stroke="url(#pathProgressGrad)" stroke-width="6" stroke-linecap="round" style="filter:drop-shadow(0 0 6px rgba(16,185,129,0.45));"/>` : ''}
            ${dFuture ? `<path class="path-track-future" d="${dFuture}" fill="none" stroke="rgba(148,163,184,0.18)" stroke-width="3" stroke-linecap="round"/>` : ''}

            <!-- Chapter ribbons -->
            ${markersSVG}

            <!-- 3D Hexagonal Nodes -->
            ${nodesSVG}

            <!-- «Челлендж мастерства» side branches -->
            ${branchesSVG}
          </svg>

          <!-- Anchored Popover Modal & Backdrop -->
          <div id="path-popover-backdrop" class="path-popover-backdrop" style="display:none;" aria-hidden="true"></div>
          <div id="path-anchored-popover" class="path-popover" style="display:none;" role="dialog" tabindex="-1" aria-labelledby="popover-title" aria-describedby="popover-status">
            <div class="path-popover-arrow path-popover-arrow--down" id="popover-arrow"></div>
            <div class="path-popover-content">
              <div class="path-popover-header">
                <div class="path-popover-badge" id="popover-badge">🎯 Модуль 1 · Python</div>
                <button type="button" class="path-popover-close" id="popover-close-btn" aria-label="Закрыть">✕</button>
              </div>
              <h3 class="path-popover-title" id="popover-title">Переменные и память</h3>
              <div class="path-popover-status" id="popover-status">В процессе изучения</div>
              <div class="path-popover-skills" id="popover-skills"></div>
              <div class="path-popover-actions">
                <button type="button" class="btn-3d-orange path-popover-cta" id="popover-cta-btn">НАЧАТЬ ➔</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Floating Jump Button to active lesson -->
        <button type="button" class="path-jump-btn" id="path-jump-btn" title="Перейти к текущему уроку" aria-label="Перейти к текущему уроку">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
        </button>

        <!-- Echelon / Program Selector Bottom Sheet & Modal -->
        <div id="path-echelon-modal-backdrop" class="path-echelon-modal-backdrop" style="display:none;" aria-hidden="true"></div>
        <div id="path-echelon-modal" class="path-echelon-modal" style="display:none;" role="dialog" aria-modal="true" aria-labelledby="path-echelon-modal-title">
          <div class="path-echelon-modal-handle"></div>
          <div class="path-echelon-modal-head">
            <div>
              <h3 class="path-echelon-modal-title" id="path-echelon-modal-title">Программы подготовки к собеседованию</h3>
              <p class="path-echelon-modal-sub">Выберите целевой эшелон. 3D-тропа перестроится под выбранную программу.</p>
            </div>
            <button type="button" class="path-echelon-modal-close" data-close-echelon-modal="1" aria-label="Закрыть">✕</button>
          </div>
          <div class="path-echelon-cards-list">
            ${renderEchelonCardsModalHTML(curEchelon)}
          </div>
        </div>
      </div>

      ${renderCoddyRightRail(totalCompletedUnits, streakText, activeChapterNum, curEchelon)}
    </div>`;
}

"""

content = content[:serpentine_start] + new_viewPathSerpentine + content[serpentine_end:]
print('6. viewPathSerpentine rewritten with echelon filter & program selector!')

# ---------------------------------------------------------------------------
# 7. Update viewProPath to also filter by selected echelon & include header trigger
# ---------------------------------------------------------------------------
pro_start = content.find('function viewProPath(options){')
pro_end = content.find('window.viewPathSerpentine = viewPathSerpentine;')
assert pro_start != -1 and pro_end != -1, 'viewProPath bounds not found'

new_viewProPath = """function viewProPath(options){
  options = options || {};
  ensureExtendedState();
  const curEchelon = (options.echelon !== undefined) ? options.echelon : ((state && state.selectedEchelon) || 1);
  const { units: allUnits, chapters } = getEchelonUnitsAndChapters(curEchelon, ALL_UNITS_COMBINED);

  // Find active unit
  let activeUnitIndex = -1;
  allUnits.forEach((u, idx) => {
    const isUnitTestPassed = (state.passedUnitTests || []).includes(u.id);
    const allSkillsMastered = (u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80);
    const isCompleted = isUnitTestPassed || allSkillsMastered;
    if(!isCompleted && activeUnitIndex === -1){
      activeUnitIndex = idx;
    }
  });
  if(activeUnitIndex === -1) activeUnitIndex = Math.max(0, allUnits.length - 1);

  const curActiveUnit = allUnits[activeUnitIndex] || allUnits[0] || ALL_UNITS_COMBINED[0];
  const totalCompletedUnits = ALL_UNITS_COMBINED.filter(isUnitCompleted).length;
  const streakText = (typeof pluralizeRu === 'function') ? pluralizeRu(state.streak || 0, 'день', 'дня', 'дней') : 'дн.';

  const activeChap = chapters.find(c => c.units.some(u => u.id === curActiveUnit.id)) || chapters[0] || { num: 1, chapterNum: 1, title: 'Python Core', units: allUnits };
  const activeChapCompleted = activeChap.units.filter(isUnitCompleted).length;
  const activeChapTotal = activeChap.units.length;
  const activeChapPct = Math.round(activeChapCompleted / activeChapTotal * 100);
  const activeChapSummary = activeChapCompleted === 0
    ? `Начни главу · ${activeChapTotal} ${pluralizeRu(activeChapTotal, 'урок', 'урока', 'уроков')}`
    : `Глава ${activeChap.chapterNum || activeChap.num}: ${escapeHtmlStr(activeChap.title)} · ${activeChapCompleted}/${activeChapTotal} уроков · ${activeChapPct}%`;

  // Segments for active chapter
  const activeChapSegmentsHTML = activeChap.units.map(u => {
    const isPassed = isUnitCompleted(u);
    const isActive = u.id === curActiveUnit.id;
    return `<div class="path-seg-bar ${isPassed ? 'done' : (isActive ? 'active' : '')}" title="Урок ${activeChap.units.findIndex(x => x.id === u.id) + 1}: ${escapeHtmlStr(cleanUnitTitle(u.id, u.title))}"></div>`;
  }).join('');

  const curTierNum = (curEchelon === 'all') ? (curActiveUnit.tier || 1) : (Number(curEchelon) || 1);
  const curEchelonMeta = (typeof INTERVIEW_ECHELONS !== 'undefined' && INTERVIEW_ECHELONS[curTierNum]) ? INTERVIEW_ECHELONS[curTierNum] : { shortLabel: `Эшелон ${curTierNum}`, icon: '🛡️' };
  const echelonFull = (curEchelon === 'all') ? '🌐 Все эшелоны' : curEchelonMeta.shortLabel;

  // Hero Card HTML
  const heroCardHTML = `
    <div class="pro-hero-card">
      <div class="pro-hero-card-head">
        <div class="pro-hero-card-left">
          <div class="pro-hero-breadcrumb-row" style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
            <button type="button" class="path-echelon-pill path-echelon-pill-btn echelon-pill--t${curTierNum}" data-open-echelon-modal="1" title="Нажмите, чтобы сменить программу / эшелон" aria-haspopup="dialog" style="padding:2px 8px;font-size:0.68rem;">
              <span>${echelonFull}</span>
              <span class="pep-chevron">▾</span>
            </button>
            <div class="pro-hero-breadcrumb">ПРОГРАММА › ГЛАВА ${activeChap.num}</div>
          </div>
          <h2 class="pro-hero-title">Урок ${activeChap.units.findIndex(x => x.id === curActiveUnit.id) + 1} · ${escapeHtmlStr(cleanUnitTitle(curActiveUnit.id, curActiveUnit.title))}</h2>
          <div class="pro-hero-meta">${activeChapSummary}</div>
        </div>
        <button type="button" class="btn-3d-orange pro-hero-cta" data-pro-start="${curActiveUnit.id}">ПРОДОЛЖИТЬ</button>
      </div>

      <div class="pro-hero-progress-track">
        <div class="pro-hero-progress-fill" style="width:${activeChapPct}%;"></div>
      </div>

      <div class="path-chapter-progress-row" style="margin-top:4px;">
        <span class="path-chapter-target-icon">🎯</span>
        <div class="path-chapter-segments">
          ${activeChapSegmentsHTML}
        </div>
        <span class="path-chapter-count" title="${activeChapCompleted === 0 ? `Начни главу: в ней ${activeChapTotal} ${pluralizeRu(activeChapTotal, 'урок', 'урока', 'уроков')}` : `Завершено уроков: ${activeChapCompleted} из ${activeChapTotal}`}" aria-label="${activeChapCompleted === 0 ? `Начни главу: ${activeChapTotal} ${pluralizeRu(activeChapTotal, 'урок', 'урока', 'уроков')}` : `Завершено уроков: ${activeChapCompleted} из ${activeChapTotal}`}">${activeChapCompleted === 0 ? `0 / ${activeChapTotal}` : `${activeChapCompleted} / ${activeChapTotal}`}</span>
      </div>
    </div>
  `;

  // Chapters list HTML
  const chaptersHTML = chapters.map(ch => {
    const isCurChap = ((ch.chapterNum || ch.num) === (activeChap.chapterNum || activeChap.num));
    const chCompleted = ch.units.filter(isUnitCompleted).length;
    const chTotal = ch.units.length;
    const chPct = Math.round(chCompleted / chTotal * 100);
    const isExpanded = isCurChap ? !proCollapsedChapters.has(ch.chapterNum || ch.num) : proCollapsedChapters.has(ch.chapterNum || ch.num);

    const lessonsListHTML = ch.units.map(u => {
      const isCompleted = isUnitCompleted(u);
      const globalIdx = allUnits.findIndex(x => x.id === u.id);
      const isActive = (globalIdx === activeUnitIndex);
      const isLocked = (globalIdx > activeUnitIndex && !isCompleted);

      let statusClass = isCompleted ? 'pro-lesson-row--completed' : (isActive ? 'pro-lesson-row--active' : 'pro-lesson-row--locked');
      let iconHtml = '';
      if(isActive){
        iconHtml = '<div class="pro-icon-play" aria-label="Текущий урок">▶</div>';
      } else if(isCompleted){
        iconHtml = '<div class="pro-icon-done" aria-label="Пройден">✓</div>';
      } else {
        iconHtml = '<div class="pro-icon-locked" aria-label="Заблокирован">🔒</div>';
      }

      const isChallenge = u.id.endsWith('.9') || u.id.endsWith('.6') || u.id.endsWith('.8');
      const badgeClass = isChallenge ? 'pro-lesson-badge pro-lesson-badge--challenge' : 'pro-lesson-badge';
      const badgeText = isChallenge ? 'Испытание' : 'Теория + Практика';
      
      const unitSkills = (u.skills || []).map(s => s.title.split('(')[0].trim());
      const previewPills = unitSkills.slice(0, 3).map(skillName => 
        `<span style="font-size:0.68rem;padding:2px 7px;border-radius:6px;background:rgba(255,255,255,0.05);color:var(--ink-muted);border:1px solid rgba(255,255,255,0.06);white-space:nowrap;">${escapeHtmlStr(skillName)}</span>`
      ).join(' ');

      return `
        <div class="pro-lesson-row ${statusClass}" data-unit-id="${u.id}" role="button" tabindex="${isLocked ? '-1' : '0'}" style="${isActive ? 'box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.4), 0 8px 24px rgba(0,0,0,0.4); background: rgba(245, 158, 11, 0.05);' : ''}">
          <div class="pro-lesson-status-icon">${iconHtml}</div>
          <div class="pro-lesson-info" style="display:flex;flex-direction:column;gap:5px;">
            <div class="pro-lesson-title" style="font-weight:${isActive ? '700' : '600'}; color:${isActive ? '#f8fafc' : (isCompleted ? 'var(--ink)' : 'var(--ink-muted)')};">
              Урок ${ch.units.findIndex(x => x.id === u.id) + 1} · ${escapeHtmlStr(cleanUnitTitle(u.id, u.title))}
            </div>
            <div class="pro-lesson-tags" style="display:flex;flex-wrap:wrap;gap:5px;align-items:center;">
              <span class="${badgeClass}">${badgeText}</span>
              ${previewPills}
            </div>
          </div>
          <div class="pro-lesson-tail">
            ${isActive ? '<span class="pro-arrow" style="font-weight:bold;color:var(--amber);">→</span>' : (isLocked ? `<span style="font-size:0.75rem;color:var(--ink-muted);opacity:0.6;">${(u.skills && u.skills.length) || 1} ${pluralizeRu((u.skills && u.skills.length) || 1, 'тема', 'темы', 'тем')}</span>` : '')}
          </div>
        </div>
      `;
    }).join('');

    return `
      <div class="pro-chapter-box ${isCurChap ? 'pro-chapter-box--active' : ''}">
        <div class="pro-chapter-header" data-toggle-chapter="${ch.chapterNum || ch.num}">
          <div class="pro-chapter-header-left">
            <div class="pro-chapter-num">ГЛАВА ${ch.chapterNum || ch.num}</div>
            <div class="pro-chapter-title">${escapeHtmlStr(ch.title)}</div>
          </div>
          <div class="pro-chapter-header-right">
            <span class="pro-chapter-stat" style="white-space:nowrap;">${chCompleted}/${chTotal} · ${chPct}%</span>
            <span class="pro-chapter-chevron" style="transform:${isExpanded ? 'rotate(180deg)' : 'none'};">▼</span>
          </div>
        </div>
        ${isExpanded ? `<div class="pro-lesson-list">${lessonsListHTML}</div>` : ''}
      </div>
    `;
  }).join('');

  return `
    <div class="coddy-path-layout">
      <div class="container path-pro-wrap">
        <!-- Desktop Quick Echelon Switcher Tabs -->
        <div class="path-echelon-quick-tabs" role="tablist" aria-label="Быстрый выбор эшелона программы">
          <button type="button" class="path-eq-tab path-eq-tab--t1 ${curEchelon===1?'active':''}" data-select-echelon="1" title="Эшелон 1: Скрининг · Фундамент (14 уроков)">🛡️ 1. Скрининг</button>
          <button type="button" class="path-eq-tab path-eq-tab--t2 ${curEchelon===2?'active':''}" data-select-echelon="2" title="Эшелон 2: Тех-интервью · Стек и БД (17 уроков)">🎯 2. Стек и БД</button>
          <button type="button" class="path-eq-tab path-eq-tab--t3 ${curEchelon===3?'active':''}" data-select-echelon="3" title="Эшелон 3: Лайвкодинг · Сервисы (11 уроков)">⚡ 3. Продакшен</button>
          <button type="button" class="path-eq-tab path-eq-tab--t4 ${curEchelon===4?'active':''}" data-select-echelon="4" title="Эшелон 4: Финал · Системный дизайн (3 урока)">👑 4. Системный дизайн</button>
          <button type="button" class="path-eq-tab ${curEchelon==='all'?'active':''}" data-select-echelon="all" title="Сквозной курс (все 45 уроков)">🌐 Все 45</button>
        </div>

        <!-- Mobile compact stats strip -->
        ${renderPathMobileStatsHTML(totalCompletedUnits, streakText, curEchelon)}

        <!-- Top Hero Card of Current Lesson -->
        ${heroCardHTML}

        <!-- Structured Chapters List -->
        ${chaptersHTML}

        <!-- Echelon / Program Selector Bottom Sheet & Modal -->
        <div id="path-echelon-modal-backdrop" class="path-echelon-modal-backdrop" style="display:none;" aria-hidden="true"></div>
        <div id="path-echelon-modal" class="path-echelon-modal" style="display:none;" role="dialog" aria-modal="true" aria-labelledby="path-echelon-modal-title">
          <div class="path-echelon-modal-handle"></div>
          <div class="path-echelon-modal-head">
            <div>
              <h3 class="path-echelon-modal-title" id="path-echelon-modal-title">Программы подготовки к собеседованию</h3>
              <p class="path-echelon-modal-sub">Выберите целевой эшелон. 3D-тропа перестроится под выбранную программу.</p>
            </div>
            <button type="button" class="path-echelon-modal-close" data-close-echelon-modal="1" aria-label="Закрыть">✕</button>
          </div>
          <div class="path-echelon-cards-list">
            ${renderEchelonCardsModalHTML(curEchelon)}
          </div>
        </div>
      </div>

      ${renderCoddyRightRail(totalCompletedUnits, streakText, activeChap.chapterNum || activeChap.num, curEchelon)}
    </div>
  `;
}
"""

content = content[:pro_start] + new_viewProPath + content[pro_end:]
print('7. viewProPath rewritten with echelon filter & program selector!')

# ---------------------------------------------------------------------------
# 8. Event Listeners for Echelon Program Selector & Modal
# ---------------------------------------------------------------------------
target_events_anchor = """  // Path Mode Switcher ('game' | 'pro')
  const modeBtn = e.target.closest('[data-set-path-mode]');"""

new_events = """  // Echelon Program Selector Triggers & Modal Actions
  if(e.target.closest('[data-open-echelon-modal]')){
    const modal = document.getElementById('path-echelon-modal');
    const backdrop = document.getElementById('path-echelon-modal-backdrop');
    if(modal && backdrop){
      modal.style.display = 'block';
      backdrop.style.display = 'block';
      // Force repaint then add open class
      void modal.offsetWidth;
      modal.classList.add('is-open');
      backdrop.classList.add('is-open');
      if(typeof navigator !== 'undefined' && navigator.vibrate){
        try{ navigator.vibrate(10); }catch(vErr){}
      }
    }
    return;
  }

  if(e.target.closest('[data-close-echelon-modal]') || e.target.id === 'path-echelon-modal-backdrop'){
    const modal = document.getElementById('path-echelon-modal');
    const backdrop = document.getElementById('path-echelon-modal-backdrop');
    if(modal) modal.classList.remove('is-open');
    if(backdrop) backdrop.classList.remove('is-open');
    setTimeout(() => {
      if(modal && !modal.classList.contains('is-open')) modal.style.display = 'none';
      if(backdrop && !backdrop.classList.contains('is-open')) backdrop.style.display = 'none';
    }, 240);
    return;
  }

  const selectEchBtn = e.target.closest('[data-select-echelon]');
  if(selectEchBtn){
    const rawVal = selectEchBtn.getAttribute('data-select-echelon');
    const targetEch = (rawVal === 'all') ? 'all' : (parseInt(rawVal, 10) || 1);
    ensureExtendedState();
    state.selectedEchelon = targetEch;
    saveState(state);

    const modal = document.getElementById('path-echelon-modal');
    const backdrop = document.getElementById('path-echelon-modal-backdrop');
    if(modal) modal.classList.remove('is-open');
    if(backdrop) backdrop.classList.remove('is-open');
    if(modal) modal.style.display = 'none';
    if(backdrop) backdrop.style.display = 'none';

    if(typeof navigator !== 'undefined' && navigator.vibrate){
      try{ navigator.vibrate(12); }catch(vErr){}
    }
    render();
    if(typeof showTactileToast === 'function'){
      if(targetEch === 'all'){
        showTactileToast('🌐 Выбран сквозной курс (все 45 уроков)');
      } else {
        const em = (typeof INTERVIEW_ECHELONS !== 'undefined' && INTERVIEW_ECHELONS[targetEch]) ? INTERVIEW_ECHELONS[targetEch] : { icon: '🛡️', shortLabel: `Эшелон ${targetEch}` };
        showTactileToast(`${em.icon} Программа переключена: ${em.shortLabel}`);
      }
    }
    return;
  }

  // Path Mode Switcher ('game' | 'pro')
  const modeBtn = e.target.closest('[data-set-path-mode]');"""

assert target_events_anchor in content, 'target_events_anchor not found'
content = content.replace(target_events_anchor, new_events, 1)
print('8. Event listeners for Echelon Program Selector injected!')

# ---------------------------------------------------------------------------
# 8b. Update Popover Click Handler to use clean human lesson titles & statuses
# ---------------------------------------------------------------------------
target_popover_block = """        if(pBadge) pBadge.textContent = `ТРЕК · ${track.title.split('Матрица Мастерства').pop().trim() || track.title}`;
        if(pTitle) pTitle.textContent = `Юнит ${u.id}: ${u.title.replace(/^Юнит\\s+[\\d.]+\\s*·\\s*/, '')}`;

        const isPassed = (state.passedUnitTests || []).includes(u.id) || ((u.skills||[]).length > 0 && (u.skills||[]).every(s => getSkillMP(s.id) >= 80));
        const uIdx = ALL_UNITS_COMBINED.findIndex(x => x.id === uid);
        let activeIdx = ALL_UNITS_COMBINED.findIndex(x => {
          const pass = (state.passedUnitTests || []).includes(x.id) || ((x.skills||[]).length > 0 && (x.skills||[]).every(s => getSkillMP(s.id) >= 80));
          return !pass;
        });
        if(activeIdx === -1) activeIdx = ALL_UNITS_COMBINED.length - 1;
        const isActive = (uIdx === activeIdx);
        const isLocked = (uIdx > activeIdx && !isPassed);

        if(pStatus){
          if(isPassed) pStatus.textContent = '✅ Юнит завершён (освоен на 100%)';
          else if(isActive) pStatus.textContent = '🏆 Текущая цель курса';
          else if(isLocked) pStatus.textContent = 'Пройдите уроки выше, чтобы открыть это!';
          else pStatus.textContent = '📖 Доступен для изучения';
        }

        if(pSkills){
          const skillItems = (u.skills || []).slice(0, 3);
          const noteCount = (u.skills || []).reduce((acc, s) => acc + (s.kIds ? s.kIds.length : 1), 0);
          pSkills.innerHTML = skillItems.length
            ? `<div class="path-popover-meta-row" style="font-size:0.75rem;color:var(--ink-muted);margin-bottom:8px;display:flex;gap:12px;"><span>📚 <b>${noteCount}</b> тем-конспектов</span><span>🎯 <b>${(u.skills||[]).length}</b> навыков</span></div><div class="path-popover-skills-label">Ключевые навыки юнита:</div><div class="path-popover-skills-list">${skillItems.map(s => `<div class="path-popover-skill">${escapeHtmlStr(s.title)}</div>`).join('')}</div>`
            : '';
        }"""

new_popover_block = """        const chapterUnits = ALL_UNITS_COMBINED.filter(x => getTrackForUnit(x.id).routePrefix === track.routePrefix);
        const uIdx = ALL_UNITS_COMBINED.findIndex(x => x.id === uid);
        const lessonNumInChap = (chapterUnits.findIndex(x => x.id === u.id) >= 0) ? (chapterUnits.findIndex(x => x.id === u.id) + 1) : (uIdx + 1);

        if(pBadge) pBadge.textContent = `ТРЕК · ${track.title.split('Матрица Мастерства').pop().trim() || track.title}`;
        if(pTitle) pTitle.textContent = `Урок ${lessonNumInChap} · ${cleanUnitTitle(u.id, u.title)}`;

        const isPassed = (state.passedUnitTests || []).includes(u.id) || ((u.skills||[]).length > 0 && (u.skills||[]).every(s => getSkillMP(s.id) >= 80));
        let activeIdx = ALL_UNITS_COMBINED.findIndex(x => {
          const pass = (state.passedUnitTests || []).includes(x.id) || ((x.skills||[]).length > 0 && (x.skills||[]).every(s => getSkillMP(s.id) >= 80));
          return !pass;
        });
        if(activeIdx === -1) activeIdx = ALL_UNITS_COMBINED.length - 1;
        const isActive = (uIdx === activeIdx);
        const isLocked = (uIdx > activeIdx && !isPassed);

        if(pStatus){
          if(isPassed) pStatus.textContent = '✅ Урок освоен на 100%';
          else if(isActive) pStatus.textContent = '🎯 Текущая цель курса';
          else if(isLocked) pStatus.textContent = '🔒 Откроется после предыдущих уроков';
          else pStatus.textContent = '📖 Доступен для изучения';
        }

        if(pSkills){
          const skillItems = (u.skills || []).slice(0, 3);
          const noteCount = (u.skills || []).reduce((acc, s) => acc + (s.kIds ? s.kIds.length : 1), 0);
          pSkills.innerHTML = skillItems.length
            ? `<div class="path-popover-meta-row" style="font-size:0.75rem;color:var(--ink-muted);margin-bottom:8px;display:flex;gap:12px;"><span>📚 <b>${noteCount}</b> тем-конспектов</span><span>🎯 <b>${(u.skills||[]).length}</b> навыков</span></div><div class="path-popover-skills-label">Ключевые темы урока:</div><div class="path-popover-skills-list">${skillItems.map(s => `<div class="path-popover-skill">${escapeHtmlStr(s.title)}</div>`).join('')}</div>`
            : '';
        }"""

assert target_popover_block in content, 'target_popover_block not found'
content = content.replace(target_popover_block, new_popover_block, 1)
print('8b. Popover click handler updated with clean lesson title & status!')

# ---------------------------------------------------------------------------
# 9. Write updated academy.html & sync to Etalons
# ---------------------------------------------------------------------------
with open(academy_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Done! academy.html updated ({len(content)} bytes).')
