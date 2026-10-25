import os
import re

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_path = os.path.join(root, 'academy.html')

with open(academy_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Original length:", len(content))

# 1. Update CSS: Add Jump-btn hidden & mobile Bottom Sheet for popover
target_css_anchor = """.path-jump-btn:active {
    transform: translateY(1px);
  }"""

replacement_css = """.path-jump-btn:active {
    transform: translateY(1px);
  }
  .path-jump-btn.is-hidden {
    opacity: 0 !important;
    pointer-events: none !important;
    transform: scale(0.75) !important;
  }
  .path-jump-btn--up svg {
    transform: rotate(180deg);
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
      z-index: 1050 !important;
      animation: popoverSlideUp 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .path-popover-arrow {
      display: none !important;
    }
    .path-popover-close {
      width: 36px !important;
      height: 36px !important;
      font-size: 1.1rem !important;
    }
  }
  @keyframes popoverSlideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
  }"""

assert target_css_anchor in content, "Error: target_css_anchor not found"
content = content.replace(target_css_anchor, replacement_css, 1)
print("1. CSS updated successfully")

# 2. Update renderPathMobileStatsHTML to show chapter progress instead of 0/45
old_mobile_stats = """function renderPathMobileStatsHTML(totalCompletedUnits, streakText, curTier){
  const tierNum = curTier || 1;
  return `
    <div class="path-mobile-stats" role="status" aria-label="Статистика обучения">
      <span class="pms-item pms-echelon" title="Текущий эшелон подготовки">🎯 <b>Эшелон ${tierNum}</b></span>
      <span class="pms-item" title="Пройдено юнитов">📘 <b>${totalCompletedUnits}/45</b></span>
      <span class="pms-item" title="Стрик активности">🔥 <b>${state.streak || 0}</b> ${streakText}</span>
      <span class="pms-item" title="Накопленный опыт">💎 <b>${state.xp || 0} XP</b></span>
    </div>`;
}"""

new_mobile_stats = """function renderPathMobileStatsHTML(totalCompletedUnits, streakText, curTier, activeChapterNum, chapterCompleted, chapterTotal){
  const tierNum = curTier || 1;
  const chNum = activeChapterNum || 1;
  const chDone = (typeof chapterCompleted === 'number') ? chapterCompleted : 0;
  const chTot = (typeof chapterTotal === 'number') ? chapterTotal : 9;
  return `
    <div class="path-mobile-stats" role="status" aria-label="Статистика обучения">
      <span class="pms-item pms-echelon" title="Текущий эшелон подготовки">🎯 <b>Эшелон ${tierNum}</b></span>
      <span class="pms-item" title="Пройдено в главе ${chNum}">📘 <b>Гл. ${chNum}: ${chDone}/${chTot}</b></span>
      <span class="pms-item" title="Стрик активности">🔥 <b>${state.streak || 0}</b> ${streakText}</span>
      <span class="pms-item" title="Накопленный опыт">💎 <b>${state.xp || 0} XP</b></span>
    </div>`;
}"""

assert old_mobile_stats in content, "Error: old_mobile_stats not found"
content = content.replace(old_mobile_stats, new_mobile_stats, 1)
print("2. renderPathMobileStatsHTML updated successfully")

# 3. Remove duplicate SRS widget in renderCoddyRightRail
duplicate_srs = """      <!-- Widget 2: SRS Cards Review (compact one-row card) -->
      <div class="panel coddy-rail-card coddy-rail-card--row">
        <div class="coddy-rail-badge">🃏 Повторение карточек</div>
        <a href="#/cards" class="coddy-rail-link">Повторить →</a>
      </div>"""

if duplicate_srs in content:
    content = content.replace(duplicate_srs, "", 1)
    print("3. Duplicate SRS widget removed from renderCoddyRightRail")
else:
    print("3. Duplicate SRS widget not found or already removed")

# 4. Add semantic icon helper function before viewPathSerpentine
semantic_icons_fn = """// Семантический маппинг иконок узлов тропы по темам юнитов
function getSemanticTrailIcon(u, i, isChapterLast){
  if(isChapterLast) return 'trophy';
  if(!u) return 'star';
  const uid = String(u.id);
  const map = {
    '1.1': 'terminal', '1.2': 'code', '1.3': 'zap', '1.4': 'layers', '1.5': 'layers', '1.6': 'shield', '1.7': 'wrench', '1.8': 'zap', '1.9': 'terminal',
    '2.1': 'globe', '2.2': 'globe', '2.3': 'code', '2.4': 'shield',
    '3.1': 'terminal', '3.2': 'layers', '3.3': 'code', '3.4': 'code', '3.5': 'shield', '3.6': 'layers', '3.7': 'zap', '3.8': 'cloud',
    '4.1': 'zap', '4.2': 'branch', '4.3': 'layers', '4.4': 'database', '4.5': 'branch', '4.6': 'star',
    '5.1': 'database', '5.2': 'database', '5.3': 'database', '5.4': 'shield', '5.5': 'layers', '5.6': 'zap',
    '6.1': 'shield', '6.2': 'layers', '6.3': 'layers', '6.4': 'book', '6.5': 'layers', '6.6': 'cloud',
    '7.1': 'branch', '7.2': 'cloud', '7.3': 'cloud', '7.4': 'wrench', '7.5': 'terminal', '7.6': 'wrench'
  };
  return map[uid] || 'star';
}

"""

target_view_path = "function viewPathSerpentine(options){"
assert target_view_path in content, "Error: target_view_path not found"
content = content.replace(target_view_path, semantic_icons_fn + target_view_path, 1)
print("4. getSemanticTrailIcon added")

# 5. In viewPathSerpentine: update screening badge label & chapterProgressLabel
old_banner_code = """  const chapterProgressLabel = completedInChapter === 0
    ? `Начни · ${totalInChapter}`
    : `${completedInChapter} / ${totalInChapter}`;"""

new_banner_code = """  const chapterProgressLabel = completedInChapter === 0
    ? `Начало · ${totalInChapter} ${pluralizeRu(totalInChapter, 'юнит', 'юнита', 'юнитов')}`
    : `${completedInChapter} из ${totalInChapter} сдано`;"""

assert old_banner_code in content, "Error: old_banner_code not found"
content = content.replace(old_banner_code, new_banner_code, 1)
print("5. chapterProgressLabel updated")

# 6. Update screening badge label in banner
old_screening = """<span class="path-screening-badge" title="Готовность к 1-му техническому скринингу">⚡ Готовность к тех-скринингу: ${e1PctTop}%</span>"""
new_screening = """<span class="path-screening-badge" title="Готовность к 1-му техническому скринингу">${e1PctTop > 0 ? `⚡ Готовность к тех-скринингу: ${e1PctTop}%` : '⚡ Старт тех-скрининга · База'}</span>"""

assert old_screening in content, "Error: old_screening not found"
content = content.replace(old_screening, new_screening, 1)
print("6. screening badge label updated")

# 7. Update renderPathMobileStatsHTML invocation in viewPathSerpentine
old_render_mobile_stats_call = "${renderPathMobileStatsHTML(totalCompletedUnits, streakText, curActiveUnit.tier || 1)}"
new_render_mobile_stats_call = "${renderPathMobileStatsHTML(totalCompletedUnits, streakText, curActiveUnit.tier || 1, activeChapterNum, completedInChapter, totalInChapter)}"

assert old_render_mobile_stats_call in content, "Error: old_render_mobile_stats_call not found"
content = content.replace(old_render_mobile_stats_call, new_render_mobile_stats_call, 1)
print("7. renderPathMobileStatsHTML call updated")

# 8. Use getSemanticTrailIcon and add Radial Progress Ring + showUnderLabel logic
old_node_loop_start = """    let centerIcon = '';
    let pulseHalo = '';
    let activeBubble = '';
    const cbIdx = chapterBreakpoints.reduce((acc, cb, ci) => (i >= cb.startIdx ? ci : acc), 0);
    const iconSet = TRAIL_CHAPTER_ICONS[cbIdx] || TRAIL_CHAPTER_ICONS[0];
    const iconName = chapterLastIdxSet.has(i) ? 'trophy' : iconSet[(i - chapterBreakpoints[cbIdx].startIdx) % iconSet.length];
    if(isCompleted){
      centerIcon = `<text x="${x}" y="${y+(usePawNodes?10:7)}" text-anchor="middle" font-size="${usePawNodes?18:22}" font-weight="900" fill="#ffffff">✓</text>`;
    } else if(isActive){
      pulseHalo = `<circle class="hex-pulse-halo" cx="${x}" cy="${y}" r="40" fill="none" stroke="rgba(245, 158, 11, 0.6)"/>`;
      centerIcon = trailIconCenter(x, y + (usePawNodes ? 5 : 1), iconName, usePawNodes ? 20 : 26, '#ffffff');
      const unitStarted = (u.skills || []).some(s => (getSkillMP(s.id) || 0) > 0);
      const bubbleTxt = unitStarted ? 'ПРОДОЛЖИТЬ' : 'НАЧАТЬ';
      const bubbleW = unitStarted ? 104 : 72;
      const bubbleY = y - 44;
      activeBubble = `
        <g class="hex-active-tooltip" transform="translate(${x}, ${bubbleY})">
          <g class="hex-active-tooltip__inner">
            <rect x="${-bubbleW/2}" y="-16" width="${bubbleW}" height="22" rx="11" fill="#ff7a00" filter="drop-shadow(0 4px 10px rgba(255,122,0,0.45))"/>
            <polygon points="-5,6 5,6 0,11" fill="#ff7a00"/>
            <text x="0" y="-1" text-anchor="middle" font-size="10.5" font-weight="900" fill="#ffffff" letter-spacing="0.08em">${bubbleTxt}</text>
          </g>
        </g>`;
    } else {
      centerIcon = trailIconCenter(x, y + (usePawNodes ? 5 : 0), iconName, usePawNodes ? 18 : 24, '#a9b3c3');
    }

    const nodeShape = usePawNodes
      ? trailPawShape(x, y, topGrad, strokeColor, strokeWidth)
      : trailIsometricButton(x, y, buttonGrad, isActive ? 'rgba(255,230,160,0.95)' : (isCompleted ? 'rgba(167,243,208,0.75)' : 'rgba(203,213,225,0.42)'), isActive ? 1.8 : 1.3);

    const buttonContent = usePawNodes ? centerIcon : `<g class="path-button-icon">${centerIcon}</g>`;
    // Подпись темы под активным узлом и двумя следующими (видно «что дальше» без клика)
    const showUnderLabel = (i >= activeUnitIndex && i <= activeUnitIndex + 2);"""

new_node_loop_start = """    let centerIcon = '';
    let pulseHalo = '';
    let activeBubble = '';
    let radialProgressRing = '';
    const cbIdx = chapterBreakpoints.reduce((acc, cb, ci) => (i >= cb.startIdx ? ci : acc), 0);
    const isChapterLast = chapterLastIdxSet.has(i);
    const iconName = getSemanticTrailIcon(u, i, isChapterLast);

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
      const bubbleTxt = unitStarted ? (unitProgPct > 0 ? `ПРОДОЛЖИТЬ · ${unitSkillsMastered}/${unitTotalSkills}` : 'ПРОДОЛЖИТЬ') : 'НАЧАТЬ';
      const bubbleW = unitStarted ? (unitProgPct > 0 ? 128 : 104) : 72;
      const bubbleY = y - 44;
      activeBubble = `
        <g class="hex-active-tooltip" transform="translate(${x}, ${bubbleY})">
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
    // Подпись темы: отображаем для всех юнитов текущей главы, пройденных и 3 ближайших вперед
    const inCurrentChapter = (cbIdx === chapterBreakpoints.findIndex(cb => cb.chapterNum === activeChapterNum));
    const showUnderLabel = inCurrentChapter || (i <= activeUnitIndex + 3) || isCompleted;"""

assert old_node_loop_start in content, "Error: old_node_loop_start not found"
content = content.replace(old_node_loop_start, new_node_loop_start, 1)
print("8. Node loop (semantic icons, radial ring, underlabels) updated")

# 9. Insert radialProgressRing into nodesSVG
old_node_svg = """      <g class="hex-3d-node hex-node--${status}" data-unit-id="${u.id}" data-node-idx="${i}" data-cx="${x}" data-cy="${y}" role="button" tabindex="0" aria-label="${escapeHtmlStr(nodeAccessibleLabel)}" aria-keyshortcuts="Enter Space ArrowUp ArrowDown Home End" title="${escapeHtmlStr(nodeAccessibleLabel)}">
        ${pulseHalo}
        <circle cx="${x}" cy="${y}" r="34" fill="transparent" pointer-events="all"/>
        ${nodeShape}
        ${buttonContent}
        ${showUnderLabel ? `<text class="hex-node-underlabel" x="${underLabelX}" y="${y + 52}" text-anchor="${underLabelAnchor}">${escapeHtmlStr(shortTitle)}</text>` : ''}
        ${activeBubble}
      </g>"""

new_node_svg = """      <g class="hex-3d-node hex-node--${status}" data-unit-id="${u.id}" data-node-idx="${i}" data-cx="${x}" data-cy="${y}" role="button" tabindex="0" aria-label="${escapeHtmlStr(nodeAccessibleLabel)}" aria-keyshortcuts="Enter Space ArrowUp ArrowDown Home End" title="${escapeHtmlStr(nodeAccessibleLabel)}">
        ${pulseHalo}
        ${radialProgressRing}
        <circle cx="${x}" cy="${y}" r="34" fill="transparent" pointer-events="all"/>
        ${nodeShape}
        ${buttonContent}
        ${showUnderLabel ? `<text class="hex-node-underlabel hex-node-underlabel--${status}" x="${underLabelX}" y="${y + 52}" text-anchor="${underLabelAnchor}">${status === 'locked' ? '🔒 ' : ''}${escapeHtmlStr(shortTitle)}</text>` : ''}
        ${activeBubble}
      </g>"""

assert old_node_svg in content, "Error: old_node_svg not found"
content = content.replace(old_node_svg, new_node_svg, 1)
print("9. nodesSVG updated with radial ring and locked icon")

# 10. Enrich popover metadata and add Haptics
old_popover_skills = """        if(pSkills){
          const skillItems = (u.skills || []).slice(0, 3);
          pSkills.innerHTML = skillItems.length
            ? `<div class="path-popover-skills-label">В этом юните</div><div class="path-popover-skills-list">${skillItems.map(s => `<div class="path-popover-skill">${escapeHtmlStr(s.title)}</div>`).join('')}</div>`
            : '';
        }"""

new_popover_skills = """        if(pSkills){
          const skillItems = (u.skills || []).slice(0, 3);
          const noteCount = (u.skills || []).reduce((acc, s) => acc + (s.kIds ? s.kIds.length : 1), 0);
          pSkills.innerHTML = skillItems.length
            ? `<div class="path-popover-meta-row" style="font-size:0.75rem;color:var(--ink-muted);margin-bottom:8px;display:flex;gap:12px;"><span>📚 <b>${noteCount}</b> тем-конспектов</span><span>🎯 <b>${(u.skills||[]).length}</b> навыков</span></div><div class="path-popover-skills-label">Ключевые навыки юнита:</div><div class="path-popover-skills-list">${skillItems.map(s => `<div class="path-popover-skill">${escapeHtmlStr(s.title)}</div>`).join('')}</div>`
            : '';
        }"""

assert old_popover_skills in content, "Error: old_popover_skills not found"
content = content.replace(old_popover_skills, new_popover_skills, 1)
print("10. Popover skills enriched with note count")

# 11. Add Haptic feedback on node click
old_hex_click = """  // 3D Serpentine Path node click (Open anchored popover)
  const hexNode = e.target.closest('.hex-3d-node');
  if(hexNode){"""

new_hex_click = """  // 3D Serpentine Path node click (Open anchored popover)
  const hexNode = e.target.closest('.hex-3d-node');
  if(hexNode){
    if(typeof navigator !== 'undefined' && navigator.vibrate){
      try{ navigator.vibrate(10); }catch(vErr){}
    }"""

assert old_hex_click in content, "Error: old_hex_click not found"
content = content.replace(old_hex_click, new_hex_click, 1)
print("11. Haptic vibration added to hexNode click")

# 12. Smart Jump-to-Active Button logic
old_jump_click = """  // Jump to active unit button
  if(e.target.closest('#path-jump-btn')){
    const targetNode = document.querySelector('.hex-node--active') || document.querySelector('.hex-3d-node');
    if(targetNode){
      targetNode.scrollIntoView({ behavior: 'smooth', block: 'center' });
      try{ targetNode.focus(); }catch(err){}
    }
    return;
  }"""

new_jump_click = """  // Jump to active unit button (with haptics and smooth scroll)
  if(e.target.closest('#path-jump-btn')){
    if(typeof navigator !== 'undefined' && navigator.vibrate){
      try{ navigator.vibrate(12); }catch(vErr){}
    }
    const targetNode = document.querySelector('.hex-node--active') || document.querySelector('.hex-3d-node');
    if(targetNode){
      targetNode.scrollIntoView({ behavior: 'smooth', block: 'center' });
      try{ targetNode.focus(); }catch(err){}
    }
    return;
  }"""

assert old_jump_click in content, "Error: old_jump_click not found"
content = content.replace(old_jump_click, new_jump_click, 1)
print("12. Jump button click updated with haptics")

# 13. Auto-update jump button visibility on scroll
old_scroll_mount = """    // V12: активная нода тропы не должна оставаться под таб-баром — мягкий автоскролл к ней
    setTimeout(function(){
      try{
        const activeNode = document.querySelector('.hex-node--active');
        if(activeNode && typeof activeNode.scrollIntoView === 'function'){
          const r = activeNode.getBoundingClientRect();
          if(r.top < 90 || r.bottom > (window.innerHeight || 800) - 110){
            activeNode.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }
      }catch(err){}
    }, 60);"""

new_scroll_mount = """    // V12: активная нода тропы не должна оставаться под таб-баром — мягкий автоскролл к ней
    setTimeout(function(){
      try{
        const activeNode = document.querySelector('.hex-node--active');
        if(activeNode && typeof activeNode.scrollIntoView === 'function'){
          const r = activeNode.getBoundingClientRect();
          if(r.top < 90 || r.bottom > (window.innerHeight || 800) - 110){
            activeNode.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }
        // Умная плавающая кнопка прыжка к активному уроку
        const jumpBtn = document.getElementById('path-jump-btn');
        if(jumpBtn && activeNode){
          const updateJumpBtn = function(){
            const rect = activeNode.getBoundingClientRect();
            const vh = window.innerHeight || 800;
            const isVisible = (rect.top >= 60 && rect.bottom <= vh - 60);
            if(isVisible){
              jumpBtn.classList.add('is-hidden');
            } else {
              jumpBtn.classList.remove('is-hidden');
              if(rect.top < 60){
                jumpBtn.classList.add('path-jump-btn--up');
                jumpBtn.title = 'Вернуться к текущему уроку (вверх)';
              } else {
                jumpBtn.classList.remove('path-jump-btn--up');
                jumpBtn.title = 'Перейти к текущему уроку (вниз)';
              }
            }
          };
          window.addEventListener('scroll', updateJumpBtn, { passive: true });
          updateJumpBtn();
        }
      }catch(err){}
    }, 60);"""

assert old_scroll_mount in content, "Error: old_scroll_mount not found"
content = content.replace(old_scroll_mount, new_scroll_mount, 1)
print("13. Smart jump button scroll observer added")

with open(academy_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying all 13 descriptor improvements to academy.html!")
