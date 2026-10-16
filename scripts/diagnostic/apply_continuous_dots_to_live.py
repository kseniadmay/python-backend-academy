# -*- coding: utf-8 -*-
import re
import shutil
import subprocess

ACADEMY_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"
BACKUP_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html.bak_before_dots"

shutil.copyfile(ACADEMY_PATH, BACKUP_PATH)
print("Backup created at", BACKUP_PATH)

with open(ACADEMY_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Обновляем CSS стили для точного соответствия утвержденному макету
new_css = """
  /* ================= УТВЕРЖДЕННЫЙ ТОПБАР ЭШЕЛОНА И НЕПРЕРЫВНАЯ НИТЬ ТОЧЕК ================= */
  .echelon-topbar-clean {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 20px;
    margin-bottom: 20px;
    border-radius: 18px;
    background: var(--surface);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow: var(--shadow-1);
  }
  .echelon-clean-wrap {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  .echelon-clean-meta {
    display: flex;
    justify-content: flex-start;
    gap: 8px;
    align-items: center;
    font-size: 0.78rem;
    font-weight: 700;
  }
  .echelon-bordeaux-title {
    color: #be123c;
    font-weight: 800;
    letter-spacing: -0.01em;
    text-shadow: 0 0 5px rgba(190, 18, 60, 0.5);
  }
  :root[data-theme="light"] .echelon-bordeaux-title {
    color: #881337;
    text-shadow: none;
  }
  .echelon-readiness-emerald {
    color: #34d399;
    font-weight: 600;
    text-shadow: 0 0 5px rgba(52, 211, 153, 0.45);
  }
  :root[data-theme="light"] .echelon-readiness-emerald {
    color: #059669;
    text-shadow: none;
  }
  .echelon-clean-track {
    height: 6px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.04);
    margin-top: 3px;
  }
  .echelon-clean-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #6b1d2f 0%, #be123c 35%, #059669 75%, #10b981 100%);
    box-shadow: none;
    transition: width .35s ease;
  }
  .topic-eyebrow-track {
    max-width: 780px;
    margin: 14px auto 16px;
    width: 100%;
  }
  .topic-eyebrow-tags {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    margin-bottom: 10px;
  }
  .unit-breadcrumb-title {
    font-family: var(--font-d);
    font-size: 1.06rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--ink);
    text-align: center;
  }
  .dots-necklace {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    width: 100%;
    position: relative;
    padding: 6px 0 10px;
    background: transparent;
    border: none;
    box-shadow: none;
  }
  .dots-stage-divider {
    width: 2px;
    height: 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.15);
    margin: 0 5px;
  }
  .dot-jewel {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.16);
    position: relative;
    z-index: 3;
    transition: all 0.25s cubic-bezier(0.2, 0.8, 0.4, 1);
    cursor: pointer;
  }
  .dot-jewel:hover {
    transform: scale(1.5);
    background: rgba(255, 255, 255, 0.5);
  }
  .dot-jewel.done {
    background: #10b981;
    box-shadow: 0 0 8px rgba(16, 185, 129, 1), 0 0 16px rgba(16, 185, 129, 0.65), 0 0 26px rgba(16, 185, 129, 0.35);
  }
  .dot-jewel.active {
    width: 9px;
    height: 9px;
    background: #ffffff;
    box-shadow: 0 0 10px #ffffff, 0 0 22px rgba(255, 255, 255, 0.95), 0 0 38px rgba(255, 255, 255, 0.6);
    animation: radar-breathe-white 4.4s infinite ease-in-out;
  }
  .dot-jewel.milestone {
    width: 8px;
    height: 8px;
    border-radius: 2px;
    transform: rotate(45deg);
    background: rgba(245, 158, 11, 0.65);
    box-shadow: 0 0 6px rgba(245, 158, 11, 0.4);
  }
  .dot-jewel.milestone.active {
    width: 10px;
    height: 10px;
    transform: rotate(45deg);
    background: #ffffff;
    box-shadow: 0 0 10px #ffffff, 0 0 22px rgba(255, 255, 255, 0.95);
  }
  @keyframes radar-breathe-white {
    0%, 100% {
      transform: scale(1);
      box-shadow: 0 0 10px #ffffff, 0 0 22px rgba(255, 255, 255, 0.95), 0 0 38px rgba(255, 255, 255, 0.6);
    }
    50% {
      transform: scale(1.15);
      box-shadow: 0 0 14px #ffffff, 0 0 30px rgba(255, 255, 255, 1), 0 0 50px rgba(255, 255, 255, 0.85);
    }
  }
"""

# Вставляем/заменяем CSS блок
old_css_marker = "/* ================= CLEAN ECHELON TOPBAR & JEWEL DOTS NECKLACE ================= */"
if old_css_marker in code:
    idx1 = code.find(old_css_marker)
    idx2 = code.find("/* ---------- Section 7:", idx1)
    if idx2 != -1:
        code = code[:idx1] + new_css.strip() + "\n  " + code[idx2:]
        print("Replaced old CSS with new_css")

# 2. Обновляем focusTopbarHTML в viewPythonSkill
focus_topbar_old_pattern = re.compile(
    r'  const focusTopbarHTML = `\s*<div class="echelon-topbar-clean[\s\S]*?</div>`;',
    re.MULTILINE
)

new_focus_topbar_code = """  const focusTopbarHTML = `
    <div class="echelon-topbar-clean sprint-focus-topbar sprint-topbar" style="padding: 12px 20px;">
      <a href="#${tr.routePrefix}" class="sprint-close-btn sr-only" title="${tr.backLabel}">${tr.backLabel}</a>
      <div class="echelon-clean-wrap">
        <div class="echelon-clean-meta" style="font-size: 0.78rem; justify-content: flex-start; gap: 8px; align-items: center;">
          <span class="echelon-bordeaux-title">Эшелон ${curEchTier}</span>
          <span style="color:var(--ink-muted);font-weight:400;opacity:0.6;">·</span>
          <span class="echelon-readiness-emerald">${echPct}% готовности ${echMeta.targetLabel || 'к скринингу'}</span>
          <span class="sr-only">Шаг ${stepIdx+1}/${steps.length}</span>
        </div>
        <div class="echelon-clean-track" style="height: 6px; margin-top: 3px;">
          <div class="echelon-clean-fill" style="width: ${echPct}%;"></div>
        </div>
      </div>
      <div style="display:flex;gap:10px;align-items:center;margin-left:14px;flex:none;">
        <div class="sprint-xp-pill" style="display:inline-flex;align-items:center;gap:4px;padding:5px 11px;border-radius:999px;background:rgba(245,158,11,0.14);border:1px solid rgba(245,158,11,0.35);color:#fbbf24;font-size:0.75rem;font-weight:700;white-space:nowrap;letter-spacing:0.01em;" title="Заработано за сутки: ${dayXpVal} XP">⚡ +${dayXpVal || 120} XP за сутки</div>
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

m_topbar = focus_topbar_old_pattern.search(code)
if m_topbar:
    code = code[:m_topbar.start()] + new_focus_topbar_code + code[m_topbar.end():]
    print("Updated focusTopbarHTML successfully")
else:
    print("Warning: could not find old focusTopbarHTML")

# 3. Обновляем eyebrowDotsHTML в viewPythonSkill
eyebrow_old_pattern = re.compile(
    r'    const rawUnitTitle = curUnit\.title[\s\S]*?const eyebrowDotsHTML = `[\s\S]*?`;',
    re.MULTILINE
)

new_eyebrow_code = """    const rawUnitTitle = curUnit.title || sk.title || '';
    const cleanUnitTitle = rawUnitTitle.replace(/^Юнит\\s+[\\d.]+\\s*[·•\\-:]\\s*/i, '').trim() || rawUnitTitle;

    // Непрерывная нить атомарных точек трекера (Continuous Atomic Dots)
    const noteDots = allUnitNotes.map((item, idx) => {
      const isDone = state.readNotes.includes(item.kId);
      const isActive = (item.kId === activeK);
      return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="📖 Конспект: ${escapeHtmlStr(item.title)}" data-py-select-k="${item.kId}" data-py-skill-id="${item.skillId}"></span>`;
    }).join('');

    const cardDots = (sk.fIds || []).map((fid, idx) => {
      const d = ALL_DECKS_COMBINED[fid] || {};
      const isDone = state.reviewedDecks.includes(fid);
      const isActive = (pySkillViewState.tab === 'cards' && (pySkillViewState.fId === fid || (!pySkillViewState.fId && idx === 0)));
      return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="🗂️ Карточки: ${escapeHtmlStr(d.title || fid)}" data-py-select-f="${fid}"></span>`;
    }).join('');

    const taskDots = (sk.taskIds || [240, 241, 242]).map((tid, idx) => {
      const t = IDE_TASKS_BY_ID[tid] || {};
      const isDone = (solvedMap[tid] === 'solved');
      const isActive = (pySkillViewState.tab === 'code' && (pySkillViewState.taskId === tid || (!pySkillViewState.taskId && idx === 0)));
      return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="⚡ Задача #${tid}: ${escapeHtmlStr(t.title || '')}" data-py-select-task="${tid}"></span>`;
    }).join('');

    const examActive = (pySkillViewState.tab === 'exam');
    const examDot = `<span class="dot-jewel milestone ${examActive ? 'active' : ''}" title="👑 Рубежный зачёт Юнита ${sk.unitId}"></span>`;

    const dotsNecklaceHTML = `
      <div class="dots-necklace" title="Конспекты → Карточки → Практика → Зачёт">
        ${noteDots}
        <span class="dots-stage-divider" title="Переход к карточкам"></span>
        ${cardDots}
        <span class="dots-stage-divider" title="Переход к практике"></span>
        ${taskDots}
        <span class="dots-stage-divider" title="Рубежный зачёт"></span>
        ${examDot}
      </div>`;

    const eyebrowDotsHTML = `
      <div class="topic-eyebrow-track">
        <div class="topic-eyebrow-tags">
          <div class="unit-breadcrumb">
            <span class="unit-breadcrumb-title">${escapeHtmlStr(cleanUnitTitle)}</span>
          </div>
        </div>
        ${dotsNecklaceHTML}
      </div>`;"""

m_eyebrow = eyebrow_old_pattern.search(code)
if m_eyebrow:
    code = code[:m_eyebrow.start()] + new_eyebrow_code + code[m_eyebrow.end():]
    print("Updated eyebrowDotsHTML successfully")
else:
    print("Warning: could not find old eyebrowDotsHTML")

with open(ACADEMY_PATH, "w", encoding="utf-8") as f:
    f.write(code)

# Обновляем extracted_academy.js
m_script = re.search(r'<script>([\s\S]*?)</script>', code)
if m_script:
    with open(r"C:\Users\fury6\OneDrive\Python_Backend_Academy\scripts\extracted_academy.js", "w", encoding="utf-8") as f:
        f.write(m_script.group(1))
    print("Refreshed extracted_academy.js successfully")

print("Done applying continuous dots to live academy.html!")
