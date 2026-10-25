import os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_path = os.path.join(root, 'academy.html')

with open(academy_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Original academy.html length:", len(content))

# 1. Update Mastery Challenge branch connector line visibility & stroke
target_branch_connector = """    const challengeContent = usePawNodes ? chIcon : `<g class="path-button-icon">${chIcon}</g>`;
    const connectorStroke = chDone ? 'rgba(16,185,129,0.55)' : (chStatus === 'open' ? 'rgba(190,18,60,0.60)' : 'rgba(148,163,184,0.25)');

    branchesSVG += `
      <g class="hex-challenge-branch">
        <path d="M ${x},${y + 24} Q ${x},${(y + by) / 2} ${bx},${by - 20}" fill="none" stroke="${connectorStroke}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="1 8"/>"""

new_branch_connector = """    const challengeContent = usePawNodes ? chIcon : `<g class="path-button-icon">${chIcon}</g>`;
    const connectorStroke = chDone ? 'rgba(52,211,153,0.80)' : (chStatus === 'open' ? 'rgba(251,113,133,0.85)' : 'rgba(148,163,184,0.48)');

    branchesSVG += `
      <g class="hex-challenge-branch">
        <path d="M ${x},${y + 24} Q ${x},${(y + by) / 2} ${bx},${by - 20}" fill="none" stroke="${connectorStroke}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="3 4"/>"""

assert target_branch_connector in content, "Error: target_branch_connector not found"
content = content.replace(target_branch_connector, new_branch_connector, 1)
print("1. [PASS] Mastery challenge branch connector made clearly visible with stroke-dasharray 3 4 and higher contrast.")

# 2. Update Mastery Challenge node icon to Trophy (instead of Zap)
target_ch_icon = """    let chIcon = '';
    let chHalo = '';
    if(chDone){
      chIcon = `<text x="${bx}" y="${by+(usePawNodes?8:6)}" text-anchor="middle" font-size="${usePawNodes?15:16}" font-weight="900" fill="#ffffff">✓</text>`;
    } else if(chStatus === 'open'){
      chHalo = `<circle class="hex-challenge-pulse" cx="${bx}" cy="${by}" r="28" fill="none" stroke="rgba(190,18,60,0.55)"/>`;
      chIcon = trailIconCenter(bx, by + (usePawNodes?4:1), 'zap', usePawNodes?17:22, '#ffffff');
    } else {
      chIcon = trailIconCenter(bx, by + (usePawNodes?4:0), 'zap', usePawNodes?16:20, '#a9b3c3');
    }"""

new_ch_icon = """    let chIcon = '';
    let chHalo = '';
    if(chDone){
      chIcon = `<text x="${bx}" y="${by+(usePawNodes?8:6)}" text-anchor="middle" font-size="${usePawNodes?15:16}" font-weight="900" fill="#ffffff">✓</text>`;
    } else if(chStatus === 'open'){
      chHalo = `<circle class="hex-challenge-pulse" cx="${bx}" cy="${by}" r="28" fill="none" stroke="rgba(190,18,60,0.55)"/>`;
      chIcon = trailIconCenter(bx, by + (usePawNodes?4:1), 'trophy', usePawNodes?17:22, '#ffffff');
    } else {
      chIcon = trailIconCenter(bx, by + (usePawNodes?4:0), 'trophy', usePawNodes?16:20, '#a9b3c3');
    }"""

assert target_ch_icon in content, "Error: target_ch_icon not found"
content = content.replace(target_ch_icon, new_ch_icon, 1)
print("2. [PASS] Mastery challenge node icon updated to trophy.")

# 3. Semantic Icon for Unit 1.9 (Tools) and units in getSemanticTrailIcon
target_sem_icon = """// Семантический маппинг иконок узлов тропы по темам юнитов
function getSemanticTrailIcon(u, i, isChapterLast){
  if(isChapterLast) return 'trophy';
  if(!u) return 'star';
  const uid = String(u.id);
  const map = {
    '1.1': 'terminal', '1.2': 'code', '1.3': 'zap', '1.4': 'layers', '1.5': 'layers', '1.6': 'shield', '1.7': 'wrench', '1.8': 'zap', '1.9': 'terminal',"""

new_sem_icon = """// Семантический маппинг иконок узлов тропы по темам юнитов (челлендж-трофей вынесен в боковую ветку)
function getSemanticTrailIcon(u, i, isChapterLast){
  if(!u) return 'star';
  const uid = String(u.id);
  const map = {
    '1.1': 'terminal', '1.2': 'code', '1.3': 'zap', '1.4': 'layers', '1.5': 'layers', '1.6': 'shield', '1.7': 'wrench', '1.8': 'zap', '1.9': 'wrench',"""

assert target_sem_icon in content, "Error: target_sem_icon not found"
content = content.replace(target_sem_icon, new_sem_icon, 1)
print("3. [PASS] getSemanticTrailIcon updated: unit 1.9 gets wrench, trophy preserved for challenge.")

# 4. Underlabel centering and visibility for all 45 units
target_underlabel = """    // Подпись темы: отображаем для всех юнитов текущей главы, пройденных и 3 ближайших вперед
    const inCurrentChapter = (cbIdx === chapterBreakpoints.findIndex(cb => cb.chapterNum === activeChapterNum));
    const showUnderLabel = inCurrentChapter || (i <= activeUnitIndex + 3) || isCompleted;
    const underTitleFull = cleanUnitTitle(u.id, u.title);
    const shortTitle = (underTitleFull.length > 24) ? underTitleFull.slice(0, 22) + '…' : underTitleFull;
    // у финишных юнитов главы снизу-сбоку висит ветка челленджа — уводим подпись в противоположную сторону
    const hasBranchBelow = chapterLastIdxSet.has(i);
    const branchDir = (x >= 210) ? 1 : -1;
    const underLabelX = hasBranchBelow ? (x - branchDir * 44) : x;
    const underLabelAnchor = hasBranchBelow ? (branchDir === 1 ? 'end' : 'start') : 'middle';"""

new_underlabel = """    // Подпись темы: отображаем для всех 45 юнитов (с замком 🔒 для закрытых) ради целостности карты
    const showUnderLabel = true;
    const underTitleFull = cleanUnitTitle(u.id, u.title);
    const shortTitle = (underTitleFull.length > 24) ? underTitleFull.slice(0, 22) + '…' : underTitleFull;
    // Подпись всегда центрируется строго под гексагоном (зазор между главами 240px обеспечивает чистый воздух)
    const underLabelX = x;
    const underLabelAnchor = 'middle';"""

assert target_underlabel in content, "Error: target_underlabel not found"
content = content.replace(target_underlabel, new_underlabel, 1)
print("4. [PASS] All 45 units have visible titles and labels are strictly centered.")

# 5. Top Chapter Banner Breadcrumb compact formatting (no bloated tier label)
target_breadcrumb = """              <div class="path-chapter-breadcrumb">
                <span class="path-echelon-pill echelon-pill--t${curActiveUnit.tier || 1}">${curActiveUnit.tierLabel || `Эшелон ${curActiveUnit.tier || 1}`}</span>
                <span class="path-crumb-sep">›</span>
                <span>ГЛАВА ${activeChapterNum}</span>
                <span class="path-screening-badge" title="Готовность к 1-му техническому скринингу">${e1PctTop > 0 ? `⚡ Готовность к тех-скринингу: ${e1PctTop}%` : '⚡ Старт тех-скрининга · База'}</span>
              </div>"""

new_breadcrumb = """              <div class="path-chapter-breadcrumb">
                <span class="path-echelon-pill echelon-pill--t${curActiveUnit.tier || 1}">${(typeof INTERVIEW_ECHELONS !== 'undefined' && INTERVIEW_ECHELONS[curActiveUnit.tier] && INTERVIEW_ECHELONS[curActiveUnit.tier].shortLabel) || `Эшелон ${curActiveUnit.tier || 1}`}</span>
                <span class="path-crumb-sep">›</span>
                <span class="path-chapter-crumb-label">ГЛАВА ${activeChapterNum}</span>
                <span class="path-screening-badge" title="Готовность к 1-му техническому скринингу">${e1PctTop > 0 ? `⚡ Готовность к тех-скринингу: ${e1PctTop}%` : '⚡ Старт тех-скрининга · База'}</span>
              </div>"""

assert target_breadcrumb in content, "Error: target_breadcrumb not found"
content = content.replace(target_breadcrumb, new_breadcrumb, 1)
print("5. [PASS] Breadcrumb compact echelon shortLabel implemented.")

# 6. Contextual SRS Queue Widget in Right Rail (no premature advanced cards)
target_srs = """      <!-- Widget: SRS Flashcards Queue -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-card-head">
          <div class="coddy-rail-badge">🧠 Очередь SRS</div>
          <a href="#/cards" class="coddy-rail-link">12 карточек →</a>
        </div>
        <div style="font-size:0.78rem;color:var(--ink-muted);line-height:1.45;margin-top:6px;">
          Интервальное повторение ключевых определений перед собеседованием: <span style="color:#f8fafc;font-weight:600;">GIL, MRO, Дескрипторы</span>.
        </div>
      </div>"""

new_srs = """      <!-- Widget: SRS Flashcards Queue (Contextual based on learner progress) -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-card-head">
          <div class="coddy-rail-badge">🧠 Очередь SRS</div>
          <a href="#/cards" class="coddy-rail-link">${totalCompletedUnits === 0 ? 'Колоды →' : '12 карточек →'}</a>
        </div>
        <div style="font-size:0.78rem;color:var(--ink-muted);line-height:1.45;margin-top:6px;">
          ${totalCompletedUnits === 0
            ? 'Очередь повторения пуста. Освойте первый юнит, чтобы активировать карточки интервального повторения к скринингу.'
            : 'Интервальное повторение ключевых определений перед собеседованием: <span style="color:#f8fafc;font-weight:600;">Синтаксис, структуры данных</span>.'}
        </div>
      </div>"""

assert target_srs in content, "Error: target_srs not found"
content = content.replace(target_srs, new_srs, 1)
print("7. [PASS] Contextual SRS Queue Widget implemented.")

# 7. Mobile FAB Jump Button bottom offset & breadcrumb styling
target_fab_css = """  @media (max-width: 768px) {
    .path-jump-btn {
      bottom: calc(84px + env(safe-area-inset-bottom, 16px));
      right: 16px;
      width: 42px;
      height: 42px;
    }"""

new_fab_css = """  .path-crumb-sep {
    color: var(--ink-muted, #64748b);
    font-size: 0.72rem;
  }
  .path-chapter-crumb-label {
    font-size: 0.72rem;
    font-weight: 800;
    color: var(--ink-soft, #cbd5e1);
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }
  @media (max-width: 768px) {
    .path-jump-btn {
      bottom: calc(96px + env(safe-area-inset-bottom, 16px));
      right: 16px;
      width: 42px;
      height: 42px;
    }"""

assert target_fab_css in content, "Error: target_fab_css not found"
content = content.replace(target_fab_css, new_fab_css, 1)
print("8. [PASS] FAB Jump button bottom clearance increased to 96px, crumb styles added.")

# Save updated academy.html
with open(academy_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated academy.html! Final length:", len(content))
