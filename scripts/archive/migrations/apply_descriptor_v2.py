import os
import re

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_path = os.path.join(root, 'academy.html')

with open(academy_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Original academy.html length:", len(content))

# ---------------------------------------------------------------------------
# 1. Update CSS: Responsive segments, underlabel modifier classes, popover z-index & backdrop
# ---------------------------------------------------------------------------
target_css_segments = """.path-chapter-segments {
    display: flex;
    gap: 4px;
    align-items: center;
  }
  .path-seg-bar {
    width: 22px;
    height: 8px;
    border-radius: 999px;
    background: rgba(190, 18, 60, 0.30);
    transition: background 0.2s ease, box-shadow 0.2s ease;
  }"""

new_css_segments = """.path-chapter-segments {
    display: flex;
    gap: 3px;
    align-items: center;
    flex: 1 1 auto;
    max-width: 200px;
    min-width: 0;
  }
  .path-seg-bar {
    flex: 1 1 0;
    min-width: 6px;
    max-width: 22px;
    height: 8px;
    border-radius: 999px;
    background: rgba(190, 18, 60, 0.30);
    transition: background 0.2s ease, box-shadow 0.2s ease;
  }"""

assert target_css_segments in content, "Error: target_css_segments not found"
content = content.replace(target_css_segments, new_css_segments, 1)
print("1.1 CSS: path-chapter-segments and path-seg-bar made responsive")

# 1.2 Update .path-chapter-count to avoid clipping
target_css_count = """.path-chapter-count {
    font-size: 0.78rem;
    font-weight: 800;
    color: #94a3b8;
    white-space: nowrap;
    margin-left: 4px;
  }"""

new_css_count = """.path-chapter-count {
    font-size: 0.78rem;
    font-weight: 800;
    color: #94a3b8;
    white-space: nowrap;
    margin-left: 4px;
    flex-shrink: 0;
  }
  .path-chapter-count .pcc-short {
    display: none;
  }
  @media (max-width: 480px) {
    .path-chapter-count .pcc-full { display: none !important; }
    .path-chapter-count .pcc-short { display: inline !important; }
  }"""

assert target_css_count in content, "Error: target_css_count not found"
content = content.replace(target_css_count, new_css_count, 1)
print("1.2 CSS: path-chapter-count responsive short/full added")

# 1.3 Add CSS for node underlabels modifiers
target_css_underlabels = """.hex-node-underlabel {
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 0.01em;
    fill: #97a1b2;
    stroke: rgba(13, 16, 22, 0.85);
    stroke-width: 3px;
    stroke-linejoin: round;
    paint-order: stroke;
    pointer-events: none;
  }
  html:not([data-theme="dark"]) .hex-node-underlabel {
    fill: #5a6678;
    stroke: rgba(250, 248, 245, 0.92);
  }"""

new_css_underlabels = """.hex-node-underlabel {
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 0.01em;
    fill: #97a1b2;
    stroke: rgba(13, 16, 22, 0.85);
    stroke-width: 3px;
    stroke-linejoin: round;
    paint-order: stroke;
    pointer-events: none;
    transition: fill 0.2s ease, font-size 0.2s ease;
  }
  html:not([data-theme="dark"]) .hex-node-underlabel {
    fill: #5a6678;
    stroke: rgba(250, 248, 245, 0.92);
  }
  .hex-node-underlabel--active {
    fill: #f8fafc !important;
    font-size: 11.5px !important;
    font-weight: 800 !important;
    letter-spacing: 0.02em;
    stroke: rgba(10, 13, 18, 0.95) !important;
    stroke-width: 3.5px !important;
    filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.85));
  }
  html:not([data-theme="dark"]) .hex-node-underlabel--active {
    fill: #0f172a !important;
    stroke: rgba(255, 255, 255, 0.95) !important;
  }
  .hex-node-underlabel--completed {
    fill: #e2e8f0 !important;
    font-weight: 700 !important;
  }
  html:not([data-theme="dark"]) .hex-node-underlabel--completed {
    fill: #1e293b !important;
  }
  .hex-node-underlabel--locked {
    fill: #64748b !important;
    opacity: 0.85;
  }"""

assert target_css_underlabels in content, "Error: target_css_underlabels not found"
content = content.replace(target_css_underlabels, new_css_underlabels, 1)
print("1.3 CSS: hex-node-underlabel status modifiers added")

# 1.4 Update Popover z-index and add Backdrop styling
target_popover_css = """  @media (max-width: 640px) {
    .path-popover {
      position: fixed !important;
      bottom: 0 !important;
      left: 0 !important;
      right: 0 !important;
      top: auto !important;
      width: 100% !important;
      max-width: 100% !important;
      transform: none !important;
      border-radius: 24px 24px 0 0 !important;
      padding: 20px 20px calc(24px + env(safe-area-inset-bottom, 16px)) 20px !important;
      box-shadow: 0 -12px 36px rgba(0, 0, 0, 0.6) !important;
      border-bottom: none !important;
      z-index: 1050 !important;
      animation: popoverSlideUp 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }"""

new_popover_css = """  .path-popover-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.65);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
    z-index: 100001;
    animation: popoverBackdropFade 0.2s ease-out;
  }
  @keyframes popoverBackdropFade {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  @media (max-width: 640px) {
    .path-popover {
      position: fixed !important;
      bottom: 0 !important;
      left: 0 !important;
      right: 0 !important;
      top: auto !important;
      width: 100% !important;
      max-width: 100% !important;
      transform: none !important;
      border-radius: 24px 24px 0 0 !important;
      padding: 20px 20px calc(24px + env(safe-area-inset-bottom, 16px)) 20px !important;
      box-shadow: 0 -12px 36px rgba(0, 0, 0, 0.6) !important;
      border-bottom: none !important;
      z-index: 100002 !important;
      animation: popoverSlideUp 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }"""

assert target_popover_css in content, "Error: target_popover_css not found"
content = content.replace(target_popover_css, new_popover_css, 1)
print("1.4 CSS: popover z-index updated to 100002 and backdrop CSS added")

# ---------------------------------------------------------------------------
# 2. Update INTERVIEW_ECHELONS: change police siren 🚨 to shield 🛡️
# ---------------------------------------------------------------------------
old_echelon1 = "1: { tier: 1, icon: '🚨', badgeClass: 'echelon-badge--t1', label: '🚨 Эшелон 1: Скрининг · Фундамент', shortLabel: '🚨 Эшелон 1: Скрининг'"
new_echelon1 = "1: { tier: 1, icon: '🛡️', badgeClass: 'echelon-badge--t1', label: '🛡️ Эшелон 1: Скрининг · Фундамент', shortLabel: '🛡️ Эшелон 1: Скрининг'"

assert old_echelon1 in content, "Error: old_echelon1 not found"
content = content.replace(old_echelon1, new_echelon1, 1)
print("2. INTERVIEW_ECHELONS echelon 1 icon updated to 🛡️")

# ---------------------------------------------------------------------------
# 3. Update chapterProgressLabel in viewPathSerpentine to support responsive pcc-full / pcc-short
# ---------------------------------------------------------------------------
old_cpl = """  const chapterProgressLabel = completedInChapter === 0
    ? `Начало · ${totalInChapter} ${pluralizeRu(totalInChapter, 'юнит', 'юнита', 'юнитов')}`
    : `${completedInChapter} из ${totalInChapter} сдано`;"""

new_cpl = """  const chapterProgressLabel = completedInChapter === 0
    ? `<span class="pcc-full">Начало · ${totalInChapter} ${pluralizeRu(totalInChapter, 'юнит', 'юнита', 'юнитов')}</span><span class="pcc-short">0 / ${totalInChapter}</span>`
    : `<span class="pcc-full">${completedInChapter} из ${totalInChapter} сдано</span><span class="pcc-short">${completedInChapter} / ${totalInChapter}</span>`;"""

assert old_cpl in content, "Error: old_cpl not found"
content = content.replace(old_cpl, new_cpl, 1)
print("3. chapterProgressLabel responsive HTML updated")

# ---------------------------------------------------------------------------
# 4. Add Backdrop HTML before #path-anchored-popover
# ---------------------------------------------------------------------------
old_popover_dom = """          <!-- Anchored Popover Modal -->
          <div id="path-anchored-popover" class="path-popover" style="display:none;" role="dialog" tabindex="-1" aria-labelledby="popover-title" aria-describedby="popover-status">"""

new_popover_dom = """          <!-- Anchored Popover Modal & Backdrop -->
          <div id="path-popover-backdrop" class="path-popover-backdrop" style="display:none;" aria-hidden="true"></div>
          <div id="path-anchored-popover" class="path-popover" style="display:none;" role="dialog" tabindex="-1" aria-labelledby="popover-title" aria-describedby="popover-status">"""

assert old_popover_dom in content, "Error: old_popover_dom not found"
content = content.replace(old_popover_dom, new_popover_dom, 1)
print("4. Backdrop DOM element added")

# ---------------------------------------------------------------------------
# 5. Update renderCoddyRightRail:
#    - Eliminate 0/45 -> show Chapter progress
#    - Eliminate 0% / "Осталось 32 темы" when not started -> show motivating START status
#    - Replace hardcoded fake radar numbers (85%, 40%, 0%) with real skill mastery
# ---------------------------------------------------------------------------
old_rail_func_start = """function renderCoddyRightRail(totalCompletedUnits, streakText, activeChapterNum){
  const chaptersMeta = getPathChaptersMeta(ALL_UNITS_COMBINED);
  const e1 = (typeof getEchelonProgress === 'function') ? getEchelonProgress(1) : null;
  const e1Pct = e1 ? e1.pct : 0;
  const e1Remaining = e1 ? e1.skills.filter(s => getSkillMP(s.id) < 100).length : 0;
  const dailyGoal = Math.max(1, Number(state.dailyGoal) || 50);
  const dailyXp = (typeof todayXp === 'function') ? todayXp() : 0;
  const dailyPct = Math.min(100, Math.round(dailyXp / dailyGoal * 100));
  const chaptersListHTML = chaptersMeta.map(ch => {
    const chCompleted = ch.units.filter(isUnitCompleted).length;
    const chPct = Math.round(chCompleted / ch.units.length * 100);
    const route = (typeof getTrackForUnit === 'function' && ch.units[0]) ? getTrackForUnit(ch.units[0].id).routePrefix : 'python';
    const isCurrent = (ch.num === activeChapterNum);
    return `
      <a class="crc-row ${isCurrent ? 'crc-row--current' : 'crc-row--compact'}" href="#/${route}" ${isCurrent ? 'aria-current="location"' : ''} title="Глава ${ch.num}: ${escapeHtmlStr(ch.title)} — перейти к модулю">
        <span class="crc-num">${ch.num}</span>
        <span class="crc-body">
          <span class="crc-title">${escapeHtmlStr(ch.title)}</span>
          ${isCurrent ? `<span class="crc-bar"><span class="crc-bar-fill" style="width:${chPct}%;"></span></span>` : ''}
        </span>
        <span class="crc-pct">${chCompleted}/${ch.units.length}</span>
      </a>`;
  }).join('');

  return `
    <aside class="coddy-right-rail">
      <!-- Top Stats Row (Coddy style) -->
      <div class="coddy-rail-stats-row">
        <div class="coddy-rail-stat" title="Пройдено юнитов">
          <span class="coddy-rail-stat-icon">📘</span>
          <span class="coddy-rail-stat-val">${totalCompletedUnits}/45</span>
        </div>
        <div class="coddy-rail-stat" title="Стрик активности">
          <span class="coddy-rail-stat-icon">🔥</span>
          <span class="coddy-rail-stat-val">${state.streak || 0} ${streakText}</span>
        </div>
        <div class="coddy-rail-stat" title="Накопленный опыт">
          <span class="coddy-rail-stat-icon">💎</span>
          <span class="coddy-rail-stat-val">${state.xp || 0} XP</span>
        </div>
      </div>

      <!-- Widget 1: Screening Readiness — мотивирующая графа «До 1-го скрининга %» (по ТЗ) -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-card-head">
          <div class="coddy-rail-badge">🎯 До 1-го скрининга</div>
          <a href="#/mock" class="coddy-rail-link">Симулятор →</a>
        </div>
        <div class="coddy-rail-meter">
          <span class="coddy-rail-meter-value">${e1Pct}%</span>
          <span class="meta">готовности к тех-скринингу</span>
        </div>
        <div class="cd-bar cd-bar-track" role="progressbar" aria-label="Готовность к техническому скринингу" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${e1Pct}"><div class="cd-fill cd-bar-fill" style="width:${Math.max(6, e1Pct)}%;"></div></div>
        <div class="meta" style="font-size:.75rem;margin-top:7px;">⏳ Осталось ${e1Remaining} ${pluralRuTopics(e1Remaining)} Эшелона 1</div>
      </div>

      <!-- Widget: Radar Screening Themes (Replaces duplicate chapter tree) -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-card-head">
          <div class="coddy-rail-badge">🎯 Радар скрининга</div>
          <span class="coddy-rail-link">14 тем</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:7px;margin-top:8px;">
          <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;">
            <span style="color:#f8fafc;">Сложность O(n) & срезы</span>
            <span style="color:var(--emerald);font-weight:700;">85%</span>
          </div>
          <div class="cd-bar cd-bar-track" style="height:4px;"><div class="cd-fill cd-bar-fill" style="width:85%;"></div></div>
          
          <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;margin-top:2px;">
            <span style="color:var(--ink-muted);">Хеш-таблицы & dict/set</span>
            <span style="color:var(--amber);font-weight:700;">40%</span>
          </div>
          <div class="cd-bar cd-bar-track" style="height:4px;"><div class="cd-fill cd-bar-fill" style="width:40%;background:var(--amber);"></div></div>

          <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;margin-top:2px;">
            <span style="color:var(--ink-muted);">SQL JOIN & индексы</span>
            <span style="color:var(--ink-muted);font-weight:600;">0%</span>
          </div>
          <div class="cd-bar cd-bar-track" style="height:4px;"><div class="cd-fill cd-bar-fill" style="width:0%;"></div></div>
        </div>
      </div>"""

new_rail_func_start = """function renderCoddyRightRail(totalCompletedUnits, streakText, activeChapterNum){
  const chaptersMeta = getPathChaptersMeta(ALL_UNITS_COMBINED);
  const e1 = (typeof getEchelonProgress === 'function') ? getEchelonProgress(1) : null;
  const e1Pct = e1 ? e1.pct : 0;
  const e1Remaining = e1 ? e1.skills.filter(s => getSkillMP(s.id) < 100).length : 0;
  const curChap = chaptersMeta.find(c => c.num === activeChapterNum) || chaptersMeta[0];
  const curChapCompleted = curChap ? curChap.units.filter(isUnitCompleted).length : 0;
  const curChapTotal = curChap ? curChap.units.length : 9;

  // Real dynamic mastery calculation for screening radar themes
  const r1Mp = (typeof getSkillMP === 'function') ? Math.round(getSkillMP('1.1.1')) : 0;
  const r2Mp = (typeof getSkillMP === 'function') ? Math.round(getSkillMP('1.1.2')) : 0;
  const r3Mp = (typeof getSkillMP === 'function') ? Math.round(getSkillMP('5.1.2')) : 0;

  const dailyGoal = Math.max(1, Number(state.dailyGoal) || 50);
  const dailyXp = (typeof todayXp === 'function') ? todayXp() : 0;
  const dailyPct = Math.min(100, Math.round(dailyXp / dailyGoal * 100));

  return `
    <aside class="coddy-right-rail">
      <!-- Top Stats Row (Coddy style) -->
      <div class="coddy-rail-stats-row">
        <div class="coddy-rail-stat" title="Пройдено в главе ${activeChapterNum}">
          <span class="coddy-rail-stat-icon">📘</span>
          <span class="coddy-rail-stat-val">Гл. ${activeChapterNum}: ${curChapCompleted}/${curChapTotal}</span>
        </div>
        <div class="coddy-rail-stat" title="Стрик активности">
          <span class="coddy-rail-stat-icon">🔥</span>
          <span class="coddy-rail-stat-val">${state.streak || 0} ${streakText}</span>
        </div>
        <div class="coddy-rail-stat" title="Накопленный опыт">
          <span class="coddy-rail-stat-icon">💎</span>
          <span class="coddy-rail-stat-val">${state.xp || 0} XP</span>
        </div>
      </div>

      <!-- Widget 1: Screening Readiness — мотивирующая графа «До 1-го скрининга %» (по ТЗ) -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-card-head">
          <div class="coddy-rail-badge">🎯 До 1-го скрининга</div>
          <a href="#/mock" class="coddy-rail-link">Симулятор →</a>
        </div>
        <div class="coddy-rail-meter">
          ${e1Pct > 0
            ? `<span class="coddy-rail-meter-value">${e1Pct}%</span><span class="meta">готовности к тех-скринингу</span>`
            : `<span class="coddy-rail-meter-value" style="font-size:1.35rem;color:var(--amber,#fbbf24);">СТАРТ</span><span class="meta">базовый тех-скрининг</span>`}
        </div>
        <div class="cd-bar cd-bar-track" role="progressbar" aria-label="Готовность к техническому скринингу" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${e1Pct}"><div class="cd-fill cd-bar-fill" style="width:${Math.max(8, e1Pct)}%;"></div></div>
        <div class="meta" style="font-size:.75rem;margin-top:7px;">${e1Pct > 0 ? `⏳ Освоено ${e1 ? e1.skills.filter(s => getSkillMP(s.id) >= 80).length : 0} из ${e1 ? e1.skills.length : 32} навыков Эшелона 1` : `🎯 Фундамент тех-скрининга · Глава ${activeChapterNum}`}</div>
      </div>

      <!-- Widget: Radar Screening Themes (Dynamic mastery from RemNote Knowledge Base) -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-card-head">
          <div class="coddy-rail-badge">🎯 Радар скрининга</div>
          <span class="coddy-rail-link">14 тем</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:7px;margin-top:8px;">
          <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;">
            <span style="color:${r1Mp > 0 ? '#f8fafc' : 'var(--ink-muted)'};">Сложность O(n) & срезы</span>
            <span style="color:${r1Mp > 0 ? 'var(--emerald)' : 'var(--ink-muted)'};font-weight:${r1Mp > 0 ? '700' : '600'};">${r1Mp > 0 ? r1Mp + '%' : 'Не начато'}</span>
          </div>
          <div class="cd-bar cd-bar-track" style="height:4px;"><div class="cd-fill cd-bar-fill" style="width:${r1Mp}%;"></div></div>
          
          <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;margin-top:2px;">
            <span style="color:${r2Mp > 0 ? '#f8fafc' : 'var(--ink-muted)'};">Хеш-таблицы & dict/set</span>
            <span style="color:${r2Mp > 0 ? 'var(--amber)' : 'var(--ink-muted)'};font-weight:${r2Mp > 0 ? '700' : '600'};">${r2Mp > 0 ? r2Mp + '%' : 'Не начато'}</span>
          </div>
          <div class="cd-bar cd-bar-track" style="height:4px;"><div class="cd-fill cd-bar-fill" style="width:${r2Mp}%;background:var(--amber);"></div></div>

          <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;margin-top:2px;">
            <span style="color:${r3Mp > 0 ? '#f8fafc' : 'var(--ink-muted)'};">SQL JOIN & индексы</span>
            <span style="color:${r3Mp > 0 ? 'var(--emerald)' : 'var(--ink-muted)'};font-weight:${r3Mp > 0 ? '700' : '600'};">${r3Mp > 0 ? r3Mp + '%' : 'Не начато'}</span>
          </div>
          <div class="cd-bar cd-bar-track" style="height:4px;"><div class="cd-fill cd-bar-fill" style="width:${r3Mp}%;"></div></div>
        </div>
      </div>"""

assert old_rail_func_start in content, "Error: old_rail_func_start not found"
content = content.replace(old_rail_func_start, new_rail_func_start, 1)
print("5. renderCoddyRightRail updated with dynamic radar and localized chapter progress")

# ---------------------------------------------------------------------------
# 6. Update Popover CTA route: target first uncompleted skill instead of [0]
# ---------------------------------------------------------------------------
old_popover_cta_assign = """        if(pCta){
          const unitStarted = (u.skills || []).some(s => (getSkillMP(s.id) || 0) > 0);
          pCta.className = isPassed ? 'btn-3d-emerald path-popover-cta' : (isLocked ? 'btn-3d-locked path-popover-cta' : 'btn-3d-orange path-popover-cta');
          pCta.textContent = isPassed ? 'ОБЗОР ➔' : (isLocked ? 'ЗАБЛОКИРОВАНО' : (unitStarted ? 'ПРОДОЛЖИТЬ ➔' : 'НАЧАТЬ ➔'));
          pCta.disabled = isLocked;
          pCta.setAttribute('data-target-route', `#${track.routePrefix}/skill/${(u.skills && u.skills[0]) ? u.skills[0].id : ''}`);
        }"""

new_popover_cta_assign = """        if(pCta){
          const unitStarted = (u.skills || []).some(s => (getSkillMP(s.id) || 0) > 0);
          pCta.className = isPassed ? 'btn-3d-emerald path-popover-cta' : (isLocked ? 'btn-3d-locked path-popover-cta' : 'btn-3d-orange path-popover-cta');
          pCta.textContent = isPassed ? 'ОБЗОР ➔' : (isLocked ? 'ЗАБЛОКИРОВАНО' : (unitStarted ? 'ПРОДОЛЖИТЬ ➔' : 'НАЧАТЬ ➔'));
          pCta.disabled = isLocked;
          const activeSkill = (u.skills || []).find(s => (getSkillMP(s.id) || 0) < 80) || (u.skills && u.skills[0]);
          const targetSkillId = activeSkill ? activeSkill.id : '';
          pCta.setAttribute('data-target-route', `#${track.routePrefix}/skill/${targetSkillId}`);
        }"""

assert old_popover_cta_assign in content, "Error: old_popover_cta_assign not found"
content = content.replace(old_popover_cta_assign, new_popover_cta_assign, 1)
print("6. Popover CTA target route dynamically points to next uncompleted skill")

# ---------------------------------------------------------------------------
# 7. Update Popover show/hide handlers to control Backdrop
# ---------------------------------------------------------------------------
old_popover_show = """        popover.style.display = 'block';
        if(openedByKeyboard && typeof popover.focus === 'function') popover.focus();"""

new_popover_show = """        popover.style.display = 'block';
        const backdropEl = document.getElementById('path-popover-backdrop');
        if(backdropEl && window.innerWidth <= 640){
          backdropEl.style.display = 'block';
        }
        if(openedByKeyboard && typeof popover.focus === 'function') popover.focus();"""

assert old_popover_show in content, "Error: old_popover_show not found"
content = content.replace(old_popover_show, new_popover_show, 1)
print("7.1 Popover show logic displays backdrop on mobile")

# 7.2 Close backdrop on close button, CTA, outside tap, Escape
old_popover_close = """  // Popover close and CTA button
  if(e.target.closest('#popover-close-btn')){
    const popover = document.getElementById('path-anchored-popover');
    if(popover){
      popover.style.display = 'none';
      const returnId = popover.getAttribute('data-return-focus-unit');
      const returnNode = Array.from(document.querySelectorAll('.hex-3d-node')).find(node => node.getAttribute('data-unit-id') === returnId);
      if(returnNode && typeof returnNode.focus === 'function') returnNode.focus();
    }
    return;
  }
  const popCta = e.target.closest('#popover-cta-btn');
  if(popCta){
    const tr = popCta.getAttribute('data-target-route');
    const popover = document.getElementById('path-anchored-popover');
    if(popover) popover.style.display = 'none';
    if(tr && !popCta.disabled){
      location.hash = tr;
    }
    return;
  }
  if(!e.target.closest('#path-anchored-popover') && !e.target.closest('.hex-3d-node')){
    const popover = document.getElementById('path-anchored-popover');
    if(popover && popover.style && popover.style.display !== 'none'){
      popover.style.display = 'none';
    }
  }"""

new_popover_close = """  // Popover backdrop tap closes mobile sheet
  if(e.target.closest('#path-popover-backdrop')){
    const popover = document.getElementById('path-anchored-popover');
    const backdrop = document.getElementById('path-popover-backdrop');
    if(popover) popover.style.display = 'none';
    if(backdrop) backdrop.style.display = 'none';
    return;
  }

  // Popover close and CTA button
  if(e.target.closest('#popover-close-btn')){
    const popover = document.getElementById('path-anchored-popover');
    const backdrop = document.getElementById('path-popover-backdrop');
    if(backdrop) backdrop.style.display = 'none';
    if(popover){
      popover.style.display = 'none';
      const returnId = popover.getAttribute('data-return-focus-unit');
      const returnNode = Array.from(document.querySelectorAll('.hex-3d-node')).find(node => node.getAttribute('data-unit-id') === returnId);
      if(returnNode && typeof returnNode.focus === 'function') returnNode.focus();
    }
    return;
  }
  const popCta = e.target.closest('#popover-cta-btn');
  if(popCta){
    const tr = popCta.getAttribute('data-target-route');
    const popover = document.getElementById('path-anchored-popover');
    const backdrop = document.getElementById('path-popover-backdrop');
    if(backdrop) backdrop.style.display = 'none';
    if(popover) popover.style.display = 'none';
    if(tr && !popCta.disabled){
      location.hash = tr;
    }
    return;
  }
  if(!e.target.closest('#path-anchored-popover') && !e.target.closest('.hex-3d-node') && !e.target.closest('#path-popover-backdrop')){
    const popover = document.getElementById('path-anchored-popover');
    const backdrop = document.getElementById('path-popover-backdrop');
    if(popover && popover.style && popover.style.display !== 'none'){
      popover.style.display = 'none';
      if(backdrop) backdrop.style.display = 'none';
    }
  }"""

assert old_popover_close in content, "Error: old_popover_close not found"
content = content.replace(old_popover_close, new_popover_close, 1)
print("7.2 Popover close logic hides backdrop on close, CTA, and backdrop tap")

# 7.3 Escape handler hides backdrop
old_escape = """    const popover = document.getElementById('path-anchored-popover');
    if(popover && popover.style && popover.style.display !== 'none'){
      popover.style.display = 'none';
      const returnId = popover.getAttribute('data-return-focus-unit');
      const returnNode = Array.from(document.querySelectorAll('.hex-3d-node')).find(node => node.getAttribute('data-unit-id') === returnId);
      if(returnNode && typeof returnNode.focus === 'function') returnNode.focus();
      return;
    }"""

new_escape = """    const popover = document.getElementById('path-anchored-popover');
    const backdrop = document.getElementById('path-popover-backdrop');
    if(backdrop) backdrop.style.display = 'none';
    if(popover && popover.style && popover.style.display !== 'none'){
      popover.style.display = 'none';
      const returnId = popover.getAttribute('data-return-focus-unit');
      const returnNode = Array.from(document.querySelectorAll('.hex-3d-node')).find(node => node.getAttribute('data-unit-id') === returnId);
      if(returnNode && typeof returnNode.focus === 'function') returnNode.focus();
      return;
    }"""

assert old_escape in content, "Error: old_escape not found"
content = content.replace(old_escape, new_escape, 1)
print("7.3 Escape handler hides backdrop")

# ---------------------------------------------------------------------------
# 8. Guard scroll listener against memory leaks
# ---------------------------------------------------------------------------
old_scroll_listener = """          window.addEventListener('scroll', updateJumpBtn, { passive: true });
          updateJumpBtn();"""

new_scroll_listener = """          if(!window._pathJumpScrollBound){
            window._pathJumpScrollBound = true;
            window.addEventListener('scroll', updateJumpBtn, { passive: true });
          }
          updateJumpBtn();"""

assert old_scroll_listener in content, "Error: old_scroll_listener not found"
content = content.replace(old_scroll_listener, new_scroll_listener, 1)
print("8. Jump button scroll listener guarded against duplicate registrations")

# ---------------------------------------------------------------------------
# Write updated content to academy.html
# ---------------------------------------------------------------------------
with open(academy_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"SUCCESS: academy.html updated successfully! New length: {len(content)}")
