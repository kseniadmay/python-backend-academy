import re

ACADEMY_PATH = '/Users/fury/OneDrive/Python_Backend_Academy/academy.html'
ETALON1_PATH = '/Users/fury/OneDrive/Python_Backend_Academy/Эталоны.html'
ETALON2_PATH = '/Users/fury/OneDrive/Python_Backend_Academy/Эталоны/Эталоны.html'

with open(ACADEMY_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add .echelon-title-group class to echelon title container
target_echelon_group = '''        <!-- Ряд 1: Звание и эшелон слева, аудио-компаньон справа -->
        <div class="echelon-topbar-row-top" style="display:flex;justify-content:space-between;align-items:center;width:100%;gap:10px;">
          <div style="display:flex;align-items:baseline;gap:10px;min-width:0;flex-wrap:wrap;">
            <h1 class="rank-title-glow echelon-bordeaux-title" style="margin:0;font-size:1.24rem;">${readinessRank}</h1>'''

replacement_echelon_group = '''        <!-- Ряд 1: Звание и эшелон слева, аудио-компаньон справа -->
        <div class="echelon-topbar-row-top" style="display:flex;justify-content:space-between;align-items:center;width:100%;gap:10px;">
          <div class="echelon-title-group" style="display:flex;align-items:baseline;gap:10px;min-width:0;flex-wrap:wrap;">
            <h1 class="rank-title-glow echelon-bordeaux-title" style="margin:0;font-size:1.24rem;">${readinessRank}</h1>'''

assert target_echelon_group in content, 'Target echelon group not found'
content = content.replace(target_echelon_group, replacement_echelon_group, 1)

# 2. Add srsMobTitle definition
target_srs_var = '''  const accordionMobStatusText = curUnitDoneCount > 0
    ? `${curUnitDoneCount}/${curUnitTotal} освоено`
    : `1 в фокусе · ${lockedCount} закрыты`;'''

replacement_srs_var = '''  const accordionMobStatusText = curUnitDoneCount > 0
    ? `${curUnitDoneCount}/${curUnitTotal} освоено`
    : `1 в фокусе · ${lockedCount} закрыты`;
  const srsMobTitle = cleanTitle.includes(' и ') ? cleanTitle.split(' и ')[0].trim() : (cleanTitle.length > 22 ? cleanTitle.slice(0, 20).trim() + '…' : cleanTitle);'''

assert target_srs_var in content, 'Target srs var not found'
content = content.replace(target_srs_var, replacement_srs_var, 1)

# 3. Use srsMobTitle and srs-deck-title classes in preview
target_srs_title = '''                        <div style="display:flex;align-items:center;gap:7px;min-width:0;flex:1 1 auto;">
                          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;flex-shrink:0;color:var(--ink-muted);"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                          <span style="font-weight:600;color:var(--ink);font-size:0.78rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                            ${escapeHtmlStr(cleanTitle)}
                          </span>
                        </div>'''

replacement_srs_title = '''                        <div style="display:flex;align-items:center;gap:7px;min-width:0;flex:1 1 auto;">
                          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;flex-shrink:0;color:var(--ink-muted);"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                          <span style="font-weight:600;color:var(--ink);font-size:0.78rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                            <span class="srs-deck-title-desk">${escapeHtmlStr(cleanTitle)}</span>
                            <span class="srs-deck-title-mob">${escapeHtmlStr(srsMobTitle)}</span>
                          </span>
                        </div>'''

assert target_srs_title in content, 'Target srs title not found'
content = content.replace(target_srs_title, replacement_srs_title, 1)

# 4. Fill desktop void in empty SRS state with srs-clean-footer
target_srs_footer = ''': (!hasReviewedAnyCard
                  ? ''
                  : `<div style="display:flex;justify-content:flex-end;"><a href="#/cards" class="btn-srs-pill link-quiet text-muted">Обзор колод ➔</a></div>`
                )'''

replacement_srs_footer = ''': (!hasReviewedAnyCard
                  ? `<div class="srs-clean-footer meta" style="font-size:.73rem;color:var(--ink-muted);display:flex;align-items:center;gap:6px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.04);margin-top:auto;"><span style="opacity:0.6;">🧠 Память:</span> <span>режим накопления базы</span></div>`
                  : `<div style="display:flex;justify-content:flex-end;"><a href="#/cards" class="btn-srs-pill link-quiet text-muted">Обзор колод ➔</a></div>`
                )'''

assert target_srs_footer in content, 'Target srs footer not found'
content = content.replace(target_srs_footer, replacement_srs_footer, 1)

# 5. CSS rules for desktop and mobile
target_css_block = '''  @media (max-width: 680px) {
    .dash-pulse-grid {
      grid-template-columns: 1fr !important;
      display: flex !important;
      flex-direction: column !important;
      width: 100% !important;
      max-width: 100% !important;
    }
    .dash-pulse-card {
      width: 100% !important;
      max-width: 100% !important;
      min-width: 0 !important;
      box-sizing: border-box !important;
      overflow: hidden !important;
    }
  }'''

replacement_css_block = '''  .srs-deck-title-desk { display: inline !important; }
  .srs-deck-title-mob { display: none !important; }
  .srs-clean-footer { display: flex !important; }
  @media (max-width: 680px) {
    .dash-pulse-grid {
      grid-template-columns: 1fr !important;
      display: flex !important;
      flex-direction: column !important;
      width: 100% !important;
      max-width: 100% !important;
      gap: 10px !important;
      margin-bottom: 10px !important;
    }
    .dash-pulse-card {
      width: 100% !important;
      max-width: 100% !important;
      min-width: 0 !important;
      box-sizing: border-box !important;
      overflow: hidden !important;
      padding: 10px 13px !important;
      min-height: auto !important;
    }
    .srs-deck-title-desk { display: none !important; }
    .srs-deck-title-mob { display: inline !important; }
    .srs-clean-footer { display: none !important; }
    .heat-row .heat-cell,
    .heat-cell {
      height: 38px !important;
      padding: 3px 1px !important;
    }
    .goal-micro-hint {
      margin-top: 5px !important;
      font-size: 0.72rem !important;
    }
    .dash-accordion {
      margin-top: 10px !important;
      margin-bottom: 12px !important;
      padding: 10px 14px !important;
    }
  }'''

assert target_css_block in content, 'Target css block not found'
content = content.replace(target_css_block, replacement_css_block, 1)

# 6. Echelon mobile single-line styling in @media (max-width: 680px)
target_echelon_mobile_css = '''    .dashboard-container .echelon-topbar-clean {
      padding: 11px 14px !important;
      gap: 6px !important;
      margin-bottom: 10px !important;
      align-items: stretch !important;
      text-align: left !important;
    }
    .dashboard-container .echelon-topbar-row-top {
      display: flex !important;
      justify-content: space-between !important;
      align-items: center !important;
      width: 100% !important;
      gap: 8px !important;
      margin-bottom: 0 !important;
      text-align: left !important;
    }'''

replacement_echelon_mobile_css = '''    .dashboard-container .echelon-topbar-clean {
      padding: 10px 13px !important;
      gap: 6px !important;
      margin-bottom: 9px !important;
      align-items: stretch !important;
      text-align: left !important;
    }
    .dashboard-container .echelon-topbar-row-top {
      display: flex !important;
      justify-content: space-between !important;
      align-items: center !important;
      width: 100% !important;
      gap: 8px !important;
      margin-bottom: 0 !important;
      text-align: left !important;
    }
    .dashboard-container .echelon-title-group {
      display: flex !important;
      align-items: baseline !important;
      gap: 6px !important;
      flex-wrap: nowrap !important;
      min-width: 0 !important;
    }
    .dashboard-container .rank-title-glow {
      font-size: 1.08rem !important;
      text-align: left !important;
      white-space: nowrap !important;
    }
    .dashboard-container .echelon-tier-tag {
      font-size: 0.68rem !important;
      opacity: 0.75 !important;
      white-space: nowrap !important;
    }
    .dashboard-container .topbar-audio-btn,
    #dashAudioCompanionBtn {
      width: 32px !important;
      height: 32px !important;
      min-width: 32px !important;
      min-height: 32px !important;
      padding: 0 !important;
      border-radius: 50% !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
    .dashboard-container .topbar-audio-btn svg {
      width: 13px !important;
      height: 13px !important;
      margin: 0 !important;
    }'''

assert target_echelon_mobile_css in content, 'Target echelon mobile css not found'
content = content.replace(target_echelon_mobile_css, replacement_echelon_mobile_css, 1)

# 7. Also in @media (max-width: 640px) at line ~7509
target_audio_640 = '''    .dashboard-container .topbar-audio-btn,
    .dashboard-container .topbar-help-btn {
      min-height: 40px !important;
      min-width: 40px !important;
    }'''

replacement_audio_640 = '''    .dashboard-container .topbar-audio-btn {
      width: 32px !important;
      height: 32px !important;
      min-width: 32px !important;
      min-height: 32px !important;
      padding: 0 !important;
      border-radius: 50% !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
    .dashboard-container .topbar-help-btn {
      min-height: 32px !important;
      min-width: 32px !important;
    }'''

assert target_audio_640 in content, 'Target audio 640 not found'
content = content.replace(target_audio_640, replacement_audio_640, 1)

# Write to academy.html and both etalons
with open(ACADEMY_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

with open(ETALON1_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

with open(ETALON2_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('Phase 4 optimizations successfully applied and synced across all 3 files!')
