import os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_path = os.path.join(root, 'academy.html')

with open(academy_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Original academy.html length:", len(content))

# 1. Update curY gap for chapter transitions
target_gap = """      curY += 115;
      if(chapterStartSet.has(i)){
        curY += 150; // Dedicated gap for Coddy Section Gate Card (Variant C)
      }"""

new_gap = """      curY += 115;
      if(chapterStartSet.has(i)){
        curY += 240; // Dedicated gap (+240px) for Mastery Challenge branch and Chapter Gate Card
      }"""

assert target_gap in content, "Error: target_gap not found"
content = content.replace(target_gap, new_gap, 1)
print("1. curY gap increased to +240px for chapter transitions")

# 2. Gate card cy positioning
target_cy = """        const prevY = coords[cb.startIdx - 1].y;
        const nextY = coords[cb.startIdx].y;
        const cy = Math.round((prevY + nextY) / 2);"""

new_cy = """        const prevY = coords[cb.startIdx - 1].y;
        const nextY = coords[cb.startIdx].y;
        // Position gate card with generous clearance (+180px) below the previous chapter's mastery challenge
        const cy = prevY + 180;"""

assert target_cy in content, "Error: target_cy not found"
content = content.replace(target_cy, new_cy, 1)
print("2. Gate card cy positioned cleanly at prevY + 180")

# 3. Subtext lock removal
target_subtext = """        let subText = '';
        if(isLocked){
          subText = `<text class="path-gate-sub" x="0" y="5" text-anchor="middle" font-size="10.5" font-weight="600" fill="#fda4af">🔒 ${cb.unitsCount} ${pluralizeRu(cb.unitsCount, 'юнит', 'юнита', 'юнитов')} · Откроется после «${escapeHtmlStr(prevCb.shortTitle)}»</text>`;
        }"""

new_subtext = """        let subText = '';
        if(isLocked){
          subText = `<text class="path-gate-sub" x="0" y="5" text-anchor="middle" font-size="10.5" font-weight="600" fill="#fda4af">${cb.unitsCount} ${pluralizeRu(cb.unitsCount, 'юнит', 'юнита', 'юнитов')} · Откроется после «${escapeHtmlStr(prevCb.shortTitle)}»</text>`;
        }"""

assert target_subtext in content, "Error: target_subtext not found"
content = content.replace(target_subtext, new_subtext, 1)
print("3. Subtext duplicate lock icon removed")

# 4. Gate card buttons terminology (РАЗДЕЛ -> ГЛАВА)
target_btn = """        let btnContent = '';
        if(isLocked){
          btnContent = `
            <g class="path-gate-btn path-gate-btn--locked" data-gate-track="${cb.track}" data-gate-locked="1" data-gate-prev-title="${escapeHtmlStr(prevCb.shortTitle)}" role="button" tabindex="0" aria-label="Раздел ${cb.chapterNum} заблокирован. Завершите темы «${escapeHtmlStr(prevCb.shortTitle)}»." aria-disabled="true">
              <rect x="-110" y="18" width="220" height="28" rx="14" fill="rgba(65, 12, 26, 0.75)" stroke="rgba(190, 18, 60, 0.55)" stroke-width="1.2"/>
              <text x="0" y="36" text-anchor="middle" font-size="10.5" font-weight="800" fill="#fda4af" letter-spacing="0.06em">🔒 РАЗДЕЛ ЗАКРЫТ</text>
            </g>`;
        } else {
          const btnLabel = isCurChapterDone ? 'ОБЗОР РАЗДЕЛА ➔' : 'ПЕРЕЙТИ К РАЗДЕЛУ ➔';
          btnContent = `
            <g class="path-gate-btn path-gate-btn--unlocked" data-gate-track="${cb.track}" data-gate-locked="0" role="button" tabindex="0" aria-label="Перейти к разделу ${cb.chapterNum}: ${escapeHtmlStr(cb.shortTitle)}" aria-keyshortcuts="Enter Space">
              <rect class="path-gate-btn-rect" x="-110" y="18" width="220" height="28" rx="14" fill="url(#hexGradCompleted)" stroke="rgba(52, 211, 153, 0.60)" stroke-width="1.2" filter="drop-shadow(0 4px 12px rgba(16,185,129,0.40))"/>
              <text x="0" y="36" text-anchor="middle" font-size="10.5" font-weight="900" fill="#ffffff" letter-spacing="0.06em">${btnLabel}</text>
            </g>`;
        }"""

new_btn = """        let btnContent = '';
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
        }"""

assert target_btn in content, "Error: target_btn not found"
content = content.replace(target_btn, new_btn, 1)
print("4. Gate card button labels and aria-labels unified to ГЛАВА")

# 5. Gate title terminology (РАЗДЕЛ -> ГЛАВА)
target_title = """            <text class="path-gate-title" x="0" y="-14" text-anchor="middle" font-size="12" font-weight="900" fill="#f8fafc" letter-spacing="0.08em">РАЗДЕЛ ${cb.chapterNum}: ${escapeHtmlStr(cb.shortTitle.toUpperCase())}</text>"""

new_title = """            <text class="path-gate-title" x="0" y="-14" text-anchor="middle" font-size="12" font-weight="900" fill="#f8fafc" letter-spacing="0.08em">ГЛАВА ${cb.chapterNum}: ${escapeHtmlStr(cb.shortTitle.toUpperCase())}</text>"""

assert target_title in content, "Error: target_title not found"
content = content.replace(target_title, new_title, 1)
print("5. Gate title updated to ГЛАВА")

# 6. Reposition Mastery Challenge branch
target_branch = """    const bx = Math.max(64, Math.min(356, x + (x >= 210 ? 66 : -66)));
    const by = y + 56;
    const chGrad = chDone ? 'url(#hexGradCompleted)' : (chStatus === 'open' ? 'url(#hexGradChallenge)' : 'url(#hexGradLocked)');
    const chButtonGrad = chDone ? 'url(#pathButtonCompleted)' : (chStatus === 'open' ? 'url(#pathButtonChallenge)' : 'url(#pathButtonLocked)');
    const chStroke = chDone ? 'rgba(255,255,255,0.3)' : (chStatus === 'open' ? 'rgba(251,113,133,0.6)' : 'rgba(148,163,184,0.28)');
    let chIcon = '';
    let chHalo = '';
    if(chDone){
      chIcon = `<text x="${bx}" y="${by+(usePawNodes?8:6)}" text-anchor="middle" font-size="${usePawNodes?15:16}" font-weight="900" fill="#ffffff">✓</text>`;
    } else if(chStatus === 'open'){
      chHalo = `<circle class="hex-challenge-pulse" cx="${bx}" cy="${by}" r="28" fill="none" stroke="rgba(190,18,60,0.55)"/>`;
      chIcon = trailIconCenter(bx, by + (usePawNodes?4:1), 'zap', usePawNodes?17:22, '#ffffff');
    } else {
      chIcon = trailIconCenter(bx, by + (usePawNodes?4:0), 'zap', usePawNodes?16:20, '#a9b3c3');
    }
    const challengeShape = usePawNodes
      ? trailPawShape(bx, by, chGrad, chStroke, chStatus === 'open' ? 1.8 : 1.3)
      : trailIsometricButton(bx, by, chButtonGrad, chStatus === 'open' ? 'rgba(253,164,175,0.9)' : 'rgba(203,213,225,0.42)', chStatus === 'open' ? 1.7 : 1.2);
    const challengeContent = usePawNodes ? chIcon : `<g class="path-button-icon">${chIcon}</g>`;
    const connectorStroke = chDone ? 'rgba(16,185,129,0.55)' : (chStatus === 'open' ? 'rgba(190,18,60,0.60)' : 'rgba(148,163,184,0.25)');

    branchesSVG += `
      <g class="hex-challenge-branch">
        <path d="M ${x},${y + 30} Q ${x},${(y + by) / 2} ${bx},${by - 22}" fill="none" stroke="${connectorStroke}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="1 8"/>
        <g class="hex-challenge-node hex-challenge-node--${chStatus}" data-challenge-route="#${track.routePrefix}/unittest/${u.id}" data-challenge-status="${chStatus}" data-cx="${bx}" data-cy="${by}" role="button" tabindex="0" aria-label="Челлендж мастерства, проверка юнита ${u.id}. ${chDone ? 'Пройдено' : (chUnlocked ? 'Доступно' : 'Заблокировано до прохождения предыдущих юнитов')}. Нажмите Enter или пробел, чтобы открыть." aria-keyshortcuts="Enter Space" aria-disabled="${chStatus === 'locked' ? 'true' : 'false'}">
          ${chHalo}
          <circle cx="${bx}" cy="${by}" r="24" fill="transparent" pointer-events="all"/>
          ${challengeShape}
          ${challengeContent}
          <text class="hex-branch-label" x="${bx}" y="${by + 44}" text-anchor="middle">ЧЕЛЛЕНДЖ<tspan x="${bx}" dy="13">МАСТЕРСТВА</tspan></text>
        </g>
      </g>`;"""

new_branch = """    const bx = Math.max(68, Math.min(352, x + (x >= 210 ? 70 : -70)));
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
      chIcon = trailIconCenter(bx, by + (usePawNodes?4:1), 'zap', usePawNodes?17:22, '#ffffff');
    } else {
      chIcon = trailIconCenter(bx, by + (usePawNodes?4:0), 'zap', usePawNodes?16:20, '#a9b3c3');
    }
    const challengeShape = usePawNodes
      ? trailPawShape(bx, by, chGrad, chStroke, chStatus === 'open' ? 1.8 : 1.3)
      : trailIsometricButton(bx, by, chButtonGrad, chStatus === 'open' ? 'rgba(253,164,175,0.9)' : 'rgba(203,213,225,0.42)', chStatus === 'open' ? 1.7 : 1.2);
    const challengeContent = usePawNodes ? chIcon : `<g class="path-button-icon">${chIcon}</g>`;
    const connectorStroke = chDone ? 'rgba(16,185,129,0.55)' : (chStatus === 'open' ? 'rgba(190,18,60,0.60)' : 'rgba(148,163,184,0.25)');

    branchesSVG += `
      <g class="hex-challenge-branch">
        <path d="M ${x},${y + 24} Q ${x},${(y + by) / 2} ${bx},${by - 20}" fill="none" stroke="${connectorStroke}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="1 8"/>
        <g class="hex-challenge-node hex-challenge-node--${chStatus}" data-challenge-route="#${track.routePrefix}/unittest/${u.id}" data-challenge-status="${chStatus}" data-cx="${bx}" data-cy="${by}" role="button" tabindex="0" aria-label="Челлендж мастерства, проверка юнита ${u.id}. ${chDone ? 'Пройдено' : (chUnlocked ? 'Доступно' : 'Заблокировано до прохождения предыдущих юнитов')}. Нажмите Enter или пробел, чтобы открыть." aria-keyshortcuts="Enter Space" aria-disabled="${chStatus === 'locked' ? 'true' : 'false'}">
          ${chHalo}
          <circle cx="${bx}" cy="${by}" r="24" fill="transparent" pointer-events="all"/>
          ${challengeShape}
          ${challengeContent}
          <text class="hex-branch-label" x="${bx}" y="${by + 36}" text-anchor="middle">ЧЕЛЛЕНДЖ<tspan x="${bx}" dy="12">МАСТЕРСТВА</tspan></text>
        </g>
      </g>`;"""

assert target_branch in content, "Error: target_branch not found"
content = content.replace(target_branch, new_branch, 1)
print("6. Mastery Challenge branch repositioned cleanly (by=y+36, bx=x+-70, label=by+36)")

# 7. Toast notification terminology in click listener
target_toast = """    const prevTitle = gateBtn.getAttribute('data-gate-prev-title') || 'предыдущего раздела';
    if(isLocked){
      if(typeof showTactileToast === 'function'){
        showTactileToast(`🔒 Завершите все темы «${prevTitle}», чтобы открыть этот раздел!`);
      }
      return;
    }"""

new_toast = """    const prevTitle = gateBtn.getAttribute('data-gate-prev-title') || 'предыдущей главы';
    if(isLocked){
      if(typeof showTactileToast === 'function'){
        showTactileToast(`🔒 Завершите все темы «${prevTitle}», чтобы открыть главу!`);
      }
      return;
    }"""

assert target_toast in content, "Error: target_toast not found"
content = content.replace(target_toast, new_toast, 1)
print("7. Toast message updated to главу")

# Save updated academy.html
with open(academy_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated academy.html! Length:", len(content))
