#!/usr/bin/env python3
"""
apply_generator_notes_fixes.py
Применение исправлений 7 системных дефектов подачи конспектов (Bugs 107..113).
"""

import sys
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACADEMY_PATH = os.path.join(ROOT, 'academy.html')
ETALON_PATH = os.path.join(ROOT, 'Эталоны', 'Эталоны.html')

with open(ACADEMY_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

orig_len = len(content)
print(f'Original academy.html size: {orig_len} chars')

# -------------------------------------------------------------
# 1. Bug 107: highlightPythonTokens &quot; / &#39; string support
# -------------------------------------------------------------
old_hl = 'const tokenRegex = /(#.*?)(?=\\n|$)|("(?:\\\\.|[^"\\\\])*"|\'(?:\\\\.|[^\'\\\\])*\')|\\b(def|return|for|in|if|else|elif|while|class|import|from|as|try|except|finally|with|lambda|yield|raise|pass|break|continue|and|or|not|is|True|False|None)\\b|\\b(print|len|range|list|dict|set|tuple|int|str|float|bool|min|max|sum|sorted|enumerate|zip|map|filter|all|any|open|isinstance|type|super|append|extend|pop|remove|add|update|get|keys|values|items)\\b(?=\\s*\\()|\\b(\\d+(?:\\.\\d+)?)\\b/g;'
new_hl = 'const tokenRegex = /(#.*?)(?=\\n|$)|(&quot;(?:\\\\.|[^&]|&(?!quot;))*&quot;|&#39;(?:\\\\.|[^&]|&(?!#39;))*&#39;|"(?:\\\\.|[^"\\\\])*"|\'(?:\\\\.|[^\'\\\\])*\')|\\b(def|return|for|in|if|else|elif|while|class|import|from|as|try|except|finally|with|lambda|yield|raise|pass|break|continue|and|or|not|is|True|False|None)\\b|\\b(print|len|range|list|dict|set|tuple|int|str|float|bool|min|max|sum|sorted|enumerate|zip|map|filter|all|any|open|isinstance|type|super|append|extend|pop|remove|add|update|get|keys|values|items)\\b(?=\\s*\\()|\\b(\\d+(?:\\.\\d+)?)\\b/g;'

if old_hl in content:
    content = content.replace(old_hl, new_hl, 1)
    print('✓ Bug 107: Updated tokenRegex in highlightPythonTokens')
else:
    print('! Bug 107: old_hl not found')

# -------------------------------------------------------------
# 2. Bug 111: Fix unescaped backslashes in NOTE_STEP_CHECKS
# -------------------------------------------------------------
# К-055:1
content = content.replace(
    "q: 'Что вернёт вызов `re.search(r\"\\d+\", text)`, если в строке `text` нет ни одной цифры?',",
    "q: 'Что вернёт вызов `re.search(r\"\\\\d+\", text)`, если в строке `text` нет ни одной цифры?',"
)
# К-055:2
content = content.replace(
    "explain: 'Классическая уязвимость скрининга: `re.match(r\"\\d+\", \"123-hack\")` вернёт Match, так как префикс совпал! Для строгой валидации всей строки (телефон, slug, ID) обязателен `re.fullmatch()`.',",
    "explain: 'Классическая уязвимость скрининга: `re.match(r\"\\\\d+\", \"123-hack\")` вернёт Match, так как префикс совпал! Для строгой валидации всей строки (телефон, slug, ID) обязателен `re.fullmatch()`.',"
)
# К-055:4
content = content.replace(
    "q: 'Какой результат вернёт вызов `re.sub(r\"\\D\", \"\", \"+7 (999) 123-45-67\")`?',",
    "q: 'Какой результат вернёт вызов `re.sub(r\"\\\\D\", \"\", \"+7 (999) 123-45-67\")`?',"
)
content = content.replace(
    "explain: 'Метасимвол `\\D` означает любой нецифровой символ. Замена `\\D` на пустую строку `\"\"` — стандартный способ очистки и нормализации номеров телефонов в бэкенде.',",
    "explain: 'Метасимвол `\\\\D` означает любой нецифровой символ. Замена `\\\\D` на пустую строку `\"\"` — стандартный способ очистки и нормализации номеров телефонов в бэкенде.',"
)
# К-055:5
content = content.replace(
    "q: 'Что означает управляющая последовательность `\\s` в регулярных выражениях Python?',",
    "q: 'Что означает управляющая последовательность `\\\\s` в регулярных выражениях Python?',"
)
content = content.replace(
    "explain: 'Класс `\\s` включает любые пробельные символы (пробел, `\\t`, `\\n`, `\\r`). Заглавная буква `\\S` инвертирует поведение — любой непробельный символ.',",
    "explain: 'Класс `\\\\s` включает любые пробельные символы (пробел, `\\\\t`, `\\\\n`, `\\\\r`). Заглавная буква `\\\\S` инвертирует поведение — любой непробельный символ.',"
)
# К-055:7 (\x08 backspace replacement)
old_k055_7 = """  'К-055:7': {
    q: 'Зачем в шаблоне поиска `r"\\bcat\\b"` используется якорь границы слова `\\b`?',
    options: [
      'Чтобы найти изолированное слово `cat`, исключив совпадения внутри `category` или `scatter`',
      'Чтобы сопоставить символ обратного слэша',
      'Чтобы перевести регулярное выражение в режим байтовой строки'
    ],
    correct: 0,
    explain: 'Якорь границы слова `\\b` отмечает границу между буквенно-цифровым символом `\\w` и непробельным/пробельным. Это предотвращает ложные срабатывания при поиске точных терминов.'
  },"""

new_k055_7 = """  'К-055:7': {
    q: 'Зачем в шаблоне поиска `r"\\\\bcat\\\\b"` используется якорь границы слова `\\\\b`?',
    options: [
      'Чтобы найти изолированное слово `cat`, исключив совпадения внутри `category` или `scatter`',
      'Чтобы сопоставить символ обратного слэша',
      'Чтобы перевести регулярное выражение в режим байтовой строки'
    ],
    correct: 0,
    explain: 'Якорь границы слова `\\\\b` отмечает границу между буквенно-цифровым символом `\\\\w` и непробельным/пробельным. Это предотвращает ложные срабатывания при поиске точных терминов.'
  },"""

if old_k055_7 in content:
    content = content.replace(old_k055_7, new_k055_7)
    print('✓ Bug 111: Fixed K-055:7 regex backslash escape')
else:
    # try regex replacement for K-055:7
    pattern = re.compile(r"'К-055:7':\s*\{\s*q:\s*'Зачем в шаблоне поиска `r\"[^\"]*\"`[^\}]+\}", re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(new_k055_7.strip(), content)
        print('✓ Bug 111: Fixed K-055:7 regex backslash escape (regex)')
    else:
        print('! Bug 111: K-055:7 not found')

# -------------------------------------------------------------
# 3. Bug 112: Trailing comment in K-222:5
# -------------------------------------------------------------
old_pure = 'pure = PurePosixPath(&quot;/etc/hosts&quot;)\\nprint(pure.name)  # hosts\\n\\n'
new_pure = 'pure = PurePosixPath(&quot;/etc/hosts&quot;)\\nprint(pure.name)  # => \'hosts\'\\n\\n'
if old_pure in content:
    content = content.replace(old_pure, new_pure)
    print('✓ Bug 112: Replaced trailing comment in K-222:5')
else:
    print('! Bug 112: pure comment not found')

# -------------------------------------------------------------
# 4. Bug 108 & 109 & 110: viewPythonSkill improvements
#    - Visible Step Counter + Segmented Stepper (Bug 108)
#    - Step vs Theme terminology (Bug 109)
#    - Phased Transition & Single Dominant CTA (Bug 110)
# -------------------------------------------------------------
# Replacement in eyebrowDotsHTML:
old_eyebrow = """  // Деликатный двухстрочный заголовок: название юнита приглушено и не кричит (Refined Eyebrow), активная тема — выразительный элегантный фокус
  const eyebrowDotsHTML = `
    <div class="topic-eyebrow-track" style="max-width:100%;margin:16px 0 22px;padding:0 2px;">
      <div style="display:flex;flex-direction:column;gap:12px;width:100%;">
        <div style="display:flex;flex-direction:column;align-items:flex-start;gap:2px;max-width:760px;margin:0 auto;width:100%;">
          <div style="font-family:var(--font-b);font-size:0.80rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.01em;line-height:1.2;">${escapeHtmlStr(cleanUnitTitleVal)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-b);font-size:1.06rem;font-weight:600;color:var(--ink);line-height:1.35;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}
        </div>
        <div style="display:flex;justify-content:center;width:100%;">
          ${dotsNecklaceHTML}
        </div>
      </div>
    </div>`;"""

new_eyebrow = """  // Деликатный заголовок: название юнита приглушено (Refined Eyebrow), активная тема, ожерелье и сегментированный степпер микро-шагов
  const stepProgressSegmentsHTML = (pySkillViewState.tab === 'theory' && steps.length > 1) ? `
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;max-width:760px;margin:10px auto 0;width:100%;">
      <div style="display:flex;justify-content:space-between;align-items:center;width:100%;font-size:0.76rem;color:var(--ink-muted);font-weight:600;">
        <span class="step-counter-pill" style="display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:2px 10px;border-radius:999px;">Шаг ${stepIdx + 1} из ${steps.length}</span>
        <span style="opacity:0.8;">Сессия ~2 мин · Активное микрообучение</span>
      </div>
      <div class="step-segmented-track" style="display:flex;gap:4px;width:100%;height:4px;border-radius:999px;overflow:hidden;">
        ${steps.map((_, si) => `<div class="step-segment" style="flex:1;height:100%;border-radius:999px;background:${si <= stepIdx ? '#10b981' : 'rgba(255,255,255,0.12)'};transition:background .2s ease;"></div>`).join('')}
      </div>
    </div>` : '';

  const eyebrowDotsHTML = `
    <div class="topic-eyebrow-track" style="max-width:100%;margin:16px 0 22px;padding:0 2px;">
      <div style="display:flex;flex-direction:column;gap:12px;width:100%;">
        <div style="display:flex;flex-direction:column;align-items:flex-start;gap:2px;max-width:760px;margin:0 auto;width:100%;">
          <div style="font-family:var(--font-b);font-size:0.80rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.01em;line-height:1.2;">${escapeHtmlStr(cleanUnitTitleVal)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-b);font-size:1.06rem;font-weight:600;color:var(--ink);line-height:1.35;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}
        </div>
        <div style="display:flex;justify-content:center;width:100%;">
          ${dotsNecklaceHTML}
        </div>
        ${stepProgressSegmentsHTML}
      </div>
    </div>`;"""

if old_eyebrow in content:
    content = content.replace(old_eyebrow, new_eyebrow)
    print('✓ Bug 108: Added visible step counter and segmented progress bar to eyebrowDotsHTML')
else:
    print('! Bug 108: old_eyebrow not found')

# Terminology & CTA Phased Flow in viewPythonSkill
old_step_check_render = """    if(!hasMoreChunks && stepCheck){
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
        <div class="step-check-container" style="margin-top:24px;padding:20px;border-radius:16px;background:rgba(255,255,255,0.03);border:1.5px solid rgba(16,185,129,0.3);box-shadow:0 8px 24px rgba(0,0,0,0.18);">
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
              <button type="button" class="${isCorrect ? 'btn-3d-emerald btn-coddy-emerald' : 'btn-glass-emerald'} btn-sprint-cta" style="flex:1;" data-py-step-check-next>
                ${stepIdx + 1 < steps.length ? 'Дальше к следующей теме ➔' : (isRead ? '✓ Конспект усвоен ➔' : '✓ Завершить конспект (+10 MP) ➔')}
              </button>
            </div>
          </div>`;
      }
    }

    let primaryActionHTML = '';
    if(hasMoreChunks){
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;max-width:440px;" data-chunk-more="py">Понятно, дальше (+10 XP) ➔</button>`;
    } else if(stepCheck){
      if(pySkillViewState.stepCheckRevealed){
        primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;max-width:440px;" data-py-step-check-next>${stepIdx + 1 < steps.length ? 'Дальше к следующей теме ➔' : (isRead ? '✓ Конспект усвоен' : '✓ Завершить конспект (+10 MP)')}</button>`;
      } else {
        primaryActionHTML = `<div style="font-size:0.86rem;color:var(--ink-muted);font-weight:600;padding:8px 0;text-align:center;">👆 Ответьте на вопрос для продолжения</div>`;
      }
    } else if(stepIdx + 1 < steps.length){"""

new_step_check_render = """    const isCheckPhase = !!pySkillViewState.stepPhaseCheck || !!pySkillViewState.stepCheckRevealed;

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
    } else if(stepIdx + 1 < steps.length){"""

if old_step_check_render in content:
    content = content.replace(old_step_check_render, new_step_check_render)
    print('✓ Bug 109 & 110: Fixed step vs theme terminology and phased Single Dominant CTA')
else:
    print('! Bug 109 & 110: old_step_check_render not found')

# Event listener for data-py-start-check:
old_psa_event = """  // Coddy Pedagogy Active Comprehension Check (Bug 85)
  const psa = e.target.closest('[data-py-step-answer]');"""

new_psa_event = """  // Active Comprehension Check Phase Start
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
  const psa = e.target.closest('[data-py-step-answer]');"""

if old_psa_event in content:
    content = content.replace(old_psa_event, new_psa_event)
    print('✓ Bug 110: Added click listener for data-py-start-check')
else:
    print('! Bug 110: old_psa_event not found')

# Reset stepPhaseCheck on next step
old_pscn_reset = """    pySkillViewState.stepCheckRevealed = false;
    pySkillViewState.stepCheckChosen = null;"""

new_pscn_reset = """    pySkillViewState.stepCheckRevealed = false;
    pySkillViewState.stepCheckChosen = null;
    pySkillViewState.stepPhaseCheck = false;"""

if old_pscn_reset in content:
    content = content.replace(old_pscn_reset, new_pscn_reset)
    print('✓ Bug 110: Reset stepPhaseCheck on next step')

# -------------------------------------------------------------
# 5. Bug 113: Rule 7 Strict Ban on "Coddy" in CSS and Code
# -------------------------------------------------------------
replacements = [
    ('.btn-coddy-emerald', '.btn-action-emerald'),
    ('.btn-coddy-ruby', '.btn-action-ruby'),
    ('btn-coddy-emerald', 'btn-action-emerald'),
    ('btn-coddy-ruby', 'btn-action-ruby'),
    ('.coddy-code-block', '.theory-code-block'),
    ('coddy-code-block', 'theory-code-block'),
    ('.coddy-lesson-card', '.interactive-step-card'),
    ('coddy-lesson-card', 'interactive-step-card'),
    ('.coddy-table', '.compare-table'),
    ('coddy-table', 'compare-table'),
    ('coddyStreamReveal', 'streamChunkReveal'),
    ('@keyframes coddyFadeIn', '@keyframes stepFadeIn'),
    ('animation:coddyFadeIn', 'animation:stepFadeIn'),
]

for old, new in replacements:
    cnt = content.count(old)
    if cnt > 0:
        content = content.replace(old, new)
        print(f'✓ Bug 113: Replaced {old} -> {new} ({cnt} times)')

with open(ACADEMY_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

with open(ETALON_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nSuccessfully updated academy.html and Эталоны/Эталоны.html!')
