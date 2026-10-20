#!/usr/bin/env python3
"""
apply_skill_and_cards_pipeline.py
Внедрение новой архитектуры экрана навыка:
1. Полное упразднение проверок понимания (NOTE_STEP_CHECKS, stepCheck, Bottom Sheet в конспектах).
2. Прямой переход после конспекта к тематическим карточкам (tab = 'cards') с последующей передачей в SRS и практику IDE.
3. Ликвидация класса .practice-coddy-split -> .practice-atomic-split.
4. Исправление анти-растягивания плашки опыта .xp-float-particle (right: auto; white-space: nowrap).
5. Человеческий заголовок рубежного зачёта («Рубежный зачёт: ...» вместо «Урок 1.1»).
6. Ликвидация чипсов-спойлеров решения (original[::-1], reversed_list).
7. Побайтовая синхронизация с Эталоны/Эталоны.html и Эталоны.html.
"""

import sys
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACADEMY_PATH = os.path.join(ROOT, 'academy.html')
ETALON_DIR_PATH = os.path.join(ROOT, 'Эталоны', 'Эталоны.html')
ETALON_ROOT_PATH = os.path.join(ROOT, 'Эталоны.html')

with open(ACADEMY_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Original academy.html size: {len(content)} bytes')

# 1. Замена .practice-coddy-split на .practice-atomic-split
coddy_split_count = content.count('practice-coddy-split')
assert coddy_split_count > 0, 'practice-coddy-split not found'
content = content.replace('practice-coddy-split', 'practice-atomic-split')
print(f'✓ Replaced {coddy_split_count} occurrences of practice-coddy-split with practice-atomic-split')

# 2. Исправление стилей .xp-float-particle
old_xp_css = '''  .xp-float-particle{
    position:fixed;right:24px;top:58px;z-index:200;pointer-events:none;
    padding:6px 12px;border-radius:999px;background:var(--emerald);color:#fff;
    font-family:var(--font-d);font-weight:800;font-size:.84rem;box-shadow:0 8px 20px rgba(16,185,129,0.35);
    animation:float-up-fade .95s cubic-bezier(0.22,1,0.36,1) forwards;
    will-change:transform, opacity;
    transform:translateZ(0);
  }'''
new_xp_css = '''  .xp-float-particle{
    position:fixed;right:auto;top:58px;z-index:200;pointer-events:none;
    width:max-content;max-width:280px;white-space:nowrap;
    padding:6px 12px;border-radius:999px;background:var(--emerald);color:#fff;
    font-family:var(--font-d);font-weight:800;font-size:.84rem;box-shadow:0 8px 20px rgba(16,185,129,0.35);
    animation:float-up-fade .95s cubic-bezier(0.22,1,0.36,1) forwards;
    will-change:transform, opacity;
    transform:translateZ(0);
  }'''
assert old_xp_css in content, 'old_xp_css not found'
content = content.replace(old_xp_css, new_xp_css, 1)
print('✓ Updated .xp-float-particle CSS (anti-stretching invariant)')

# 3. Человеческий заголовок рубежного зачёта в нити точек и шапке
old_exam_dot = '<span class="dot-jewel milestone ${examActive ? \'active\' : \'\'}" title="Рубежный зачёт урока ${sk.unitId}" data-py-select-exam="${sk.unitId}"></span>'
new_exam_dot = '<span class="dot-jewel milestone ${examActive ? \'active\' : \'\'}" title="Рубежный зачёт: ${escapeHtmlStr(cleanUnitTitleVal)}" data-py-select-exam="${sk.unitId}"></span>'
assert old_exam_dot in content, 'old_exam_dot not found'
content = content.replace(old_exam_dot, new_exam_dot, 1)

old_exam_title = "activeItemTitle = 'Рубежный зачёт урока ' + sk.unitId;"
new_exam_title = "activeItemTitle = 'Рубежный зачёт: ' + cleanUnitTitleVal;"
assert old_exam_title in content, 'old_exam_title not found'
content = content.replace(old_exam_title, new_exam_title, 1)
print('✓ Clean human title for milestone exam in necklace and active header')

# 4. Ликвидация чипсов-спойлеров в buildTaskSpecDetails
old_spoilers = """  const tokens = [];
  if(sol){
    if(sol.includes('[::-1]')) tokens.push('[::-1]');
    if(sol.includes('original[::-1]')) tokens.push('original[::-1]');
    if(sol.includes('reversed_list')) tokens.push('reversed_list');"""
new_spoilers = """  const tokens = [];
  if(sol){
    if(sol.includes('[::-1]')) tokens.push('[::-1]');"""
assert old_spoilers in content, 'old_spoilers not found'
content = content.replace(old_spoilers, new_spoilers, 1)
print('✓ Removed solution spoiler tokens from buildTaskSpecDetails')

# 5. Упразднение проверок понимания в viewPythonSkill
# Заменяем блок от const stepCheckKey до bodyHTML
old_theory_logic = """    const stepCheckKey = `${activeK}:${stepIdx}`;
    const stepCheck = (typeof NOTE_STEP_CHECKS !== 'undefined') ? NOTE_STEP_CHECKS[stepCheckKey] : null;

    let stepCheckHTML = '';
    let bottomSheetHTML = '';

    const isCheckPhase = !!pySkillViewState.stepPhaseCheck || !!pySkillViewState.stepCheckRevealed;

    if(!hasMoreChunks && stepCheck && isCheckPhase){
      const isRevealed = !!pySkillViewState.stepCheckRevealed;
      const chosen = pySkillViewState.stepCheckChosen;
      const isCorrect = (chosen === stepCheck.correct);

      const optsHTML = stepCheck.options.map((opt, oi) => {
        let optStyle = 'width:100%;text-align:left;padding:12px 16px;border-radius:12px;display:flex;align-items:flex-start;gap:12px;font-size:0.92rem;line-height:1.45;transition:all 0.15s ease;cursor:pointer;';
        if(isRevealed){
          if(oi === stepCheck.correct){
            optStyle += 'background:rgba(16,185,129,0.18);border:1.5px solid #10b981;color:#34d399;font-weight:700;';
          } else if(oi === chosen){
            optStyle += 'background:rgba(239,68,68,0.18);border:1.5px solid #ef4444;color:#fca5a5;';
          } else {
            optStyle += 'background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);color:var(--ink-muted);opacity:0.6;';
          }
        } else {
          optStyle += 'background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.12);color:var(--ink);';
        }
        return `
          <button type="button" class="btn-step-check-opt" data-py-step-answer="${oi}" style="${optStyle}" ${isRevealed ? 'disabled' : ''}>
            <span style="display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:rgba(255,255,255,0.08);font-size:0.75rem;font-weight:700;flex:none;">${oi + 1}</span>
            <span style="flex:1;">${formatRichInlineText(opt)}</span>
          </button>`;
      }).join('');

      stepCheckHTML = `
        <div class="step-check-container" style="margin-top:24px;padding:20px;border-radius:16px;background:rgba(255,255,255,0.03);border:1.5px solid rgba(16,185,129,0.3);box-shadow:0 8px 24px rgba(0,0,0,0.18);animation:fadeIn 0.25s ease;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;gap:8px;flex-wrap:wrap;">
            <div style="display:inline-flex;align-items:center;gap:6px;font-size:0.78rem;font-weight:700;color:#34d399;background:rgba(16,185,129,0.15);padding:3px 10px;border-radius:999px;">
              <span>🎯 Проверка понимания</span>
            </div>
            <span style="font-size:0.75rem;color:var(--ink-muted);font-weight:600;">+10 XP за верный ответ</span>
          </div>
          <div style="font-size:1.02rem;font-weight:700;color:var(--ink);line-height:1.45;margin-bottom:14px;">${formatRichInlineText(stepCheck.q)}</div>
          <div style="display:flex;flex-direction:column;gap:10px;">${optsHTML}</div>
        </div>`;

      if(isRevealed){
        bottomSheetHTML = `
          <div class="academy-bottom-sheet ${isCorrect ? 'academy-bottom-sheet--correct' : 'academy-bottom-sheet--wrong'}">
            <div class="bs-title-row">
              <span>${isCorrect ? '✓ Правильно! Материал усвоен' : '✕ Не совсем так'}</span>
              <span class="bs-badge">${isCorrect ? '⚡ +10 XP' : 'Разбор'}</span>
            </div>
            <div class="bs-explain-text">${formatRichInlineText(stepCheck.explain)}</div>
            <div style="display:flex;gap:10px;align-items:center;width:100%;">
              <button type="button" class="${isCorrect ? 'btn-3d-emerald btn-action-emerald' : 'btn-glass-emerald'} btn-sprint-cta" style="flex:1;" data-py-step-check-next>
                ${stepIdx + 1 < steps.length ? 'Дальше к следующему шагу ➔' : (isRead ? '✓ Конспект усвоен ➔' : '✓ Завершить конспект (+10 MP) ➔')}
              </button>
            </div>
          </div>`;
      }
    }

    let primaryActionHTML = '';
    if(hasMoreChunks){
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;max-width:440px;" data-chunk-more="py">Понятно, дальше (+10 XP) ➔</button>`;
    } else if(stepCheck){
      if(!isCheckPhase){
        primaryActionHTML = `<button type="button" class="btn-3d-emerald btn-action-emerald btn-sprint-cta" style="flex:1;max-width:440px;" data-py-start-check>Проверить понимание (+10 XP) ➔</button>`;
      } else if(pySkillViewState.stepCheckRevealed){
        primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;max-width:440px;" data-py-step-check-next>${stepIdx + 1 < steps.length ? 'Дальше к следующему шагу ➔' : (isRead ? '✓ Конспект усвоен' : '✓ Завершить конспект (+10 MP)')}</button>`;
      } else {
        primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;max-width:440px;opacity:0.6;" disabled>Выберите вариант ответа выше</button>`;
      }
    } else if(stepIdx + 1 < steps.length){
      const activeK = pySkillViewState.kId || 'unknown';
      const stepKey = `${activeK}:${stepIdx+1}`;
      const stepAlreadyDone = isRead || (state.completedNoteSteps && state.completedNoteSteps[stepKey]);
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;max-width:440px;" data-py-next-step="${stepIdx+1}">Понятно, дальше${stepAlreadyDone ? '' : ' (+10 XP)'} ➔</button>`;
    } else {
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;max-width:440px;" data-py-finish-note="${activeK}">${isRead ? '✓ Конспект усвоен' : '✓ Завершить конспект (+10 MP)'}</button>`;
    }

    bodyHTML = `
      <div class="card interactive-step-card" style="margin-top:0;display:flex;flex-direction:column;justify-content:space-between;min-height:280px;">
        <div style="flex:1;">
          ${feedHTML}
          ${stepCheckHTML}
        </div>
        <div class="sprint-actions-bar" style="display:flex;align-items:center;gap:10px;margin-top:24px;flex-wrap:nowrap;flex:none;justify-content:center;">
          ${backBtnHTML}
          <div style="display:flex;gap:10px;align-items:center;flex:1;justify-content:center;max-width:440px;">
            ${primaryActionHTML}
          </div>
        </div>
      </div>
      ${bottomSheetHTML}`;"""

new_theory_logic = """    let primaryActionHTML = '';
    if(hasMoreChunks){
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;max-width:440px;" data-chunk-more="py">Понятно, дальше (+10 XP) ➔</button>`;
    } else if(stepIdx + 1 < steps.length){
      const activeK = pySkillViewState.kId || 'unknown';
      const stepKey = `${activeK}:${stepIdx+1}`;
      const stepAlreadyDone = isRead || (state.completedNoteSteps && state.completedNoteSteps[stepKey]);
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;max-width:440px;" data-py-next-step="${stepIdx+1}">Понятно, дальше${stepAlreadyDone ? '' : ' (+10 XP)'} ➔</button>`;
    } else {
      primaryActionHTML = `<button type="button" class="btn-3d-emerald btn-action-emerald btn-sprint-cta" style="flex:1;max-width:440px;" data-py-finish-note="${activeK}">Закрепить в карточках (+10 XP) ➔</button>`;
    }

    bodyHTML = `
      <div class="card interactive-step-card" style="margin-top:0;display:flex;flex-direction:column;justify-content:space-between;min-height:280px;">
        <div style="flex:1;">
          ${feedHTML}
        </div>
        <div class="sprint-actions-bar" style="display:flex;align-items:center;gap:10px;margin-top:24px;flex-wrap:nowrap;flex:none;justify-content:center;">
          ${backBtnHTML}
          <div style="display:flex;gap:10px;align-items:center;flex:1;justify-content:center;max-width:440px;">
            ${primaryActionHTML}
          </div>
        </div>
      </div>`;"""

assert old_theory_logic in content, 'old_theory_logic not found'
content = content.replace(old_theory_logic, new_theory_logic, 1)
print('✓ Replaced theory logic with direct pipeline to flashcards')

# 6. Убираем hasBottomSheet в конце viewPythonSkill
old_has_bs = "  const hasBottomSheet = (pySkillViewState.tab === 'theory' && !!pySkillViewState.stepCheckRevealed);\n  return `\n    <div class=\"container\" style=\"max-width:880px;${hasBottomSheet ? 'padding-bottom:220px;' : ''}\">"
new_has_bs = "  return `\n    <div class=\"container\" style=\"max-width:880px;\">"
assert old_has_bs in content, 'old_has_bs not found'
content = content.replace(old_has_bs, new_has_bs, 1)
print('✓ Removed bottom sheet padding check in viewPythonSkill container')

# 7. Обновляем обработчик data-py-finish-note: прямой переход на карточки темы
old_pfn = """  const pfn = e.target.closest('[data-py-finish-note]');
  if(pfn){
    const kid = pfn.getAttribute('data-py-finish-note');
    const prevE1 = getEchelonProgress(1);
    const wasAlreadyRead = state.readNotes.includes(kid);
    if(!wasAlreadyRead){
      state.readNotes.push(kid);
      awardXp(15);
    }
    if(pySkillViewState.sid) setSkillMP(pySkillViewState.sid, 50);
    const newE1 = getEchelonProgress(1);
    const remE1 = newE1.skills.filter(s => getSkillMP(s.id) < 100).length;
    pySkillViewState.sprintCelebration = {
      kid: kid,
      wasAlreadyRead: wasAlreadyRead,
      prevPct: prevE1.pct,
      newPct: Math.max(newE1.pct, Math.min(100, prevE1.pct + 2)),
      remainingTopics: remE1
    };
    // Advance managed via celebration modal choice (Home = Journey)
    saveReadingPosition();
    render();
    return;
  }"""

new_pfn = """  const pfn = e.target.closest('[data-py-finish-note]');
  if(pfn){
    const kid = pfn.getAttribute('data-py-finish-note');
    const wasAlreadyRead = state.readNotes.includes(kid);
    if(!wasAlreadyRead){
      state.readNotes.push(kid);
      awardXp(15);
    }
    if(pySkillViewState.sid) setSkillMP(pySkillViewState.sid, 50);
    // Прямой переход к тематическим карточкам темы (Clean 3-Stage Pipeline: Конспект ➔ Карточки ➔ IDE)
    pySkillViewState.tab = 'cards';
    pySkillViewState.sessionFid = null;
    pySkillViewState.sessionPos = 0;
    pySkillViewState.sessionRepeats = 0;
    pySkillViewState.sessionLearned = 0;
    pySkillViewState.sessionDone = false;
    pySkillViewState.cardFlipped = false;
    pySkillViewState.sprintCelebration = null;
    saveReadingPosition();
    render();
    return;
  }"""

assert old_pfn in content, 'old_pfn not found'
content = content.replace(old_pfn, new_pfn, 1)
print('✓ Updated data-py-finish-note event handler for direct transition to cards')

# 8. Очистка устаревших обработчиков проверок понимания (data-py-start-check, data-py-step-answer, data-py-step-check-next)
old_check_handlers = """  // Active Comprehension Check Phase Start
  const pscStart = e.target.closest('[data-py-start-check]');
  if(pscStart){
    pySkillViewState.stepPhaseCheck = true;
    saveReadingPosition();
    render();
    setTimeout(() => {
      const qEl = document.querySelector('.step-check-container');
      if(qEl) qEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 50);
    return;
  }

  // Active Comprehension Check Answer
  const psa = e.target.closest('[data-py-step-answer]');
  if(psa){
    const ansIdx = parseInt(psa.getAttribute('data-py-step-answer'), 10);
    const activeK = pySkillViewState.kId || 'unknown';
    const stepIdx = pySkillViewState.stepIdx || 0;
    const check = (typeof NOTE_STEP_CHECKS !== 'undefined') ? NOTE_STEP_CHECKS[`${activeK}:${stepIdx}`] : null;
    if(check){
      pySkillViewState.stepCheckRevealed = true;
      pySkillViewState.stepCheckChosen = ansIdx;
      if(ansIdx === check.correct){
        ensureExtendedState();
        if(!state.completedNoteSteps) state.completedNoteSteps = {};
        const stepKey = `${activeK}:${stepIdx}`;
        if(!state.completedNoteSteps[stepKey]){
          state.completedNoteSteps[stepKey] = true;
          awardXp(10);
        }
      }
      saveReadingPosition();
      render();
    }
    return;
  }

  const pscn = e.target.closest('[data-py-step-check-next]');
  if(pscn){
    const activeK = pySkillViewState.kId || 'unknown';
    const noteObj = (typeof ALL_NOTES_COMBINED !== 'undefined' ? ALL_NOTES_COMBINED[activeK] : null) || {steps:[]};
    const steps = noteObj.steps || [];
    const stepIdx = pySkillViewState.stepIdx || 0;
    pySkillViewState.stepCheckRevealed = false;
    pySkillViewState.stepCheckChosen = null;
    pySkillViewState.stepPhaseCheck = false;

    if(stepIdx + 1 < steps.length){
      pySkillViewState.stepIdx = stepIdx + 1;
      pySkillViewState.chunkIdx = 0;
      saveReadingPosition();
      render();
    } else {
      const prevE1 = getEchelonProgress(1);
      const wasAlreadyRead = state.readNotes.includes(activeK);
      if(!wasAlreadyRead){
        state.readNotes.push(activeK);
        awardXp(15);
      }
      if(pySkillViewState.sid) setSkillMP(pySkillViewState.sid, 50);
      const newE1 = getEchelonProgress(1);
      const remE1 = newE1.skills.filter(s => getSkillMP(s.id) < 100).length;
      pySkillViewState.sprintCelebration = {
        kid: activeK,
        wasAlreadyRead: wasAlreadyRead,
        prevPct: prevE1.pct,
        newPct: Math.max(newE1.pct, Math.min(100, prevE1.pct + 2)),
        remainingTopics: remE1
      };
      saveReadingPosition();
      render();
    }
    return;
  }"""

new_check_handlers = """  // (Comprehension check handlers completely removed in favor of direct thematic cards transition)"""
assert old_check_handlers in content, 'old_check_handlers not found'
content = content.replace(old_check_handlers, new_check_handlers, 1)
print('✓ Removed obsolete comprehension check event handlers')

# 9. Очистка реестра NOTE_STEP_CHECKS: заменяем на компактный пустой объект для обратной совместимости
note_checks_match = re.search(r'// Инвариант Coddy: активный отклик.*?\nconst NOTE_STEP_CHECKS = \{.*?\n\};\nwindow\.NOTE_STEP_CHECKS = NOTE_STEP_CHECKS;', content, re.DOTALL)
if note_checks_match:
    content = content.replace(note_checks_match.group(0), '// Тематические карточки и интервальное повторение (Clean 3-Stage Atomic Pipeline)\nconst NOTE_STEP_CHECKS = {};\nwindow.NOTE_STEP_CHECKS = NOTE_STEP_CHECKS;')
    print('✓ Cleaned up NOTE_STEP_CHECKS registry (~460 lines removed)')
else:
    print('NOTE_STEP_CHECKS pattern not matched directly')

with open(ACADEMY_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'New academy.html size: {len(content)} bytes')

with open(ETALON_DIR_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
with open(ETALON_ROOT_PATH, 'w', encoding='utf-8') as f:
    f.write(content)
print('✓ Synchronized academy.html with Эталоны/Эталоны.html and Эталоны.html (100% byte-matching)')
