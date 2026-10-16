# -*- coding: utf-8 -*-
import re
import shutil
import subprocess

ACADEMY_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"

with open(ACADEMY_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Заменяем focusTopbarHTML в viewPythonSkill
old_focus_topbar_re = re.compile(
    r'  const focusTopbarHTML = `\s*<div class="sprint-focus-topbar sprint-topbar">[\s\S]*?</div>`;',
    re.MULTILINE
)

new_focus_topbar = """  const curEchTier = effTier || 1;
  const echMeta = INTERVIEW_ECHELONS[curEchTier] || INTERVIEW_ECHELONS[1];
  const echProg = (typeof getEchelonProgress === 'function') ? getEchelonProgress(curEchTier) : { pct: 35 };
  const echPct = echProg.pct || 0;
  const dayXpVal = (typeof todayXp === 'function') ? todayXp() : 0;

  const focusTopbarHTML = `
    <div class="echelon-topbar-clean">
      <div class="echelon-clean-wrap">
        <div class="echelon-clean-meta">
          <span><strong style="color:var(--ink);">${echMeta.shortLabel}</strong> <span style="color:rgba(255,255,255,0.28);margin:0 4px;">·</span> <span style="color:var(--ink-muted);font-weight:600;">${echMeta.focus}</span></span>
          <span style="color:${echMeta.color || '#34d399'};font-family:var(--font-m);font-weight:800;">
            🎯 ${echPct}% готовности ${echMeta.targetLabel}
          </span>
        </div>
        <div class="echelon-clean-track">
          <div class="echelon-clean-fill" style="width:${echPct}%;background:${echMeta.gradient};"></div>
        </div>
      </div>
      <div style="display:flex;gap:10px;align-items:center;margin-left:14px;">
        <div class="sprint-xp-pill" style="display:inline-flex;align-items:center;gap:4px;padding:5px 11px;border-radius:999px;background:rgba(16,185,129,0.14);border:1px solid rgba(52,211,153,0.35);color:#34d399;font-size:0.75rem;font-weight:700;white-space:nowrap;letter-spacing:0.01em;" title="Заработано за сутки: ${dayXpVal} XP">⚡ ${dayXpVal} XP сегодня</div>
        ${pySkillViewState.tab === 'theory' ? `<button type="button" class="btn btn-ghost" data-py-toggle-fullnote style="padding:6px 12px;font-size:.76rem;border-radius:10px;" title="Переключить режим полного конспекта">${pySkillViewState.fullNoteMode ? '📖 По шагам' : '📄 Весь конспект'}</button>` : ''}
        <a href="#/docs" class="topbar-help-btn" style="padding:6px 14px;border-radius:10px;" title="Справочник синтаксиса и методов Python"><span class="topbar-help-text">📖 Справка</span></a>
      </div>
    </div>
    <div id="theory-audio-bar" class="theory-audio-bar" style="display:${state.audioBarOpen ? 'flex' : 'none'};">
      <button type="button" class="theory-audio-btn" data-audio-play title="Воспроизвести / Пауза">▶</button>
      <button type="button" class="theory-audio-btn" data-audio-rewind title="Перемотка назад на 10 сек">⏪ -10с</button>
      <button type="button" class="theory-audio-btn" data-audio-rate title="Скорость чтения">1.0x</button>
      <span class="audio-status-text">Аудио-компаньон</span>
      <button type="button" class="theory-audio-btn" data-audio-close style="margin-left:auto;" title="Скрыть аудио-бар">✕</button>
    </div>`;"""

m = old_focus_topbar_re.search(code)
if m:
    code = code[:m.start()] + new_focus_topbar + code[m.end():]
    print("Replaced focusTopbarHTML successfully")
else:
    print("WARNING: could not find old focusTopbarHTML")

# 2. Убираем tabsHTML (stepper) - устанавливаем showTopTabs = false
code = code.replace("  let showTopTabs = true;", "  let showTopTabs = false;", 1)
print("Disabled showTopTabs")

# 3. Добавляем eyebrowDotsHTML над заголовком в stage 'theory'
old_theory_body = """    bodyHTML = pySkillViewState.fullNoteMode
      ? steps.map((st, i) => `<div class="microstep-card"><div class="topic-badge">Шаг ${i+1} из ${steps.length}</div><h3>${st.title}</h3><div class="lesson-theory">${decorateCodeBlocksWithRunBtn(st.html)}</div></div>`).join('')
      : `<div class="coddy-lesson-card" style="max-width:760px;margin:0 auto;">${feedHTML}${primaryActionHTML}</div>`;"""

new_theory_body = """    const curUnit = (typeof ALL_UNITS_COMBINED !== 'undefined') ? (ALL_UNITS_COMBINED.find(u => u.id === sk.unitId) || { skills: [sk], title: sk.title || '' }) : { skills: [sk], title: sk.title || '' };
    const allUnitNotes = [];
    (curUnit.skills || [sk]).forEach(s => {
      (s.kIds || []).forEach(k => {
        const n = ALL_NOTES_COMBINED[k] || { title: k };
        allUnitNotes.push({ kId: k, skillId: s.id, title: n.title });
      });
    });
    const totalNotesInUnit = Math.max(1, allUnitNotes.length);
    const activeNoteIdx = Math.max(0, allUnitNotes.findIndex(item => item.kId === activeK));
    const curNoteNum = activeNoteIdx + 1;
    const dotsActivePct = totalNotesInUnit > 1 ? Math.round((activeNoteIdx / (totalNotesInUnit - 1)) * 100) : 100;

    const unitJewelDotsHTML = allUnitNotes.map((item, idx) => {
      const isDone = state.readNotes.includes(item.kId);
      const isActive = (item.kId === activeK);
      const isMilestone = (idx === totalNotesInUnit - 1);
      let cls = 'dot-jewel';
      if(isActive) cls += ' active';
      else if(isDone) cls += ' done';
      if(isMilestone) cls += ' milestone';
      return `<span class="${cls}" title="${idx+1}. ${item.kId}: ${escapeHtmlStr(item.title)}" data-py-select-k="${item.kId}"></span>`;
    }).join('');

    const eyebrowDotsHTML = `
      <div class="topic-eyebrow-track">
        <div class="topic-eyebrow-tags">
          <span class="topic-eyebrow-unit">Юнит ${sk.unitId}: ${escapeHtmlStr(curUnit.title || sk.title || '')}</span>
          <span style="color:var(--line);">•</span>
          <span class="topic-eyebrow-num">Тема ${curNoteNum} из ${totalNotesInUnit}</span>
        </div>
        <div class="dots-necklace" title="${totalNotesInUnit} тем Юнита ${sk.unitId}">
          <div class="dots-necklace-wire"></div>
          <div class="dots-necklace-wire-active" style="width:${dotsActivePct}%;"></div>
          ${unitJewelDotsHTML}
          <span class="dots-necklace-label">${curNoteNum}/${totalNotesInUnit}</span>
        </div>
      </div>`;

    bodyHTML = pySkillViewState.fullNoteMode
      ? `<div class="coddy-lesson-card" style="max-width:780px;margin:0 auto;">${eyebrowDotsHTML}` + steps.map((st, i) => `<div class="microstep-card"><div class="topic-badge">Шаг ${i+1} из ${steps.length}</div><h3>${st.title}</h3><div class="lesson-theory">${decorateCodeBlocksWithRunBtn(st.html)}</div></div>`).join('') + `</div>`
      : `<div class="coddy-lesson-card" style="max-width:780px;margin:0 auto;">${eyebrowDotsHTML}${feedHTML}${primaryActionHTML}</div>`;"""

if old_theory_body in code:
    code = code.replace(old_theory_body, new_theory_body, 1)
    print("Replaced theory bodyHTML with eyebrowDotsHTML successfully")
else:
    print("WARNING: could not find old_theory_body")

with open(ACADEMY_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved updated academy.html")
