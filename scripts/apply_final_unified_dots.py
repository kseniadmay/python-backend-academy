import re
import shutil

ACADEMY_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"
SW_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\sw.js"
EXTRACTED_JS_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\scripts\extracted_academy.js"

with open(ACADEMY_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Ensure CSS
css_to_inject = """
  /* ================= ТОПБАР: ЭШЕЛОН 1, ГОТОВНОСТЬ И ЯНТАРНЫЙ БЭЙДЖ ================= */
  .echelon-topbar-clean {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 18px;
    margin-bottom: 24px;
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
    justify-content: space-between;
    align-items: center;
    font-size: 0.74rem;
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
  }
  .echelon-clean-fill {
    height: 100%;
    width: 35%;
    border-radius: 999px;
    background: linear-gradient(90deg, #6b1d2f 0%, #be123c 35%, #059669 75%, #10b981 100%);
    box-shadow: none;
    position: relative;
  }

  /* ================= ЕДИНЫЙ ПЕДАГОГИЧЕСКИЙ ТРЕКЕР: CONTINUOUS ATOMIC DOTS ================= */
  .topic-eyebrow-track {
    display: flex;
    flex-direction: column;
    gap: 14px;
    margin-bottom: 22px;
    width: 100%;
  }
  .topic-eyebrow-tags {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    width: 100%;
  }
  .unit-breadcrumb {
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }
  .unit-breadcrumb-title {
    color: var(--ink);
    font-weight: 600;
    font-size: 0.88rem;
    letter-spacing: -0.01em;
  }

  .dots-necklace {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    width: 100%;
    position: relative;
    padding: 6px 0;
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
  .dot-jewel.active::before,
  .dot-jewel.active::after {
    content: '';
    position: absolute;
    left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.8);
    pointer-events: none;
    animation: radar-ripple-white 4.4s infinite cubic-bezier(0.2, 0.8, 0.4, 1);
  }
  .dot-jewel.active::after {
    animation-delay: 2.2s;
  }
  .dot-jewel.milestone {
    border-radius: 2px;
    transform: rotate(45deg);
    background: rgba(255, 255, 255, 0.25);
  }
  .dot-jewel.milestone:hover {
    transform: rotate(45deg) scale(1.4);
  }

  @keyframes radar-breathe-white {
    0%, 100% {
      box-shadow: 0 0 8px #ffffff, 0 0 16px rgba(255, 255, 255, 0.75), 0 0 26px rgba(255, 255, 255, 0.4);
    }
    50% {
      box-shadow: 0 0 14px #ffffff, 0 0 28px rgba(255, 255, 255, 1), 0 0 46px rgba(255, 255, 255, 0.7);
    }
  }
  @keyframes radar-ripple-white {
    0% { width: 9px; height: 9px; opacity: 1; border-color: rgba(255, 255, 255, 0.9); }
    100% { width: 32px; height: 32px; opacity: 0; border-color: rgba(255, 255, 255, 0); }
  }
"""

if ".echelon-bordeaux-title" not in html:
    style_pos = html.find("</style>")
    if style_pos != -1:
        html = html[:style_pos] + "\n" + css_to_inject + "\n" + html[style_pos:]
        print("Injected CSS into academy.html")
    else:
        print("Warning: </style> not found")

# 2. Replace viewPythonSkill function completely with the new clean, continuous version
new_view_python_skill = """function viewPythonSkill(sid){
  const sk = ensurePySkillState(sid);
  const tr = getTrackForSkill(sk.id);
  const mp = getSkillMP(sk.id);
  const effTier = getEffectiveSkillTier(sk.id);
  const echMeta = getEchelonMeta(effTier);
  const solvedMap = getIdeSolvedMap();
  const celebrationBanner = buildSprintFinishCelebrationHTML(pySkillViewState.sprintCelebration);

  const activeK = pySkillViewState.kId || sk.kIds[0];
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

  // Расчёт непрерывной нити точек (Continuous Atomic Dots) для всего Юнита
  const curUnit = (typeof ALL_UNITS_COMBINED !== 'undefined') ? (ALL_UNITS_COMBINED.find(u => u.id === sk.unitId) || { skills: [sk], title: sk.title || '' }) : { skills: [sk], title: sk.title || '' };
  const allUnitNotes = [];
  (curUnit.skills || [sk]).forEach(s => {
    (s.kIds || []).forEach(k => {
      const n = ALL_NOTES_COMBINED[k] || { title: k };
      allUnitNotes.push({ kId: k, skillId: s.id, title: n.title });
    });
  });

  const rawUnitTitle = curUnit.title || sk.title || '';
  const cleanUnitTitle = rawUnitTitle.replace(/^Юнит\\s+[\\d.]+\\s*[·•\\-:]\\s*/i, '').trim() || rawUnitTitle;

  // 1. Конспекты теории
  const noteDots = allUnitNotes.map((item, idx) => {
    const isDone = state.readNotes.includes(item.kId);
    const isActive = (pySkillViewState.tab === 'theory' && item.kId === activeK);
    return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="📖 Конспект: ${escapeHtmlStr(item.title)}" data-py-select-k="${item.kId}" data-py-skill-id="${item.skillId}"></span>`;
  }).join('');

  // 2. Флеш-карточки
  const activeF = pySkillViewState.fId || (sk.fIds && sk.fIds[0]);
  const cardDots = (sk.fIds || []).map((fid, idx) => {
    const d = ALL_DECKS_COMBINED[fid] || {};
    const isDone = state.reviewedDecks.includes(fid);
    const isActive = (pySkillViewState.tab === 'cards' && (activeF === fid || (!activeF && idx === 0)));
    return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="🗂️ Карточки: ${escapeHtmlStr(d.title || fid)}" data-py-select-f="${fid}"></span>`;
  }).join('');

  // 3. Задачи практики кода
  const tIds = (sk.taskIds && sk.taskIds.length) ? sk.taskIds : [240, 241, 242];
  const activeTid = tIds.includes(pySkillViewState.taskId) ? pySkillViewState.taskId : tIds[0];
  const taskDots = tIds.map((tid, idx) => {
    const t = IDE_TASKS_BY_ID[tid] || {};
    const isDone = (solvedMap[tid] === 'solved');
    const isActive = (pySkillViewState.tab === 'code' && (activeTid === tid || (!activeTid && idx === 0)));
    return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="⚡ Задача #${tid}: ${escapeHtmlStr(t.title || '')}" data-py-select-task="${tid}"></span>`;
  }).join('');

  // 4. Рубежный зачёт
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
    activeItemTitle = rawNoteTitle.replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();
  } else if(pySkillViewState.tab === 'cards'){
    const curDeck = ALL_DECKS_COMBINED[activeF] || {};
    const rawDeckTitle = curDeck.title || activeF || '';
    activeItemTitle = rawDeckTitle.replace(/^Ф-\d+\s*[:·•\-]\s*/i, '').trim();
  } else if(pySkillViewState.tab === 'code'){
    const curTask = IDE_TASKS_BY_ID[activeTid] || {};
    activeItemTitle = curTask.title || ('Задача #' + activeTid);
  } else if(pySkillViewState.tab === 'exam'){
    activeItemTitle = 'Рубежный зачёт';
  }

  const eyebrowDotsHTML = `
    <div class="topic-eyebrow-track" style="max-width:780px;margin:14px auto 20px;">
      <div style="display:flex;flex-direction:column;gap:14px;width:100%;">
        <div style="display:flex;flex-direction:column;align-items:flex-start;padding-left:2px;">
          <h2 style="font-family:var(--font-d);font-size:1.15rem;font-weight:700;color:var(--ink);letter-spacing:-0.01em;line-height:1.25;margin:0;">${escapeHtmlStr(cleanUnitTitle)}</h2>
          ${activeItemTitle ? `<div style="font-family:var(--font-b);font-size:0.88rem;font-weight:500;color:var(--ink-soft);line-height:1.4;margin-top:3px;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}
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

    const primaryActionHTML = hasMoreChunks ? `
      <div style="margin-top:12px;display:flex;gap:8px;align-items:center;">
        ${backBtnHTML}
        <button class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-chunk-more="py">Понятно, дальше (+10 XP) ➔</button>
      </div>` : `
      <div style="margin-top:12px;">
        <div style="display:flex;gap:8px;align-items:center;">
          ${backBtnHTML}
          ${stepIdx + 1 < steps.length
            ? `<button class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-py-next-step="${stepIdx+1}">Понятно, дальше (+10 XP) ➔</button>`
            : `<button class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-py-finish-note="${activeK}">✓ Конспект изучен — перейти к карточкам (+15 XP) ${ICONS.arrowRight}</button>`}
        </div>
        <div style="display:flex;justify-content:flex-end;align-items:center;gap:8px;margin-top:6px;">
          <span class="meta">${isRead ? '✓ Теория прочитана' : 'Этап 1 из 3: Теория → Карточки → Код'}</span>
        </div>
      </div>`;

    bodyHTML = pySkillViewState.fullNoteMode
      ? `<div class="coddy-lesson-card" style="max-width:780px;margin:0 auto;">` + steps.map((st, i) => `<div class="microstep-card"><div class="topic-badge">Шаг ${i+1} из ${steps.length}</div><h3>${st.title}</h3><div class="lesson-theory">${decorateCodeBlocksWithRunBtn(st.html)}</div></div>`).join('') + `</div>`
      : `<div class="coddy-lesson-card" style="max-width:780px;margin:0 auto;">${feedHTML}${primaryActionHTML}</div>`;
  } else if(pySkillViewState.tab === 'cards'){
    const deckObj = ALL_DECKS_COMBINED[activeF] || {id: activeF, title: activeF, cards: []};
    const cards = deckObj.cards || [];
    const cIdx = Math.min(pySkillViewState.cardIdx, Math.max(0, cards.length - 1));
    const curCard = cards[cIdx] || {q: 'Карточки загружаются', a: ''};

    bodyHTML = `
      <div class="fc-stage" style="margin:10px auto;max-width:780px;">
        <div class="fc-card ${pySkillViewState.cardFlipped?'fc-card--Answer':''}" data-py-flip-card>
          <div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div class="topic-badge">${pySkillViewState.cardFlipped ? 'Ответ' : 'Вопрос'}</div>
              <a href="#/docs" class="card-help-badge" onclick="event.stopPropagation();" title="Открыть справку по теме в боковой панели">💡 Шпаргалка</a>
            </div>
            <div class="fc-q">${formatRichInlineText(curCard.q)}</div>
            ${pySkillViewState.cardFlipped ? `<div class="fc-a">${formatRichInlineText(curCard.a)}</div>` : ''}
          </div>
          <div class="meta" style="margin-top:12px;text-align:center;">Карточка ${cIdx+1} из ${cards.length}</div>
        </div>
        ${pySkillViewState.cardFlipped ? `
          <div class="fc-rate-row" style="margin-top:12px;">
            <button class="btn btn-ghost" data-py-rate-card="1">Снова</button>
            <button class="btn btn-burgundy" data-py-rate-card="2">Трудно (+2 XP)</button>
            <button class="btn btn-clay" data-py-rate-card="3">Хорошо (+5 XP)</button>
            <button class="btn btn-primary" data-py-rate-card="4">Легко (+10 XP)</button>
          </div>` : `
          <div style="margin-top:12px;display:flex;gap:10px;flex-wrap:wrap;">
            <button class="btn btn-ghost" data-py-prev-card ${cIdx===0?'disabled':''}>← Назад</button>
            <button class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-py-flip-card>Показать ответ (Пробел)</button>
            <button class="btn btn-ghost" data-py-rate-card="3">Дальше →</button>
          </div>`}
      </div>`;
  } else {
    // Code Practice tab
    pySkillViewState.taskId = activeTid;
    const tObj = IDE_TASKS_BY_ID[activeTid] || IDE_TASKS[0];
    if(!pySkillViewState.codeDraft) pySkillViewState.codeDraft = getIdeDraft(activeTid, tObj.initialCode);

    const socraticHints = buildSocraticHintsForTask(tObj);
    const socraticLabels = [
      'Уровень 0 (Zero Hint — Граничные условия)',
      'Уровень 1 (Conceptual Hint — Концепция)',
      'Уровень 2 (Structural Hint — Декомпозиция)',
      'Уровень 3 (Tactical Hint — Сигнатура и контракт)'
    ];
    const shownHints = socraticHints.slice(0, pySkillViewState.hintLevel).map((h, idx) =>
      `<div class="hint-box"><strong>${socraticLabels[idx] || ('Уровень опоры ' + idx)}:</strong> ${h}</div>`
    ).join('');

    const curTaskIdx = tIds.indexOf(activeTid);
    const nextUnsolvedTid = tIds.find(tid => tid !== activeTid && solvedMap[tid] !== 'solved') || (curTaskIdx >= 0 && curTaskIdx + 1 < tIds.length ? tIds[curTaskIdx + 1] : null);
    let runFeedback = '';
    if(pySkillViewState.runStatus === 'running') runFeedback = `<div class="test-running-shimmer" style="margin-top:10px;">⚡ Выполняю тесты в Python…</div>`;
    else if(pySkillViewState.runStatus === 'pass') runFeedback = `
      <div class="result-box--pass correct-pulse-anim">${ICONS.check} Все тесты пройдены! (+25 XP, навык закреплён на практике!)\\n${pySkillViewState.runOutput||''}</div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;">
        ${nextUnsolvedTid ? `<button class="btn btn-primary" data-py-select-task="${nextUnsolvedTid}">Следующая задача навыка (#${nextUnsolvedTid}) →</button>` : ''}
        <a href="#${tr.routePrefix}/unittest/${sk.unitId}" class="btn btn-clay">⚡ Пройти рубежный Unit Test ${sk.unitId} (на 100 MP 👑)</a>
      </div>`;
    else if(pySkillViewState.runStatus === 'fail') runFeedback = `
      <div class="result-box--fail">Пока не проходит:\\n${pySkillViewState.runOutput||''}</div>
      <div style="margin-top:8px;"><button class="btn btn-ghost" style="padding:6px 12px;font-size:.78rem;" data-py-task-hint>💡 Разобрать ошибку с Сократовским интервьюером (${pySkillViewState.hintLevel}/${socraticHints.length})</button></div>`;

    bodyHTML = `
      <div class="microstep-card" style="max-width:780px;margin:0 auto;">
        <div class="practice-desktop-grid">
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

# Locate viewPythonSkill in academy.html
func_start = html.find("function viewPythonSkill(sid){")
if func_start == -1:
    raise Exception("function viewPythonSkill(sid) not found!")

# Find end of function (before function escapeHtmlStr(s))
func_end = html.find("function escapeHtmlStr(s){", func_start)
if func_end == -1:
    raise Exception("function escapeHtmlStr(s) not found!")

html = html[:func_start] + new_view_python_skill + "\n\n" + html[func_end:]
print("viewPythonSkill replaced successfully")

# 3. Add data-py-select-exam listener if missing
if "data-py-select-exam" not in html:
    exam_handler = """  const pse = e.target.closest('[data-py-select-exam]');
  if(pse){
    const unitId = pse.getAttribute('data-py-select-exam');
    const tr = getTrackForSkill(pySkillViewState.sid || '1.1.1');
    location.hash = '#' + tr.routePrefix + '/unittest/' + unitId;
    return;
  }
"""
    # Insert before const psk = e.target.closest('[data-py-select-k]');
    k_pos = html.find("const psk = e.target.closest('[data-py-select-k]');")
    if k_pos != -1:
        html = html[:k_pos] + exam_handler + "\n" + html[k_pos:]
        print("data-py-select-exam handler added")

# 4. Save academy.html
with open(ACADEMY_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("Saved academy.html")

# 5. Update sw.js to v24
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw_content = f.read()

sw_content = re.sub(r"const CACHE_NAME = 'academy-pwa-v\d+';", "const CACHE_NAME = 'academy-pwa-v27';", sw_content)
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw_content)
print("Updated sw.js to v27")

# 6. Extract academy script to scripts/extracted_academy.js if exists
try:
    script_m = re.findall(r'<script\b[^>]*>([\s\S]*?)<\/script>', html)
    if script_m:
        largest_script = max(script_m, key=len)
        with open(EXTRACTED_JS_PATH, "w", encoding="utf-8") as f:
            f.write(largest_script)
        print("Updated scripts/extracted_academy.js")
except Exception as e:
    print("Could not update extracted_academy.js:", e)

print("Done applying unified dots and topbar!")
