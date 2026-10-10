import re
import shutil

ACADEMY_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"
SW_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\sw.js"
EXTRACTED_JS_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\scripts\extracted_academy.js"

with open(ACADEMY_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Сформируем новую функцию viewPythonSkill(sid)
new_view_python_skill = """function viewPythonSkill(sid){
  const sk = ensurePySkillState(sid);
  const tr = getTrackForSkill(sk.id);
  const mp = getSkillMP(sk.id);
  const effTier = getEffectiveSkillTier(sk.id);
  const echMeta = getEchelonMeta(effTier);
  const solvedMap = getIdeSolvedMap();
  const celebrationBanner = buildSprintFinishCelebrationHTML(pySkillViewState.sprintCelebration);

  const activeK = pySkillViewState.kId || (sk.kIds && sk.kIds[0]);
  const noteObj = ALL_NOTES_COMBINED[activeK] || {id: activeK, title: activeK, steps: [{title: activeK, html: '<p>Конспект загружается.</p>'}]};
  const steps = noteObj.steps || [];
  const stepIdx = Math.min(pySkillViewState.stepIdx, Math.max(0, steps.length - 1));
  const curStep = steps[stepIdx] || {title: noteObj.title, html: ''};
  const chunks = splitStepHtmlIntoChunks(curStep.html).slice();
  if(chunks.length > 0 && curStep.title && !/^<h[1-6]\\b/i.test(String(chunks[0] || '').trim())){
    chunks[0] = `<h4>${curStep.title}</h4>\\n` + chunks[0];
  }
  const totalChunks = chunks.length;
  const curChunkIdx = Math.min(pySkillViewState.chunkIdx || 0, Math.max(0, totalChunks - 1));

  const curEchTier = effTier || 1;
  const echProg = (typeof getEchelonProgress === 'function') ? getEchelonProgress(curEchTier) : { pct: 35 };
  const echPct = echProg.pct || 0;
  const dayXpVal = (typeof todayXp === 'function') ? todayXp() : 0;

  const focusTopbarHTML = `
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
        <div class="sprint-xp-pill" style="display:inline-flex;align-items:center;gap:4px;padding:5px 11px;border-radius:999px;background:rgba(245,158,11,0.14);border:1px solid rgba(245,158,11,0.35);color:#fbbf24;font-size:0.75rem;font-weight:700;white-space:nowrap;letter-spacing:0.01em;" title="Заработано за сутки: ${dayXpVal} XP">⚡ +${dayXpVal || 55} XP за сутки</div>
        <a href="#/docs" class="topbar-help-btn" style="padding:6px 14px;border-radius:10px;" title="Справочник синтаксиса и методов Python"><span class="topbar-help-text">📖 Справка</span></a>
      </div>
    </div>
    <div id="theory-audio-bar" class="theory-audio-bar" style="display:${state.audioBarOpen ? 'flex' : 'none'};">
      <button type="button" class="theory-audio-btn" data-audio-play title="Воспроизвести / Пауза">▶</button>
      <button type="button" class="theory-audio-btn" data-audio-rewind title="Перемотка назад на 10 сек">⏪ -10с</button>
      <button type="button" class="theory-audio-btn" data-audio-rate title="Скорость чтения">1.0x</button>
      <span class="audio-status-text">Аудио-компаньон</span>
      <button type="button" class="theory-audio-btn" data-audio-close style="margin-left:auto;" title="Скрыть аудио-бар">✕</button>
    </div>`;

  // Расчёт непрерывной нити точек (Continuous Atomic Dots) строго для текущего навыка
  const curUnit = (typeof ALL_UNITS_COMBINED !== 'undefined') ? (ALL_UNITS_COMBINED.find(u => u.id === sk.unitId) || { skills: [sk], title: sk.title || '' }) : { skills: [sk], title: sk.title || '' };
  const rawUnitTitle = curUnit.title || sk.title || '';
  const cleanUnitTitle = rawUnitTitle.replace(/^Юнит\\s+[\\d.]+\\s*[·•\\-:]\\s*/i, '').trim() || rawUnitTitle;

  // 1. Конспекты теории текущего навыка
  const noteDots = (sk.kIds || []).map((kId, idx) => {
    const n = ALL_NOTES_COMBINED[kId] || { title: kId };
    const isDone = state.readNotes.includes(kId);
    const isActive = (pySkillViewState.tab === 'theory' && kId === activeK);
    return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="📖 Конспект: ${escapeHtmlStr(n.title)}" data-py-select-k="${kId}" data-py-skill-id="${sk.id}"></span>`;
  }).join('');

  // 2. Флеш-карточки текущего навыка
  const activeF = pySkillViewState.fId || (sk.fIds && sk.fIds[0]);
  const cardDots = (sk.fIds || []).map((fid, idx) => {
    const d = ALL_DECKS_COMBINED[fid] || {};
    const isDone = state.reviewedDecks.includes(fid);
    const isActive = (pySkillViewState.tab === 'cards' && (activeF === fid || (!activeF && idx === 0)));
    return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="🗂️ Карточки: ${escapeHtmlStr(d.title || fid)}" data-py-select-f="${fid}"></span>`;
  }).join('');

  // 3. Задачи практики кода текущего навыка
  const tIds = (sk.taskIds && sk.taskIds.length) ? sk.taskIds : [20, 19, 39, 255, 258];
  const activeTid = tIds.includes(pySkillViewState.taskId) ? pySkillViewState.taskId : tIds[0];
  const taskDots = tIds.map((tid, idx) => {
    const t = IDE_TASKS_BY_ID[tid] || {};
    const isDone = (solvedMap[tid] === 'solved');
    const isActive = (pySkillViewState.tab === 'code' && (activeTid === tid || (!activeTid && idx === 0)));
    return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="⚡ Задача #${tid}: ${escapeHtmlStr(t.title || '')}" data-py-select-task="${tid}"></span>`;
  }).join('');

  // 4. Рубежный зачёт Юнита
  const examActive = (pySkillViewState.tab === 'exam');
  const examDot = `<span class="dot-jewel milestone ${examActive ? 'active' : ''}" title="👑 Рубежный зачёт Юнита ${sk.unitId}" data-py-select-exam="${sk.unitId}"></span>`;

  const dotsNecklaceHTML = `
    <div class="dots-necklace" id="radar-dots-necklace" title="Конспекты → Карточки → Практика → Зачёт">
      ${noteDots}
      <span class="dots-stage-divider" title="Переход к карточкам"></span>
      ${cardDots}
      <span class="dots-stage-divider" title="Переход к практике"></span>
      ${taskDots}
      <span class="dots-stage-divider" title="Рубежный зачёт"></span>
      ${examDot}
    </div>`;

  let activeItemTitle = '';
  if(pySkillViewState.tab === 'theory'){
    const rawNoteTitle = (noteObj && noteObj.title) || activeK || '';
    activeItemTitle = rawNoteTitle.replace(/^К-\\d+\\s*[:·•\\-]\\s*/i, '').trim();
  } else if(pySkillViewState.tab === 'cards'){
    const curDeck = ALL_DECKS_COMBINED[activeF] || {};
    const rawDeckTitle = curDeck.title || activeF || '';
    activeItemTitle = rawDeckTitle.replace(/^Ф-\\d+\\s*[:·•\\-]\\s*/i, '').trim();
  } else if(pySkillViewState.tab === 'code'){
    const curTask = IDE_TASKS_BY_ID[activeTid] || {};
    activeItemTitle = curTask.title || ('Задача #' + activeTid);
  } else if(pySkillViewState.tab === 'exam'){
    activeItemTitle = 'Рубежный зачёт Юнита ' + sk.unitId;
  }

  // Деликатный двухстрочный заголовок: название юнита приглушено и не кричит (Refined Eyebrow), активная тема — выразительный элегантный фокус
  const eyebrowDotsHTML = `
    <div class="topic-eyebrow-track" style="max-width:780px;margin:14px auto 20px;">
      <div style="display:flex;flex-direction:column;gap:12px;width:100%;">
        <div style="display:flex;flex-direction:column;align-items:flex-start;padding-left:2px;gap:2px;">
          <div style="font-family:var(--font-b);font-size:0.82rem;font-weight:600;color:var(--ink-muted);letter-spacing:0.04em;text-transform:uppercase;line-height:1.2;">${escapeHtmlStr(cleanUnitTitle)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-d);font-size:1.15rem;font-weight:600;color:var(--ink);line-height:1.3;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}
        </div>
        <div style="display:flex;justify-content:center;width:100%;">
          ${dotsNecklaceHTML}
        </div>
      </div>
    </div>`;

  let bodyHTML = '';
  if(pySkillViewState.tab === 'theory'){
    const isRead = state.readNotes.includes(activeK);

    const feedHTML = `<div class="scroll-feed" id="py-theory-text">` + chunks.slice(0, curChunkIdx + 1).map((ch, ci) =>
      `<div class="feed-chunk ${ci < curChunkIdx ? 'feed-chunk-prev' : 'feed-chunk-new'} lesson-theory" data-chunk-idx="${ci}">${ch}</div>`
    ).join('') + `</div>`;

    const hasMoreChunks = (curChunkIdx + 1 < totalChunks);
    const canGoBack = (curChunkIdx > 0 || stepIdx > 0);
    const backBtnHTML = canGoBack ? `<button type="button" class="btn btn-ghost" data-chunk-prev="py" style="padding:11px 16px;border-radius:14px;font-size:.88rem;">← Назад</button>` : '';

    let primaryActionHTML = '';
    if(hasMoreChunks){
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-chunk-more="py">Понятно, дальше (+10 XP) ➔</button>`;
    } else if(stepIdx + 1 < steps.length){
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-py-next-step="${stepIdx+1}">Понятно, дальше (+10 XP) ➔</button>`;
    } else {
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-py-finish-note="${activeK}">${isRead ? '✓ Конспект усвоен' : '✓ Завершить конспект (+10 MP)'}</button>`;
    }

    bodyHTML = `
      <div class="card coddy-lesson-card" style="margin-top:0;">
        ${feedHTML}
        <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:18px;padding-top:14px;border-top:1px solid var(--glass-border);flex-wrap:wrap;">
          <div>${backBtnHTML}</div>
          <div style="display:flex;gap:10px;align-items:center;">
            <button type="button" class="btn btn-ghost" data-audio-toggle style="padding:11px 14px;border-radius:14px;font-size:.88rem;" title="Слушать аудио">🎧 Озвучить</button>
            ${primaryActionHTML}
          </div>
        </div>
      </div>`;
  } else if(pySkillViewState.tab === 'cards'){
    const deckObj = ALL_DECKS_COMBINED[activeF] || {id: activeF, title: activeF, cards: []};
    const cards = deckObj.cards || [];
    const cardIdx = Math.min(pySkillViewState.cardIdx, Math.max(0, cards.length - 1));
    const curCard = cards[cardIdx] || {q: 'Карточек пока нет', a: ''};
    const isFlipped = pySkillViewState.cardFlipped;

    bodyHTML = `
      <div class="card" style="margin-top:0;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
          <span style="font-size:0.80rem;color:var(--ink-muted);font-weight:600;">Карточка ${cards.length ? cardIdx + 1 : 0} из ${cards.length}</span>
          <span style="font-size:0.75rem;padding:2px 8px;border-radius:999px;background:rgba(20,90,70,0.1);color:var(--moss);font-weight:600;">Интервальное повторение</span>
        </div>
        <div class="py-flashcard ${isFlipped ? 'flipped' : ''}" data-py-flip-card style="min-height:180px;cursor:pointer;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:26px 20px;border-radius:16px;background:rgba(255,255,255,0.03);border:1px solid var(--glass-border);transition:all .25s ease;">
          <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:.05em;color:var(--ink-muted);margin-bottom:8px;">${isFlipped ? 'Ответ' : 'Вопрос (нажмите или пробел)'}</div>
          <div style="font-size:1.08rem;font-weight:600;line-height:1.45;color:var(--ink);">${isFlipped ? curCard.a : curCard.q}</div>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:16px;">
          <button class="btn btn-ghost" data-py-prev-card ${cardIdx === 0 ? 'disabled' : ''}>← Назад</button>
          <div style="display:flex;gap:8px;">
            <button class="btn btn-ghost" data-py-rate-card="hard" title="Повторить скоро">Сложно</button>
            <button class="btn btn-ghost" data-py-rate-card="good" title="В пределах нормы">Нормально</button>
            <button class="btn btn-emerald" data-py-rate-card="easy" title="Отлично знаю">Легко (+5 MP)</button>
          </div>
          <button class="btn btn-ghost" data-py-next-card ${cardIdx + 1 >= cards.length ? 'disabled' : ''}>Дальше →</button>
        </div>
      </div>`;
  } else if(pySkillViewState.tab === 'code'){
    const tObj = IDE_TASKS_BY_ID[activeTid] || {id: activeTid, title: 'Задача #' + activeTid, desc: '', initialCode: ''};
    const socraticHints = buildSocraticHintsForTask(tObj);
    const shownHints = socraticHints.slice(0, pySkillViewState.hintLevel).map((h, i) =>
      `<div class="socratic-hint" style="margin:8px 0;padding:10px 14px;border-radius:12px;background:rgba(217,119,6,0.08);border-left:3px solid var(--amber);font-size:0.86rem;line-height:1.45;"><strong>💡 Наводка ${i+1}:</strong> ${h}</div>`
    ).join('');

    let runFeedback = '';
    if(pySkillViewState.runStatus === 'pass') runFeedback = `
      <div class="result-feedback result-feedback--pass" style="margin-top:12px;padding:12px;border-radius:12px;background:rgba(16,185,129,0.12);border:1px solid #10b981;color:#10b981;">
        <div style="font-weight:700;">✓ Все тесты пройдены! (+15 MP)</div>
      </div>`;
    else if(pySkillViewState.runStatus === 'fail') runFeedback = `
      <div class="result-feedback result-feedback--fail" style="margin-top:12px;padding:12px;border-radius:12px;background:rgba(239,68,68,0.12);border:1px solid #ef4444;color:#ef4444;">
        <div style="font-weight:700;">✗ Ошибка выполнения или неверный результат</div>
        <pre style="margin-top:6px;font-size:0.80rem;white-space:pre-wrap;">${escapeHtmlStr(pySkillViewState.runOutput)}</pre>
      </div>`;

    bodyHTML = `
      <div class="card" style="margin-top:0;">
        <div class="practice-layout">
          <div class="practice-left-pane">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
              <span class="topic-badge" style="margin:0;display:inline-flex;align-items:center;gap:6px;">Задача #${tObj.id} · <span class="badge" style="background:rgba(217,119,6,0.18);color:var(--amber);padding:1px 7px;border-radius:10px;font-weight:700;">${tObj.tier}</span> · ${tObj.topic}</span>
              <div style="display:flex;gap:8px;align-items:center;">
                <a href="#/docs" class="link-quiet" style="font-size:.78rem;">📚 Справка по методам Python</a>
                ${solvedMap[tObj.id]==='solved' ? `<span class="state-tag state-tag--mastered" style="margin:0;">✓ Решено</span>` : ''}
              </div>
            </div>
            <h2 style="margin-bottom:10px;">${tObj.title}</h2>
            <div class="lesson-theory" style="margin-bottom:12px;">${tObj.desc}</div>
            ${shownHints}
          </div>
          <div class="practice-right-pane">
            ${buildCodeEditorWithGutterHTML('py-skill-editor', pySkillViewState.codeDraft, 220)}
            <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
              <button class="btn-glass-emerald" data-py-run-task="${tObj.id}">${ICONS.play} Проверить решение (Ctrl+Enter)</button>
              <button class="btn btn-ghost" data-py-task-hint ${pySkillViewState.hintLevel>=socraticHints.length?'disabled':''}>💡 Сократовская наводка (${pySkillViewState.hintLevel}/${socraticHints.length})</button>
              <button class="btn btn-ghost" data-py-reset-task="${tObj.id}">Сбросить код</button>
            </div>
            ${runFeedback}
          </div>
        </div>
      </div>`;
  }

  return `
    <div class="container" style="max-width:880px;">
      ${focusTopbarHTML}
      ${celebrationBanner}
      ${eyebrowDotsHTML}
      ${bodyHTML}
    </div>`;
}"""

# Заменим функцию viewPythonSkill в academy.html
func_start = html.find("function viewPythonSkill(sid){")
if func_start == -1:
    raise Exception("function viewPythonSkill(sid) not found!")

func_end = html.find("function escapeHtmlStr(s){", func_start)
if func_end == -1:
    raise Exception("function escapeHtmlStr(s) not found!")

html = html[:func_start] + new_view_python_skill + "\n\n" + html[func_end:]
print("viewPythonSkill replaced")

# 2. Обновим обработчики кликов в click listener:
# Добавим tab switching для data-py-select-k, data-py-select-f, data-py-select-task и обработчик data-py-select-exam

# а) data-py-select-k: убедимся что pySkillViewState.tab = 'theory'
k_target = "const psk = e.target.closest('[data-py-select-k]');\n  if(psk){\n"
k_replace = "const psk = e.target.closest('[data-py-select-k]');\n  if(psk){\n    pySkillViewState.tab = 'theory';\n"
if k_target in html and "pySkillViewState.tab = 'theory';" not in html[html.find(k_target):html.find(k_target)+150]:
    html = html.replace(k_target, k_replace, 1)
    print("Updated data-py-select-k with pySkillViewState.tab = 'theory'")

# б) data-py-select-f: убедимся что pySkillViewState.tab = 'cards'
f_target = "const psf = e.target.closest('[data-py-select-f]');\n  if(psf){\n"
f_replace = "const psf = e.target.closest('[data-py-select-f]');\n  if(psf){\n    pySkillViewState.tab = 'cards';\n"
if f_target in html and "pySkillViewState.tab = 'cards';" not in html[html.find(f_target):html.find(f_target)+150]:
    html = html.replace(f_target, f_replace, 1)
    print("Updated data-py-select-f with pySkillViewState.tab = 'cards'")

# в) data-py-select-task: убедимся что pySkillViewState.tab = 'code'
task_target = "const pstask = e.target.closest('[data-py-select-task]');\n  if(pstask){\n    pySkillViewState.sprintCelebration = null;"
task_replace = "const pstask = e.target.closest('[data-py-select-task]');\n  if(pstask){\n    pySkillViewState.tab = 'code';\n    pySkillViewState.sprintCelebration = null;"
if task_target in html:
    html = html.replace(task_target, task_replace, 1)
    print("Updated data-py-select-task with pySkillViewState.tab = 'code'")

# г) data-py-select-exam: добавим обработчик перед data-py-select-k
if "closest('[data-py-select-exam]')" not in html:
    exam_handler = """  const pse = e.target.closest('[data-py-select-exam]');
  if(pse){
    const unitId = pse.getAttribute('data-py-select-exam');
    const tr = getTrackForSkill(pySkillViewState.sid || '1.1.1');
    location.hash = '#' + tr.routePrefix + '/unittest/' + unitId;
    return;
  }
"""
    k_pos = html.find("const psk = e.target.closest('[data-py-select-k]');")
    if k_pos != -1:
        html = html[:k_pos] + exam_handler + "\n" + html[k_pos:]
        print("Added data-py-select-exam click handler")

# 3. Сохраним academy.html
with open(ACADEMY_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("Saved academy.html successfully")

# 4. Обновим sw.js
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw = f.read()
sw = re.sub(r"const CACHE_NAME = 'academy-pwa-v\d+';", "const CACHE_NAME = 'academy-pwa-v28';", sw)
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw)
print("Updated sw.js to v28")

# 5. Обновим extracted_academy.js
script_m = re.findall(r'<script\b[^>]*>([\s\S]*?)<\/script>', html)
if script_m:
    largest = max(script_m, key=len)
    with open(EXTRACTED_JS_PATH, "w", encoding="utf-8") as f:
        f.write(largest)
    print("Updated scripts/extracted_academy.js")

print("All done!")
