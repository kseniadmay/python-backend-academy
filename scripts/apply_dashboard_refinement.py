import os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_path = os.path.join(root, 'academy.html')

with open(academy_path, 'r', encoding='utf-8') as f:
    content = f.read()

print('Original academy.html length:', len(content))

# 1. Ban Coddy comment in viewDashboard
t1 = '// Рефакторинг экрана Дашборда в соответствии с инвариантами Coddy & Duolingo и дизайн-системой «Вечерний Обсидиан»'
r1 = '// Рефакторинг экрана Дашборда в соответствии с инвариантами активного микрообучения (Active Micro-learning) и дизайн-системой «Вечерний Обсидиан»'
assert t1 in content, 'Target 1 not found'
content = content.replace(t1, r1, 1)
print('1. [PASS] Removed Coddy mention from dashboard comment')

# 2. Universal step 1 phase subtitle (instead of hardcoded collections intuition)
t2 = "let stepPhaseName = 'Интуиция коллекций';"
r2 = "let stepPhaseName = 'Интуиция и основы';"
assert t2 in content, 'Target 2 not found'
content = content.replace(t2, r2, 1)
print('2. [PASS] Universal step 1 phase subtitle applied')

# 3. Dynamic title in SRS deck preview (instead of hardcoded list, tuple & slice)
t3 = 'Флеш-колода к теме: list, tuple & slice'
r3 = 'Флеш-колода к теме: ${escapeHtmlStr(cleanTitle)}'
assert t3 in content, 'Target 3 not found'
content = content.replace(t3, r3, 1)
print('3. [PASS] Dynamic title in SRS deck preview applied')

# 4. Human-friendly module counter in echelon topbar (avoid 0/3)
t4 = '<span class="meta echelon-mp-counter" style="font-size:.74rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:2px 7px;border-radius:6px;white-space:nowrap;flex-shrink:0;">Модуль 1 · ${curUnitDone}/${curUnitTotal}</span>'
r4 = '<span class="meta echelon-mp-counter" style="font-size:.74rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:2px 7px;border-radius:6px;white-space:nowrap;flex-shrink:0;">Модуль 1 · ${curUnitDone === 0 ? "Старт темы 1" : `${curUnitDone} из ${curUnitTotal} тем`}</span>'
assert t4 in content, 'Target 4 not found'
content = content.replace(t4, r4, 1)
print('4. [PASS] Human-friendly module counter applied')

# 5. Eliminate percentage duplication in echelon progress
t5 = "${e1CurMp === 0 ? 'Старт 🚀' : e1Pct + '%'}"
r5 = "${e1CurMp === 0 ? 'Старт 🚀' : 'Цель: 100% 🎯'}"
assert t5 in content, 'Target 5 not found'
content = content.replace(t5, r5, 1)
print('5. [PASS] Percentage duplication eliminated in echelon bar')

# 6. SVG phase icons in focusContextText with harmonized phase colors
t6 = """  // Чистый SVG-символ книги
  const bookIconSvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-2px;margin-right:4px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>`;

  let focusContextText = '';
  let focusCtaHTML = '';
  if(firstUnreadK){
    const savedReading = (state.readingPositions && state.readingPositions[focusSid]) || {};
    const hasAnyRead = (state.readNotes && state.readNotes.length > 0 && state.readNotes.some(k => focusKIds.includes(k)));
    const isStarted = Boolean(hasAnyRead || curKIdx > 0 || (savedReading.stepIdx && savedReading.stepIdx > 0) || (savedReading.chunkIdx && savedReading.chunkIdx > 0));
    const ctaLabel = isStarted ? 'Продолжить (2 мин)' : 'Начать (2 мин)';
    let stepPhaseName = 'Интуиция и основы';
    if(curKIdx === 1){
      stepPhaseName = 'Ключевые нюансы';
    } else if(curKIdx >= 2){
      stepPhaseName = 'Закрепление темы';
    }
    const currentStepNum = curKIdx + 1;
    focusContextText = `<span class="badge" style="background:rgba(16,185,129,0.14);border:1px solid rgba(16,185,129,0.3);color:#34d399;padding:2px 8px;border-radius:6px;font-size:0.74rem;font-weight:700;display:inline-flex;align-items:center;margin-right:6px;">📖 Теория</span> Шаг ${currentStepNum} из 13 (${stepPhaseName})`;
    focusCtaHTML = `<div class="focus-cta-wrap"><button class="btn-glass-emerald btn-sprint-cta btn-dominant-cta cocoon-focus-cta" data-quick-microstep="${focusSid}" data-quick-kid="${firstUnreadK}"><span class="cocoon-focus-cta-label">${ctaLabel}</span><span class="cocoon-focus-cta-right"><span class="btn-reward-badge">+15&nbsp;XP ⚡</span><span class="btn-cta-arrow">➔</span></span></button></div>`;
  } else if(firstUnreviewedF){
    const cardStepNum = focusKIds.length + curFIdx + 1;
    focusContextText = `<span class="badge" style="background:rgba(16,185,129,0.14);border:1px solid rgba(16,185,129,0.3);color:#34d399;padding:2px 8px;border-radius:6px;font-size:0.74rem;font-weight:700;display:inline-flex;align-items:center;margin-right:6px;">📇 Карточки</span> Шаг ${cardStepNum} из 13 · Закрепление темы карточками`;
    focusCtaHTML = `<div class="focus-cta-wrap"><a href="#/cards" data-srs-open-deck="${firstUnreviewedF}" class="btn-glass-emerald btn-sprint-cta btn-dominant-cta cocoon-focus-cta"><span class="cocoon-focus-cta-label">Повторить карточки (2 мин)</span><span class="cocoon-focus-cta-right"><span class="btn-reward-badge">+10&nbsp;XP ⚡</span><span class="btn-cta-arrow">➔</span></span></a></div>`;
  } else if(firstUnsolvedT){
    const practiceStepNum = focusKIds.length + cardList.length + curTIdx + 1;
    focusContextText = `<span class="badge" style="background:rgba(16,185,129,0.14);border:1px solid rgba(16,185,129,0.3);color:#34d399;padding:2px 8px;border-radius:6px;font-size:0.74rem;font-weight:700;display:inline-flex;align-items:center;margin-right:6px;">💻 Практика</span> Шаг ${practiceStepNum} из 13 · Практика в редакторе IDE`;
    focusCtaHTML = `<div class="focus-cta-wrap"><a href="#/practice?task=${firstUnsolvedT}" class="btn-glass-emerald btn-sprint-cta btn-dominant-cta cocoon-focus-cta"><span class="cocoon-focus-cta-label">Решить задачу в IDE</span><span class="cocoon-focus-cta-right"><span class="btn-reward-badge">+15&nbsp;XP ⚡</span><span class="btn-cta-arrow">➔</span></span></a></div>`;
  } else {
    focusContextText = `<span class="badge" style="background:rgba(16,185,129,0.14);border:1px solid rgba(16,185,129,0.3);color:#34d399;padding:2px 8px;border-radius:6px;font-size:0.74rem;font-weight:700;display:inline-flex;align-items:center;margin-right:6px;">🧪 Зачёт</span> Шаг 13 из 13 · Рубежный тест открыт`;"""

r6 = """  // Гармоничные векторные SVG-иконки для фаз карточки фокуса
  const phaseTheorySvg = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;margin-right:5px;flex-shrink:0;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>`;
  const phaseCardsSvg = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;margin-right:5px;flex-shrink:0;"><rect x="3" y="6" width="14" height="15" rx="2"></rect><path d="M7 2h12a2 2 0 0 1 2 2v13"></path></svg>`;
  const phasePracticeSvg = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;margin-right:5px;flex-shrink:0;"><polyline points="4 17 10 11 4 5"></polyline><line x1="12" y1="19" x2="20" y2="19"></line></svg>`;
  const phaseQuizSvg = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;margin-right:5px;flex-shrink:0;"><path d="M10 2v7.31L4.1 19.46A2 2 0 0 0 5.8 22h12.4a2 2 0 0 0 1.7-2.54L14 9.31V2"></path><path d="M8.5 2h7"></path><path d="M7 16h10"></path></svg>`;

  let focusContextText = '';
  let focusCtaHTML = '';
  if(firstUnreadK){
    const savedReading = (state.readingPositions && state.readingPositions[focusSid]) || {};
    const hasAnyRead = (state.readNotes && state.readNotes.length > 0 && state.readNotes.some(k => focusKIds.includes(k)));
    const isStarted = Boolean(hasAnyRead || curKIdx > 0 || (savedReading.stepIdx && savedReading.stepIdx > 0) || (savedReading.chunkIdx && savedReading.chunkIdx > 0));
    const ctaLabel = isStarted ? 'Продолжить (2 мин)' : 'Начать (2 мин)';
    let stepPhaseName = 'Интуиция и основы';
    if(curKIdx === 1){
      stepPhaseName = 'Ключевые нюансы';
    } else if(curKIdx >= 2){
      stepPhaseName = 'Закрепление темы';
    }
    const currentStepNum = curKIdx + 1;
    focusContextText = `<span class="badge" style="background:rgba(16,185,129,0.14);border:1px solid rgba(16,185,129,0.3);color:#34d399;padding:2px 8px;border-radius:6px;font-size:0.74rem;font-weight:700;display:inline-flex;align-items:center;margin-right:6px;">${phaseTheorySvg}Теория</span> Шаг ${currentStepNum} из 13 (${stepPhaseName})`;
    focusCtaHTML = `<div class="focus-cta-wrap"><button class="btn-glass-emerald btn-sprint-cta btn-dominant-cta cocoon-focus-cta" data-quick-microstep="${focusSid}" data-quick-kid="${firstUnreadK}"><span class="cocoon-focus-cta-label">${ctaLabel}</span><span class="cocoon-focus-cta-right"><span class="btn-reward-badge">+15&nbsp;XP ⚡</span><span class="btn-cta-arrow">➔</span></span></button></div>`;
  } else if(firstUnreviewedF){
    const cardStepNum = focusKIds.length + curFIdx + 1;
    focusContextText = `<span class="badge" style="background:rgba(129,140,248,0.14);border:1px solid rgba(129,140,248,0.3);color:#a5b4fc;padding:2px 8px;border-radius:6px;font-size:0.74rem;font-weight:700;display:inline-flex;align-items:center;margin-right:6px;">${phaseCardsSvg}Карточки</span> Шаг ${cardStepNum} из 13 · Закрепление темы карточками`;
    focusCtaHTML = `<div class="focus-cta-wrap"><a href="#/cards" data-srs-open-deck="${firstUnreviewedF}" class="btn-glass-emerald btn-sprint-cta btn-dominant-cta cocoon-focus-cta"><span class="cocoon-focus-cta-label">Повторить карточки (2 мин)</span><span class="cocoon-focus-cta-right"><span class="btn-reward-badge">+10&nbsp;XP ⚡</span><span class="btn-cta-arrow">➔</span></span></a></div>`;
  } else if(firstUnsolvedT){
    const practiceStepNum = focusKIds.length + cardList.length + curTIdx + 1;
    focusContextText = `<span class="badge" style="background:rgba(56,189,248,0.14);border:1px solid rgba(56,189,248,0.3);color:#38bdf8;padding:2px 8px;border-radius:6px;font-size:0.74rem;font-weight:700;display:inline-flex;align-items:center;margin-right:6px;">${phasePracticeSvg}Практика</span> Шаг ${practiceStepNum} из 13 · Практика в редакторе IDE`;
    focusCtaHTML = `<div class="focus-cta-wrap"><a href="#/practice?task=${firstUnsolvedT}" class="btn-glass-emerald btn-sprint-cta btn-dominant-cta cocoon-focus-cta"><span class="cocoon-focus-cta-label">Решить задачу в IDE (2 мин)</span><span class="cocoon-focus-cta-right"><span class="btn-reward-badge">+15&nbsp;XP ⚡</span><span class="btn-cta-arrow">➔</span></span></a></div>`;
  } else {
    focusContextText = `<span class="badge" style="background:rgba(251,191,36,0.14);border:1px solid rgba(251,191,36,0.3);color:#fbbf24;padding:2px 8px;border-radius:6px;font-size:0.74rem;font-weight:700;display:inline-flex;align-items:center;margin-right:6px;">${phaseQuizSvg}Зачёт</span> Шаг 13 из 13 · Рубежный тест открыт`;"""
assert t6 in content, 'Target 6 not found'
content = content.replace(t6, r6, 1)
print('6. [PASS] Clean SVG phase icons and consistent 2 min timing applied to hero card')

# 7. Practice dot fallback tooltip enhancement
t7 = "const shortT = taskShortTitles[tId] || 'Практическое задание';"
r7 = "const shortT = taskShortTitles[tId] || (typeof IDE_TASKS_BY_ID !== 'undefined' && IDE_TASKS_BY_ID[tId] && IDE_TASKS_BY_ID[tId].title) || 'Практическое задание';"
assert t7 in content, 'Target 7 not found'
content = content.replace(t7, r7, 1)
print('7. [PASS] Real task title fallback for practice dots applied')

# 8. Interactive state for Audio Companion Button
t8 = """  // Dashboard Audio Companion button
  if(e.target.closest('#dashAudioCompanionBtn, .topbar-audio-btn')){
    if(window.theoryAudioPlayer){
      const focusCardTitle = document.querySelector('.cocoon-focus-title');
      const focusText = 'Голосовой наставник Сократ. Текущий спринт-фокус: ' + (focusCardTitle ? focusCardTitle.innerText.trim() : 'коллекции Python');
      window.theoryAudioPlayer.togglePlay(focusText);
      showToast('Голосовой наставник Сократ: аудио-сопровождение спринта', 'info');
    } else {"""

r8 = """  // Dashboard Audio Companion button
  if(e.target.closest('#dashAudioCompanionBtn, .topbar-audio-btn')){
    const audioBtn = e.target.closest('#dashAudioCompanionBtn, .topbar-audio-btn');
    if(window.theoryAudioPlayer){
      const focusCardTitle = document.querySelector('.cocoon-focus-title');
      const focusText = 'Голосовой наставник Сократ. Текущий спринт-фокус: ' + (focusCardTitle ? focusCardTitle.innerText.trim() : 'коллекции Python');
      window.theoryAudioPlayer.togglePlay(focusText);
      const isNowActive = Boolean(window.theoryAudioPlayer.isPlaying && !window.theoryAudioPlayer.isPaused);
      if(audioBtn){
        audioBtn.classList.toggle('is-audio-active', isNowActive);
        audioBtn.style.borderColor = isNowActive ? 'rgba(16,185,129,0.5)' : '';
        audioBtn.style.color = isNowActive ? '#34d399' : '';
      }
      showToast(isNowActive ? 'Голосовой наставник Сократ: аудио-сопровождение спринта' : 'Голосовой наставник Сократ: пауза', 'info');
    } else {"""
assert t8 in content, 'Target 8 not found'
content = content.replace(t8, r8, 1)
print('8. [PASS] Audio companion button interactive state applied')

# 9. Mobile bottom clearance for dashboard container
t9 = """.dashboard-container {
      padding-bottom: calc(84px + env(safe-area-inset-bottom, 24px)) !important;
    }"""
r9 = """.dashboard-container {
      padding-bottom: calc(108px + env(safe-area-inset-bottom, 24px)) !important;
    }"""
assert t9 in content, 'Target 9 not found'
content = content.replace(t9, r9, 1)
print('9. [PASS] Mobile dashboard container bottom clearance increased to 108px')

with open(academy_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated academy.html successfully. New length:', len(content))
