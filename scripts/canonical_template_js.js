/* ================= KHAN MASTERY: PYTHON, WEB, BACKEND, ALGORITHMS, DATABASES, ARCHITECTURE & INFRASTRUCTURE + 401 IDE TASKS ================= */
const PY_MASTERY = __PY_MASTERY_JSON__;
const WEB_MASTERY = __WEB_MASTERY_JSON__;
const BACKEND_MASTERY = __BACKEND_MASTERY_JSON__;
const ALGO_MASTERY = __ALGO_MASTERY_JSON__;
const DB_MASTERY = __DB_MASTERY_JSON__;
const ARCH_MASTERY = __ARCH_MASTERY_JSON__;
const INFRA_MASTERY = __INFRA_MASTERY_JSON__;
const IDE_TASKS = __IDE_TASKS_JSON__;
const IDE_TASKS_BY_ID = Object.fromEntries(IDE_TASKS.map(t => [t.id, t]));
const EXTRA_LESSONS = __NEW_LESSONS_JSON__;
Object.assign(LESSONS, EXTRA_LESSONS);
window.PY_MASTERY = PY_MASTERY;
window.WEB_MASTERY = WEB_MASTERY;
window.BACKEND_MASTERY = BACKEND_MASTERY;
window.ALGO_MASTERY = ALGO_MASTERY;
window.DB_MASTERY = DB_MASTERY;
window.ARCH_MASTERY = ARCH_MASTERY;
window.INFRA_MASTERY = INFRA_MASTERY;
window.IDE_TASKS = IDE_TASKS;
window.IDE_TASKS_BY_ID = IDE_TASKS_BY_ID;
window.LESSONS = LESSONS;

/* ================= THEORY AUDIO COMPANION (WEB SPEECH API) ================= */
window.theoryAudioPlayer = {
  isPlaying: false,
  isPaused: false,
  rate: 1.0,
  currentText: '',
  utterance: null,
  normalizePythonTerms: function(text) {
    if(!text) return '';
    let t = String(text);
    t = t.replace(/<[^>]*>/g, ' ');
    t = t.replace(/`([^`]+)`/g, '$1');
    t = t.replace(/\*\*([^*]+)\*\*/g, '$1');
    t = t.replace(/\*([^*]+)\*/g, '$1');
    const dict = [
      [/\bCPython\b/gi, 'Си-Пайтон'],
      [/\bPython\b/gi, 'Пайтон'],
      [/\basyncio\b/gi, 'асинк-и-о'],
      [/\basync\s+def\b/gi, 'асинк дэф'],
      [/\bdef\b/g, 'дэф'],
      [/\bGIL\b/g, 'Гил'],
      [/\b__init__\b/g, 'дандер инит'],
      [/\b__enter__\b/g, 'дандер энтер'],
      [/\b__exit__\b/g, 'дандер экзит'],
      [/\b__slots__\b/g, 'дандер слотс'],
      [/\b__dict__\b/g, 'дандер дикт'],
      [/\b__repr__\b/g, 'дандер репре'],
      [/\b__len__\b/g, 'дандер лен'],
      [/\bkwargs\b/gi, 'кварги'],
      [/\bargs\b/gi, 'арги'],
      [/\bO\(1\)/g, 'О от одного'],
      [/\bO\(n\)/g, 'О от эн'],
      [/\bO\(log\s*n\)/gi, 'О от лог эн'],
      [/\bO\(n\s*log\s*n\)/gi, 'О от эн лог эн'],
      [/\bdict\b/g, 'дикт'],
      [/\blist\b/g, 'лист'],
      [/\btuple\b/g, 'тюпл'],
      [/\bset\b/g, 'сет'],
      [/\bdeque\b/gi, 'дэк'],
      [/\bNone\b/g, 'Нан'],
      [/\bTrue\b/g, 'Тру'],
      [/\bFalse\b/g, 'Фолс'],
      [/\byield\b/g, 'йилд'],
      [/\bFastAPI\b/gi, 'Фаст-А-Пи-Ай'],
      [/\bPydantic\b/gi, 'Пайдантик'],
      [/\bDocker\b/gi, 'Докер'],
      [/\bPostgreSQL\b/gi, 'Постгрес'],
      [/\bRedis\b/gi, 'Редис'],
      [/\bpytest\b/gi, 'пайтест'],
      [/\bSQL\b/g, 'Эс-Кью-Эль'],
      [/\bAPI\b/g, 'А-Пи-Ай'],
      [/\bHTTP\b/gi, 'Эйч-Ти-Ти-Пи'],
      [/\bJSON\b/gi, 'Джейсон'],
      [/\bawait\b/g, 'эвейт'],
      [/\blambda\b/g, 'лямбда'],
      [/\bself\b/g, 'селф'],
      [/\bcls\b/g, 'класс'],
      [/\b__str__\b/g, 'дандер стр'],
      [/\b__getitem__\b/g, 'дандер гет-айтем'],
      [/\b__setitem__\b/g, 'дандер сет-айтем'],
      [/\b__call__\b/g, 'дандер колл'],
      [/\b__iter__\b/g, 'дандер итер'],
      [/\b__next__\b/g, 'дандер некст']
    ];
    for(const [pat, repl] of dict){
      t = t.replace(pat, repl);
    }
    return t.replace(/\s+/g, ' ').trim();
  },
  play: function(text) {
    if(typeof window === 'undefined' || !window.speechSynthesis) return;
    try{ window.speechSynthesis.cancel(); }catch(e){}
    const cleanText = this.normalizePythonTerms(text || this.currentText);
    if(!cleanText) return;
    this.currentText = cleanText;
    try {
      const utt = (typeof SpeechSynthesisUtterance !== 'undefined') ? new SpeechSynthesisUtterance(cleanText) : { text: cleanText };
      utt.lang = 'ru-RU';
      utt.rate = this.rate;
      utt.onend = () => { this.isPlaying = false; this.isPaused = false; this.updateUI(); };
      utt.onerror = () => { this.isPlaying = false; this.isPaused = false; this.updateUI(); };
      this.utterance = utt;
      window.speechSynthesis.speak(utt);
    }catch(e){}
    this.isPlaying = true;
    this.isPaused = false;
    this.updateUI();
  },
  pause: function() {
    if(typeof window === 'undefined' || !window.speechSynthesis) return;
    if(this.isPlaying && !this.isPaused){
      try{ window.speechSynthesis.pause(); }catch(e){}
      this.isPaused = true;
      this.updateUI();
    }
  },
  resume: function() {
    if(typeof window === 'undefined' || !window.speechSynthesis) return;
    if(this.isPlaying && this.isPaused){
      try{ window.speechSynthesis.resume(); }catch(e){}
      this.isPaused = false;
      this.updateUI();
    }
  },
  togglePlay: function(text) {
    if(this.isPlaying){
      if(this.isPaused) this.resume();
      else this.pause();
    } else {
      this.play(text);
    }
  },
  stop: function() {
    if(typeof window === 'undefined' || !window.speechSynthesis) return;
    try{ window.speechSynthesis.cancel(); }catch(e){}
    this.isPlaying = false;
    this.isPaused = false;
    this.updateUI();
  },
  rewind10: function() {
    if(this.currentText){ this.stop(); this.play(this.currentText); }
  },
  forward10: function() {
    if(this.currentText){ this.stop(); }
  },
  toggleRate: function() {
    const rates = [1.0, 1.25, 1.5];
    const curIdx = rates.indexOf(this.rate);
    this.rate = rates[(curIdx + 1) % rates.length];
    if(this.isPlaying && !this.isPaused){
      this.play(this.currentText);
    } else {
      this.updateUI();
    }
  },
  updateUI: function() {
    const bar = document.getElementById('theory-audio-bar');
    if(!bar) return;
    const playBtn = bar.querySelector('[data-audio-play]');
    const rateBtn = bar.querySelector('[data-audio-rate]');
    const statusText = bar.querySelector('.audio-status-text');
    if(playBtn) playBtn.innerHTML = (this.isPlaying && !this.isPaused) ? '⏸' : '▶';
    if(rateBtn) rateBtn.textContent = `${this.rate}x`;
    if(statusText) statusText.textContent = (this.isPlaying && !this.isPaused) ? 'Озвучивание…' : (this.isPaused ? 'Пауза' : 'Аудио-компаньон');
  }
};


// Add icons for new sections
ICONS.python = '<svg class="icon" viewBox="0 0 24 24"><path d="M12 2c-4 0-4 2-4 4v2h4v1H6c-2.5 0-4 1.8-4 4.5S3.5 18 6 18h2v-2.5c0-1.7 1.3-3 3-3h5c1.4 0 2.5-1.1 2.5-2.5V6c0-2-1.5-4-6.5-4z"/><path d="M12 22c4 0 4-2 4-4v-2h-4v-1h6c2.5 0 4-1.8 4-4.5S20.5 6 18 6h-2v2.5c0 1.7-1.3 3-3 3H8c-1.4 0-2.5 1.1-2.5 2.5V18c0 2 1.5 4 6.5 4z"/></svg>';
ICONS.globe = '<svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3.6 9h16.8M3.6 15h16.8M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/></svg>';
ICONS.server = '<svg class="icon" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 7h.01M7 17h.01M11 7h6M11 17h6"/></svg>';
ICONS.cards = '<svg class="icon" viewBox="0 0 24 24"><rect x="3" y="5" width="14" height="15" rx="2.5"/><path d="M7 5V3.5A1.5 1.5 0 0 1 8.5 2h10A2.5 2.5 0 0 1 21 4.5v11a1.5 1.5 0 0 1-1.5 1.5H17"/></svg>';
ICONS.code = '<svg class="icon" viewBox="0 0 24 24"><path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 6l-3 12"/></svg>';
ICONS.bolt = '<svg class="icon" viewBox="0 0 24 24"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/></svg>';
ICONS.database = '<svg class="icon" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/></svg>';
ICONS.arch = '<svg class="icon" viewBox="0 0 24 24"><path d="M3 21h18M4 18h16M6 18v-7M10 18v-7M14 18v-7M18 18v-7M12 3 2 8h20L12 3z"/></svg>';
ICONS.rocket = '<svg class="icon" viewBox="0 0 24 24"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>';
ICONS.crown = '<svg class="icon" viewBox="0 0 24 24"><path d="m3 7 4.5 4L12 5l4.5 6L21 7l-2 12H5L3 7z"/></svg>';

// Extend state fields for Mastery Learning, Anti-Procrastination & Bulletproof Persistence
const ACADEMY_SCHEMA_VERSION = 3;
const LEGACY_ACADEMY_KEYS = [
  STORE_KEY,
  'py_backend_academy_v1',
  'py-backend-academy-v2',
  'academy_state_backup_v1'
];
const IDE_STATUS_KEYS = [
  'practice-ide-status',
  'practice-ide-status-backup'
];
const IDE_DRAFTS_KEY = 'practice-ide-drafts';
const PRE_RESET_BACKUP_KEY = 'academy_state_pre_reset_backup';
const WIN_NAME_PREFIX = '__ACADEMY_SYNC_V1__:';

function parseVisitTimestamp(v){
  if(!v || typeof v !== 'string') return 0;
  const s = v.trim();
  const isoM = s.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if(isoM){
    const d = new Date(Number(isoM[1]), Number(isoM[2]) - 1, Number(isoM[3]));
    return isNaN(d.getTime()) ? 0 : d.getTime();
  }
  const t = Date.parse(s);
  return isNaN(t) ? 0 : t;
}

function normalizeLegacyDateToVisitStr(v){
  if(!v || typeof v !== 'string') return null;
  const s = v.trim();
  const isoM = s.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if(isoM){
    const d = new Date(Number(isoM[1]), Number(isoM[2]) - 1, Number(isoM[3]));
    if(!isNaN(d.getTime())) return d.toDateString();
  }
  const t = Date.parse(s);
  if(!isNaN(t)) return new Date(t).toDateString();
  return s;
}

function ensureExtendedState(target){
  const s = target || state;
  if(!s || typeof s !== 'object') return s;
  if(typeof s.schemaVersion !== 'number') s.schemaVersion = ACADEMY_SCHEMA_VERSION;
  if(typeof s.updatedAt !== 'number') s.updatedAt = Date.now();
  if(typeof s.streak !== 'number') s.streak = 0;
  if(typeof s.bestStreak !== 'number') s.bestStreak = s.streak || 0;
  if(s.lastVisit === undefined) s.lastVisit = null;
  // Migrate legacy lastActiveDate -> lastVisit
  if(!s.lastVisit && typeof s.lastActiveDate === 'string' && s.lastActiveDate.trim()){
    s.lastVisit = normalizeLegacyDateToVisitStr(s.lastActiveDate);
  } else if(typeof s.lastVisit === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(s.lastVisit.trim())){
    s.lastVisit = normalizeLegacyDateToVisitStr(s.lastVisit);
  }
  if(!Array.isArray(s.mastered)) s.mastered = [];
  if(!Array.isArray(s.completedLessons)) s.completedLessons = [];
  // Migrate legacy completedTasks (array or map) -> s.completedTasks & practice-ide-status
  if(Array.isArray(s.completedTasks)){
    s.completedTasks = s.completedTasks.map(x => Number(x) || x).filter(Boolean);
  } else if(s.completedTasks && typeof s.completedTasks === 'object'){
    s.completedTasks = Object.keys(s.completedTasks).filter(k => s.completedTasks[k]).map(k => Number(k) || k);
  } else {
    s.completedTasks = [];
  }
  if(s.completedTasks.length > 0){
    try{
      const curIdeRaw = localStorage.getItem('practice-ide-status');
      const curIde = (curIdeRaw && typeof curIdeRaw === 'string') ? JSON.parse(curIdeRaw) : {};
      let ideChanged = false;
      s.completedTasks.forEach(tid => {
        const tk = String(tid);
        if(tk && curIde[tk] !== 'mastered'){
          curIde[tk] = 'mastered';
          ideChanged = true;
        }
      });
      if(ideChanged){
        const ser = JSON.stringify(curIde);
        localStorage.setItem('practice-ide-status', ser);
        try{ localStorage.setItem('practice-ide-status-backup', ser); }catch(ignore){}
      }
    }catch(ignore){}
  }
  if(typeof s.xp !== 'number') s.xp = 0;
  if(!s.dailyGoal) s.dailyGoal = 50;
  if(!s.dailyXpByDate || typeof s.dailyXpByDate !== 'object') s.dailyXpByDate = {};
  // Migrate legacy activityLog & dailyXp -> dailyXpByDate
  if(s.activityLog && typeof s.activityLog === 'object' && !Array.isArray(s.activityLog)){
    Object.keys(s.activityLog).forEach(dt => {
      const val = Number(s.activityLog[dt]) || 0;
      if(val > 0) s.dailyXpByDate[dt] = Math.max(Number(s.dailyXpByDate[dt]) || 0, val);
    });
  }
  if(typeof s.dailyXp === 'number' && s.dailyXp > 0){
    let dk = null;
    if(typeof s.lastActiveDate === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(s.lastActiveDate.trim())){
      dk = s.lastActiveDate.trim();
    } else if(s.lastVisit){
      const ts = parseVisitTimestamp(s.lastVisit);
      if(ts > 0){
        const dt = new Date(ts);
        dk = dt.getFullYear() + '-' + String(dt.getMonth()+1).padStart(2,'0') + '-' + String(dt.getDate()).padStart(2,'0');
      }
    }
    if(dk) s.dailyXpByDate[dk] = Math.max(Number(s.dailyXpByDate[dk]) || 0, s.dailyXp);
  }
  if(typeof s.streakFreezes !== 'number') s.streakFreezes = 1;
  if(!s.skillMastery || typeof s.skillMastery !== 'object') s.skillMastery = {}; // sid -> 0 | 50 | 80 | 100
  if(!s.readNotes || !Array.isArray(s.readNotes)) s.readNotes = [];
  if(!s.reviewedDecks || !Array.isArray(s.reviewedDecks)) s.reviewedDecks = [];
  if(!s.passedUnitTests || !Array.isArray(s.passedUnitTests)) s.passedUnitTests = [];
  if(!s.passedBosses || !Array.isArray(s.passedBosses)) s.passedBosses = [];
  if(typeof s.mockCompletedCount !== 'number') s.mockCompletedCount = 0;
  if(!s.cardRatings || typeof s.cardRatings !== 'object') s.cardRatings = {};
  if(!s.cardSrs || typeof s.cardSrs !== 'object') s.cardSrs = {};
  // Migrate legacy cards map -> cardRatings & reviewedDecks
  if(s.cards && typeof s.cards === 'object' && !Array.isArray(s.cards)){
    const ratingMap = { again: 1, hard: 2, good: 3, easy: 4 };
    const toRatingNum = function(v){
      if(typeof v === 'number') return v;
      if(typeof v === 'string') return ratingMap[v.toLowerCase()] || Number(v) || 0;
      return 0;
    };
    Object.keys(s.cards).forEach(ck => {
      const rawV = s.cards[ck];
      const deckPrefix = String(ck).split(':')[0];
      if(rawV && typeof rawV === 'object' && !Array.isArray(rawV)){
        if(rawV.rating !== undefined){
          const rn = toRatingNum(rawV.rating);
          if(rn > 0) s.cardRatings[ck] = Math.max(Number(s.cardRatings[ck]) || 0, rn);
        }
        if(rawV.ratings && typeof rawV.ratings === 'object'){
          Object.keys(rawV.ratings).forEach(subIdx => {
            const rn = toRatingNum(rawV.ratings[subIdx]);
            const fullKey = String(ck).includes(':') ? ck : (deckPrefix + ':' + subIdx);
            if(rn > 0) s.cardRatings[fullKey] = Math.max(Number(s.cardRatings[fullKey]) || 0, rn);
          });
        }
        if((rawV.reviewed || rawV.done || rawV.completed || rawV.ratings) && /^Ф-\d+/.test(deckPrefix) && !s.reviewedDecks.includes(deckPrefix)){
          s.reviewedDecks.push(deckPrefix);
        }
      } else {
        const numV = toRatingNum(rawV);
        if(numV > 0) s.cardRatings[ck] = Math.max(Number(s.cardRatings[ck]) || 0, numV);
        if(/^Ф-\d+/.test(deckPrefix) && !s.reviewedDecks.includes(deckPrefix)){
          s.reviewedDecks.push(deckPrefix);
        }
      }
    });
  }
  if(!s.lessonDrafts || typeof s.lessonDrafts !== 'object') s.lessonDrafts = {};
  if(!s.readingPositions || typeof s.readingPositions !== 'object') s.readingPositions = {};
  if(!s.starDrafts || typeof s.starDrafts !== 'object') s.starDrafts = {};
  if(!s.unitTestDrafts || typeof s.unitTestDrafts !== 'object') s.unitTestDrafts = {};
  if(!s.diagDraft || typeof s.diagDraft !== 'object' || Array.isArray(s.diagDraft)) s.diagDraft = null;
  if(!s.cardsHubPos || typeof s.cardsHubPos !== 'object' || Array.isArray(s.cardsHubPos)) s.cardsHubPos = null;
  if(!s.practiceHubPos || typeof s.practiceHubPos !== 'object' || Array.isArray(s.practiceHubPos)) s.practiceHubPos = null;
  if(typeof s.sandboxDraft !== 'string') s.sandboxDraft = '';
  if(typeof s.lastRoute !== 'string') s.lastRoute = '/';
  if(!s.completedLessonSteps || typeof s.completedLessonSteps !== 'object') s.completedLessonSteps = {};
  if(!s.completedNoteSteps || typeof s.completedNoteSteps !== 'object') s.completedNoteSteps = {};
  if(!s.unlockedChunks || typeof s.unlockedChunks !== 'object') s.unlockedChunks = {};
  if(typeof s.soundEnabled !== 'boolean') s.soundEnabled = true;
  if(typeof s.utShowExplanations !== 'boolean') s.utShowExplanations = true; // тумблер «Показывать разбор после ответа»
  if(typeof s.utSkipStartModal !== 'boolean') s.utSkipStartModal = false; // «Всегда открывать тест без этой модалки»
  if(!s.stackBranch || !['fastapi','django','both'].includes(s.stackBranch)) s.stackBranch = 'fastapi';
  if(!s.unitSortMode || !['priority','number'].includes(s.unitSortMode)) s.unitSortMode = 'priority';
  if(!s.pathViewMode || !['game','pro'].includes(s.pathViewMode)) s.pathViewMode = 'game';
  if(!s.pathNodeStyle || !['paw','button'].includes(s.pathNodeStyle)) s.pathNodeStyle = 'button'; // выбор Ксении: по умолчанию «Кнопки» (ближе к Coddy)
  if(!s.diagnosticGaps || !Array.isArray(s.diagnosticGaps)) s.diagnosticGaps = [];
  if(typeof s.diagCompleted !== 'boolean') s.diagCompleted = false;
  if(typeof s.diagScore !== 'number') s.diagScore = 0;
  if(typeof s.diagTotal !== 'number') s.diagTotal = 0;
  // Migrate legacy diag object -> diagCompleted, diagScore, diagTotal, diagnosticGaps
  if(s.diag && typeof s.diag === 'object' && !Array.isArray(s.diag)){
    if(s.diag.completed) s.diagCompleted = true;
    if(typeof s.diag.score === 'number') s.diagScore = Math.max(s.diagScore || 0, s.diag.score);
    if(typeof s.diag.total === 'number') s.diagTotal = Math.max(s.diagTotal || 0, s.diag.total);
    if(Array.isArray(s.diag.gaps)){
      s.diag.gaps.forEach(g => {
        if(g && !s.diagnosticGaps.includes(g)) s.diagnosticGaps.push(g);
      });
    }
  }
  return s;
}

function uniqueArrayUnion(a, b){
  const out = [];
  const seen = new Set();
  (Array.isArray(a) ? a : []).concat(Array.isArray(b) ? b : []).forEach(item => {
    if(item !== null && item !== undefined && !seen.has(item)){
      seen.add(item);
      out.push(item);
    }
  });
  return out;
}

// Non-destructive monotonic union merge of two progress state objects:
// Never loses XP, streak, completed lessons, read notes, reviewed decks, unit tests, bosses, skill MP, or drafts!
function mergeProgressStates(baseRaw, incomingRaw){
  const a = ensureExtendedState(Object.assign({}, baseRaw || {}));
  const b = ensureExtendedState(Object.assign({}, incomingRaw || {}));
  const bNewer = (b.updatedAt || 0) >= (a.updatedAt || 0);
  const merged = Object.assign({}, a, b);

  merged.schemaVersion = Math.max(a.schemaVersion || 1, b.schemaVersion || 1, ACADEMY_SCHEMA_VERSION);
  merged.updatedAt = Math.max(a.updatedAt || 0, b.updatedAt || 0, Date.now());
  merged.xp = Math.max(a.xp || 0, b.xp || 0);
  merged.streak = Math.max(a.streak || 0, b.streak || 0);
  merged.bestStreak = Math.max(a.bestStreak || 0, b.bestStreak || 0, merged.streak);
  merged.streakFreezes = Math.max(a.streakFreezes || 0, b.streakFreezes || 0);
  merged.mockCompletedCount = Math.max(a.mockCompletedCount || 0, b.mockCompletedCount || 0);
  merged.diagCompleted = !!(a.diagCompleted || b.diagCompleted);
  merged.diagScore = Math.max(a.diagScore || 0, b.diagScore || 0);
  merged.diagTotal = Math.max(a.diagTotal || 0, b.diagTotal || 0);

  if(a.lastVisit && b.lastVisit){
    const tsA = parseVisitTimestamp(a.lastVisit);
    const tsB = parseVisitTimestamp(b.lastVisit);
    if(tsA > 0 && tsB > 0){
      merged.lastVisit = tsA >= tsB ? a.lastVisit : b.lastVisit;
    } else {
      merged.lastVisit = bNewer ? b.lastVisit : a.lastVisit;
    }
  } else {
    merged.lastVisit = b.lastVisit || a.lastVisit || null;
  }

  merged.mastered = uniqueArrayUnion(a.mastered, b.mastered);
  merged.completedLessons = uniqueArrayUnion(a.completedLessons, b.completedLessons);
  merged.completedTasks = uniqueArrayUnion(a.completedTasks, b.completedTasks);
  merged.readNotes = uniqueArrayUnion(a.readNotes, b.readNotes);
  merged.reviewedDecks = uniqueArrayUnion(a.reviewedDecks, b.reviewedDecks);
  merged.passedUnitTests = uniqueArrayUnion(a.passedUnitTests, b.passedUnitTests);
  merged.passedBosses = uniqueArrayUnion(a.passedBosses, b.passedBosses);
  merged.diagnosticGaps = uniqueArrayUnion(a.diagnosticGaps, b.diagnosticGaps);

  merged.skillMastery = {};
  Object.keys(a.skillMastery || {}).concat(Object.keys(b.skillMastery || {})).forEach(sid => {
    merged.skillMastery[sid] = Math.max(Number(a.skillMastery[sid]) || 0, Number(b.skillMastery[sid]) || 0);
  });

  merged.dailyXpByDate = {};
  Object.keys(a.dailyXpByDate || {}).concat(Object.keys(b.dailyXpByDate || {})).forEach(dt => {
    merged.dailyXpByDate[dt] = Math.max(Number(a.dailyXpByDate[dt]) || 0, Number(b.dailyXpByDate[dt]) || 0);
  });

  merged.cardRatings = Object.assign({}, a.cardRatings || {}, b.cardRatings || {});
  Object.keys(a.cardRatings || {}).forEach(ck => {
    if(b.cardRatings && b.cardRatings[ck] !== undefined){
      merged.cardRatings[ck] = Math.max(Number(a.cardRatings[ck]) || 0, Number(b.cardRatings[ck]) || 0);
    }
  });

  merged.lessonDrafts = Object.assign({}, a.lessonDrafts || {});
  Object.keys(b.lessonDrafts || {}).forEach(lid => {
    const da = merged.lessonDrafts[lid];
    const db = b.lessonDrafts[lid];
    if(!da || typeof da !== 'object'){
      merged.lessonDrafts[lid] = db;
    } else if(db && typeof db === 'object'){
      const pickB = (db.updatedAt || 0) >= (da.updatedAt || 0);
      merged.lessonDrafts[lid] = Object.assign({}, da, pickB ? db : da);
      ['practiceCode','taskCode','practice2Code','task2Code','debugCode'].forEach(ck => {
        if(db[ck] && (!da[ck] || pickB)) merged.lessonDrafts[lid][ck] = db[ck];
        else if(da[ck]) merged.lessonDrafts[lid][ck] = da[ck];
      });
    }
  });

  merged.readingPositions = Object.assign({}, a.readingPositions || {});
  Object.keys(b.readingPositions || {}).forEach(sid => {
    const ra = merged.readingPositions[sid];
    const rb = b.readingPositions[sid];
    if(!ra || ((rb && rb.updatedAt || 0) >= (ra.updatedAt || 0))){
      merged.readingPositions[sid] = rb;
    }
  });

  merged.unitTestDrafts = Object.assign({}, a.unitTestDrafts || {});
  Object.keys(b.unitTestDrafts || {}).forEach(uk => {
    const ua = merged.unitTestDrafts[uk];
    const ub = b.unitTestDrafts[uk];
    if(!ua || ((ub && ub.updatedAt || 0) >= (ua.updatedAt || 0))){
      merged.unitTestDrafts[uk] = ub;
    }
  });

  if(a.diagDraft && b.diagDraft){
    merged.diagDraft = ((b.diagDraft.updatedAt || 0) >= (a.diagDraft.updatedAt || 0)) ? b.diagDraft : a.diagDraft;
  } else {
    merged.diagDraft = b.diagDraft || a.diagDraft || null;
  }

  if(a.cardsHubPos && b.cardsHubPos){
    merged.cardsHubPos = ((b.cardsHubPos.updatedAt || 0) >= (a.cardsHubPos.updatedAt || 0)) ? b.cardsHubPos : a.cardsHubPos;
  } else {
    merged.cardsHubPos = b.cardsHubPos || a.cardsHubPos || null;
  }

  if(a.practiceHubPos && b.practiceHubPos){
    merged.practiceHubPos = ((b.practiceHubPos.updatedAt || 0) >= (a.practiceHubPos.updatedAt || 0)) ? b.practiceHubPos : a.practiceHubPos;
  } else {
    merged.practiceHubPos = b.practiceHubPos || a.practiceHubPos || null;
  }

  merged.sandboxDraft = (bNewer && b.sandboxDraft) ? b.sandboxDraft : (a.sandboxDraft || b.sandboxDraft || '');
  merged.lastRoute = (bNewer && b.lastRoute && b.lastRoute !== '/') ? b.lastRoute : (a.lastRoute && a.lastRoute !== '/' ? a.lastRoute : (b.lastRoute || '/'));
  merged.starDrafts = Object.assign({}, a.starDrafts || {}, b.starDrafts || {});
  merged.theme = bNewer ? (b.theme || a.theme) : (a.theme || b.theme);
  merged.stackBranch = bNewer ? (b.stackBranch || a.stackBranch) : (a.stackBranch || b.stackBranch);
  merged.unitSortMode = bNewer ? (b.unitSortMode || a.unitSortMode) : (a.unitSortMode || b.unitSortMode);
  // Предпочтения рубежных тестов: явное булево сильнее дефолта, более свежий источник сильнее старого
  const pickUtPref = (x, y, dflt) => (typeof x === 'boolean' ? x : (typeof y === 'boolean' ? y : dflt));
  merged.utShowExplanations = bNewer ? pickUtPref(b.utShowExplanations, a.utShowExplanations, true) : pickUtPref(a.utShowExplanations, b.utShowExplanations, true);
  merged.utSkipStartModal = bNewer ? pickUtPref(b.utSkipStartModal, a.utSkipStartModal, false) : pickUtPref(a.utSkipStartModal, b.utSkipStartModal, false);
  return ensureExtendedState(merged);
}
window.mergeProgressStates = mergeProgressStates;

function mergeIdeStatusMaps(baseMap, incMap){
  const out = {};
  Object.keys(baseMap || {}).forEach(k => {
    const v = baseMap[k];
    out[k] = (v === 'mastered' || v === 'solved') ? 'mastered' : v;
  });
  Object.keys(incMap || {}).forEach(k => {
    const v = incMap[k];
    if(out[k] === 'mastered' || out[k] === 'solved' || v === 'mastered' || v === 'solved'){
      out[k] = 'mastered';
    } else if(v && !out[k]){
      out[k] = v;
    }
  });
  return out;
}
window.mergeIdeStatusMaps = mergeIdeStatusMaps;

function mergeIdeDraftMaps(baseDrafts, incDrafts){
  const out = Object.assign({}, baseDrafts || {});
  Object.keys(incDrafts || {}).forEach(k => {
    const v = incDrafts[k];
    if(typeof v === 'string' && v.trim().length > 0){
      out[k] = v;
    }
  });
  return out;
}
window.mergeIdeDraftMaps = mergeIdeDraftMaps;

function safeParseJsonObj(raw){
  if(!raw || typeof raw !== 'string') return null;
  try{
    const p = JSON.parse(raw);
    return (p && typeof p === 'object' && !Array.isArray(p)) ? p : null;
  }catch(e){ return null; }
}

function readWindowNameBackup(){
  try{
    const wn = String(window.name || '');
    if(wn.indexOf(WIN_NAME_PREFIX) === 0){
      return safeParseJsonObj(wn.slice(WIN_NAME_PREFIX.length));
    }
  }catch(e){}
  return null;
}

function writeWindowNameBackup(academySt, ideStatusMap, ideDraftsMap){
  try{
    const prevWn = readWindowNameBackup() || {};
    const curDrafts = ideDraftsMap || safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || prevWn.ideDrafts || {};
    const payload = {
      academyState: academySt || prevWn.academyState || state,
      ideStatus: ideStatusMap || getIdeSolvedMap(),
      ideDrafts: curDrafts
    };
    window.name = WIN_NAME_PREFIX + JSON.stringify(payload);
  }catch(e){}
}

function syncToIndexedDBAsync(academySt, ideStatusMap, ideDraftsMap){
  try{
    if(typeof indexedDB === 'undefined' || !indexedDB || typeof indexedDB.open !== 'function') return;
    const curDrafts = ideDraftsMap || safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {};
    const req = indexedDB.open('AcademyProgressDB', 1);
    req.onupgradeneeded = function(ev){
      try{
        const db = ev.target.result;
        if(!db.objectStoreNames.contains('snapshots')){
          db.createObjectStore('snapshots');
        }
      }catch(err){}
    };
    req.onsuccess = function(ev){
      try{
        const db = ev.target.result;
        const tx = db.transaction('snapshots', 'readwrite');
        const store = tx.objectStore('snapshots');
        store.put({
          academyState: academySt,
          ideStatus: ideStatusMap || getIdeSolvedMap(),
          ideDrafts: curDrafts,
          savedAt: Date.now()
        }, 'latest');
      }catch(err){}
    };
  }catch(e){}
}

function restoreFromIndexedDBIfNeeded(){
  try{
    if(typeof indexedDB === 'undefined' || !indexedDB || typeof indexedDB.open !== 'function') return;
    const req = indexedDB.open('AcademyProgressDB', 1);
    req.onupgradeneeded = function(ev){
      try{
        const db = ev.target.result;
        if(!db.objectStoreNames.contains('snapshots')){
          db.createObjectStore('snapshots');
        }
      }catch(err){}
    };
    req.onsuccess = function(ev){
      try{
        const db = ev.target.result;
        if(!db.objectStoreNames.contains('snapshots')) return;
        const tx = db.transaction('snapshots', 'readonly');
        const getReq = tx.objectStore('snapshots').get('latest');
        getReq.onsuccess = function(){
          try{
            const snap = getReq.result;
            if(!snap || typeof snap !== 'object') return;
            let changed = false;
            if(snap.academyState && typeof snap.academyState === 'object'){
              const prevXp = state.xp || 0;
              const prevLessons = (state.completedLessons || []).length;
              const prevNotes = (state.readNotes || []).length;
              state = mergeProgressStates(state, snap.academyState);
              if((state.xp || 0) > prevXp || (state.completedLessons || []).length > prevLessons || (state.readNotes || []).length > prevNotes){
                changed = true;
              }
            }
            if(snap.ideStatus && typeof snap.ideStatus === 'object'){
              const curIde = getIdeSolvedMap();
              const mergedIde = mergeIdeStatusMaps(curIde, snap.ideStatus);
              if(Object.keys(mergedIde).length > Object.keys(curIde).length){
                const ideSer = JSON.stringify(mergedIde);
                try{ localStorage.setItem('practice-ide-status', ideSer); }catch(err){}
                try{ localStorage.setItem('practice-ide-status-backup', ideSer); }catch(err){}
                changed = true;
              }
            }
            if(snap.ideDrafts && typeof snap.ideDrafts === 'object'){
              const curDr = safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {};
              const mergedDr = mergeIdeDraftMaps(curDr, snap.ideDrafts);
              if(Object.keys(mergedDr).length > Object.keys(curDr).length){
                try{ localStorage.setItem(IDE_DRAFTS_KEY, JSON.stringify(mergedDr)); }catch(err){}
                changed = true;
              }
            }
            if(changed){
              saveState(state);
              if(typeof render === 'function') render();
            }
          }catch(err){}
        };
      }catch(err){}
    };
  }catch(e){}
}

// Hydrate & merge across all legacy/current localStorage keys and window.name so updates never lose data
function hydrateAndMergeAllProgressSources(){
  ensureExtendedState();
  let combined = ensureExtendedState(Object.assign({}, state));
  LEGACY_ACADEMY_KEYS.forEach(k => {
    try{
      const parsed = safeParseJsonObj(localStorage.getItem(k));
      if(parsed){
        const candidate = (parsed.academyState && typeof parsed.academyState === 'object') ? parsed.academyState : parsed;
        combined = mergeProgressStates(combined, candidate);
      }
    }catch(e){}
  });
  const wnSnap = readWindowNameBackup();
  if(wnSnap && wnSnap.academyState){
    combined = mergeProgressStates(combined, wnSnap.academyState);
  }
  state = Object.assign(state, combined);
  ensureExtendedState();

  // Also merge IDE status keys + window.name ideStatus + legacy state.completedTasks
  let combinedIde = {};
  IDE_STATUS_KEYS.forEach(k => {
    try{
      const parsed = safeParseJsonObj(localStorage.getItem(k));
      if(parsed) combinedIde = mergeIdeStatusMaps(combinedIde, parsed);
    }catch(e){}
  });
  if(wnSnap && wnSnap.ideStatus){
    combinedIde = mergeIdeStatusMaps(combinedIde, wnSnap.ideStatus);
  }
  if(Array.isArray(state.completedTasks) && state.completedTasks.length > 0){
    const legacyTaskMap = {};
    state.completedTasks.forEach(tid => { if(tid !== null && tid !== undefined) legacyTaskMap[tid] = 'mastered'; });
    combinedIde = mergeIdeStatusMaps(combinedIde, legacyTaskMap);
  }
  if(Object.keys(combinedIde).length > 0){
    try{
      const ideJson = JSON.stringify(combinedIde);
      localStorage.setItem('practice-ide-status', ideJson);
      localStorage.setItem('practice-ide-status-backup', ideJson);
    }catch(e){}
  }

  // Also merge IDE drafts from window.name if present
  if(wnSnap && wnSnap.ideDrafts && typeof wnSnap.ideDrafts === 'object'){
    try{
      const curDr = safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {};
      const mergedDr = mergeIdeDraftMaps(curDr, wnSnap.ideDrafts);
      if(Object.keys(mergedDr).length > 0){
        localStorage.setItem(IDE_DRAFTS_KEY, JSON.stringify(mergedDr));
      }
    }catch(e){}
  }
}

function evictOlderIdeDrafts(){
  try{
    const dr = safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {};
    const keys = Object.keys(dr);
    if(keys.length > 0){
      keys.slice(0, Math.max(1, Math.ceil(keys.length / 2))).forEach(k => { delete dr[k]; });
      localStorage.setItem(IDE_DRAFTS_KEY, JSON.stringify(dr));
    }
  }catch(e){}
}

// Resilient saveState with multi-key mirroring, non-destructive pre-read merge, window.name backup, IndexedDB snapshot, and safe draft eviction on QuotaExceededError
saveState = function(s){
  let target = ensureExtendedState(s || state);
  if(!window.__isResettingProgress){
    try{
      const existingRaw = safeParseJsonObj(localStorage.getItem(STORE_KEY));
      if(existingRaw && typeof existingRaw === 'object'){
        const hasHigherProgress = (existingRaw.xp || 0) > (target.xp || 0) ||
          ((existingRaw.completedLessons || []).length > (target.completedLessons || []).length) ||
          ((existingRaw.readNotes || []).length > (target.readNotes || []).length) ||
          ((existingRaw.reviewedDecks || []).length > (target.reviewedDecks || []).length);
        if(hasHigherProgress){
          target = mergeProgressStates(existingRaw, target);
          if(target !== state) Object.assign(state, target);
        }
      }
    }catch(ignore){}
  }
  target.schemaVersion = ACADEMY_SCHEMA_VERSION;
  target.updatedAt = Date.now();
  const serialized = JSON.stringify(target);
  try{
    localStorage.setItem(STORE_KEY, serialized);
    try{ localStorage.setItem('py_backend_academy_v1', serialized); }catch(ignore){}
    try{ localStorage.setItem('py-backend-academy-v2', serialized); }catch(ignore){}
    try{ localStorage.setItem('academy_state_backup_v1', serialized); }catch(ignore){}
  }catch(e){
    try{
      evictOlderIdeDrafts();
      localStorage.setItem(STORE_KEY, JSON.stringify(target));
      try{ localStorage.setItem('academy_state_backup_v1', JSON.stringify(target)); }catch(ignore){}
    }catch(e2){}
  }
  writeWindowNameBackup(target);
  syncToIndexedDBAsync(target);
};

// Upgrade bumpStreak so it runs AFTER multi-source hydration, consumes streakFreezes on missed days, and never resets a student's streak on update
bumpStreak = function(){
  ensureExtendedState();
  const today = todayStr();
  const todayTs = parseVisitTimestamp(today);
  const prevTs = parseVisitTimestamp(state.lastVisit);
  if(state.lastVisit === today || (prevTs > 0 && Math.round((todayTs - prevTs) / 86400000) === 0)){
    if((state.streak || 0) < 1) state.streak = 1;
    state.bestStreak = Math.max(state.bestStreak || 0, state.streak);
    state.lastVisit = today;
    saveState(state);
    return;
  }
  if(prevTs > 0){
    const diffDays = Math.round((todayTs - prevTs) / 86400000);
    if(diffDays === 1){
      state.streak = Math.max(1, (state.streak || 0) + 1);
    } else if(diffDays > 1){
      const missedDays = diffDays - 1;
      if((state.streakFreezes || 0) >= missedDays){
        state.streakFreezes -= missedDays;
        state.streak = Math.max(1, (state.streak || 0) + 1);
      } else {
        if((state.streakFreezes || 0) > 0) state.streakFreezes = 0;
        state.streak = Math.max(1, state.streak || 1);
      }
    } else {
      state.streak = Math.max(1, state.streak || 1);
    }
  } else {
    state.streak = Math.max(1, state.streak || 1);
  }
  state.bestStreak = Math.max(state.bestStreak || 0, state.streak || 1);
  state.lastVisit = today;
  saveState(state);
};

// Sync with standalone IDE trainer localStorage ('practice-ide-status' and 'practice-ide-drafts')
function getIdeSolvedMap(){
  try{
    let merged = {};
    IDE_STATUS_KEYS.forEach(k => {
      const parsed = safeParseJsonObj(localStorage.getItem(k));
      if(parsed) merged = mergeIdeStatusMaps(merged, parsed);
    });
    const wn = readWindowNameBackup();
    if(wn && wn.ideStatus) merged = mergeIdeStatusMaps(merged, wn.ideStatus);
    if(state && Array.isArray(state.completedTasks)){
      state.completedTasks.forEach(tid => { if(tid !== null && tid !== undefined) merged[tid] = 'mastered'; });
    }
    const out = {};
    Object.keys(merged).forEach(k => {
      out[k] = (merged[k] === 'mastered' || merged[k] === 'solved') ? 'solved' : merged[k];
    });
    return out;
  }catch(e){ return {}; }
}
function countSolvedIdeTasks(solvedMap){
  const sm = solvedMap || getIdeSolvedMap();
  return IDE_TASKS.filter(t => sm[t.id] === 'solved').length;
}
function saveIdeDraft(taskId, codeStr){
  if(taskId === undefined || taskId === null || typeof codeStr !== 'string') return;
  let dr = {};
  try{
    dr = safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {};
    dr[taskId] = codeStr;
    localStorage.setItem(IDE_DRAFTS_KEY, JSON.stringify(dr));
  }catch(e){
    try{
      dr = safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {};
      const keys = Object.keys(dr);
      if(keys.length > 10){
        keys.slice(0, Math.max(1, Math.floor(keys.length / 2))).forEach(k => { delete dr[k]; });
      } else {
        keys.forEach(k => { delete dr[k]; });
      }
      dr[taskId] = codeStr;
      localStorage.setItem(IDE_DRAFTS_KEY, JSON.stringify(dr));
    }catch(e2){
      try{
        dr = {};
        dr[taskId] = codeStr;
        localStorage.setItem(IDE_DRAFTS_KEY, JSON.stringify(dr));
      }catch(e3){}
    }
  }
  writeWindowNameBackup(state, null, dr);
}
function setIdeTaskSolved(taskId, codeStr){
  if(IDE_TASKS_BY_ID[taskId] || String(taskId).indexOf('boss-') === 0){
    try{
      let st = {};
      IDE_STATUS_KEYS.forEach(k => {
        const parsed = safeParseJsonObj(localStorage.getItem(k));
        if(parsed) st = mergeIdeStatusMaps(st, parsed);
      });
      st[taskId] = 'mastered';
      const ser = JSON.stringify(st);
      localStorage.setItem('practice-ide-status', ser);
      try{ localStorage.setItem('practice-ide-status-backup', ser); }catch(ignore){}
      writeWindowNameBackup(state, st);
      syncToIndexedDBAsync(state, st);
    }catch(e){
      try{
        evictOlderIdeDrafts();
        const raw = localStorage.getItem('practice-ide-status');
        const st = safeParseJsonObj(raw) || {};
        st[taskId] = 'mastered';
        const ser = JSON.stringify(st);
        localStorage.setItem('practice-ide-status', ser);
        try{ localStorage.setItem('practice-ide-status-backup', ser); }catch(ignore){}
      }catch(e2){}
    }
  }
  if(codeStr){
    saveIdeDraft(taskId, codeStr);
  }
}
function getIdeDraft(taskId, fallback){
  try{
    const dr = safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {};
    let draft = (dr[taskId] !== undefined) ? dr[taskId] : undefined;
    if(draft === undefined){
      const wn = readWindowNameBackup();
      if(wn && wn.ideDrafts && wn.ideDrafts[taskId] !== undefined) draft = wn.ideDrafts[taskId];
    }
    if(typeof draft === 'string'){
      const isLegacyStub = draft.includes('# TODO') || draft.includes('# Заполните значения целевых переменных') || draft.includes('# Задача #');
      const nonCommentLines = draft.split('\n').filter(l => l.trim() && !l.trim().startsWith('#'));
      const isOnlyStubValues = nonCommentLines.length === 0 || nonCommentLines.every(l => l.includes('= None') || l.trim() === 'pass' || l.startsWith('import ') || l.startsWith('from '));
      if(isLegacyStub && isOnlyStubValues){
        return fallback;
      }
      let cleaned = draft
        .replace(/^#\s*Задача\s*#\d+:.*$/gm, '')
        .replace(/^#\s*Заполните значения.*$/gm, '')
        .replace(/^#\s*Напишите ваше решение.*$/gm, '')
        .replace(/^#\s*TODO:.*$/gm, '')
        .replace(/\s*#\s*TODO\b/g, '');
      cleaned = cleaned.replace(/^\n+/, '');
      return cleaned;
    }
    return fallback;
  }catch(e){ return fallback; }
}

// Cross-tab live synchronization via storage event
window.addEventListener('storage', function(e){
  if(!e || !e.key) return;
  const rawVal = (typeof e.newValue === 'string') ? e.newValue : localStorage.getItem(e.key);
  if(!rawVal) return;
  try{
    if(LEGACY_ACADEMY_KEYS.includes(e.key)){
      const inc = safeParseJsonObj(rawVal);
      if(inc){
        const candidate = (inc.academyState && typeof inc.academyState === 'object') ? inc.academyState : inc;
        state = mergeProgressStates(state, candidate);
        writeWindowNameBackup(state);
        const activeTag = (document.activeElement && document.activeElement.tagName) ? document.activeElement.tagName.toLowerCase() : '';
        if(activeTag !== 'textarea' && activeTag !== 'input' && typeof render === 'function') render();
      }
    } else if(IDE_STATUS_KEYS.includes(e.key)){
      const incIde = safeParseJsonObj(rawVal);
      if(incIde){
        const mergedIde = mergeIdeStatusMaps(getIdeSolvedMap(), incIde);
        writeWindowNameBackup(state, mergedIde);
        const activeTag = (document.activeElement && document.activeElement.tagName) ? document.activeElement.tagName.toLowerCase() : '';
        if(activeTag !== 'textarea' && activeTag !== 'input' && typeof render === 'function') render();
      }
    } else if(e.key === IDE_DRAFTS_KEY){
      const incDr = safeParseJsonObj(rawVal);
      if(incDr) writeWindowNameBackup(state, null, incDr);
    }
  }catch(err){}
});

hydrateAndMergeAllProgressSources();
bumpStreak();
restoreFromIndexedDBIfNeeded();
saveState(state);

const PROGRESS_SYNC_ENDPOINT = window.ACADEMY_SYNC_ENDPOINT || '/api/sync';
const PROGRESS_SYNC_TOKEN_KEY = 'academy_sync_access_code';
const PROGRESS_SYNC_DEVICE_KEY = 'academy_sync_device_id';
const PROGRESS_SYNC_REVISION_KEY = 'academy_sync_server_revision';
const PROGRESS_SYNC_INTERVAL_MS = 20000;
let progressSyncTimer = null;
let progressSyncInFlight = false;
let progressSyncDirty = false;
let progressSyncLastSignature = '';
let progressSyncPromptOpen = false;
let progressSyncAuthPrompted = false;

function progressSyncClientId(){
  try{
    let id = localStorage.getItem(PROGRESS_SYNC_DEVICE_KEY);
    if(!id){ id = 'device-' + (window.crypto && crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).slice(2) + Date.now().toString(36)); localStorage.setItem(PROGRESS_SYNC_DEVICE_KEY, id); }
    return id;
  }catch(e){ return 'device-' + Math.random().toString(36).slice(2); }
}
function progressSyncBundle(){
  return {
    academyState: state,
    ideStatus: (typeof getIdeSolvedMap === 'function') ? getIdeSolvedMap() : {},
    ideDrafts: safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {}
  };
}
function progressSyncMergeBundle(bundle){
  if(!bundle || typeof bundle !== 'object') return false;
  let changed = false;
  if(bundle.academyState && typeof bundle.academyState === 'object'){
    const before = JSON.stringify(state);
    state = mergeProgressStates(state, bundle.academyState);
    changed = changed || before !== JSON.stringify(state);
  }
  if(bundle.ideStatus && typeof bundle.ideStatus === 'object'){
    const current = getIdeSolvedMap();
    const merged = mergeIdeStatusMaps(current, bundle.ideStatus);
    if(JSON.stringify(current) !== JSON.stringify(merged)) changed = true;
    try{ localStorage.setItem('practice-ide-status', JSON.stringify(merged)); localStorage.setItem('practice-ide-status-backup', JSON.stringify(merged)); }catch(e){}
  }
  if(bundle.ideDrafts && typeof bundle.ideDrafts === 'object'){
    const current = safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {};
    const merged = mergeIdeDraftMaps(current, bundle.ideDrafts);
    if(JSON.stringify(current) !== JSON.stringify(merged)) changed = true;
    try{ localStorage.setItem(IDE_DRAFTS_KEY, JSON.stringify(merged)); }catch(e){}
  }
  if(changed){ saveState(state); writeWindowNameBackup(state); }
  return changed;
}
function progressSyncSaveRevision(revision){
  try{ localStorage.setItem(PROGRESS_SYNC_REVISION_KEY, String(Number(revision) || 0)); }catch(e){}
}
async function progressSyncRequest(method, payload){
  const token = localStorage.getItem(PROGRESS_SYNC_TOKEN_KEY) || '';
  const response = await fetch(PROGRESS_SYNC_ENDPOINT, {
    method,
    headers: Object.assign(method === 'POST' ? {'Content-Type':'application/json'} : {}, token ? {Authorization:'Bearer ' + token} : {}),
    cache: 'no-store',
    body: method === 'POST' ? JSON.stringify(payload) : undefined
  });
  const data = await response.json();
  if(!response.ok && response.status !== 409){ const error = new Error(data.error || ('HTTP ' + response.status)); error.status = response.status; throw error; }
  return {data, status: response.status};
}
async function runProgressSync(){
  if(progressSyncInFlight || location.protocol === 'file:') return;
  progressSyncInFlight = true;
  progressSyncDirty = false;
  try{
    const remote = await progressSyncRequest('GET');
    const revision = Number(remote.data.updatedAt) || 0;
    const knownRevision = Number(localStorage.getItem(PROGRESS_SYNC_REVISION_KEY)) || 0;
    if(remote.data.bundle && revision > knownRevision){
      if(progressSyncMergeBundle(remote.data.bundle) && typeof render === 'function') render();
      progressSyncSaveRevision(revision);
    }
    const bundle = progressSyncBundle();
    const signature = JSON.stringify(bundle);
    if(signature !== progressSyncLastSignature || progressSyncDirty || !revision){
      const pushed = await progressSyncRequest('POST', {
        bundle,
        baseUpdatedAt: Number(localStorage.getItem(PROGRESS_SYNC_REVISION_KEY)) || revision,
        clientId: progressSyncClientId(),
        device: /Android|iPhone|iPad|iPod/i.test(navigator.userAgent) ? 'mobile' : 'desktop'
      });
      if(pushed.status === 409){
        if(progressSyncMergeBundle(pushed.data.bundle) && typeof render === 'function') render();
        progressSyncSaveRevision(pushed.data.updatedAt);
        progressSyncDirty = true;
      }else{
        progressSyncSaveRevision(pushed.data.updatedAt);
        if(pushed.data.bundle && progressSyncMergeBundle(pushed.data.bundle) && typeof render === 'function'){
          if(location.hash && location.hash.includes('tab=theory')){
            restoreSnippetOutputs();
          } else {
            render();
          }
        }
        progressSyncLastSignature = JSON.stringify(progressSyncBundle());
      }
    }
  }catch(e){
    if(e && e.status === 401 && !progressSyncPromptOpen && !progressSyncAuthPrompted){
      progressSyncPromptOpen = true;
      progressSyncAuthPrompted = true;
      try{
        const code = window.prompt('Введите код синхронизации с Render (одинаковый на ПК и телефоне):');
        if(code && code.trim()){ localStorage.setItem(PROGRESS_SYNC_TOKEN_KEY, code.trim()); progressSyncDirty = true; }
      }catch(ignore){}
      finally{ progressSyncPromptOpen = false; }
    }
    // Network may be unavailable while the local multi-layer backup remains active.
  }finally{
    progressSyncInFlight = false;
    if(progressSyncDirty) setTimeout(runProgressSync, 250);
  }
}
function scheduleProgressSync(){
  progressSyncDirty = true;
  if(progressSyncTimer) clearTimeout(progressSyncTimer);
  progressSyncTimer = setTimeout(runProgressSync, 800);
}
const localSaveState = saveState;
saveState = function(s){ localSaveState(s); scheduleProgressSync(); };
const localSaveIdeDraft = saveIdeDraft;
saveIdeDraft = function(taskId, codeStr){ localSaveIdeDraft(taskId, codeStr); scheduleProgressSync(); };
const localSetIdeTaskSolved = setIdeTaskSolved;
setIdeTaskSolved = function(taskId, codeStr){ localSetIdeTaskSolved(taskId, codeStr); scheduleProgressSync(); };
window.addEventListener('storage', function(e){
  if(e && (e.key === 'practice-ide-status' || e.key === 'practice-ide-status-backup' || e.key === IDE_DRAFTS_KEY)) scheduleProgressSync();
});
window.addEventListener('focus', runProgressSync);
window.addEventListener('online', runProgressSync);
document.addEventListener('visibilitychange', function(){ if(document.visibilityState === 'visible') runProgressSync(); });
window.addEventListener('pagehide', function(){
  if(location.protocol === 'file:') return;
  try{
    const body = JSON.stringify({bundle: progressSyncBundle(), baseUpdatedAt: Number(localStorage.getItem(PROGRESS_SYNC_REVISION_KEY)) || 0, clientId: progressSyncClientId(), device: 'pagehide'});
    const token = localStorage.getItem(PROGRESS_SYNC_TOKEN_KEY) || '';
    fetch(PROGRESS_SYNC_ENDPOINT, {method:'POST', headers:Object.assign({'Content-Type':'application/json'}, token ? {Authorization:'Bearer ' + token} : {}), body, keepalive:true}).catch(function(){});
  }catch(e){}
});
progressSyncTimer = setInterval(runProgressSync, PROGRESS_SYNC_INTERVAL_MS);
setTimeout(runProgressSync, 1200);


// Russian pluralization helper (1 день / 2 дня / 5 дней)
function pluralizeRu(n, one, two, five){
  const abs = Math.abs(Number(n) || 0) % 100;
  const n1 = abs % 10;
  if(abs > 10 && abs < 20) return five;
  if(n1 > 1 && n1 < 5) return two;
  if(n1 === 1) return one;
  return five;
}
window.pluralizeRu = pluralizeRu;
window.pluralize = pluralizeRu;

// Web Audio API Synthesizer (SoundFx: zero external audio files)
const SoundFx = {
  _ctx: null,
  _getCtx: function(){
    if(!state || !state.soundEnabled) return null;
    try{
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if(!Ctx) return null;
      if(!this._ctx) this._ctx = new Ctx();
      if(this._ctx.state === 'suspended' && typeof this._ctx.resume === 'function') this._ctx.resume();
      return this._ctx;
    }catch(e){ return null; }
  },
  playXp: function(){
    try{
      const ctx = this._getCtx();
      if(!ctx) return;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.connect(gain); gain.connect(ctx.destination);
      const now = ctx.currentTime;
      osc.frequency.setValueAtTime(523.25, now);
      osc.frequency.exponentialRampToValueAtTime(659.25, now + 0.09);
      gain.gain.setValueAtTime(0.06, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);
      osc.start(now); osc.stop(now + 0.14);
    }catch(e){}
  },
  playSuccess: function(){
    try{
      const ctx = this._getCtx();
      if(!ctx) return;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.connect(gain); gain.connect(ctx.destination);
      const now = ctx.currentTime;
      osc.frequency.setValueAtTime(523.25, now);
      osc.frequency.setValueAtTime(659.25, now + 0.08);
      osc.frequency.setValueAtTime(783.99, now + 0.16);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.34);
      osc.start(now); osc.stop(now + 0.34);
    }catch(e){}
  },
  playFlip: function(){
    try{
      const ctx = this._getCtx();
      if(!ctx) return;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.connect(gain); gain.connect(ctx.destination);
      const now = ctx.currentTime;
      osc.frequency.setValueAtTime(320, now);
      osc.frequency.exponentialRampToValueAtTime(480, now + 0.045);
      gain.gain.setValueAtTime(0.04, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.055);
      osc.start(now); osc.stop(now + 0.055);
    }catch(e){}
  },
  playTick: function(){
    try{
      const ctx = this._getCtx();
      if(!ctx) return;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.connect(gain); gain.connect(ctx.destination);
      const now = ctx.currentTime;
      osc.frequency.setValueAtTime(880, now);
      gain.gain.setValueAtTime(0.03, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.035);
      osc.start(now); osc.stop(now + 0.035);
    }catch(e){}
  }
};
window.SoundFx = SoundFx;

function playSound(kind){
  if(!state || !state.soundEnabled) return;
  if(kind === 'xp') SoundFx.playXp();
  else if(kind === 'mastery' || kind === 'success') SoundFx.playSuccess();
  else if(kind === 'flip') SoundFx.playFlip();
  else if(kind === 'tick') SoundFx.playTick();
}

function spawnXpParticle(amount, anchorEl){
  try{
    if(!document || !document.body) return;
    const prev = document.querySelectorAll('.xp-float-particle');
    if(prev && prev.length > 4){
      for(let i = 0; i < prev.length - 4; i++){
        if(prev[i] && prev[i].remove) prev[i].remove();
      }
    }
    const el = document.createElement('div');
    el.className = 'xp-float-particle';
    el.textContent = `+${amount} XP ⚡`;
    let x = Math.round((window.innerWidth || 800) / 2 - 40);
    let y = Math.round((window.innerHeight || 600) / 2);
    const target = anchorEl || document.activeElement;
    if(target && typeof target.getBoundingClientRect === 'function'){
      const r = target.getBoundingClientRect();
      if(r && (r.width > 0 || r.height > 0)){
        x = Math.max(16, Math.min((window.innerWidth || 800) - 110, Math.round(r.left + r.width / 2 - 36)));
        y = Math.max(24, Math.round(r.top - 8));
      }
    }
    el.style.left = x + 'px';
    el.style.top = y + 'px';
    document.body.appendChild(el);
    setTimeout(function(){ try{ el.remove(); }catch(e){} }, 950);
  }catch(e){}
}
window.spawnXpParticle = spawnXpParticle;

function dateIsoKey(d){
  const dt = d || new Date();
  return dt.getFullYear() + '-' + String(dt.getMonth()+1).padStart(2,'0') + '-' + String(dt.getDate()).padStart(2,'0');
}
function awardXp(amount, anchorEl){
  ensureExtendedState();
  state.xp += amount;
  const k = dateIsoKey();
  state.dailyXpByDate[k] = (state.dailyXpByDate[k] || 0) + amount;
  saveState(state);
  playSound('xp');
  spawnXpParticle(amount, anchorEl);
  try {
    const dayVal = (typeof todayXp === 'function') ? todayXp() : (state.dailyXpByDate[k] || 0);
    document.querySelectorAll('.sprint-xp-pill').forEach(function(el){
      el.innerHTML = `⚡ +${dayVal} XP<span class="sprint-xp-subtext"> за сутки</span>`;
      el.title = `Заработано за сутки: ${dayVal} XP`;
    });
  } catch(e){}
}
function todayXp(){
  ensureExtendedState();
  return state.dailyXpByDate[dateIsoKey()] || 0;
}

// Helper: Build Code Editor with synchronized Line-Numbers Gutter and Sticky Python Accessory Bar
function buildCodeEditorWithGutterHTML(editorId, codeStr, minHeightPx, customTokens){
  const raw = String(codeStr || '');
  const lineCount = Math.max(1, raw.split('\n').length);
  const nums = [];
  for(let i = 1; i <= lineCount; i++) nums.push(i);
  const mh = typeof minHeightPx === 'number'
    ? minHeightPx
    : (parseInt(String(minHeightPx || '').replace(/\D+/g, ''), 10) || 200);

  const tokens = [];
  if(Array.isArray(customTokens) && customTokens.length > 0){
    customTokens.forEach(ct => {
      if(ct && typeof ct === 'string') tokens.push({ label: ct, val: ct, isSpecial: true });
    });
  }
  const defaultTokens = [
    { label: 'Tab ⇥', val: '    ' },
    { label: ':', val: ':' },
    { label: '_', val: '_' },
    { label: '( )', val: '()' },
    { label: '[ ]', val: '[]' },
    { label: '{ }', val: '{}' },
    { label: 'def', val: 'def ' },
    { label: 'return', val: 'return ' },
    { label: 'self.', val: 'self.' },
    { label: 'in', val: 'in ' },
    { label: '==', val: ' == ' },
    { label: '->', val: ' -> ' }
  ];
  defaultTokens.forEach(dt => {
    if(!tokens.some(t => t.val === dt.val)){
      tokens.push(dt);
    }
  });

  const barBtns = tokens.map(t =>
    `<button type="button" class="py-key-btn py-acc-btn ${t.isSpecial ? 'py-acc-btn--special' : ''}" data-insert-token="${escapeHtmlStr(t.val)}" data-target-editor="${editorId}">${escapeHtmlStr(t.label)}</button>`
  ).join('');
  return `
    <div class="py-editor-shell" data-editor-shell="${editorId}">
      <div class="py-accessory-bar" role="toolbar" aria-label="Быстрый ввод символов Python">${barBtns}</div>
      <div class="editor-with-gutter code-editor-shell">
        <div class="line-numbers-gutter" id="${editorId}-gutter" aria-hidden="true">${nums.join('\n')}</div>
        <textarea id="${editorId}" class="code-editor" spellcheck="false" style="min-height:${mh}px;">${escapeHtmlStr(raw)}</textarea>
      </div>
    </div>`;
}
window.buildCodeEditorWithGutterHTML = buildCodeEditorWithGutterHTML;

// Helper: Build Segmented Stories-style Flashcard Progress Bar
function buildFcStoriesBarHTML(deckId, totalCards, curIdx){
  ensureExtendedState();
  const ratings = state.cardRatings || {};
  const count = Math.max(1, Math.min(60, Number(totalCards) || 1));
  const segs = [];
  for(let i = 0; i < count; i++){
    const r = Number(ratings[deckId + ':' + i]) || 0;
    let cls = 'fc-story-seg';
    if(i === curIdx) cls += ' fc-story-seg--active seg--current';
    if(r === 4) cls += ' fc-story-seg--r4 seg--easy';
    else if(r === 3) cls += ' fc-story-seg--r3 seg--easy';
    else if(r === 2) cls += ' fc-story-seg--r2 seg--hard';
    else if(r === 1) cls += ' fc-story-seg--r1 seg--again';
    segs.push(`<div class="${cls}" title="Карточка ${i+1}"></div>`);
  }
  return `<div class="fc-stories-bar" aria-label="Прогресс колоды">${segs.join('')}</div>`;
}
window.buildFcStoriesBarHTML = buildFcStoriesBarHTML;

// Helper: Build Interactive CPython Memory Layout SVG/HTML Diagram for Consolidation Lab
function buildCPythonMemoryDiagramHTML(activeK, skillId){
  const isDictOrSet = /1\.2\.[23]|4\.3\.2|К-01[2-9]|К-118/.test(String(activeK) + ' ' + String(skillId));
  return `
    <div class="cpython-mem-diagram">
      <div class="cpython-mem-title">🔬 CPython Memory Layout · ${isDictOrSet ? 'Compact Dict Hash Table' : 'PyObject & Pointer Array'}</div>
      <svg class="cpython-mem-svg" viewBox="0 0 380 54" width="100%" height="54" role="img" aria-label="Схема ссылок в памяти CPython" style="display:block;margin-bottom:6px;">
        <rect x="2" y="6" width="102" height="42" rx="6" fill="rgba(16,185,129,0.12)" stroke="rgba(16,185,129,0.45)" stroke-width="1.2"/>
        <text x="10" y="22" font-size="9.5" font-weight="700" fill="currentColor">Stack Frame</text>
        <text x="10" y="37" font-size="8.5" font-family="monospace" fill="currentColor">data ➔ 0x7f8a10</text>
        <path d="M106 27 L138 27" stroke="#10b981" stroke-width="1.6" stroke-dasharray="3 2"/>
        <polygon points="138,23 145,27 138,31" fill="#10b981"/>
        <rect x="147" y="6" width="230" height="42" rx="6" fill="rgba(245,158,11,0.10)" stroke="rgba(245,158,11,0.42)" stroke-width="1.2"/>
        <text x="156" y="22" font-size="9.5" font-weight="700" fill="currentColor">PyObject @ 0x7f8a10 (Heap)</text>
        <text x="156" y="37" font-size="8.5" font-family="monospace" fill="currentColor">${isDictOrSet ? 'ob_refcnt:1 | dk_indices | dk_entries' : 'ob_refcnt:1 | ob_type | ob_item[0..n]'}</text>
      </svg>
      <div class="cpython-mem-grid">
        <div class="cpython-mem-box">
          <div style="font-weight:700;color:var(--moss-deep);margin-bottom:3px;">PyObject Header (24 B)</div>
          <div><code>ob_refcnt</code> · счётчик ссылок GC</div>
          <div><code>ob_type</code> ➔ <code>&amp;PyList_Type</code></div>
          <div><code>ob_item</code> ➔ массив указателей <code>PyObject*</code> (<span class="math-formula">O(1)</span> индекс)</div>
        </div>
        <div class="cpython-mem-box">
          <div style="font-weight:700;color:var(--clay-deep);margin-bottom:3px;">Compact Dict (Python 3.6+)</div>
          <div><code>dk_indices</code> · разреженная таблица индексов (1–8 B)</div>
          <div><code>dk_entries</code> · плотный массив <code>(hash, key*, val*)</code> (<span class="math-formula">O(1)</span> поиск)</div>
        </div>
      </div>
    </div>`;
}
window.buildCPythonMemoryDiagramHTML = buildCPythonMemoryDiagramHTML;

// Helper: Build Tap-to-Fill Chips Zero-Keyboard Exercise
function buildTapToFillExerciseHTML(activeK, skillId){
  const exercises = {
    '1.1': {
      prompt: 'In-place мутация существующего списка без аллокации нового объекта:',
      codePrefix: 'a = [1, 2]; b = a; b ',
      codeSuffix: ' [3]  # a и b ссылаются на один и тот же список',
      options: ['=', '+=', '+', '=='],
      correct: '+=',
      explain: 'Оператор += вызывает метод __iadd__, модифицирующий список по месту за O(k).'
    },
    '1.2': {
      prompt: 'Вычислите номер корзины для ключа <code>emp_id</code> в хеш-таблице из 16 ячеек:',
      codePrefix: 'bucket = ',
      codeSuffix: '(emp_id) % 16  # Переход к корзине за O(1)',
      options: ['len', 'id', 'hash', 'type'],
      correct: 'hash',
      explain: 'Функция hash() вычисляет 64-битный хеш неизменяемого ключа за O(1).'
    },
    '1.3': {
      prompt: 'Каноническое строковое представление объекта для отладки и REPL:',
      codePrefix: 'def ',
      codeSuffix: '(self): return f"Item({self.name!r})"',
      options: ['__str__', '__repr__', '__name__', '__init__'],
      correct: '__repr__',
      explain: 'Метод __repr__ возвращает однозначное, воспроизводимое строковое представление для логов.'
    },
    '1.4': {
      prompt: 'Сохранение метаданных оригинальной функции внутри декоратора:',
      codePrefix: '@functools.',
      codeSuffix: '(func)\ndef wrapper(*args, **kwargs): return func(*args, **kwargs)',
      options: ['cache', 'lru_cache', 'wraps', 'partial'],
      correct: 'wraps',
      explain: 'Декоратор @functools.wraps копирует __name__, __doc__ и __annotations__ с целевой функции.'
    },
    '1.5': {
      prompt: 'Делегирование генерации значений во вложенный генератор:',
      codePrefix: '',
      codeSuffix: ' sub_generator()  # Прозрачное проксирование yield',
      options: ['return', 'yield', 'yield from', 'await'],
      correct: 'yield from',
      explain: 'Конструкция yield from прозрачно проксирует yield, send() и throw() во внутренний генератор.'
    },
    '1.6': {
      prompt: 'Подавление исключения внутри контекстного менеджера (__exit__):',
      codePrefix: 'def __exit__(self, exc_type, exc_val, exc_tb):\n    return ',
      codeSuffix: '  # Подавить исключение без проброса выше',
      options: ['True', 'False', 'None', 'pass'],
      correct: 'True',
      explain: 'Возврат True из __exit__ сообщает Python, что исключение перехвачено и обработано.'
    },
    '1.7': {
      prompt: 'Освобождение GIL на время блокирующего системного ввода/вывода в C-extension:',
      codePrefix: 'Py_',
      codeSuffix: '_ALLOW_THREADS  # Освобождение GIL',
      options: ['BEGIN', 'SET', 'ENABLE', 'START'],
      correct: 'BEGIN',
      explain: 'Макрос Py_BEGIN_ALLOW_THREADS временно отпускает GIL перед блокирующим вызовом I/O.'
    },
    '1.8': {
      prompt: 'Конкурентный запуск нескольких задач с получением упорядоченного результата:',
      codePrefix: 'results = await asyncio.',
      codeSuffix: '(*tasks)  # Конкурентный запуск',
      options: ['wait', 'gather', 'run', 'create_task'],
      correct: 'gather',
      explain: 'asyncio.gather(*tasks) запускает переданные задачи конкурентно и возвращает список ответов.'
    },
    '1.9': {
      prompt: 'Отключение динамического __dict__ экземпляра для радикальной экономии RAM:',
      codePrefix: '__',
      codeSuffix: '__ = ("x", "y")  # Фиксация дескрипторов атрибутов',
      options: ['slots', 'all', 'dict', 'fields'],
      correct: 'slots',
      explain: '__slots__ резервирует статический массив указателей в CPython struct вместо словаря.'
    }
  };
  const uPrefix = String(skillId || '').slice(0, 3);
  const ex = exercises[skillId] || exercises[uPrefix] || exercises['1.1'];
  const exKey = 'tap_ex_' + skillId;
  const curVal = window.__tapExState ? window.__tapExState[exKey] : null;
  const isDone = (curVal === ex.correct);

  const chipsHTML = ex.options.map(function(opt){
    let cls = 'tap-chip';
    if(curVal === opt){
      cls += isDone ? ' selected-correct' : ' selected-wrong';
    }
    return `<button type="button" class="${cls}" data-tap-chip-val="${escapeHtmlStr(opt)}" data-tap-chip-key="${exKey}" data-tap-chip-correct="${escapeHtmlStr(ex.correct)}">${escapeHtmlStr(opt)}</button>`;
  }).join('');

  return `
    <div class="tap-chip-card" style="margin-top:10px;">
      <div class="topic-badge" style="margin-bottom:6px;">Zero-Keyboard Scaffolding · Интерактив</div>
      <p style="font-size:.88rem;line-height:1.48;margin-bottom:8px;color:var(--ink);">${ex.prompt}</p>
      <div class="tap-code-slot-container" style="margin:8px 0;">
        <code>${ex.codePrefix}<span class="tap-code-slot ${curVal ? (isDone ? 'filled selected-correct' : 'filled selected-wrong') : 'empty'}">${curVal ? escapeHtmlStr(curVal) : '[ ? ]'}</span>${ex.codeSuffix}</code>
      </div>
      <div class="tap-chips-bank-label">Банк токенов (тапни для выбора):</div>
      <div class="tap-chips-row">${chipsHTML}</div>
      ${curVal ? `
        <div class="bottom-sheet-correct" style="margin-top:10px;padding:8px 12px;border-radius:12px;background:${isDone ? 'rgba(16,185,129,0.18)' : 'rgba(190,18,60,0.18)'};">
          <span style="font-size:.82rem;font-weight:700;color:${isDone ? 'var(--moss)' : 'var(--bordeaux)'};">${isDone ? '✓ Верно!' : '✕ Попробуй другой токен.'} ${ex.explain}</span>
        </div>` : ''}
    </div>`;
}
window.buildTapToFillExerciseHTML = buildTapToFillExerciseHTML;

// Register all 7 Mastery Tracks (Python, Web, Backend, Algorithms, Databases, Architecture, Infrastructure)
const MASTERY_TRACKS = {
  python: {
    key: 'python',
    routePrefix: '/python',
    title: '🐍 Матрица Мастерства Python',
    shortTitle: '🐍 Модуль 1 · Python',
    badge: 'Модуль 01 · Полная база RemNote (68 конспектов · 126 колод · 401 задача)',
    backLabel: 'К Матрице Мастерства Python',
    courseUnitRange: 'Юниты 1.1–1.9',
    cols: 7,
    data: PY_MASTERY,
    skills: []
  },
  web: {
    key: 'web',
    routePrefix: '/web',
    title: '🌐 Матрица Мастерства Web',
    shortTitle: '🌐 Модуль 2 · Web',
    badge: 'Модуль 02 · 🌐 Web (4 юнита 2.1–2.4 · 10 навыков · 23 конспекта · 25 колод · 491 карточка)',
    backLabel: 'К Матрице Мастерства Web',
    courseUnitRange: 'Юниты 2.1–2.4',
    cols: 5,
    data: WEB_MASTERY,
    skills: []
  },
  backend: {
    key: 'backend',
    routePrefix: '/backend',
    title: '⚙️ Матрица Мастерства Backend',
    shortTitle: '⚙️ Модуль 3 · Backend',
    badge: 'Модуль 03 · ⚙️ Backend (8 частей 3.1–3.8 · 24 навыка · 40 конспектов · 43 колоды · 890 карточек)',
    backLabel: 'К Матрице Мастерства Backend',
    courseUnitRange: 'Юниты 3.1–3.8',
    cols: 8,
    data: BACKEND_MASTERY,
    skills: []
  },
  algorithms: {
    key: 'algorithms',
    routePrefix: '/algorithms',
    title: '⚡ Матрица Мастерства Алгоритмы',
    shortTitle: '⚡ Модуль 4 · Алгоритмы',
    badge: 'Модуль 04 · ⚡ Алгоритмы (6 юнитов 4.1–4.6 · 12 навыков · 14 конспектов · 16 колод · 463 карточки)',
    backLabel: 'К Матрице Мастерства Алгоритмы',
    courseUnitRange: 'Юниты 4.1–4.6',
    cols: 6,
    data: ALGO_MASTERY,
    skills: []
  },
  databases: {
    key: 'databases',
    routePrefix: '/databases',
    title: '🗄️ Матрица Мастерства Базы данных',
    shortTitle: '🗄️ Модуль 5 · Базы данных',
    badge: 'Модуль 05 · 🗄️ Базы данных (6 юнитов 5.1–5.6 · 17 навыков · 32 конспекта · 32 колоды · 927 карточек)',
    backLabel: 'К Матрице Мастерства Базы данных',
    courseUnitRange: 'Юниты 5.1–5.6',
    cols: 6,
    data: DB_MASTERY,
    skills: []
  },
  architecture: {
    key: 'architecture',
    routePrefix: '/architecture',
    title: '🏛️ Матрица Мастерства Архитектура',
    shortTitle: '🏛️ Модуль 6 · Архитектура',
    badge: 'Модуль 06 · 🏛️ Архитектура (6 юнитов 6.1–6.6 · 14 навыков · 14 конспектов · 17 колод · 263 карточки)',
    backLabel: 'К Матрице Мастерства Архитектура',
    courseUnitRange: 'Юниты 6.1–6.6',
    cols: 7,
    data: ARCH_MASTERY,
    skills: []
  },
  infra: {
    key: 'infra',
    routePrefix: '/infra',
    title: '🚀 Матрица Мастерства Инфраструктура',
    shortTitle: '🚀 Модуль 7 · Инфраструктура',
    badge: 'Модуль 07 · 🚀 Инфраструктура (6 юнитов 7.1–7.6 · 21 навык · 47 конспектов · 45 колод · 1 286 карточек)',
    backLabel: 'К Матрице Мастерства Инфраструктура',
    courseUnitRange: 'Юниты 7.1–7.6',
    cols: 7,
    data: INFRA_MASTERY,
    skills: []
  }
};

const ALL_PY_SKILLS = [];
const ALL_WEB_SKILLS = [];
const ALL_BACKEND_SKILLS = [];
const ALL_ALGO_SKILLS = [];
const ALL_DB_SKILLS = [];
const ALL_ARCH_SKILLS = [];
const ALL_INFRA_SKILLS = [];
const PY_SKILLS_BY_ID = {};
const ALL_NOTES_COMBINED = Object.assign({}, PY_MASTERY.notes, WEB_MASTERY.notes, BACKEND_MASTERY.notes, ALGO_MASTERY.notes, DB_MASTERY.notes, ARCH_MASTERY.notes, INFRA_MASTERY.notes);
const ALL_DECKS_COMBINED = Object.assign({}, PY_MASTERY.decks, WEB_MASTERY.decks, BACKEND_MASTERY.decks, ALGO_MASTERY.decks, DB_MASTERY.decks, ARCH_MASTERY.decks, INFRA_MASTERY.decks);
const ALL_UNIT_TESTS_COMBINED = Object.assign({}, PY_MASTERY.unitTests, WEB_MASTERY.unitTests, BACKEND_MASTERY.unitTests, ALGO_MASTERY.unitTests, DB_MASTERY.unitTests, ARCH_MASTERY.unitTests, INFRA_MASTERY.unitTests);
const ALL_UNITS_COMBINED = [].concat(PY_MASTERY.units, WEB_MASTERY.units, BACKEND_MASTERY.units, ALGO_MASTERY.units, DB_MASTERY.units, ARCH_MASTERY.units, INFRA_MASTERY.units);

Object.values(MASTERY_TRACKS).forEach(tr => {
  tr.data.units.forEach(u => {
    u.trackKey = tr.key;
    u.skills.forEach(s => {
      s.unitId = u.id;
      s.unitTitle = u.title;
      s.trackKey = tr.key;
      s.routePrefix = tr.routePrefix;
      tr.skills.push(s);
      PY_SKILLS_BY_ID[s.id] = s;
      if(tr.key === 'python') ALL_PY_SKILLS.push(s);
      else if(tr.key === 'web') ALL_WEB_SKILLS.push(s);
      else if(tr.key === 'backend') ALL_BACKEND_SKILLS.push(s);
      else if(tr.key === 'algorithms') ALL_ALGO_SKILLS.push(s);
      else if(tr.key === 'databases') ALL_DB_SKILLS.push(s);
      else if(tr.key === 'architecture') ALL_ARCH_SKILLS.push(s);
      else if(tr.key === 'infra') ALL_INFRA_SKILLS.push(s);
    });
  });
});

function getTrackForSkill(sid){
  const s = PY_SKILLS_BY_ID[sid];
  return (s && MASTERY_TRACKS[s.trackKey]) || MASTERY_TRACKS.python;
}
function getTrackForUnit(unitId, fallbackTrackKey){
  if(fallbackTrackKey && MASTERY_TRACKS[fallbackTrackKey]) return MASTERY_TRACKS[fallbackTrackKey];
  const u = ALL_UNITS_COMBINED.find(x => x.id === unitId);
  return (u && MASTERY_TRACKS[u.trackKey]) || MASTERY_TRACKS.python;
}

function getSkillMP(sid){
  ensureExtendedState();
  const s = PY_SKILLS_BY_ID[sid];
  if(!s) return 0;
  let mp = state.skillMastery[sid] || 0;
  const solvedMap = getIdeSolvedMap();
  const notesDone = s.kIds.length > 0 && s.kIds.every(k => state.readNotes.includes(k));
  const anyNoteOrDeck = s.kIds.some(k => state.readNotes.includes(k)) || s.fIds.some(f => state.reviewedDecks.includes(f));
  const solvedCount = (s.taskIds || []).filter(tid => solvedMap[tid] === 'solved').length;
  if(anyNoteOrDeck && mp < 50) mp = 50;
  if((solvedCount >= 1 || (notesDone && s.fIds.some(f => state.reviewedDecks.includes(f)))) && mp < 80) mp = 80;
  if((state.passedUnitTests.includes(s.unitId) || (notesDone && solvedCount >= Math.min(2, (s.taskIds||[]).length || 1))) && mp < 100) mp = 100;
  return mp;
}
function setSkillMP(sid, newMp){
  ensureExtendedState();
  const cur = getSkillMP(sid);
  if(newMp > cur || (newMp >= cur && (state.skillMastery[sid] || 0) < newMp)){
    state.skillMastery[sid] = newMp;
    saveState(state);
    if(newMp > cur) playSound('mastery');
  }
}
function totalTrackMP(trackKey){
  const tr = MASTERY_TRACKS[trackKey] || MASTERY_TRACKS.python;
  return tr.skills.reduce((acc, s) => acc + getSkillMP(s.id), 0);
}
function maxTrackMP(trackKey){
  const tr = MASTERY_TRACKS[trackKey] || MASTERY_TRACKS.python;
  return tr.skills.length * 100;
}
function totalPythonMP(){ return totalTrackMP('python'); }
function maxPythonMP(){ return maxTrackMP('python'); } // 2800 MP
function totalWebMP(){ return totalTrackMP('web'); }
function maxWebMP(){ return maxTrackMP('web'); } // 1000 MP
function totalBackendMP(){ return totalTrackMP('backend'); }
function maxBackendMP(){ return maxTrackMP('backend'); } // 2400 MP
function totalAlgoMP(){ return totalTrackMP('algorithms'); }
function maxAlgoMP(){ return maxTrackMP('algorithms'); } // 1200 MP
function totalDbMP(){ return totalTrackMP('databases'); }
function maxDbMP(){ return maxTrackMP('databases'); } // 1700 MP
function totalArchMP(){ return totalTrackMP('architecture'); }
function maxArchMP(){ return maxTrackMP('architecture'); } // 1400 MP
function totalInfraMP(){ return totalTrackMP('infra'); }
function maxInfraMP(){ return maxTrackMP('infra'); } // 2100 MP

function mpLabel(mp){
  if(mp >= 100) return '👑 Мастерство (100 MP)';
  if(mp >= 80) return 'Практика / Proficient (80 MP)';
  if(mp >= 50) return 'Знакомство / Familiar (50 MP)';
  return 'Не начато (0 MP)';
}

// Pomodoro Focus Timer (synced across Dashboard, Topbar, and Sidebar)
let pomoState = { running: false, secondsLeft: 15 * 60, modeMin: 15, intervalId: null };
function syncPomoDisplays(){
  const formatted = formatPomo(pomoState.secondsLeft);
  ['pomo-time-display', 'topbar-pomo-time', 'sidebar-pomo-time'].forEach(id => {
    const el = document.getElementById(id);
    if(el) el.textContent = formatted;
  });
  ['topbar-pomo-btn', 'sidebar-pomo-btn'].forEach(id => {
    const btn = document.getElementById(id);
    if(btn) btn.classList.toggle('is-running', !!pomoState.running);
  });
}
function togglePomodoro(mins){
  playSound('tick');
  if(mins && mins !== pomoState.modeMin){
    pomoState.modeMin = mins;
    pomoState.secondsLeft = mins * 60;
    pomoState.running = false;
    if(pomoState.intervalId){ clearInterval(pomoState.intervalId); pomoState.intervalId = null; }
  }
  if(pomoState.running){
    pomoState.running = false;
    if(pomoState.intervalId){ clearInterval(pomoState.intervalId); pomoState.intervalId = null; }
  } else {
    pomoState.running = true;
    pomoState.intervalId = setInterval(function(){
      if(pomoState.secondsLeft > 0){
        pomoState.secondsLeft--;
        syncPomoDisplays();
      } else {
        clearInterval(pomoState.intervalId);
        pomoState.intervalId = null;
        pomoState.running = false;
        playSound('success');
        awardXp(25);
        render();
      }
    }, 1000);
  }
  syncPomoDisplays();
  render();
}
function formatPomo(sec){
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
}
window.syncPomoDisplays = syncPomoDisplays;
window.togglePomodoro = togglePomodoro;
window.formatPomo = formatPomo;


/* ================= INTERVIEW-FIRST PRIORITY ARCHITECTURE (4 ECHELONS + PARALLEL STACK BRANCHES) ================= */
const INTERVIEW_ECHELONS = {
  1: { tier: 1, icon: '🚨', badgeClass: 'echelon-badge--t1', label: '🚨 Эшелон 1: Скрининг · Фундамент', shortLabel: '🚨 Эшелон 1: Скрининг', focus: 'Фундамент', targetLabel: 'к скринингу', desc: 'Первичный отсев на HR и тех-скрининге (Python Core, сложность O(n), два указателя, SQL JOIN, HTTP/REST, Git и pytest)', color: '#34d399', gradient: 'linear-gradient(90deg, #f43f5e, #34d399)' },
  2: { tier: 2, icon: '🎯', badgeClass: 'echelon-badge--t2', label: '🎯 Эшелон 2: Тех-интервью · Стек и базы данных', shortLabel: '🎯 Эшелон 2: Тех-интервью', focus: 'Стек и базы данных', targetLabel: 'к тех-интервью', desc: 'Основное техническое собеседование по выбранному стеку (ООП, Итераторы, Asyncio/GIL, FastAPI + SQLAlchemy или Django + DRF, ACID/Индексы, Docker)', color: '#fbbf24', gradient: 'linear-gradient(90deg, #f59e0b, #10b981)' },
  3: { tier: 3, icon: '⚡', badgeClass: 'echelon-badge--t3', label: '⚡ Эшелон 3: Лайвкодинг · Сервисы и продакшен', shortLabel: '⚡ Эшелон 3: Лайвкодинг', focus: 'Сервисы и продакшен', targetLabel: 'к лайвкодингу', desc: 'Инженерия уровня Strong Junior / Middle (Redis, Celery/Kafka, SOLID и Чистая архитектура, CI/CD, Linux/Nginx, Observability)', color: '#34d399', gradient: 'linear-gradient(90deg, #10b981, #06b6d4)' },
  4: { tier: 4, icon: '👑', badgeClass: 'echelon-badge--t4', label: '👑 Эшелон 4: Финал · Системный дизайн и оффер', shortLabel: '👑 Эшелон 4: Финал', focus: 'Системный дизайн и оффер', targetLabel: 'к офферу', desc: 'Конкурентное преимущество на оффер (Highload, System Design, паттерны проектирования, альтернативный фреймворк в резерве)', color: '#c084fc', gradient: 'linear-gradient(90deg, #a855f7, #ec4899)' }
};
window.INTERVIEW_ECHELONS = INTERVIEW_ECHELONS;

const UNIT_INTERVIEW_META = {
  '1.1': { tier: 1, stackTag: 'core' },
  '1.2': { tier: 1, stackTag: 'core' },
  '1.3': { tier: 1, stackTag: 'core' },
  '1.4': { tier: 1, stackTag: 'core' },
  '1.5': { tier: 2, stackTag: 'core' },
  '1.6': { tier: 2, stackTag: 'core' },
  '1.7': { tier: 2, stackTag: 'core' },
  '1.8': { tier: 2, stackTag: 'fastapi' },
  '1.9': { tier: 1, stackTag: 'core' },
  '2.1': { tier: 2, stackTag: 'core' },
  '2.2': { tier: 1, stackTag: 'core' },
  '2.3': { tier: 1, stackTag: 'core' },
  '2.4': { tier: 2, stackTag: 'core' },
  '3.1': { tier: 2, stackTag: 'fastapi' },
  '3.2': { tier: 2, stackTag: 'django' },
  '3.3': { tier: 2, stackTag: 'django' },
  '3.4': { tier: 4, stackTag: 'flask' },
  '3.5': { tier: 2, stackTag: 'core' },
  '3.6': { tier: 2, stackTag: 'core' },
  '3.7': { tier: 3, stackTag: 'core' },
  '3.8': { tier: 3, stackTag: 'core' },
  '4.1': { tier: 1, stackTag: 'core' },
  '4.2': { tier: 1, stackTag: 'core' },
  '4.3': { tier: 2, stackTag: 'core' },
  '4.4': { tier: 1, stackTag: 'core' },
  '4.5': { tier: 3, stackTag: 'core' },
  '4.6': { tier: 2, stackTag: 'core' },
  '5.1': { tier: 1, stackTag: 'core' },
  '5.2': { tier: 1, stackTag: 'core' },
  '5.3': { tier: 1, stackTag: 'core' },
  '5.4': { tier: 2, stackTag: 'core' },
  '5.5': { tier: 2, stackTag: 'fastapi' },
  '5.6': { tier: 3, stackTag: 'core' },
  '6.1': { tier: 3, stackTag: 'core' },
  '6.2': { tier: 3, stackTag: 'core' },
  '6.3': { tier: 3, stackTag: 'core' },
  '6.4': { tier: 4, stackTag: 'core' },
  '6.5': { tier: 3, stackTag: 'core' },
  '6.6': { tier: 4, stackTag: 'core' },
  '7.1': { tier: 1, stackTag: 'core' },
  '7.2': { tier: 2, stackTag: 'core' },
  '7.3': { tier: 3, stackTag: 'core' },
  '7.4': { tier: 3, stackTag: 'core' },
  '7.5': { tier: 3, stackTag: 'core' },
  '7.6': { tier: 2, stackTag: 'core' }
};
window.UNIT_INTERVIEW_META = UNIT_INTERVIEW_META;

// Map each of the 18 Skill Tree nodes (#/map & #/topic/<id>) to its corresponding units across the 7 modules
const NODE_TO_UNITS_MAP = {
  'diag': ['1.1', '1.2', '2.2', '4.1', '5.2', '7.1'],
  'py-basics': ['1.1', '1.2', '1.3', '1.4', '1.9'],
  'py-core': ['1.1', '1.2', '1.3', '1.4', '1.9'],
  'git': ['7.1'],
  'sql': ['5.1', '5.2', '5.3', '5.4'],
  'http': ['2.1', '2.2', '2.3'],
  'oop': ['1.5', '1.6', '1.7'],
  'algo': ['4.1', '4.2', '4.3', '4.4', '4.5', '4.6'],
  'algos': ['4.1', '4.2', '4.3', '4.4', '4.5', '4.6'],
  'orm': ['5.5', '3.2'],
  'async': ['1.8'],
  'framework': ['3.1', '3.2', '3.3', '3.4', '3.5', '3.6'],
  'fastapi': ['3.1', '3.3', '3.4', '3.5', '3.6'],
  'testing': ['7.6'],
  'pytest': ['7.6'],
  'cache': ['5.6', '3.7', '7.5'],
  'redis': ['5.6', '3.7', '7.5'],
  'docker': ['7.2', '7.3', '7.4', '3.8'],
  'security': ['2.4', '3.5'],
  'sec': ['2.4', '3.5'],
  'sysdesign': ['6.1', '6.2', '6.3', '6.4', '6.5', '6.6'],
  'llm': ['3.1', '2.3'],
  'final': ['3.6', '3.8', '7.2', '7.6'],
  'capstone': ['3.6', '3.8', '7.2', '7.6'],
  'interview': ['1.1', '1.4', '2.2', '3.1', '4.1', '5.2', '5.4', '7.1']
};
window.NODE_TO_UNITS_MAP = NODE_TO_UNITS_MAP;

const UNITS_BY_ID = {};
const TASK_TO_SKILLS_MAP = {};
const DECK_TO_SKILLS_MAP = {};
ALL_UNITS_COMBINED.forEach(u => {
  UNITS_BY_ID[u.id] = u;
  const meta = UNIT_INTERVIEW_META[u.id] || { tier: u.tier || 2, stackTag: u.stackTag || 'core' };
  u.tier = meta.tier;
  u.stackTag = meta.stackTag;
  u.tierLabel = INTERVIEW_ECHELONS[meta.tier].label;
  u.skills.forEach(s => {
    s.tier = meta.tier;
    s.stackTag = meta.stackTag;
    s.tierLabel = INTERVIEW_ECHELONS[meta.tier].label;
    (s.taskIds || []).forEach(tid => {
      if(!TASK_TO_SKILLS_MAP[tid]) TASK_TO_SKILLS_MAP[tid] = [];
      TASK_TO_SKILLS_MAP[tid].push(s);
    });
    (s.fIds || []).forEach(fid => {
      if(!DECK_TO_SKILLS_MAP[fid]) DECK_TO_SKILLS_MAP[fid] = [];
      DECK_TO_SKILLS_MAP[fid].push(s);
    });
  });
});

function getEffectiveUnitTier(unitId, branchOverride){
  ensureExtendedState();
  const branch = branchOverride || state.stackBranch || 'fastapi';
  const meta = UNIT_INTERVIEW_META[unitId] || { tier: 2, stackTag: 'core' };
  if(branch === 'fastapi' && meta.stackTag === 'django') return 4;
  if(branch === 'django' && unitId === '3.1') return 4;
  return meta.tier;
}
window.getEffectiveUnitTier = getEffectiveUnitTier;

function getEffectiveSkillTier(skillId, branchOverride){
  const s = PY_SKILLS_BY_ID[skillId];
  if(!s) return 2;
  return getEffectiveUnitTier(s.unitId, branchOverride);
}
window.getEffectiveSkillTier = getEffectiveSkillTier;

function getEchelonMeta(tierNum){
  return INTERVIEW_ECHELONS[tierNum] || INTERVIEW_ECHELONS[2];
}

function renderEchelonBadge(tierNum, extraText){
  const em = getEchelonMeta(tierNum);
  return `<span class="echelon-badge echelon-badge--t${em.tier}" title="${escapeHtmlStr(em.desc)}">${em.shortLabel}${extraText ? ' · ' + extraText : ''}</span>`;
}

function getTaskInterviewTier(taskId){
  const skills = TASK_TO_SKILLS_MAP[taskId];
  if(skills && skills.length > 0){
    let best = 4;
    for(let i=0; i<skills.length; i++){
      const t = getEffectiveSkillTier(skills[i].id);
      if(t < best) best = t;
    }
    return best;
  }
  const tObj = IDE_TASKS_BY_ID[taskId];
  if(!tObj) return 2;
  const tr = String(tObj.tier || '');
  if(tr.includes('1') || tr.includes('2')) return 1;
  if(tr.includes('3') || tr.includes('4') || tr.includes('5')) return 2;
  if(tr.includes('6')) return 3;
  return 4;
}
window.getTaskInterviewTier = getTaskInterviewTier;

function getDeckInterviewTier(deckId){
  const skills = DECK_TO_SKILLS_MAP[deckId];
  if(skills && skills.length > 0){
    let best = 4;
    for(let i=0; i<skills.length; i++){
      const t = getEffectiveSkillTier(skills[i].id);
      if(t < best) best = t;
    }
    return best;
  }
  return 2;
}
window.getDeckInterviewTier = getDeckInterviewTier;

function getEchelonProgress(tierNum){
  const allSkills = [].concat(ALL_PY_SKILLS, ALL_WEB_SKILLS, ALL_BACKEND_SKILLS, ALL_ALGO_SKILLS, ALL_DB_SKILLS, ALL_ARCH_SKILLS, ALL_INFRA_SKILLS);
  const tierSkills = allSkills.filter(s => getEffectiveSkillTier(s.id) === tierNum);
  const curMp = tierSkills.reduce((acc, s) => acc + getSkillMP(s.id), 0);
  const maxMp = tierSkills.length * 100;
  const pct = maxMp > 0 ? Math.round(curMp / maxMp * 100) : 0;
  const mastered = tierSkills.filter(s => getSkillMP(s.id) >= 100).length;
  const units = ALL_UNITS_COMBINED.filter(u => getEffectiveUnitTier(u.id) === tierNum);
  const nextSk = tierSkills.find(s => getSkillMP(s.id) < 100) || tierSkills[0] || ALL_PY_SKILLS[0];
  return {
    tier: tierNum,
    skills: tierSkills,
    nextSkill: nextSk,
    skillsCount: tierSkills.length,
    unitsCount: units.length,
    curMp: curMp,
    maxMp: maxMp,
    curMP: curMp,
    maxMP: maxMp,
    pct: pct,
    mastered: mastered
  };
}
window.getEchelonProgress = getEchelonProgress;

function setStackBranch(branch){
  ensureExtendedState();
  if(['fastapi','django','both'].includes(branch)){
    state.stackBranch = branch;
    saveState(state);
  }
}
window.setStackBranch = setStackBranch;

function getFirstUnmasteredSkillInEchelon(tierNum, preferredTrackKey){
  const baseSkills = (preferredTrackKey && MASTERY_TRACKS[preferredTrackKey])
    ? MASTERY_TRACKS[preferredTrackKey].skills
    : [].concat(ALL_PY_SKILLS, ALL_WEB_SKILLS, ALL_BACKEND_SKILLS, ALL_ALGO_SKILLS, ALL_DB_SKILLS, ALL_ARCH_SKILLS, ALL_INFRA_SKILLS);
  const candidates = baseSkills.filter(s => (!tierNum || getEffectiveSkillTier(s.id) === tierNum) && getSkillMP(s.id) < 100);
  if(candidates.length > 0) return candidates[0];
  return baseSkills[0] || ALL_PY_SKILLS[0];
}

// Fast 2-Minute Anti-Procrastination Launcher (prioritizes Diagnostic Gaps -> Echelon 1 -> Echelon 2 -> Echelon 3 -> Echelon 4)
function startTwoMinuteMicroStep(preferredTrackKey, prefKid){
  ensureExtendedState();
  function goToSkillSprint(sk, kid){
    const targetHash = '#' + sk.routePrefix + '/skill/' + sk.id;
    ensurePySkillState(sk.id);
    pySkillViewState.tab = 'theory';
    if(kid) pySkillViewState.kId = kid;
    pySkillViewState.sprintCelebration = null;
    if(location.hash === targetHash) render();
    else location.hash = targetHash;
  }
  if(preferredTrackKey && PY_SKILLS_BY_ID[preferredTrackKey]){
    goToSkillSprint(PY_SKILLS_BY_ID[preferredTrackKey], prefKid);
    return;
  }
  if(preferredTrackKey && MASTERY_TRACKS[preferredTrackKey]){
    const prefSkills = (MASTERY_TRACKS[preferredTrackKey].skills || []).slice().sort((a, b) => {
      const gapA = state.diagnosticGaps.includes(a.id) ? 0 : 1;
      const gapB = state.diagnosticGaps.includes(b.id) ? 0 : 1;
      if(gapA !== gapB) return gapA - gapB;
      return getEffectiveSkillTier(a.id) - getEffectiveSkillTier(b.id);
    });
    for(let i=0; i<prefSkills.length; i++){
      const sk = prefSkills[i];
      if(getSkillMP(sk.id) < 100){
        goToSkillSprint(sk);
        return;
      }
    }
  }
  if(state.diagnosticGaps && state.diagnosticGaps.length > 0){
    for(let i=0; i<state.diagnosticGaps.length; i++){
      const gid = state.diagnosticGaps[i];
      const gSk = PY_SKILLS_BY_ID[gid];
      if(gSk && getSkillMP(gSk.id) < 100){
        goToSkillSprint(gSk);
        return;
      }
    }
  }
  const allSkills = [].concat(ALL_PY_SKILLS, ALL_WEB_SKILLS, ALL_BACKEND_SKILLS, ALL_ALGO_SKILLS, ALL_DB_SKILLS, ALL_ARCH_SKILLS, ALL_INFRA_SKILLS);
  for(let tier = 1; tier <= 4; tier++){
    for(let i=0; i<allSkills.length; i++){
      const sk = allSkills[i];
      if(getEffectiveSkillTier(sk.id) === tier && getSkillMP(sk.id) < 100){
        goToSkillSprint(sk);
        return;
      }
    }
  }
  const fallbackTr = (preferredTrackKey && MASTERY_TRACKS[preferredTrackKey]) || MASTERY_TRACKS.python;
  const firstSk = (fallbackTr.skills && fallbackTr.skills[0]) || ALL_PY_SKILLS[0];
  if(firstSk) goToSkillSprint(firstSk);
}

/* ================= PYTHON EXECUTION ENGINE (BRYTHON 3.13 + PYODIDE 0.26.4) ================= */
const BRYTHON_PRELUDE = __BRYTHON_PRELUDE_JSON__;

let brythonReady = false;
let pyodidePreludeLoaded = false;
function ensureBrythonInit(){
  if(brythonReady) return true;
  if(window.__BRYTHON__ && typeof window.brython === 'function'){
    try{
      if(!window.__BRYTHON__.builtins){
        window.brython({debug: 0});
      }
      brythonReady = !!window.__BRYTHON__.builtins;
    }catch(e){}
  }
  return brythonReady;
}

// Provide a Pyodide-compatible wrapper backed by instant Brython 3.13.0 (or Pyodide 0.26.4 fallback)
async function getFastPythonRunner(){
  if(ensureBrythonInit() && window.__BRYTHON__ && window.__BRYTHON__.runPythonSource){
    let stdoutFn = null, stderrFn = null;
    let lastGlobals = {};
    return {
      setStdout: function(o){ stdoutFn = o && o.batched; },
      setStderr: function(o){ stderrFn = o && o.batched; },
      runPython: function(src){
        window.pba_stdout_cb = function(s){
          if(typeof s !== 'string'){
            try { s = (s && typeof s.$js === 'function') ? String(s.$js()) : String(s); } catch(e){ s = String(s); }
          }
          if(stdoutFn) stdoutFn(String(s));
        };
        window.pba_stderr_cb = function(s){
          if(typeof s !== 'string'){
            try { s = (s && typeof s.$js === 'function') ? String(s.$js()) : String(s); } catch(e){ s = String(s); }
          }
          if(stderrFn) stderrFn(String(s));
        };
        window.pba_result_bridge = {};
        const wrapped = BRYTHON_PRELUDE + `\nimport sys, io as _io\nfrom browser import window as _bw\nclass _PBAOut:\n    def write(self, s):\n        if s is not None:\n            _bw.pba_stdout_cb(str(s))\n    def flush(self): pass\nclass _PBAErr:\n    def write(self, s):\n        if s is not None:\n            _bw.pba_stderr_cb(str(s))\n    def flush(self): pass\nsys.stdout = _PBAOut()\nsys.stderr = _PBAErr()\n` + src + `\ntry:\n    _bw.pba_result_bridge.res = bool(__result__)\n    _bw.pba_result_bridge.msg = str(__message__)\nexcept Exception:\n    pass\n`;
        window.__BRYTHON__.runPythonSource(wrapped, '__main_' + Math.random().toString(36).slice(2));
        lastGlobals = {
          __result__: window.pba_result_bridge.res,
          __message__: window.pba_result_bridge.msg || ''
        };
      },
      globals: {
        get: function(k){ return lastGlobals[k]; }
      }
    };
  }
  const py = await getPyodide();
  if(!pyodidePreludeLoaded){
    try{ py.runPython(BRYTHON_PRELUDE + '\nimport sys, io as _io\n'); pyodidePreludeLoaded = true; }catch(e){}
  }
  return py;
}

// Run inline code snippet inside theory cards (supports both .snippet-wrap from RemNote K-notes and .code-snippet-wrap from lessons)
// Snippet Output Cache & Restoration (prevents premature disappearance of code output)
window.__snippetOutputs = window.__snippetOutputs || {};
function restoreSnippetOutputs(){
  if(!window.__snippetOutputs) return;
  try {
    document.querySelectorAll('.snippet-wrap, .code-snippet-wrap').forEach(function(wrap){
      const codeEl = wrap.querySelector('code');
      if(!codeEl) return;
      const key = (codeEl.textContent || '').trim();
      if(window.__snippetOutputs[key]){
        let outEl = wrap.querySelector('.snippet-out');
        if(!outEl){
          outEl = wrap.nextElementSibling;
          if(!outEl || !outEl.classList.contains('inline-code-out')){
            outEl = document.createElement('pre');
            outEl.className = 'inline-code-out';
            wrap.insertAdjacentElement('afterend', outEl);
          }
        }
        if(outEl){
          outEl.classList.remove('hidden');
          outEl.textContent = window.__snippetOutputs[key];
        }
      }
    });
  } catch(e){}
}

async function runInlineSnippet(btnEl){
  const wrap = btnEl.closest('.snippet-wrap, .code-snippet-wrap');
  if(!wrap) return;
  const codeEl = wrap.querySelector('code');
  if(!codeEl) return;
  let outEl = wrap.querySelector('.snippet-out');
  if(!outEl){
    outEl = wrap.nextElementSibling;
    if(!outEl || !outEl.classList.contains('inline-code-out')){
      outEl = document.createElement('pre');
      outEl.className = 'inline-code-out';
      wrap.insertAdjacentElement('afterend', outEl);
    }
  } else {
    outEl.classList.remove('hidden');
  }
  outEl.textContent = 'Выполняю…';
  let buf = '';
  try{
    const runner = await getFastPythonRunner();
    runner.setStdout({ batched: function(s){ buf += s; } });
    runner.setStderr({ batched: function(s){ buf += s; } });
    const ctxCode = btnEl.getAttribute('data-ctx') || '';
    const rawCode = codeEl.textContent || '';
    const nonComment = rawCode.split('\n').filter(l => !l.trim().startsWith('#')).join('\n');
    let bodyToRun = rawCode;
    if(/\bawait\s+/.test(nonComment) && !/\basync\s+def\s+/.test(nonComment)){
      const ind = rawCode.split('\n').map(l => '    ' + l).join('\n');
      bodyToRun = 'import asyncio\nasync def __top_snip():\n' + ind + '\n    pass\nasyncio.run(__top_snip())';
    } else if(/\basync\s+def\s+main\s*\(/.test(nonComment) && !/\basyncio\.run\s*\(/.test(nonComment)){
      bodyToRun = rawCode + '\nimport asyncio\nasyncio.run(main())';
    }
    const indBody = bodyToRun.split('\n').map(l => '    ' + l).join('\n');
    let fullScript = 'import sys, io as _io\n';
    if(ctxCode){
      const indCtx = ctxCode.split('\n').map(l => '    ' + l).join('\n');
      fullScript += `_orig_out, _orig_err = sys.stdout, sys.stderr\nsys.stdout = sys.stderr = _io.StringIO()\ntry:\n${indCtx}\nexcept Exception:\n    pass\nfinally:\n    sys.stdout, sys.stderr = _orig_out, _orig_err\n`;
    }
    fullScript += `__SNIP_SRC__ = ${JSON.stringify(rawCode)}\n_before_keys = set(globals().keys())\ntry:\n${indBody}\nexcept Exception as _snip_e:\n    _ename = type(_snip_e).__name__\n    if _ename in __SNIP_SRC__:\n        print(f"{_ename}: {_snip_e}")\n    else:\n        raise\n`;
    runner.runPython(fullScript);
    if(!buf.trim()){
      const defMatches = Array.from(rawCode.matchAll(/^\s*(?:async\s+)?def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(/gm)).map(m => m[1]);
      const clsMatches = Array.from(rawCode.matchAll(/^\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)/gm)).map(m => m[1]);
      if(defMatches.length || clsMatches.length){
        const items = defMatches.map(fn => `${fn}()`).concat(clsMatches.map(cn => `class ${cn}`));
        outEl.textContent = '✓ Определено в памяти Python: ' + items.join(', ');
      } else {
        outEl.textContent = '✓ Код выполнен без ошибок';
      }
    } else {
      outEl.textContent = buf.trim();
    }
    window.__snippetOutputs = window.__snippetOutputs || {};
    const codeKeyToCache = (codeEl.textContent || '').trim();
    if(codeKeyToCache){
      window.__snippetOutputs[codeKeyToCache] = outEl.textContent;
    }
    awardXp(2);
  }catch(err){
    outEl.textContent = 'Ошибка: ' + String(err);
    window.__snippetOutputs = window.__snippetOutputs || {};
    const codeKeyToCache = (codeEl.textContent || '').trim();
    if(codeKeyToCache){
      window.__snippetOutputs[codeKeyToCache] = outEl.textContent;
    }
  }
}


/* ================= PYTHON MASTERY VIEWS (KHAN ACADEMY STYLE) ================= */
let pySkillViewState = {
  sid: null,
  tab: 'theory', // 'theory' | 'cards' | 'code'
  kId: null,
  stepIdx: 0,
  chunkIdx: 0,
  fullNoteMode: false,
  sprintCelebration: null,
  fId: null,
  cardIdx: 0,
  cardFlipped: false,
  taskId: null,
  codeDraft: '',
  hintLevel: 0,
  runStatus: null,
  runOutput: '',
  labDrafts: {}
};

function saveReadingPosition(){
  ensureExtendedState();
  if(!pySkillViewState || !pySkillViewState.sid) return;
  state.readingPositions[pySkillViewState.sid] = {
    tab: pySkillViewState.tab || 'theory',
    kId: pySkillViewState.kId,
    stepIdx: pySkillViewState.stepIdx || 0,
    chunkIdx: pySkillViewState.chunkIdx || 0,
    fullNoteMode: !!pySkillViewState.fullNoteMode,
    fId: pySkillViewState.fId,
    cardIdx: pySkillViewState.cardIdx || 0,
    taskId: pySkillViewState.taskId,
    updatedAt: Date.now()
  };
  saveState(state);
}

function ensurePySkillState(sid){
  ensureExtendedState();
  const sk = PY_SKILLS_BY_ID[sid] || ALL_PY_SKILLS[0];
  if(pySkillViewState.sid !== sk.id){
    const isInitialBoot = (pySkillViewState.sid === null);
    const saved = (state.readingPositions && state.readingPositions[sk.id]) || {};
    const firstK = (saved.kId && sk.kIds.includes(saved.kId)) ? saved.kId : (sk.kIds[0] || null);
    const firstF = (saved.fId && sk.fIds.includes(saved.fId)) ? saved.fId : (sk.fIds[0] || null);
    const firstT = (saved.taskId && sk.taskIds && sk.taskIds.includes(saved.taskId)) ? saved.taskId : ((sk.taskIds && sk.taskIds[0]) || 240);
    const tObj = IDE_TASKS_BY_ID[firstT];
    const oldDrafts = (pySkillViewState && pySkillViewState.labDrafts) ? pySkillViewState.labDrafts : {};
    pySkillViewState = {
      sid: sk.id,
      tab: (isInitialBoot && ['theory','cards','code'].includes(saved.tab)) ? saved.tab : 'theory',
      kId: firstK,
      stepIdx: typeof saved.stepIdx === 'number' ? saved.stepIdx : 0,
      chunkIdx: typeof saved.chunkIdx === 'number' ? saved.chunkIdx : 0,
      fullNoteMode: !!saved.fullNoteMode,
      sprintCelebration: null,
      fId: firstF,
      cardIdx: typeof saved.cardIdx === 'number' ? saved.cardIdx : 0,
      cardFlipped: false,
      taskId: firstT,
      codeDraft: tObj ? getIdeDraft(firstT, tObj.initialCode) : '',
      hintLevel: 0,
      runStatus: null,
      runOutput: '',
      labDrafts: oldDrafts
    };
  }
  return sk;
}

let backendPartFilter = 'all';
let trackTierFilter = 'all';
let lastTrackKeyForTierFilter = '';

function buildPriorityRoadmapWidgetHTML(opts){
  ensureExtendedState();
  const o = opts || {};
  const branch = state.stackBranch || 'fastapi';
  const e1 = getEchelonProgress(1);
  const e2 = getEchelonProgress(2);
  const e3 = getEchelonProgress(3);
  const e4 = getEchelonProgress(4);
  const echelons = [e1, e2, e3, e4];
  const openGaps = (state.diagnosticGaps || []).filter(sid => PY_SKILLS_BY_ID[sid] && getSkillMP(sid) < 100);
  const nextSk = openGaps.length > 0
    ? PY_SKILLS_BY_ID[openGaps[0]]
    : (getFirstUnmasteredSkillInEchelon(e1.pct < 100 ? 1 : (e2.pct < 100 ? 2 : (e3.pct < 100 ? 3 : 4)), o.trackKey));

  const cardsHTML = echelons.map(ep => {
    const meta = getEchelonMeta(ep.tier);
    return `
      <div class="echelon-card">
        <div>
          <div class="echelon-card__header">
            <span class="echelon-badge echelon-badge--t${ep.tier}">${meta.label}</span>
            <span class="echelon-pct-chip">${ep.pct}%</span>
          </div>
          <div class="meta" style="font-size:.76rem;line-height:1.38;margin-bottom:6px;">${meta.desc}</div>
        </div>
        <div>
          <div class="mp-progress-track" style="height:7px;margin:4px 0;"><div class="mp-progress-fill" style="width:${ep.pct}%;"></div></div>
          <div style="display:flex;justify-content:space-between;align-items:center;font-size:.75rem;margin-top:4px;">
            <span class="meta">${ep.curMp} / ${ep.maxMp} MP (${ep.unitsCount} юнитов)</span>
            <button class="link-quiet" style="font-size:.75rem;font-weight:600;" data-open-echelon-next="${ep.tier}">Изучать →</button>
          </div>
        </div>
      </div>`;
  }).join('');

  const gapsBanner = `
    <div style="margin-top:12px;padding:10px 14px;border-radius:12px;background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.22);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
        <span class="badge" style="background:rgba(16,185,129,0.18);border:1px solid rgba(16,185,129,0.35);color:var(--moss);padding:2px 8px;border-radius:6px;font-size:.72rem;font-weight:700;">🎯 Следующий рубеж</span>
        <span style="font-size:.84rem;color:var(--ink);">Следующий рубеж: завершите Unit 1.1 для перехода к скринингу${openGaps.length > 0 ? ` · Фокус: <b>${openGaps.slice(0,3).join(', ')}</b>` : ''}</span>
      </div>
      <a href="#/path" class="link-quiet" style="font-size:.8rem;font-weight:600;">К тропе обучения ➔</a>
    </div>`;

  return `
    <div class="priority-roadmap-card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
        <div>
          <div class="topic-badge" style="margin-bottom:4px;">🎯 Приоритетная архитектура подготовки к собеседованию (4 эшелона)</div>
          <h3 style="margin:0;">Сначала база для 90% собеседований — затем профильный стек и продакшен</h3>
        </div>
        <div class="stack-branch-bar">
          <span class="meta" style="font-weight:600;font-size:.8rem;">Ветка стека:</span>
          <button class="btn ${branch==='fastapi'?'btn-primary':'btn-ghost'}" style="padding:6px 11px;font-size:.78rem;" data-stack-branch="fastapi">⚡ FastAPI + SQLAlchemy</button>
          <button class="btn ${branch==='django'?'btn-primary':'btn-ghost'}" style="padding:6px 11px;font-size:.78rem;" data-stack-branch="django">🎸 Django + DRF</button>
          <button class="btn ${branch==='both'?'btn-primary':'btn-ghost'}" style="padding:6px 11px;font-size:.78rem;" data-stack-branch="both">🔥 Оба стека</button>
          ${nextSk ? `<button class="btn btn-clay" style="padding:6px 12px;font-size:.78rem;" data-priority-next-skill="${nextSk.id}">🚀 Следующий приоритетный шаг: ${nextSk.id}</button>` : ''}
        </div>
      </div>
      <div class="echelon-grid">${cardsHTML}</div>
      ${gapsBanner}
    </div>`;
}
window.buildPriorityRoadmapWidgetHTML = buildPriorityRoadmapWidgetHTML;

function viewPythonMastery(trackKey){
  ensureExtendedState();
  const tr = MASTERY_TRACKS[trackKey] || MASTERY_TRACKS.python;
  if(lastTrackKeyForTierFilter && lastTrackKeyForTierFilter !== tr.key){
    trackTierFilter = 'all';
  }
  lastTrackKeyForTierFilter = tr.key;
  const trackSkills = tr.skills;
  const trackData = tr.data;
  const curMp = totalTrackMP(tr.key);
  const maxMp = maxTrackMP(tr.key);
  const pct = Math.round(curMp / (maxMp || 1) * 100);
  const masteredSkills = trackSkills.filter(s => getSkillMP(s.id) >= 100).length;
  const proficientSkills = trackSkills.filter(s => getSkillMP(s.id) === 80).length;
  const familiarSkills = trackSkills.filter(s => getSkillMP(s.id) === 50).length;
  const solvedMap = getIdeSolvedMap();
  const totalSolvedIde = countSolvedIdeTasks(solvedMap);
  const sortMode = state.unitSortMode || 'priority';
  const branch = state.stackBranch || 'fastapi';

  // Build visual Khan Academy Mastery Matrix grid for the active track
  const matrixSquares = trackSkills.map(s => {
    const mp = getSkillMP(s.id);
    const effTier = getEffectiveSkillTier(s.id);
    return `<button class="m-sq m-sq--${mp}" data-py-open-skill="${s.id}" title="[Эшелон ${effTier}] ${s.id} ${s.title} — ${mpLabel(mp)}">${mp===100?'👑':(mp||'')}</button>`;
  }).join('');

  let visibleUnits = (tr.key === 'backend' && backendPartFilter !== 'all')
    ? trackData.units.filter(u => backendPartFilter === 'prod' ? ['3.5','3.6','3.7','3.8'].includes(u.id) : u.id === backendPartFilter)
    : trackData.units.slice();

  let emptyTierFallbackNotice = '';
  if(trackTierFilter !== 'all'){
    const tfNum = parseInt(trackTierFilter, 10);
    const byTier = visibleUnits.filter(u => getEffectiveUnitTier(u.id) === tfNum);
    if(byTier.length > 0){
      visibleUnits = byTier;
    } else {
      emptyTierFallbackNotice = `<div class="notice" style="margin-top:10px;padding:8px 12px;font-size:.82rem;">В этом модуле при выбранной ветке стека нет юнитов Эшелона ${tfNum} — показаны все юниты модуля.</div>`;
    }
  }

  if(sortMode === 'priority'){
    visibleUnits = visibleUnits.slice().sort((a, b) => {
      const ta = getEffectiveUnitTier(a.id);
      const tb = getEffectiveUnitTier(b.id);
      if(ta !== tb) return ta - tb;
      return String(a.id).localeCompare(String(b.id), undefined, {numeric: true});
    });
  }

  const priorityBarHTML = `
    <div class="panel" style="padding:14px 16px;margin-bottom:16px;">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
        <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">
          <span class="meta" style="font-weight:600;">Порядок изучения:</span>
          <button class="btn ${sortMode==='priority'?'btn-primary':'btn-ghost'}" style="padding:6px 12px;font-size:.8rem;" data-unit-sort="priority">🎯 По приоритету собеседования (Эшелон 1 → 4)</button>
          <button class="btn ${sortMode==='number'?'btn-primary':'btn-ghost'}" style="padding:6px 12px;font-size:.8rem;" data-unit-sort="number">📚 По порядку номеров (${tr.courseUnitRange})</button>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">
          <span class="meta" style="font-weight:600;">Фильтр эшелона:</span>
          <button class="btn ${trackTierFilter==='all'?'btn-primary':'btn-ghost'}" style="padding:5px 10px;font-size:.78rem;" data-track-tier-filter="all">Все</button>
          <button class="btn ${trackTierFilter==='1'?'btn-primary':'btn-ghost'}" style="padding:5px 10px;font-size:.78rem;" data-track-tier-filter="1">🚨 Эшелон 1</button>
          <button class="btn ${trackTierFilter==='2'?'btn-primary':'btn-ghost'}" style="padding:5px 10px;font-size:.78rem;" data-track-tier-filter="2">🔥 Эшелон 2</button>
          <button class="btn ${trackTierFilter==='3'?'btn-primary':'btn-ghost'}" style="padding:5px 10px;font-size:.78rem;" data-track-tier-filter="3">⚡ Эшелон 3</button>
          <button class="btn ${trackTierFilter==='4'?'btn-primary':'btn-ghost'}" style="padding:5px 10px;font-size:.78rem;" data-track-tier-filter="4">👑 Эшелон 4</button>
        </div>
      </div>
      ${['backend','databases','python'].includes(tr.key) ? `
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-top:10px;padding-top:10px;border-top:1px solid var(--line-soft);">
        <span class="meta">Активная ветка стека определяет, какие фреймворки входят в <b>🔥 Эшелон 2</b>, а какие уходят в резерв <b>👑 Эшелон 4</b>:</span>
        <div class="stack-branch-bar">
          <button class="btn ${branch==='fastapi'?'btn-primary':'btn-ghost'}" style="padding:5px 10px;font-size:.78rem;" data-stack-branch="fastapi">⚡ FastAPI + SQLAlchemy</button>
          <button class="btn ${branch==='django'?'btn-primary':'btn-ghost'}" style="padding:5px 10px;font-size:.78rem;" data-stack-branch="django">🎸 Django + DRF</button>
          <button class="btn ${branch==='both'?'btn-primary':'btn-ghost'}" style="padding:5px 10px;font-size:.78rem;" data-stack-branch="both">🔥 Оба стека</button>
        </div>
      </div>` : ''}
      ${emptyTierFallbackNotice}
    </div>`;

  const backendPartsBarHTML = tr.key === 'backend' ? `
    <div class="panel" style="padding:14px 16px;margin-bottom:16px;">
      <div class="meta" style="margin-bottom:8px;font-weight:600;">Навигация по 8 частям Модуля 03 · ⚙️ Backend (от фреймворков с нуля до продакшен-архитектуры):</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <button class="btn ${backendPartFilter==='all'?'btn-primary':'btn-ghost'}" style="padding:7px 12px;font-size:.82rem;" data-backend-part-filter="all">Все 8 частей (3.1–3.8)</button>
        <button class="btn ${backendPartFilter==='3.1'?'btn-primary':'btn-ghost'}" style="padding:7px 12px;font-size:.82rem;" data-backend-part-filter="3.1">⚡ Часть I: FastAPI и Pydantic v2 (3.1)</button>
        <button class="btn ${backendPartFilter==='3.2'?'btn-primary':'btn-ghost'}" style="padding:7px 12px;font-size:.82rem;" data-backend-part-filter="3.2">🎸 Часть II: Django и ORM (3.2)</button>
        <button class="btn ${backendPartFilter==='3.3'?'btn-primary':'btn-ghost'}" style="padding:7px 12px;font-size:.82rem;" data-backend-part-filter="3.3">🛡️ Часть III: Django REST Framework (3.3)</button>
        <button class="btn ${backendPartFilter==='3.4'?'btn-primary':'btn-ghost'}" style="padding:7px 12px;font-size:.82rem;" data-backend-part-filter="3.4">🌶️ Часть IV: Flask (3.4)</button>
        <button class="btn ${backendPartFilter==='prod'?'btn-primary':'btn-ghost'}" style="padding:7px 12px;font-size:.82rem;" data-backend-part-filter="prod">🏛️ Части V–VIII: Auth, Архитектура и Production (3.5–3.8)</button>
      </div>
    </div>` : '';

  const unitsHTML = visibleUnits.map(u => {
    const uMp = u.skills.reduce((a, s) => a + getSkillMP(s.id), 0);
    const uMax = u.skills.length * 100;
    const uPct = Math.round(uMp / (uMax || 1) * 100);
    const utPassed = state.passedUnitTests.includes(u.id);
    const effTier = getEffectiveUnitTier(u.id);

    const skillsRows = u.skills.map(s => {
      const mp = getSkillMP(s.id);
      const isGap = (state.diagnosticGaps || []).includes(s.id) && mp < 100;

      return `
        <div class="skill-row">
          <div class="skill-row__left">
            <button class="m-sq m-sq--${mp}" data-py-open-skill="${s.id}" title="${mpLabel(mp)}">${mp===100?'👑':mp}</button>
            <div style="min-width:0;flex:1;">
              <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;min-width:0;">
                <a href="#${tr.routePrefix}/skill/${s.id}" class="skill-row__title" style="font-weight:600;text-decoration:none;font-size:.96rem;">${s.id} · ${s.title}</a>
                ${isGap ? `<span class="echelon-badge echelon-badge--gap">🎯 Пробел диагностики</span>` : ''}
              </div>
            </div>
          </div>
          <div class="skill-row__badges">
            <a href="#${tr.routePrefix}/skill/${s.id}" class="btn btn-ghost skill-row__open-btn" style="padding:6px 12px;font-size:.8rem;">Открыть →</a>
          </div>
        </div>`;
    }).join('');

    return `
      <div class="unit-card" data-unit-card="${u.id}" data-unit-tier="${effTier}">
        <div class="unit-card__head">
          <div style="min-width:0;flex:1;">
            <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:4px;">
              <span class="topic-badge" style="margin:0;">Юнит ${u.id} · ${uMp}/${uMax} MP · ${uPct}%</span>
            </div>
            <h2>${u.title}</h2>
          </div>
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;flex:none;">
            <a href="#${tr.routePrefix}/unittest/${u.id}" class="btn ${utPassed?'btn-primary':'btn-clay unit-test-btn'}" style="padding:7px 11px;font-size:.78rem;white-space:nowrap;">
              ${utPassed ? '👑 Unit Test пройден' : '⚡ Unit Test ' + u.id}
            </a>
          </div>
        </div>
        <div class="mp-progress-track" style="margin-bottom:10px;"><div class="mp-progress-fill" style="width:${uPct}%;"></div></div>
        ${skillsRows}
      </div>`;
  });

  const firstUnitHTML = unitsHTML.length > 0 ? unitsHTML[0] : '';
  const restUnitsHTML = unitsHTML.length > 1 ? `
    <details class="cocoon-details">
      <summary><span>📚 Остальные юниты (${unitsHTML.length - 1} из ${unitsHTML.length}) · раскрыть ▾</span></summary>
      ${unitsHTML.slice(1).join('')}
    </details>` : '';

  const nextTrackSk = getFirstUnmasteredSkillInEchelon(null, tr.key) || trackSkills[0];
  const nextTrackKId = (nextTrackSk && nextTrackSk.kIds && nextTrackSk.kIds.find(k => !state.readNotes.includes(k))) || (nextTrackSk && nextTrackSk.kIds && nextTrackSk.kIds[0]) || '';

  return `
    <div class="container">
      <div class="cd-box" style="margin-bottom:10px;">
        <div class="cd-top">
          <span class="cd-title">${tr.shortTitle || tr.title}<span class="sr-only"> ${tr.title}</span></span>
          <span class="cd-count">${curMp} / ${maxMp} MP (${pct}%)</span>
        </div>
        <div class="cd-bar cd-bar-track"><div class="cd-fill cd-bar-fill" style="width:${Math.max(6, pct)}%;"></div></div>
      </div>

      <div class="cocoon-focus-card" style="margin-bottom:10px;">
        <div class="cocoon-focus-eyebrow">✨ Фокус модуля · ${tr.courseUnitRange}<span class="sr-only"> ${tr.badge}</span></div>
        <div class="cocoon-focus-title">${nextTrackSk ? (nextTrackSk.id + ' · ' + nextTrackSk.title) : tr.title}</div>
        <div class="cocoon-focus-desc">Следующий шаг: конспект <b>${nextTrackKId}</b> (1. Конспект → 2. Карточки Ф-xxx → 3. Практика в IDE) с разбором Junior vs Senior.</div>
        <div style="display:flex;flex-direction:column;gap:8px;">
          <button class="btn-glass-emerald btn-sprint-cta" data-quick-microstep="${tr.key}">⚡ Быстрый микро-шаг (2 мин) ➔</button>
          <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
            <a href="#${tr.routePrefix}/unittest/course" class="btn-glass-ruby" style="flex:1;padding:8px 12px;font-size:.8rem;">🏆 Вызов (${tr.courseUnitRange})</a>
            <a href="#${tr.routePrefix}/boss" class="btn ${(state.passedBosses||[]).includes(tr.key)?'btn-primary':'btn-ghost'}" style="padding:8px 12px;font-size:.8rem;">👑 ${(state.passedBosses||[]).includes(tr.key)?'Босс взят':'Босс модуля'}</a>
            <a href="#/docs" class="btn btn-ghost" style="padding:8px 12px;font-size:.8rem;">📚 Справочник Python</a>
          </div>
        </div>
      </div>

      <details class="cocoon-details cocoon-details--compact">
        <summary><span>🗺️ Матрица навыков (${trackSkills.length}) и эшелоны</span><span class="meta">${masteredSkills}/${trackSkills.length} 👑 ▾</span></summary>
        <div class="mastery-banner">
          <div style="flex:1;min-width:260px;">
            <div class="meta">Система Мастерства (4 ступени: Не начато → Знакомство → Практика → Мастерство)<span class="sr-only"> Khan Academy Mastery System</span></div>
            <div style="display:flex;align-items:baseline;gap:12px;margin-top:2px;">
              <span style="font-family:var(--font-d);font-size:2.2rem;font-weight:700;color:var(--moss-deep);">${curMp}</span>
              <span class="meta">из ${maxMp} MP (${pct}%) · Решено задач IDE: <b>${totalSolvedIde}/401</b></span>
            </div>
            <div class="mp-progress-track"><div class="mp-progress-fill" style="width:${pct}%;"></div></div>
            <div class="matrix-legend">
              <span><i class="m-sq m-sq--100" style="width:14px;height:14px;font-size:.55rem;">👑</i> Мастерство 100 MP (${masteredSkills})</span>
              <span><i class="m-sq m-sq--80" style="width:14px;height:14px;"></i> Практика 80 MP (${proficientSkills})</span>
              <span><i class="m-sq m-sq--50" style="width:14px;height:14px;"></i> Знакомство 50 MP (${familiarSkills})</span>
              <span><i class="m-sq m-sq--0" style="width:14px;height:14px;"></i> Не начато 0 MP (${trackSkills.length - masteredSkills - proficientSkills - familiarSkills})</span>
            </div>
          </div>
          <div>
            <div class="meta" style="margin-bottom:6px;font-weight:600;">Карта ${trackSkills.length} навыков (нажми на клетку):</div>
            <div style="display:grid;grid-template-columns:repeat(${tr.cols || 7}, 26px);gap:5px;">
              ${matrixSquares}
            </div>
          </div>
        </div>
        ${priorityBarHTML}
        ${backendPartsBarHTML}
      </details>

      ${firstUnitHTML}
      ${restUnitsHTML}
    </div>`;
}
function viewWebMastery(){ return viewPythonMastery('web'); }
function viewBackendMastery(){ return viewPythonMastery('backend'); }

// Helper to format Big-O math formulas and inline code tokens in quiz questions, options, explanations, and flashcards
function formatRichInlineText(rawStr){
  let s = String(rawStr || '');
  if(!s) return '';
  // Clean awkward spaces around existing <code> tags
  s = s.replace(/<\/code>\s+([,.;:?!])/g, '</code>$1');
  s = s.replace(/\(\s+<code>/g, '(<code>').replace(/<\/code>\s+\)/g, '</code>)');
  // If string has no HTML tags yet, escape basic HTML entities first
  if(!/<(code|strong|b|em|i|span|pre|br|p|div|ul|ol|li)\b/i.test(s)){
    s = escapeHtmlStr(s);
    s = s.replace(/\b(d\[key\]|d\.get\(key\)|\.get\(\)|\.append\(\)|x in seen|x in collection|range\(\d+\)|Dog\(\)\.speak\(\)|raise ValueError\([^)]*\)|DELETE FROM users;|PRIMARY KEY|FOREIGN KEY|GROUP BY|ORDER BY|HAVING|WHERE|JOIN|UNION|COMMIT|ROLLBACK|git commit|git push|git clone|git init|Content-Type|application\/json|@property|@staticmethod|@cached_property|@lru_cache|KeyError|IndexError|TypeError|SyntaxError|UnboundLocalError|RecursionError|__defaults__|sys\.getrecursionlimit\(\))\b/g, '<code>$1</code>');
  }
  // Guaranteed markdown backticks conversion to <code> tags across all cards and notes
  // Поддержка fenced code blocks в карточках
  s = s.replace(/```(?:python)?\s*([\s\S]*?)```/g, function(_, codeInner){
    const highlighted = (typeof highlightPythonTokens === 'function') ? highlightPythonTokens(escapeHtmlStr(codeInner.trim())) : escapeHtmlStr(codeInner.trim());
    return `<pre class="quiz-question-code fc-code-block" style="margin:10px 0;text-align:left;"><code>${highlighted}</code></pre>`;
  });
  s = s.replace(/`([^`\n]+)`/g, '<code>$1</code>');
  // Format Big-O notation and mathematical styling
  s = s.replace(/\$([^\$\n]+)\$/g, '<span class="math-formula">$1</span>');
  s = s.replace(/\bO\((?:n\^2|n²)\)/g, '<span class="math-formula">O(n²)</span>');
  s = s.replace(/\bO\(1\)/g, '<span class="math-formula">O(1)</span>');
  s = s.replace(/\bO\(n\)/g, '<span class="math-formula">O(n)</span>');
  s = s.replace(/\bO\(log\s*n\)/g, '<span class="math-formula">O(log n)</span>');
  s = s.replace(/\bO\(n\s*log\s*n\)/g, '<span class="math-formula">O(n log n)</span>');
  s = s.replace(/\bO\(V\s*\+\s*E\)/g, '<span class="math-formula">O(V + E)</span>');
  s = s.replace(/\bO\(min\([^)]+\)\)/gi, '<span class="math-formula">O(min(n, m))</span>');
  s = s.replace(/\bO\(max\([^)]+\)\)/gi, '<span class="math-formula">O(max(n, m))</span>');
  s = s.replace(/\bO\(len\([^)]+\)\)/gi, function(m){ return '<span class="math-formula">' + m + '</span>'; });
  s = s.replace(/\bO\(n\s*\+\s*m\)/gi, '<span class="math-formula">O(n + m)</span>');
  s = s.replace(/<span class="math-formula"><span class="math-formula">([^<]+)<\/span><\/span>/g, '<span class="math-formula">$1</span>');
  // Normalize LaTeX backslashes inside math formulas (e.g. \min -> min, \text{len} -> len)
  s = s.replace(/<span class="math-formula">([^<]*)<\/span>/g, function(_, m){
    return '<span class="math-formula">' + m.replace(/\\text\{([^}]*)\}/g, '$1').replace(/\\(?:min|max|log|cdot)\b/g, function(fn){ return fn.slice(1); }).replace(/\\/g, '').trim() + '</span>';
  });
  return s;
}
window.formatRichInlineText = formatRichInlineText;

function formatQuizQuestionPromptHTML(rawText){
  const s = String(rawText || '').trim();
  const nlIdx = s.indexOf('\n');
  if(nlIdx !== -1){
    const lead = s.slice(0, nlIdx).trim();
    const codePart = s.slice(nlIdx + 1).trim();
    const highlighted = (typeof highlightPythonTokens === 'function') ? highlightPythonTokens(escapeHtmlStr(codePart)) : escapeHtmlStr(codePart);
    return `<div>${formatRichInlineText(lead)}</div><pre class="quiz-question-code"><code>${highlighted}</code></pre>`;
  }
  const colonCodeMatch = s.match(/^(Что выведет(?: код)?[:?])\s*(.+)$/i);
  if(colonCodeMatch){
    const codePart = colonCodeMatch[2].replace(/;\s*/g, '\n').replace(/\?$/, '').trim();
    const highlighted = (typeof highlightPythonTokens === 'function') ? highlightPythonTokens(escapeHtmlStr(codePart)) : escapeHtmlStr(codePart);
    return `<div>${escapeHtmlStr(colonCodeMatch[1])}</div><pre class="quiz-question-code"><code>${highlighted}</code></pre>`;
  }
  return formatRichInlineText(s);
}
window.formatQuizQuestionPromptHTML = formatQuizQuestionPromptHTML;

// Lightweight client-side Python syntax highlighter (keywords, strings, comments, numbers, built-in calls)
function highlightPythonTokens(codeInner){
  if(codeInner.indexOf('tok-') !== -1) return codeInner;
  let out = codeInner;
  // 1. Comments
  out = out.replace(/(#.*?)(?=\n|$)/g, '<span class="tok-com">$1</span>');
  // 2. Strings
  out = out.replace(/(['"][^'"\n]*['"])/g, '<span class="tok-str">$1</span>');
  // 3. Keywords
  out = out.replace(/\b(def|return|for|in|if|else|elif|while|class|import|from|as|try|except|finally|with|lambda|yield|raise|pass|break|continue|and|or|not|is|True|False|None)\b/g, '<span class="tok-kw">$1</span>');
  // 4. Builtins & Methods
  out = out.replace(/\b(print|len|range|list|dict|set|tuple|int|str|float|bool|min|max|sum|sorted|enumerate|zip|map|filter|all|any|open|isinstance|type|super|append|extend|pop|remove|add|update|get|keys|values|items)\b(?=\s*\()/g, '<span class="tok-builtin">$1</span>');
  // 5. Numbers
  out = out.replace(/\b(\d+)\b(?![^<]*>)/g, '<span class="tok-num">$1</span>');
  return out;
}

// Helper to decorate <pre><code> blocks with inline "▶ Запустить в Python" button (skips already-decorated RemNote K-note blocks)
function decorateCodeBlocksWithRunBtn(htmlStr){
  let s = String(htmlStr || '');
  s = s.replace(/<pre><code>([\s\S]*?)<\/code><\/pre>/g, function(full, codeInner){
    const looksLikePython = !(/^(SELECT|INSERT|UPDATE|DELETE|CREATE|FROM|docker|git|GET|POST|PATCH|PUT|paths:)/i.test(codeInner.trim()));
    const highlighted = (looksLikePython && typeof highlightPythonTokens === 'function') ? highlightPythonTokens(codeInner) : codeInner;
    return `<pre><code>${highlighted}</code></pre>`;
  });
  if(s.indexOf('snippet-wrap') !== -1 || s.indexOf('code-snippet-wrap') !== -1) return s;
  return s.replace(/<pre><code>([\s\S]*?)<\/code><\/pre>/g, function(full, codeInner){
    const looksLikePython = !(/^(SELECT|INSERT|UPDATE|DELETE|CREATE|FROM|docker|git|GET|POST|PATCH|PUT|paths:)/i.test(codeInner.trim()));
    const highlighted = looksLikePython ? highlightPythonTokens(codeInner) : codeInner;
    if(!looksLikePython) return `<pre><code>${highlighted}</code></pre>`;
    return `<div class="code-snippet-wrap"><button type="button" class="run-inline-btn" data-run-inline>▶ Запустить код</button><pre><code>${highlighted}</code></pre></div>`;
  });
}

// Split a micro-step's HTML into small progressive chunks (paragraphs, tables, code blocks, Junior vs Senior callouts)
function splitStepHtmlIntoChunks(htmlStr){
  let cleanIn = String(htmlStr || '').trim();
  if(/^<div\s+class=["']lesson-theory["'][^>]*>/i.test(cleanIn) && /<\/div>\s*$/i.test(cleanIn)){
    if(/^<div\s+class=["']lesson-theory["'][^>]*>/i.test(cleanIn) && /<\/div>\s*$/i.test(cleanIn)){
    if(/^<div\s+class=["']lesson-theory["'][^>]*>/i.test(cleanIn) && /<\/div>\s*$/i.test(cleanIn)){
    if(/^<div\s+class=["']lesson-theory["'][^>]*>/i.test(cleanIn) && /<\/div>\s*$/i.test(cleanIn)){
    cleanIn = cleanIn.replace(/^<div\s+class=["']lesson-theory["'][^>]*>/i, '').replace(/<\/div>\s*$/i, '').trim();
  }
  }
  }
  }
  const decorated = (typeof decorateCodeBlocksWithRunBtn === 'function') ? decorateCodeBlocksWithRunBtn(cleanIn) : cleanIn;
  const s = String(decorated || '').trim();
  if(!s) return [''];
  const rawBlocks = [];
  const tagRe = /<\/?(div|table|ul|ol|pre|blockquote|p|h[1-6])\b[^>]*>/gi;
  let depth = 0;
  let rootTag = '';
  let blockStart = 0;
  let lastEnd = 0;
  let m;
  while((m = tagRe.exec(s)) !== null){
    const fullTag = m[0];
    const tagName = m[1].toLowerCase();
    const isClosing = fullTag.charAt(1) === '/';
    const isSelfClosing = fullTag.charAt(fullTag.length - 2) === '/';
    if(depth === 0){
      if(!isClosing && !isSelfClosing){
        if(m.index > lastEnd){
          const lead = s.slice(lastEnd, m.index).trim();
          if(lead) rawBlocks.push(lead);
        }
        rootTag = tagName;
        blockStart = m.index;
        depth = 1;
      }
    } else {
      if(tagName === rootTag){
        if(isClosing){
          depth--;
          if(depth === 0){
            const blk = s.slice(blockStart, m.index + fullTag.length).trim();
            if(blk) rawBlocks.push(blk);
            lastEnd = m.index + fullTag.length;
            rootTag = '';
          }
        } else if(!isSelfClosing){
          depth++;
        }
      }
    }
  }
  if(lastEnd < s.length){
    const tail = s.slice(lastEnd).trim();
    if(tail) rawBlocks.push(tail);
  }

  function isHeadingBlock(b){
    if(/^<h[1-6]\b/i.test(b)) return true;
    const plain = b.replace(/<[^>]+>/g, '').trim();
    if(/^<p\b/i.test(b) && /^<strong>[\s\S]*<\/strong>$/i.test(b.replace(/^<p\b[^>]*>/i, '').replace(/<\/p>$/i, '').trim())){
      if(plain.length < 120 && !plain.endsWith('.')) return true;
    }
    return false;
  }

  function isLeadInBlock(b, nextB){
    if(!/^<p\b/i.test(b)) return false;
    const plain = b.replace(/<[^>]+>/g, '').trim();
    if(/[:—–]\s*$/i.test(plain) && plain.length < 400 && nextB) return true;
    return false;
  }

  const merged = [];
  let pending = '';
  for(let i = 0; i < rawBlocks.length; i++){
    const b = rawBlocks[i];
    const nextB = (i + 1 < rawBlocks.length) ? rawBlocks[i + 1] : null;
    const isH = isHeadingBlock(b);
    const isLeadIn = isLeadInBlock(b, nextB);
    if(isH || isLeadIn){
      pending = pending ? (pending + '\n' + b) : b;
    } else if(pending){
      merged.push(pending + '\n' + b);
      pending = '';
    } else {
      merged.push(b);
    }
  }
  if(pending){
    if(merged.length > 0) merged[merged.length - 1] += '\n' + pending;
    else merged.push(pending);
  }

  const finalChunks = [];
  for(let i = 0; i < merged.length; i++){
    const c = merged[i];
    const plainLen = c.replace(/<[^>]+>/g, '').trim().length;
    if(i === 1 && finalChunks.length === 1 && finalChunks[0].replace(/<[^>]+>/g, '').trim().length < 350 && isHeadingBlock(c)){
      finalChunks[0] += '\n' + c;
      continue;
    }
    const isVisualContrastCard = /class=["'][^"']*(?:theory-contrast-card|visual-contrast|contrast-grid)[^"']*["']/i.test(c);
    if(finalChunks.length > 0 && isVisualContrastCard && finalChunks[finalChunks.length - 1].replace(/<[^>]+>/g, '').trim().length < 450){
      finalChunks[finalChunks.length - 1] += '\n' + c;
      continue;
    }
    const isCodeSnippet = /class=["'][^"']*(?:snippet-wrap|code-snippet-wrap)[^"']*["']/i.test(c) || /^<pre\b/i.test(c);
    if(finalChunks.length > 0 && isCodeSnippet && (finalChunks.length === 1 || finalChunks[finalChunks.length - 1].replace(/<[^>]+>/g, '').trim().length < 900)){
      finalChunks[finalChunks.length - 1] += '\n' + c;
      continue;
    }
    if(finalChunks.length > 0 && plainLen < 75 && !isHeadingBlock(c) && !isCodeSnippet){
      finalChunks[finalChunks.length - 1] += '\n' + c;
    } else {
      finalChunks.push(c);
    }
  }
  return finalChunks.length > 0 ? finalChunks : [s];
}
window.splitStepHtmlIntoChunks = splitStepHtmlIntoChunks;

function pluralRuTopics(n){
  const abs = Math.abs(n || 0) % 100;
  const n1 = abs % 10;
  if(abs > 10 && abs < 20) return 'тем';
  if(n1 > 1 && n1 < 5) return 'темы';
  if(n1 === 1) return 'тема';
  return 'тем';
}

function buildSprintFinishCelebrationHTML(cel){
  if(!cel) return '';
  const isAlreadyRead = Boolean(cel.wasAlreadyRead || (state.readNotes && state.readNotes.includes(cel.kid)));
  const xpBadge = isAlreadyRead ? '' : ' · +15 XP';
  const noteObj = (typeof ALL_NOTES_COMBINED !== 'undefined' && ALL_NOTES_COMBINED[cel.kid]) || {};
  const rawTitle = (noteObj && noteObj.title) || cel.kid || 'Тема';
  const cleanTitle = rawTitle.replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();

  let nextKid = null;
  try {
    const sk = (typeof PY_SKILLS_BY_ID !== 'undefined' && pySkillViewState && pySkillViewState.sid) ? PY_SKILLS_BY_ID[pySkillViewState.sid] : null;
    if(sk && sk.kIds){
      const idx = sk.kIds.indexOf(cel.kid);
      if(idx >= 0 && idx + 1 < sk.kIds.length){
        nextKid = sk.kIds[idx + 1];
      }
    }
  } catch(e){}

  const nextBtnHTML = nextKid ? `
    <button type="button" class="btn-glass-emerald btn-lg" style="width:100%;max-width:380px;justify-content:center;margin-bottom:8px;" data-py-select-k="${nextKid}" data-dismiss-celebration>📖 Продолжить чтение конспектов ➔</button>
    <button type="button" class="btn btn-ghost" style="width:100%;max-width:380px;justify-content:center;" data-py-tab="cards" data-dismiss-celebration>🃏 Перейти к карточкам</button>
  ` : `
    <button type="button" class="btn-glass-emerald btn-lg" style="width:100%;max-width:380px;justify-content:center;" data-py-tab="cards" data-dismiss-celebration>🃏 Закрепить на карточках ➔</button>
  `;

  return `
    <div class="celebration-modal-overlay" style="position:fixed;inset:0;background:rgba(10,14,20,0.72);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);z-index:9999;display:flex;align-items:center;justify-content:center;padding:16px;">
      <div class="sprint-finish-card" style="max-width:500px;width:100%;margin:0 auto;text-align:center;box-shadow:0 24px 60px rgba(0,0,0,0.65);border:1.5px solid rgba(52,211,153,0.5);">
        <div class="sprint-finish-orb" style="font-size:2.2rem;margin-bottom:6px;">✨</div>
        <div class="cocoon-focus-eyebrow" style="margin-bottom:6px;">Конспект закреплён${xpBadge}</div>
        <h2 style="font-size:1.35rem;margin-bottom:8px;">«${escapeHtmlStr(cleanTitle)}» ${isAlreadyRead ? 'повторён' : 'усвоен'}!</h2>
        <p class="meta" style="max-width:440px;margin:0 auto 14px;font-size:.9rem;">Отличный темп! Закрепи изученное или переходи к следующей теме:</p>
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;margin-top:14px;">
          ${nextBtnHTML}
        </div>
      </div>
    </div>`;
}

function getStepDefaultScratchpadCode(activeK, sid, curStep, stepIdx){
  if(curStep && curStep.html){
    const m = curStep.html.match(/<pre><code>([\s\S]*?)<\/code><\/pre>/i);
    if(m && m[1]){
      const raw = m[1].replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&').replace(/&quot;/g, '"').trim();
      const lines = raw.split('\n');
      if(lines.length >= 1 && lines.length <= 15 && !/^(SELECT|INSERT|docker|git)/i.test(lines[0])){
        return raw;
      }
    }
  }
  if(/1\.1\.[1-4]|К-00[1-4]/.test(String(sid) + ' ' + String(activeK))){
    if(stepIdx === 0 || stepIdx === 1){
      return `# Быстрый эксперимент со списками (Шаг ${stepIdx+1})\nitems = [1, 2, 3, 4, 5]\nitems.append(6)\nprint("Список:", items, "Срез:", items[1:4])`;
    } else if(stepIdx === 2){
      return `# Быстрый эксперимент со словарем (Шаг 3)\nuser = {"id": 42, "role": "admin"}\nprint("Ключи:", list(user.keys()), "Значения:", list(user.values()))`;
    } else if(stepIdx === 3){
      return `# Быстрый эксперимент с множеством (Шаг 4)\na = {1, 2, 3}\nb = {3, 4, 5}\nprint("Пересечение:", a & b, "Объединение:", a | b)`;
    }
  }
  const cleanNoteTitle = (ALL_NOTES_COMBINED[activeK] && ALL_NOTES_COMBINED[activeK].title) ? ALL_NOTES_COMBINED[activeK].title.replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim() : '';
  const topicLabel = cleanNoteTitle ? `«${cleanNoteTitle}»` : 'теории';
  return `# Проверь идею из конспекта ${topicLabel} (Шаг ${stepIdx+1})\nitems = [10, 20, 30]\nprint("Длина:", len(items), "Первый элемент:", items[0])`;
}

function buildTaskSpecDetails(tObj){
  if(!tObj) return { ioCard: '', quickTokens: [] };
  let inputVal = '';
  let outputVal = '';
  const desc = String(tObj.desc || '');
  const sol = String(tObj.solution || '');

  const printCommentMatch = sol.match(/print\([^)]+\)\s*#\s*([^\n]+)/);
  const commentMatch = sol.match(/#\s*(?:Результат|Вывод|Output|Реверс|Пример|Expected|Ожидание)?\s*[:=-]?\s*([\[\{"'\d].*)$/m);
  if(printCommentMatch && printCommentMatch[1]){
    outputVal = printCommentMatch[1].trim();
  } else if(commentMatch && commentMatch[1]){
    outputVal = commentMatch[1].trim();
  }

  const inputAssignMatch = sol.match(/(?:original|numbers|nums|items|data|lst|s|text|a|b|val)\s*=\s*([\[\{"'\d].*?)(?:\n|$)/);
  if(inputAssignMatch && inputAssignMatch[1]){
    inputVal = inputAssignMatch[1].trim().replace(/#.*$/, '').trim();
  }

  if(!inputVal && !outputVal){
    if(/реверс|срез|\[::-1\]/i.test(tObj.title + ' ' + desc)){
      inputVal = '[1, 2, 3, 4, 5]';
      outputVal = '[5, 4, 3, 2, 1]';
    } else if(/join|inner join/i.test(tObj.title)){
      inputVal = 'users JOIN orders';
      outputVal = 'id, name, order_id';
    }
  }

  let ioCard = '';
  if(inputVal || outputVal){
    let sliceVisual = '';
    if(/реверс|срез|\[::-1\]|reverse/i.test(tObj.title + ' ' + desc) || (sol && sol.includes('[::-1]'))){
      sliceVisual = `
        <div class="slice-anatomy-widget">
          <div class="slice-anatomy-header">
            <span>📐 Анатомия среза [start:stop:step]</span>
            <span class="slice-step-badge">step = -1 (реверс)</span>
          </div>
          <div class="slice-grid">
            <div class="slice-col"><span class="slice-pos-idx">0</span><span class="slice-cell">1</span><span class="slice-neg-idx">-5</span></div>
            <div class="slice-col"><span class="slice-pos-idx">1</span><span class="slice-cell">2</span><span class="slice-neg-idx">-4</span></div>
            <div class="slice-col"><span class="slice-pos-idx">2</span><span class="slice-cell">3</span><span class="slice-neg-idx">-3</span></div>
            <div class="slice-col"><span class="slice-pos-idx">3</span><span class="slice-cell">4</span><span class="slice-neg-idx">-2</span></div>
            <div class="slice-col"><span class="slice-pos-idx">4</span><span class="slice-cell">5</span><span class="slice-neg-idx">-1</span></div>
          </div>
          <div class="slice-flow-cue">⟵ Обход справа налево от конца списка: original[::-1]</div>
        </div>`;
    }

    if(inputVal && outputVal){
      ioCard = `
        <div class="dataflow-card">
          <div class="dataflow-header">
            <span>⚡ Поток данных (I/O Flow)</span>
            <span style="font-family:var(--font-mono, monospace);font-size:0.75rem;color:#93c5fd;">step: -1</span>
          </div>
          <div class="dataflow-stream">
            <div class="df-box">
              <span class="df-label">Вход (original)</span>
              <span class="df-val input-val">${escapeHtmlStr(inputVal)}</span>
            </div>
            <div class="df-arrow">➔</div>
            <div class="df-box">
              <span class="df-label">Ожидание (результат)</span>
              <span class="df-val">${escapeHtmlStr(outputVal)}</span>
            </div>
          </div>
        </div>
        ${sliceVisual}`;
    } else {
      ioCard = `
        <div class="dataflow-card">
          <div class="dataflow-header">
            <span>⚡ Контракт задачи</span>
          </div>
          <div class="dataflow-stream">
            <div class="df-box">
              <span class="df-label">${inputVal ? 'Входные данные' : 'Ожидаемый результат'}</span>
              <span class="df-val">${escapeHtmlStr(inputVal || outputVal)}</span>
            </div>
          </div>
        </div>
        ${sliceVisual}`;
    }
  }

  const tokens = [];
  if(sol){
    if(sol.includes('[::-1]')) tokens.push('[::-1]');
    if(sol.includes('original[::-1]')) tokens.push('original[::-1]');
    if(sol.includes('reversed_list')) tokens.push('reversed_list');
    const sliceMatches = sol.match(/\[[^\]]+\]/g);
    if(sliceMatches){
      sliceMatches.forEach(sm => {
        if(sm.length <= 16 && !sm.includes(',') && !tokens.includes(sm)) tokens.push(sm);
      });
    }
    const methodMatches = sol.match(/\.[a-zA-Z_][a-zA-Z0-9_]*\(\)/g);
    if(methodMatches){
      methodMatches.forEach(mm => {
        if(!tokens.includes(mm)) tokens.push(mm);
      });
    }
  }
  if(tokens.length === 0){
    tokens.push('[::-1]', 'original', 'reversed()', 'list()');
  }
  const cleanTokens = Array.from(new Set(tokens)).slice(0, 5);
  return { ioCard, quickTokens: cleanTokens };
}

function viewPythonSkill(sid){
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
  if(chunks.length > 0 && curStep.title && !/^<h[1-6]\b/i.test(String(chunks[0] || '').trim())){
    chunks[0] = `<h4>${curStep.title}</h4>\n` + chunks[0];
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
      <div class="echelon-topbar-actions" style="display:flex;gap:8px;align-items:center;margin-left:14px;flex:none;">
        <div class="sprint-xp-pill" style="display:inline-flex;align-items:center;gap:4px;padding:5px 11px;border-radius:999px;background:rgba(245,158,11,0.14);border:1px solid rgba(245,158,11,0.35);color:#fbbf24;font-size:0.75rem;font-weight:700;white-space:nowrap;letter-spacing:0.01em;" title="Заработано за сутки: ${dayXpVal} XP">⚡ +${dayXpVal} XP<span class="sprint-xp-subtext"> за сутки</span></div>
        <a href="#/docs" class="topbar-help-btn" style="padding:6px 12px;border-radius:10px;" title="Справочник синтаксиса и методов Python"><span class="topbar-help-text">📖 Справка</span></a>
        <button type="button" class="topbar-help-btn" data-toggle-audio data-audio-toggle style="padding:6px 12px;border-radius:10px;cursor:pointer;" title="Слушать аудио / Аудио-компаньон"><span class="topbar-audio-text">🎧 Озвучить</span></button>
        
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
  const cleanUnitTitle = rawUnitTitle.replace(/^Юнит\s+[\d.]+\s*[·•\-:]\s*/i, '').trim() || rawUnitTitle;

  // 1. Конспекты теории текущего навыка
  const noteDots = (sk.kIds || []).map((kId, idx) => {
    const n = ALL_NOTES_COMBINED[kId] || { title: kId };
    const isDone = state.readNotes.includes(kId);
    const isActive = (pySkillViewState.tab === 'theory' && kId === activeK);
    const cleanNoteTitle = (n.title || kId).replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();
    return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="${escapeHtmlStr(cleanNoteTitle)}" data-py-select-k="${kId}" data-py-skill-id="${sk.id}"></span>`;
  }).join('');

  // 2. Флеш-карточки текущего навыка
  const activeF = pySkillViewState.fId || (sk.fIds && sk.fIds[0]);
  const cardDots = (sk.fIds || []).map((fid, idx) => {
    const d = ALL_DECKS_COMBINED[fid] || {};
    const isDone = state.reviewedDecks.includes(fid);
    const isActive = (pySkillViewState.tab === 'cards' && (activeF === fid || (!activeF && idx === 0)));
    const cleanDeckTitle = (d.title || fid).replace(/^Ф-\d+\s*[:·•\-]\s*/i, '').trim();
    return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="${escapeHtmlStr(cleanDeckTitle)}" data-py-select-f="${fid}"></span>`;
  }).join('');

  // 3. Задачи практики кода текущего навыка
  const tIds = (sk.taskIds && sk.taskIds.length) ? sk.taskIds : [20, 19, 39, 255, 258];
  const activeTid = tIds.includes(pySkillViewState.taskId) ? pySkillViewState.taskId : tIds[0];
  const taskDots = tIds.map((tid, idx) => {
    const t = IDE_TASKS_BY_ID[tid] || {};
    const isDone = (solvedMap[tid] === 'solved');
    const isActive = (pySkillViewState.tab === 'code' && (activeTid === tid || (!activeTid && idx === 0)));
    const cleanTaskTitle = t.title || ('Задача #' + tid);
    return `<span class="dot-jewel ${isActive ? 'active' : (isDone ? 'done' : '')}" title="${escapeHtmlStr(cleanTaskTitle)}" data-py-select-task="${tid}"></span>`;
  }).join('');

  // 4. Рубежный зачёт Юнита
  const examActive = (pySkillViewState.tab === 'exam');
  const examDot = `<span class="dot-jewel milestone ${examActive ? 'active' : ''}" title="Рубежный зачёт Юнита ${sk.unitId}" data-py-select-exam="${sk.unitId}"></span>`;

  const dotsNecklaceHTML = `
    <div class="dots-necklace" id="radar-dots-necklace">
      ${noteDots}
      <span class="dots-stage-divider"></span>
      ${cardDots}
      <span class="dots-stage-divider"></span>
      ${taskDots}
      <span class="dots-stage-divider"></span>
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
    activeItemTitle = 'Рубежный зачёт Юнита ' + sk.unitId;
  }

  // Деликатный двухстрочный заголовок: название юнита приглушено и не кричит (Refined Eyebrow), активная тема — выразительный элегантный фокус
  const eyebrowDotsHTML = `
    <div class="topic-eyebrow-track" style="max-width:100%;margin:16px 0 22px;padding:0 2px;">
      <div style="display:flex;flex-direction:column;gap:12px;width:100%;">
        <div style="display:flex;flex-direction:column;align-items:flex-start;gap:2px;">
          <div style="font-family:var(--font-b);font-size:0.80rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.01em;line-height:1.2;">${escapeHtmlStr(cleanUnitTitle)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-b);font-size:1.06rem;font-weight:600;color:var(--ink);line-height:1.35;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}
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
    const backBtnHTML = `<button type="button" class="btn btn-ghost" data-chunk-prev="py" style="padding:11px 16px;border-radius:14px;font-size:.88rem;white-space:nowrap;${canGoBack ? 'display:inline-flex;' : 'display:none;'}" ${canGoBack ? '' : 'disabled aria-hidden="true"'}>← Назад</button>`;

    let primaryActionHTML = '';
    if(hasMoreChunks){
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-chunk-more="py">Понятно, дальше (+10 XP) ➔</button>`;
    } else if(stepIdx + 1 < steps.length){
      const activeK = pySkillViewState.kId || 'unknown';
      const stepKey = `${activeK}:${stepIdx+1}`;
      const stepAlreadyDone = isRead || (state.completedNoteSteps && state.completedNoteSteps[stepKey]);
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-py-next-step="${stepIdx+1}">Понятно, дальше${stepAlreadyDone ? '' : ' (+10 XP)'} ➔</button>`;
    } else {
      primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-py-finish-note="${activeK}">${isRead ? '✓ Конспект усвоен' : '✓ Завершить конспект (+10 MP)'}</button>`;
    }

    bodyHTML = `
      <div class="card coddy-lesson-card" style="margin-top:0;display:flex;flex-direction:column;justify-content:space-between;min-height:280px;">
        <div style="flex:1;">${feedHTML}</div>
        <div class="sprint-actions-bar" style="display:flex;align-items:center;gap:10px;margin-top:18px;padding-top:14px;border-top:1px solid var(--glass-border);flex-wrap:nowrap;flex:none;">
          ${backBtnHTML}
          <div style="display:flex;gap:10px;align-items:center;flex:1;justify-content:center;">
            ${primaryActionHTML}
          </div>
        </div>
      </div>`;
  } else if(pySkillViewState.tab === 'cards'){
    const deckObj = ALL_DECKS_COMBINED[activeF] || {id: activeF, title: activeF, cards: []};
    const cards = deckObj.cards || [];
    const cIdx = Math.min(pySkillViewState.cardIdx, Math.max(0, cards.length - 1));
    const curCard = cards[cIdx] || {q: 'Карточки загружаются', a: ''};

    bodyHTML = `
      <div class="card" style="margin-top:0;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
          <span style="font-size:0.80rem;color:var(--ink-muted);font-weight:600;">Карточка ${cards.length ? cIdx + 1 : 0} из ${cards.length}</span>
          ${typeof getRemNoteCardStatusBadgeHTML === 'function' ? getRemNoteCardStatusBadgeHTML(activeF + ':' + cIdx) : '<span style="font-size:0.75rem;padding:2px 8px;border-radius:999px;background:rgba(20,90,70,0.1);color:var(--moss);font-weight:600;">Интервальное повторение</span>'}
        </div>
        <div class="fc-card ${pySkillViewState.cardFlipped?'fc-card--Answer':''}" data-py-flip-card>
          <div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div class="topic-badge">${pySkillViewState.cardFlipped ? 'Ответ' : 'Вопрос'}</div>
              
            </div>
            <div class="fc-q">${formatRichInlineText(curCard.q)}</div>
            ${pySkillViewState.cardFlipped ? `<div class="fc-a">${formatRichInlineText(curCard.a)}</div>` : ''}
          </div>
        </div>
        ${pySkillViewState.cardFlipped ? (() => {
          const srsPrev = typeof computeRemNoteIntervals === 'function' ? computeRemNoteIntervals(activeF + ':' + cIdx) : {again:{days:1},hard:{days:2},good:{days:3},easy:{days:7}};
          return `
          <div class="fc-rate-row" style="margin-top:14px;">
            <button class="btn btn-ghost" data-py-rate-card="1" title="Повторить снова">Снова</button>
            <button class="btn btn-burgundy" data-py-rate-card="2" title="Повторить через 2 дня (+2 XP)">Трудно (+2 XP)</button>
            <button class="btn btn-clay" data-py-rate-card="3" title="Повторить через 3 дня (+5 XP)">Хорошо (+5 XP)</button>
            <button class="btn btn-primary" data-py-rate-card="4" title="Повторить через 7 дней (+10 XP)">Легко (+10 XP)</button>
          </div>`;
        })() : `
          <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">
            <button class="btn btn-ghost" data-py-prev-card ${cIdx===0?'disabled':''}>← Назад</button>
            <button class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-py-flip-card>Показать ответ</button>
            <button class="btn btn-ghost" data-py-rate-card="3" ${cIdx + 1 >= cards.length ? 'disabled' : ''}>Дальше →</button>
          </div>`}
      </div>`;
  } else if(pySkillViewState.tab === 'code'){
    const tObj = IDE_TASKS_BY_ID[activeTid] || {id: activeTid, title: 'Задача #' + activeTid, desc: '', initialCode: ''};
    const socraticHints = buildSocraticHintsForTask(tObj);
    const shownHints = socraticHints.slice(0, pySkillViewState.hintLevel).map((h, i) =>
      `<div class="socratic-hint" style="margin:8px 0;padding:10px 14px;border-radius:12px;background:rgba(217,119,6,0.08);border-left:3px solid var(--amber);font-size:0.86rem;line-height:1.45;"><strong>💡 Наводка ${i+1}:</strong> ${h}</div>`
    ).join('');

    const spec = buildTaskSpecDetails(tObj);
    const taskIdx = tIds.indexOf(activeTid);
    const isLastTask = (taskIdx >= tIds.length - 1);
    const nextBtnLabel = isLastTask ? 'Рубежный зачёт ➔' : 'Следующая задача ➔';

    let runFeedback = '';
    if(pySkillViewState.runStatus === 'pass') runFeedback = `
      <div class="result-feedback result-feedback--pass" style="margin-top:12px;padding:12px 16px;border-radius:14px;background:rgba(16,185,129,0.12);border:1px solid #10b981;color:#10b981;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;">
        <div>
          <div style="font-weight:700;">✓ Все тесты пройдены! (+15 MP)</div>
          <div style="font-size:0.78rem;opacity:0.85;margin-top:2px;">Задача #${tObj.id} успешно решена и закреплена.</div>
        </div>
        <button type="button" class="btn-glass-emerald" style="padding:8px 16px;border-radius:10px;font-size:0.84rem;white-space:nowrap;" data-py-next-task-btn="${tObj.id}">${nextBtnLabel}</button>
      </div>`;
    else if(pySkillViewState.runStatus === 'fail') runFeedback = `
      <div class="result-feedback result-feedback--fail" style="margin-top:12px;padding:12px;border-radius:12px;background:rgba(239,68,68,0.12);border:1px solid #ef4444;color:#ef4444;">
        <div style="font-weight:700;">✗ Ошибка выполнения или неверный результат</div>
        <pre style="margin-top:6px;font-size:0.80rem;white-space:pre-wrap;">${escapeHtmlStr(pySkillViewState.runOutput)}</pre>
      </div>`;

    let cleanDesc = String(tObj.desc || '');
    cleanDesc = cleanDesc.replace(/^<p>\s*<strong>\s*Задание\s*[:.-]?\s*<\/strong>\s*/i, '<p>');
    cleanDesc = cleanDesc.replace(/^<p>\s*Задание\s*[:.-]?\s*/i, '<p>');
    cleanDesc = cleanDesc.replace(/^<strong>\s*Задание\s*[:.-]?\s*<\/strong>\s*/i, '');
    cleanDesc = cleanDesc.replace(/^Задание\s*[:.-]?\s*/i, '').trim();
    cleanDesc = cleanDesc.replace(/^<p>/i, '').replace(/<\/p>$/i, '').trim();

    bodyHTML = `
      <div class="card" style="margin-top:0;">
        <div class="practice-layout practice-coddy-split">
          <div class="practice-left-pane practice-spec-pane">
            <div>
              <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:12px;">
                <div style="display:inline-flex;align-items:center;gap:6px;font-size:0.78rem;font-weight:700;">
                  <span style="color:var(--ink-muted);">Задача #${tObj.id}</span>
                  <span class="badge" style="background:rgba(217,119,6,0.18);color:var(--amber);padding:2px 8px;border-radius:8px;font-weight:700;white-space:nowrap;">${tObj.tier}</span>
                </div>
                <div style="display:flex;gap:8px;align-items:center;">
                  <span style="font-size:0.78rem;color:var(--ink-muted);font-weight:600;">${taskIdx >= 0 ? taskIdx + 1 : 1} из ${tIds.length}</span>
                  ${solvedMap[tObj.id]==='solved' ? `<span class="state-tag state-tag--mastered" style="margin:0;">✓ Решено</span>` : ''}
                </div>
              </div>
              <div class="lesson-theory" style="font-size:0.89rem;color:var(--ink-soft);line-height:1.55;margin-bottom:12px;">
                <strong>Задание:</strong> ${cleanDesc}
              </div>
              ${spec.ioCard}
            </div>
            <div style="margin-top:auto;padding-top:12px;border-top:1px solid var(--glass-border);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span style="font-size:0.75rem;font-weight:700;color:var(--amber);text-transform:uppercase;letter-spacing:0.04em;">💡 Наставник Сократ</span>
                <span style="font-size:0.72rem;color:var(--ink-muted);">Уровень скаффолдинга: <strong>${pySkillViewState.hintLevel} / ${socraticHints.length}</strong></span>
              </div>
              <button type="button" class="btn btn-ghost" data-py-task-hint style="width:100%;justify-content:center;font-size:0.82rem;padding:9px 12px;border-radius:12px;border:1px dashed rgba(217,119,6,0.35);background:rgba(217,119,6,0.04);" ${pySkillViewState.hintLevel>=socraticHints.length?'disabled':''}>
                ${pySkillViewState.hintLevel>=socraticHints.length ? '✓ Все наводки раскрыты' : 'Получить наводку без готового кода ➔'}
              </button>
              ${shownHints}
            </div>
          </div>
          <div class="practice-right-pane" style="display:flex;flex-direction:column;justify-content:space-between;">
            <div>
              ${buildCodeEditorWithGutterHTML('py-skill-editor', pySkillViewState.codeDraft, 220, spec.quickTokens)}
              <div class="practice-kbd-dock">
                <span><kbd>Ctrl</kbd>+<kbd>Enter</kbd> Запустить тесты</span>
                <span><kbd>Tab</kbd> Отступ</span>
              </div>
            </div>
            <div style="margin-top:10px;">
              <div style="display:flex;gap:10px;align-items:center;">
                <button type="button" class="btn btn-ghost" data-py-reset-task="${tObj.id}" style="padding:12px 14px;border-radius:14px;flex:none;opacity:0.8;" title="Сбросить код к исходному шаблону">↺</button>
                <button type="button" class="btn-check-solution" data-py-run-task="${tObj.id}">
                  <span>${ICONS.play} Проверить решение</span>
                  <span class="xp-tag">+15 XP</span>
                  <span style="font-size:0.75rem;opacity:0.85;font-weight:500;">(Ctrl+Enter)</span>
                </button>
              </div>
              ${runFeedback}
            </div>
          </div>
        </div>
      </div>`;
  }

  return `
    <div class="container" style="max-width:880px;">
      ${focusTopbarHTML}
      ${eyebrowDotsHTML}
      ${bodyHTML}
      ${celebrationBanner}
    </div>`;
}

function escapeHtmlStr(s){
  return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// 4-Level Socratic Scaffolding (Zero -> Conceptual -> Structural -> Tactical, strictly 0 solution code, <=70 words, 1 question per turn)
function buildSocraticHintsForTask(tObj){
  const rawHint = String((tObj && tObj.hint) || '').replace(/\?/g, '.').trim();
  const codeLines = String((tObj && tObj.initialCode) || '').split('\n');
  const unimplementedDefs = [];
  const allDefs = [];
  for(let i = 0; i < codeLines.length; i++){
    const line = codeLines[i];
    const m = line.match(/^(\s*)(def |async def |class )/);
    if(m){
      const trimmed = line.trim();
      allDefs.push(trimmed);
      if(m[2] !== 'class '){
        const baseIndent = m[1].length;
        let bodyLines = [];
        for(let j = i + 1; j < codeLines.length; j++){
          const nl = codeLines[j];
          if(!nl.trim()) continue;
          const ind = (nl.match(/^\s*/)[0] || '').length;
          if(ind <= baseIndent) break;
          bodyLines.push(nl.trim());
        }
        const isStub = bodyLines.length === 0 || bodyLines.some(b => b === 'pass' || b === '...' || /^#/.test(b) || /TODO/i.test(b));
        if(isStub) unimplementedDefs.push(trimmed);
      }
    }
  }
  const targetDefs = unimplementedDefs.length ? unimplementedDefs.slice(0, 2) : allDefs.slice(-2);
  let h3 = '';
  if(targetDefs.length > 0){
    const sigLines = targetDefs.join(' | ');
    h3 = `Тактический ориентир — проверь сигнатуру (${escapeHtmlStr(sigLines)}) и убедись, что возвращаешь результат нужного типа, а не печатаешь его. Какой тип объекта ожидает вызывающий код на выходе?`;
  } else {
    const varNames = [];
    for(let i = 0; i < codeLines.length; i++){
      const vm = codeLines[i].match(/^\s*([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)\s*=/);
      if(vm){
        const lhs = vm[1].trim();
        if(lhs && !varNames.includes(lhs)) varNames.push(lhs);
      }
    }
    const targetVars = varNames.slice(-3).join(', ') || 'result';
    h3 = `Тактический ориентир — проверь целевые переменные (${escapeHtmlStr(targetVars)}) и убедись, что присваиваешь им вычисленное значение нужного типа вместо заглушки None. Какой тип и формат данных ожидает проверка в итоговой переменной?`;
  }
  const h0 = 'Внимательно изучи условие и типы входных данных задачи. Какой граничный случай (пустой ввод, 0 или None) может нарушить базовую логику?';
  const h1 = rawHint
    ? `Опорная идея: ${rawHint} Какая структура данных или инвариант обеспечат здесь оптимальную сложность?`
    : 'Подумай о выборе структуры данных (хеш-таблица, множество, генератор) и избегай лишних вложенных проходов. Какой инвариант должен сохраняться на каждом шаге?';
  const h2 = 'Алгоритмический план: 1) Проверь базовый или пустой случай на входе; 2) Выполни основное преобразование без побочных мутаций аргументов; 3) Сформируй итоговое значение. Какой из этих шагов сейчас вызывает затруднение?';
  return [h0, h1, h2, h3];
}
window.buildSocraticHintsForTask = buildSocraticHintsForTask;
window.getSkillMP = getSkillMP;

async function runIdeTaskVerification(taskObj, codeStr){
  let buf = '';
  let passed = false;
  try{
    const runner = await getFastPythonRunner();
    runner.setStdout({ batched: function(s){ buf += s; } });
    runner.setStderr({ batched: function(s){ buf += s; } });
    const uJsonLit = JSON.stringify(JSON.stringify(String(codeStr || '')));
    const tJsonLit = JSON.stringify(JSON.stringify(String((taskObj && taskObj.tests) || '')));
    const fullTestScript = `
import json as _json
__USER_CODE__ = _json.loads(${uJsonLit})
_t_src = _json.loads(${tJsonLit})
try:
    exec(__USER_CODE__, globals())
    exec(_t_src, globals())
    __result__ = True
    __message__ = "OK"
except Exception as _e:
    __result__ = False
    __message__ = f"{type(_e).__name__}: {_e}"
`;
    runner.runPython(fullTestScript);
    passed = !!runner.globals.get('__result__');
    const msg = runner.globals.get('__message__') || '';
    if(!passed && msg) buf = msg + (buf ? '\n' + buf : '');
  }catch(err){
    passed = false;
    buf = String(err);
  }
  return { passed: passed, output: buf.trim() };
}

/* ================= UNIT MASTERY TEST & COURSE CHALLENGE ================= */
let unitTestState = null;
function saveUnitTestDraftState(){
  ensureExtendedState();
  if(!unitTestState || !unitTestState.stateKey) return;
  state.unitTestDrafts[unitTestState.stateKey] = {
    stateKey: unitTestState.stateKey,
    unitId: unitTestState.unitId,
    trackKey: unitTestState.trackKey,
    idx: unitTestState.idx || 0,
    answers: Array.isArray(unitTestState.answers) ? unitTestState.answers.slice() : [],
    revealed: !!unitTestState.revealed,
    finished: !!unitTestState.finished,
    updatedAt: Date.now()
  };
  saveState(state);
}

function viewPythonUnitTest(unitId, trackKey){
  const tr = getTrackForUnit(unitId, trackKey);
  const isCourse = unitId === 'course';
  let questions = [];
  let title = '';
  if(isCourse){
    title = `🏆 Итоговый вызов курса (Course Challenge · ${tr.courseUnitRange})`;
    Object.values(tr.data.unitTests).forEach(ut => {
      questions = questions.concat(ut.questions.slice(0, 2));
    });
  } else {
    const ut = ALL_UNIT_TESTS_COMBINED[unitId] || tr.data.unitTests[unitId] || PY_MASTERY.unitTests['1.1'];
    title = ut.title;
    questions = ut.questions;
  }

  const stateKey = tr.key + ':' + unitId;
  if(!unitTestState || unitTestState.stateKey !== stateKey){
    ensureExtendedState();
    const savedUt = state.unitTestDrafts && state.unitTestDrafts[stateKey];
    if(savedUt && typeof savedUt === 'object'){
      unitTestState = {
        stateKey: stateKey,
        unitId: unitId,
        trackKey: tr.key,
        idx: Math.min(Math.max(0, Number(savedUt.idx) || 0), Math.max(0, questions.length - 1)),
        answers: Array.isArray(savedUt.answers) ? savedUt.answers.slice() : [],
        revealed: !!savedUt.revealed,
        finished: !!savedUt.finished
      };
    } else {
      unitTestState = { stateKey: stateKey, unitId: unitId, trackKey: tr.key, idx: 0, answers: [], revealed: false, finished: false };
    }
  }

  // Стартовая модалка «Готовы начать тест?» — только на открытии «с нуля»:
  // ни одного ответа, не ретейк, настройка «без модалки» не включена, тест ещё не начат в этой сессии.
  const answeredCount = (unitTestState.answers || []).filter(a => a !== undefined && a !== null).length;
  const isRetake = !isCourse && (state.passedUnitTests || []).includes(unitId);
  const showStartModal = !unitTestState.finished && !unitTestState.started && answeredCount === 0 && !isRetake && !state.utSkipStartModal;

  if(unitTestState.finished){
    const score = questions.filter((q, i) => unitTestState.answers[i] === q.correct).length;
    const pct = Math.round(score / questions.length * 100);
    const passed = pct >= 75;
    return `
      <div class="container">
        <div class="diag-header-row">
          <a href="#${tr.routePrefix}" class="back-link">${ICONS.chevronLeft} ${tr.backLabel}</a>
          <div class="topic-badge">${title}</div>
        </div>
        <div class="microstep-card">
          <h1>${passed ? '👑 Рубежный тест успешно взят!' : 'Почти получилось — попробуй ещё раз'}</h1>
          <p style="font-size:1.08rem;margin-top:8px;">Результат: <b>${score} из ${questions.length}</b> (${pct}%). ${passed ? 'Все навыки юнита повышены до 100 MP (Мастерство 👑)!' : 'Для ранга Мастерство (100 MP) нужно набрать не менее 75%.'}</p>
          <div style="display:flex;gap:10px;margin-top:18px;">
            <a href="#${tr.routePrefix}" class="btn btn-primary">Вернуться к матрице навыков</a>
            <button class="btn btn-ghost" data-ut-restart="${unitId}">Пройти ещё раз</button>
          </div>
        </div>
      </div>`;
  }

  const q = questions[unitTestState.idx];
  const answeredSel = unitTestState.answers[unitTestState.idx];
  const pendingSel = (typeof unitTestState.pending === 'number') ? unitTestState.pending : answeredSel;
  const rev = unitTestState.revealed;
  const optsHTML = q.options.map((opt, i) => {
    let cls = 'quiz-opt';
    if(rev){
      if(i === q.correct) cls += ' quiz-opt--correct';
      else if(i === answeredSel) cls += ' quiz-opt--wrong';
    } else if(i === pendingSel){
      cls += ' quiz-opt--pending';
    }
    return `<button type="button" class="${cls}" data-ut-ans="${i}" ${rev?'disabled':''}>${i+1}. ${formatRichInlineText(opt)}</button>`;
  }).join('');

  return `
    <div class="container">
      <div class="diag-header-row">
        <a href="#${tr.routePrefix}" class="back-link">${ICONS.chevronLeft} ${tr.backLabel}</a>
        <div style="display:flex;gap:6px;align-items:center;flex-wrap:nowrap;min-width:0;">
          ${(state.passedUnitTests || []).includes(unitId) && !isCourse ? `<span class="topic-badge" style="margin:0;background:var(--moss-soft);border-color:rgba(52,211,153,0.4);color:var(--moss-deep);white-space:nowrap;">✓ Сдано · ретейк</span>` : ''}
          <div class="topic-badge">${title} · Вопрос ${unitTestState.idx+1} из ${questions.length}</div>
        </div>
      </div>
      <div class="quiz-progress"><div class="quiz-progress__bar" style="width:${Math.round(unitTestState.idx/questions.length*100)}%;"></div></div>
      <div class="microstep-card">
        <h2 style="margin-bottom:16px;">${formatQuizQuestionPromptHTML(q.q)}</h2>
        <div style="display:flex;flex-direction:column;gap:9px;">${optsHTML}</div>
        <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-top:14px;">
          ${unitTestState.idx > 0 ? `<button type="button" class="btn btn-ghost" data-ut-prev>← Предыдущий вопрос</button>` : `<span></span>`}
          ${rev ? `<button type="button" class="btn btn-primary" data-ut-next>${unitTestState.idx+1>=questions.length?'Завершить тест':'Следующий вопрос'} ${ICONS.arrowRight}</button>` : (typeof pendingSel === 'number' ? `<button type="button" class="btn btn-primary" data-ut-confirm>Ответить</button>` : `<span></span>`)}
        </div>
        ${rev && state.utShowExplanations ? `<div class="notice" style="margin-top:14px;">${sel===q.correct?'✓ Верно! ':'✗ Обрати внимание: '}${formatRichInlineText(q.explain)}</div>` : ''}
      </div>
    </div>` + (!showStartModal ? '' : (() => {
      const qn = questions.length;
      const qWord = (qn % 10 === 1 && qn % 100 !== 11) ? 'вопрос' : ([2,3,4].includes(qn % 10) && ![12,13,14].includes(qn % 100)) ? 'вопроса' : 'вопросов';
      return `
    <div class="modal-backdrop ut-start-backdrop" role="dialog" aria-modal="true" aria-label="Готовы начать тест?">
      <div class="ut-start-card">
        <div class="ut-start-emoji" aria-hidden="true">🧪</div>
        <h2 class="ut-start-title">Готовы начать тест?</h2>
        <p class="ut-start-sub">${qn} ${qWord} · порог 75% · +50 XP</p>
        <button type="button" class="btn-glass-emerald ut-start-btn" data-ut-start>▶ Начать тест</button>
        <a href="#${tr.routePrefix}" class="btn btn-ghost ut-skip-btn">Пропустить</a>
        <button type="button" class="ut-toggle-row" data-ut-toggle-explain aria-pressed="${state.utShowExplanations ? 'true' : 'false'}">
          <span>Показывать разбор после ответа</span>
          <span class="ut-switch ${state.utShowExplanations ? 'ut-switch--on' : ''}" aria-hidden="true"><span class="ut-switch-knob"></span></span>
        </button>
        <button type="button" class="link-quiet" data-ut-always-skip>Всегда открывать тест без этой модалки</button>
        <p class="ut-start-hint">Это можно изменить в «⚙️ Настройки платформы»</p>
      </div>
    </div>`;
    })());
}

/* ================= GLOBAL FLASHCARDS HUB (#/cards) ================= */
const _initCardsPos = (state && state.cardsHubPos && typeof state.cardsHubPos === 'object') ? state.cardsHubPos : {};
let cardsHubState = {
  echelonFilter: _initCardsPos.echelonFilter || 'all',
  unitFilter: _initCardsPos.unitFilter || 'all',
  deckId: _initCardsPos.deckId || 'Ф-001',
  cardIdx: typeof _initCardsPos.cardIdx === 'number' ? _initCardsPos.cardIdx : 0,
  flipped: !!_initCardsPos.flipped,
  completed: !!_initCardsPos.completed
};
window.cardsHubState = cardsHubState;
function saveCardsHubPosState(){
  ensureExtendedState();
  state.cardsHubPos = {
    echelonFilter: cardsHubState.echelonFilter || 'all',
    unitFilter: cardsHubState.unitFilter || 'all',
    deckId: cardsHubState.deckId || 'Ф-001',
    cardIdx: cardsHubState.cardIdx || 0,
    flipped: !!cardsHubState.flipped,
    completed: !!cardsHubState.completed,
    updatedAt: Date.now()
  };
  saveState(state);
}
function viewCardsHub(){
  const allDeckIds = Object.keys(ALL_DECKS_COMBINED).sort();
  if(!ALL_DECKS_COMBINED[cardsHubState.deckId]) cardsHubState.deckId = allDeckIds[0];

  const echelonOpts = `
    <option value="all" ${cardsHubState.echelonFilter==='all'?'selected':''}>🎯 Все 4 эшелона приоритета собеседований</option>
    <option value="1" ${cardsHubState.echelonFilter==='1'?'selected':''}>🚨 Эшелон 1 · Скрининг и база (первая очередь)</option>
    <option value="2" ${cardsHubState.echelonFilter==='2'?'selected':''}>🔥 Эшелон 2 · Тех-ядро и выбранный стек</option>
    <option value="3" ${cardsHubState.echelonFilter==='3'?'selected':''}>⚡ Эшелон 3 · Продакшен-инженерия</option>
    <option value="4" ${cardsHubState.echelonFilter==='4'?'selected':''}>👑 Эшелон 4 · Архитектурный резерв</option>
    <option value="gaps" ${cardsHubState.echelonFilter==='gaps'?'selected':''}>🎯 Пробелы по диагностике</option>`;

  const unitOpts = `<option value="all" ${cardsHubState.unitFilter==='all'?'selected':''}>Все 9 юнитов Python (126 колод · 2 181 карточка) + все 7 модулей (${allDeckIds.length} колод)</option>` +
    ALL_UNITS_COMBINED.map(u => `<option value="${u.id}" ${cardsHubState.unitFilter===u.id?'selected':''}>[Эшелон ${getEffectiveUnitTier(u.id)}] ${String(u.title).startsWith('Юнит') ? u.title : `Юнит ${u.id}: ${u.title}`}</option>`).join('');

  let filteredDecks = allDeckIds;
  if(cardsHubState.echelonFilter === 'gaps'){
    const gapSet = new Set();
    (state.diagnosticGaps || []).forEach(sid => {
      const sk = PY_SKILLS_BY_ID[sid];
      if(sk) (sk.fIds || []).forEach(fid => gapSet.add(fid));
    });
    if(gapSet.size > 0) filteredDecks = filteredDecks.filter(d => gapSet.has(d));
  } else if(cardsHubState.echelonFilter !== 'all'){
    const targetTier = parseInt(cardsHubState.echelonFilter, 10);
    filteredDecks = filteredDecks.filter(d => getDeckInterviewTier(d) === targetTier);
  }
  if(cardsHubState.unitFilter !== 'all'){
    const u = ALL_UNITS_COMBINED.find(x => x.id === cardsHubState.unitFilter);
    if(u){
      const setF = new Set();
      u.skills.forEach(s => s.fIds.forEach(f => setF.add(f)));
      filteredDecks = filteredDecks.filter(d => setF.has(d));
    }
  }
  if(!filteredDecks.length) filteredDecks = allDeckIds;
  if(filteredDecks.length && !filteredDecks.includes(cardsHubState.deckId)){
    cardsHubState.deckId = filteredDecks[0];
  }

  const deck = ALL_DECKS_COMBINED[cardsHubState.deckId];
  const cards = deck.cards || [];
  const cIdx = Math.min(cardsHubState.cardIdx, Math.max(0, cards.length - 1));
  const cur = cards[cIdx] || {q:'', a:''};
  const curDeckTier = getDeckInterviewTier(deck.id);
  const linkedSkills = DECK_TO_SKILLS_MAP[deck.id] || [];
  const primarySkill = linkedSkills[0] || ALL_PY_SKILLS[0];

  const deckOpts = filteredDecks.map(fid => {
    const d = ALL_DECKS_COMBINED[fid];
    const done = state.reviewedDecks.includes(fid);
    const dt = getDeckInterviewTier(fid);
    return `<option value="${fid}" ${fid===cardsHubState.deckId?'selected':''}>${done?'✓ ':''}[Эшелон ${dt}] ${fid}: ${d.title} (${(d.cards||[]).length})</option>`;
  }).join('');

  if(cardsHubState.completed && cards.length > 0){
    const curDeckIdx = filteredDecks.indexOf(cardsHubState.deckId);
    const nextDeckId = (curDeckIdx >= 0 && curDeckIdx + 1 < filteredDecks.length) ? filteredDecks[curDeckIdx + 1] : null;
    const nextDeck = nextDeckId ? ALL_DECKS_COMBINED[nextDeckId] : null;
    return `
    <div class="container">
      <div class="cards-hub-header" style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px;">
        <div>
          <span class="sr-only">Интервальное повторение RemNote · 286 колод · 6 051 карточка</span>
          <h1 style="margin:0;">🎉 Колода изучена!</h1>
        </div>
        <div style="display:flex;gap:8px;align-items:center;">
          ${(() => {
            const srsStats = typeof getSpacedRepetitionStats === 'function' ? getSpacedRepetitionStats() : {dueTodayCardsCount:0, masteredCardsCount:0};
            return `<span class="cocoon-pill">Изучено: <b>${state.reviewedDecks.length}/${allDeckIds.length}</b></span>
            ${srsStats.dueTodayCardsCount > 0 ? `<span class="cocoon-pill" style="border-color:rgba(251,113,133,0.45);color:#fb7185;">🔥 К повторению: <b>${srsStats.dueTodayCardsCount}</b></span>` : `<span class="cocoon-pill" style="color:var(--moss);">✓ Повторено на сегодня</span>`}
            <span class="cocoon-pill" style="color:#34d399;">👑 Закреплено: <b>${srsStats.masteredCardsCount || 0}</b></span>`;
          })()}
          ${primarySkill ? `<a href="#${primarySkill.routePrefix}/skill/${primarySkill.id}" class="btn btn-ghost" style="padding:6px 11px;font-size:.78rem;">💻 К практике темы (${primarySkill.id}) →</a>` : ''}
        </div>
      </div>
      <div class="cards-hub-controls">
        <div class="cards-hub-subfilters">
          <select id="cards-echelon-filter" class="code-editor" style="min-height:auto;padding:8px 10px;font-size:.82rem;">${echelonOpts}</select>
          <select id="cards-unit-select" class="code-editor" style="min-height:auto;padding:8px 10px;font-size:.82rem;">${unitOpts}</select>
        </div>
        <select id="cards-deck-select" class="code-editor" style="min-height:auto;padding:8px 10px;font-size:.85rem;font-weight:600;">${deckOpts}</select>
      </div>
      <div class="panel" style="padding:32px 24px;text-align:center;margin-top:20px;">
        <div style="font-size:3rem;margin-bottom:12px;">🏆</div>
        <h2 style="margin:0 0 10px;">Все ${cards.length} карточек колоды «${deck.title}» пройдены!</h2>
        <p class="meta" style="max-width:540px;margin:0 auto 24px;line-height:1.55;">Колода успешно добавлена в интервальное повторение. Теперь закрепите теорию практическим написанием кода в тренажёре или переходите к следующей теме.</p>
        <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
          ${primarySkill ? `<a href="#${primarySkill.routePrefix}/skill/${primarySkill.id}" class="btn btn-primary btn-lg">💻 Перейти к практике темы (${primarySkill.id})</a>` : ''}
          ${nextDeckId ? `<button class="btn btn-clay btn-lg" data-hub-next-deck="${nextDeckId}">Следующая колода (${nextDeckId}: ${nextDeck.title}) →</button>` : ''}
          <button class="btn btn-ghost btn-lg" data-hub-restart-deck>🔄 Повторить колоду сначала</button>
        </div>
      </div>
    </div>`;
  }

  return `
    <div class="container">
      <div class="cards-hub-header" style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px;">
        <div>
          <span class="sr-only">Интервальное повторение RemNote · 286 колод · 6 051 карточка (126 колод Python + 25 колод Web + 43 колоды Backend + 16 колод Алгоритмы + 32 колоды Базы данных + 17 колод Архитектура + 45 колод Инфраструктура)</span>
          <h1 style="margin:0;">🃏 Центр 3D Флеш-карточек</h1>
        </div>
        <div style="display:flex;gap:8px;align-items:center;">
          <span class="cocoon-pill">Изучено колод: <b>${state.reviewedDecks.length} / ${allDeckIds.length}</b></span>
          ${primarySkill ? `<a href="#${primarySkill.routePrefix}/skill/${primarySkill.id}" class="btn btn-ghost" style="padding:6px 11px;font-size:.78rem;">💻 К практике темы (${primarySkill.id}) →</a>` : ''}
        </div>
      </div>
      <div class="cards-hub-controls">
        <div class="cards-hub-subfilters">
          <select id="cards-echelon-filter" class="code-editor" style="min-height:auto;padding:8px 10px;font-size:.82rem;">${echelonOpts}</select>
          <select id="cards-unit-select" class="code-editor" style="min-height:auto;padding:8px 10px;font-size:.82rem;">${unitOpts}</select>
        </div>
        <select id="cards-deck-select" class="code-editor" style="min-height:auto;padding:8px 10px;font-size:.85rem;font-weight:600;">${deckOpts}</select>
      </div>
      <div class="fc-stage" style="margin-top:16px;">
        ${buildFcStoriesBarHTML(deck.id, cards.length, cIdx)}
        <div class="fc-card fc-card--3d ${cardsHubState.flipped ? 'fc-card--flipped fc-card--Answer' : ''}" data-hub-flip style="margin-top:10px;">
          <div class="fc-card-inner">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div style="display:flex;align-items:center;gap:8px;">
                <div class="topic-badge">${cardsHubState.flipped ? 'Ответ' : 'Вопрос'}</div>
                ${typeof getRemNoteCardStatusBadgeHTML === 'function' ? getRemNoteCardStatusBadgeHTML(cardsHubState.deckId + ':' + cIdx) : ''}
              </div>
              
            </div>
            <div class="fc-q">${typeof formatRichInlineText === 'function' ? formatRichInlineText(cur.q) : cur.q}</div>
            ${cardsHubState.flipped ? `<div class="fc-a" style="margin-top:14px;padding-top:14px;border-top:1px dashed var(--line);">${typeof formatRichInlineText === 'function' ? formatRichInlineText(cur.a) : cur.a}</div>` : ''}
          </div>
          <div class="meta" style="margin-top:12px;text-align:center;">Карточка ${cards.length ? cIdx + 1 : 0} из ${cards.length}</div>
        </div>
        ${cardsHubState.flipped ? (() => {
          const srsPrev = typeof computeRemNoteIntervals === 'function' ? computeRemNoteIntervals(cardsHubState.deckId + ':' + cIdx) : {again:{days:1},hard:{days:2},good:{days:3},easy:{days:7}};
          return `
          <div class="fc-rate-row" style="margin-top:12px;">
            <button class="btn btn-ghost" data-hub-rate="1" title="Повторить снова">Снова</button>
            <button class="btn btn-burgundy" data-hub-rate="2" title="Повторить через 2 дня (+2 XP)">Трудно (+2 XP)</button>
            <button class="btn btn-clay" data-hub-rate="3" title="Повторить через 3 дня (+5 XP)">Хорошо (+5 XP)</button>
            <button class="btn btn-primary" data-hub-rate="4" title="Повторить через 7 дней (+10 XP)">Легко (+10 XP)</button>
          </div>`;
        })() : `
          <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">
            <button class="btn btn-ghost" data-hub-prev ${cIdx===0?'disabled':''}>← Назад</button>
            <button class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-hub-flip>Показать ответ</button>
            <button class="btn btn-ghost" data-hub-next ${cIdx + 1 >= cards.length ? 'disabled' : ''}>Дальше →</button>
          </div>`}
      </div>
    </div>`;
}

/* ================= 401-TASK CODING TRAINER HUB (#/practice) ================= */
const _initPracPos = (state && state.practiceHubPos && typeof state.practiceHubPos === 'object') ? state.practiceHubPos : {};
let practiceHubState = {
  echelonFilter: _initPracPos.echelonFilter || 'all',
  tierFilter: _initPracPos.tierFilter || 'all',
  catFilter: _initPracPos.catFilter || 'all',
  statusFilter: _initPracPos.statusFilter || 'all',
  search: _initPracPos.search || '',
  taskId: (typeof _initPracPos.taskId === 'number' && IDE_TASKS_BY_ID[_initPracPos.taskId]) ? _initPracPos.taskId : 240,
  codeDraft: '',
  hintLevel: typeof _initPracPos.hintLevel === 'number' ? _initPracPos.hintLevel : 0,
  runStatus: null,
  runOutput: '',
  mobileFiltersOpen: false
};
window.practiceHubState = practiceHubState;
function savePracticeHubPosState(){
  ensureExtendedState();
  state.practiceHubPos = {
    echelonFilter: practiceHubState.echelonFilter || 'all',
    tierFilter: practiceHubState.tierFilter || 'all',
    catFilter: practiceHubState.catFilter || 'all',
    statusFilter: practiceHubState.statusFilter || 'all',
    search: practiceHubState.search || '',
    taskId: practiceHubState.taskId || 240,
    hintLevel: practiceHubState.hintLevel || 0,
    updatedAt: Date.now()
  };
  saveState(state);
}

function selectPracticeTask(tid){
  const ed = document.getElementById('prac-code-editor');
  if(ed && ed.value && practiceHubState.taskId){
    saveIdeDraft(practiceHubState.taskId, ed.value);
  }
  const t = IDE_TASKS_BY_ID[tid] || IDE_TASKS[0];
  practiceHubState.taskId = t.id;
  practiceHubState.codeDraft = getIdeDraft(t.id, t.initialCode);
  if(ed) ed.value = practiceHubState.codeDraft;
  practiceHubState.hintLevel = 0;
  practiceHubState.runStatus = null;
  practiceHubState.runOutput = '';
  savePracticeHubPosState();
}

function viewPracticeHub(){
  const solvedMap = getIdeSolvedMap();
  const totalSolved = countSolvedIdeTasks(solvedMap);
  if(!practiceHubState.codeDraft && IDE_TASKS_BY_ID[practiceHubState.taskId]){
    practiceHubState.codeDraft = getIdeDraft(practiceHubState.taskId, IDE_TASKS_BY_ID[practiceHubState.taskId].initialCode);
  }

  const gapTaskIds = new Set();
  (state.diagnosticGaps || []).forEach(sid => {
    const sk = PY_SKILLS_BY_ID[sid];
    if(sk) (sk.taskIds || []).forEach(tid => gapTaskIds.add(tid));
  });

  const tiers = ['🥚 Уровень 1','🐣 Уровень 2','🐢 Уровень 3','🦊 Уровень 4','🦅 Уровень 5','🦁 Уровень 6','👑 Уровень 7'];
  const filtered = IDE_TASKS.filter(t => {
    if(practiceHubState.echelonFilter === 'gaps'){
      if(gapTaskIds.size > 0 && !gapTaskIds.has(t.id)) return false;
      if(gapTaskIds.size === 0 && getTaskInterviewTier(t.id) !== 1) return false;
    } else if(practiceHubState.echelonFilter !== 'all'){
      if(getTaskInterviewTier(t.id) !== parseInt(practiceHubState.echelonFilter, 10)) return false;
    }
    if(practiceHubState.tierFilter !== 'all' && t.tier !== practiceHubState.tierFilter) return false;
    const isPyCore = (t.id >= 240 && t.id <= 381) || String(t.topic).includes('Python Core');
    if(practiceHubState.catFilter === 'python' && !isPyCore) return false;
    if(practiceHubState.catFilter === 'backend' && isPyCore) return false;
    if(practiceHubState.statusFilter === 'solved' && solvedMap[t.id] !== 'solved') return false;
    if(practiceHubState.statusFilter === 'unsolved' && solvedMap[t.id] === 'solved') return false;
    if(practiceHubState.search){
      const q = practiceHubState.search.toLowerCase();
      if(!String(t.id).includes(q) && !t.title.toLowerCase().includes(q) && !t.topic.toLowerCase().includes(q)) return false;
    }
    return true;
  });

  const taskInFiltered = filtered.find(t => t.id === practiceHubState.taskId);
  const curTask = taskInFiltered || filtered[0] || IDE_TASKS_BY_ID[practiceHubState.taskId] || IDE_TASKS[0];
  if(!taskInFiltered && filtered.length > 0 && curTask && curTask.id !== practiceHubState.taskId){
    practiceHubState.taskId = curTask.id;
    practiceHubState.codeDraft = getIdeDraft(curTask.id, curTask.initialCode);
    practiceHubState.hintLevel = 0;
    practiceHubState.runStatus = null;
    practiceHubState.runOutput = '';
    savePracticeHubPosState();
  }
  const curFilteredIdx = filtered.length > 0 ? Math.max(0, filtered.findIndex(t => t.id === curTask.id)) : 0;
  const curTaskEchelon = getTaskInterviewTier(curTask.id);
  const socraticHints = buildSocraticHintsForTask(curTask);
  const socraticLabels = [
    'Уровень 0 (Zero Hint — Граничные условия)',
    'Уровень 1 (Conceptual Hint — Концепция)',
    'Уровень 2 (Structural Hint — Декомпозиция)',
    'Уровень 3 (Tactical Hint — Сигнатура и контракт)'
  ];
  const shownHints = socraticHints.slice(0, practiceHubState.hintLevel).map((h, idx) =>
    `<div class="hint-box"><strong>${socraticLabels[idx] || ('Уровень опоры ' + idx)}:</strong> ${h}</div>`
  ).join('');

  let runFeedback = '';
  if(practiceHubState.runStatus === 'running') runFeedback = `<div class="test-running-shimmer" style="margin-top:10px;">⚡ Выполняю pytest-проверки в браузере…</div>`;
  else if(practiceHubState.runStatus === 'pass') runFeedback = `<div class="result-box--pass correct-pulse-anim">${ICONS.check} Задача #${curTask.id} решена верно! (+25 XP)\n${practiceHubState.runOutput||''}</div>`;
  else if(practiceHubState.runStatus === 'fail') runFeedback = `
    <div class="result-box--fail">Тесты не прошли:\n${practiceHubState.runOutput||''}</div>
    <div style="margin-top:8px;"><button class="btn btn-ghost" style="padding:6px 12px;font-size:.78rem;" data-prac-hint>💡 Разобрать ошибку с Сократовским интервьюером (${practiceHubState.hintLevel}/${socraticHints.length})</button></div>`;

  // V7 (Coddy-ref): один механизм навигации по задачам — инлайн-свайпер в шапке задачи (‹ N/M ›);
  // селект-список и дубль «Пред/След» из дравера фильтров сняты, поиск остался

  let echelonLabel = '🎯 Все эшелоны';
  if(practiceHubState.echelonFilter === '1') echelonLabel = '🎯 Эшелон 1';
  else if(practiceHubState.echelonFilter === '2') echelonLabel = '🔥 Эшелон 2';
  else if(practiceHubState.echelonFilter === '3') echelonLabel = '⚡ Эшелон 3';
  else if(practiceHubState.echelonFilter === '4') echelonLabel = '👑 Эшелон 4';
  else if(practiceHubState.echelonFilter === 'gaps') echelonLabel = '🎯 Пробелы';

  let catLabel = '🌐 Все модули';
  if(practiceHubState.catFilter === 'python') catLabel = '🐍 Python';
  else if(practiceHubState.catFilter === 'backend') catLabel = '⚙️ Backend';

  let tierLabel = 'Все уровни';
  if(practiceHubState.tierFilter !== 'all'){
    tierLabel = practiceHubState.tierFilter.replace('Уровень ', 'Ур. ');
  }

  let statusLabel = 'Все статусы';
  if(practiceHubState.statusFilter === 'unsolved') statusLabel = '⏳ Не решено';
  else if(practiceHubState.statusFilter === 'solved') statusLabel = '✓ Решено';

  const chipsBarHTML = `
    <div class="prac-chips-bar prac-quick-chips">
      <label class="prac-chip-select-pill prac-chip prac-chip--echelon ${practiceHubState.echelonFilter!=='all'?'is-active active':''}" title="Фильтр по эшелону собеседования">
        <select id="prac-echelon-filter" class="prac-chip-select">
          <option value="all" ${practiceHubState.echelonFilter==='all'?'selected':''}>🎯 Все эшелоны (1–4)</option>
          <option value="1" ${practiceHubState.echelonFilter==='1'?'selected':''}>🎯 Эшелон 1 · Скрининг</option>
          <option value="2" ${practiceHubState.echelonFilter==='2'?'selected':''}>🔥 Эшелон 2 · Тех-ядро</option>
          <option value="3" ${practiceHubState.echelonFilter==='3'?'selected':''}>⚡ Эшелон 3 · Продакшен</option>
          <option value="4" ${practiceHubState.echelonFilter==='4'?'selected':''}>👑 Эшелон 4 · Резерв</option>
          <option value="gaps" ${practiceHubState.echelonFilter==='gaps'?'selected':''}>🎯 Пробелы диагностики</option>
        </select>
        <span class="prac-chip-display">${echelonLabel} ▾</span>
      </label>

      <label class="prac-chip-select-pill prac-chip prac-chip--cat ${practiceHubState.catFilter!=='all'?'is-active active':''}" title="Фильтр по стеку">
        <select id="prac-cat-filter" class="prac-chip-select">
          <option value="all" ${practiceHubState.catFilter==='all'?'selected':''}>🌐 Все модули (401)</option>
          <option value="python" ${practiceHubState.catFilter==='python'?'selected':''}>🐍 Python Core 1.1–1.9</option>
          <option value="backend" ${practiceHubState.catFilter==='backend'?'selected':''}>⚙️ Backend, SQL, FastAPI, Docker</option>
        </select>
        <span class="prac-chip-display">${catLabel} ▾</span>
      </label>

      <label class="prac-chip-select-pill prac-chip prac-chip--tier ${practiceHubState.tierFilter!=='all'?'is-active active':''}" title="Фильтр по уровню сложности">
        <select id="prac-tier-filter" class="prac-chip-select">
          <option value="all" ${practiceHubState.tierFilter==='all'?'selected':''}>Все уровни (🥚..👑)</option>
          ${tiers.map(tr => `<option value="${tr}" ${practiceHubState.tierFilter===tr?'selected':''}>${tr.replace('Уровень ', 'Ур. ')}</option>`).join('')}
        </select>
        <span class="prac-chip-display">${tierLabel} ▾</span>
      </label>

      <button type="button" class="prac-chip-btn prac-chip prac-search-toggle ${practiceHubState.searchOpen || practiceHubState.search?'is-active active':''}" data-toggle-prac-search title="Поиск задачи">🔍</button>

      <label class="prac-chip-select-pill prac-chip prac-chip--status ${practiceHubState.statusFilter!=='all'?'is-active active':''}" title="Фильтр по статусу решения">
        <select id="prac-status-filter" class="prac-chip-select">
          <option value="all" ${practiceHubState.statusFilter==='all'?'selected':''}>Все статусы</option>
          <option value="unsolved" ${practiceHubState.statusFilter==='unsolved'?'selected':''}>⏳ Не решённые</option>
          <option value="solved" ${practiceHubState.statusFilter==='solved'?'selected':''}>✓ Решённые</option>
        </select>
        <span class="prac-chip-display">${statusLabel} ▾</span>
      </label>
    </div>`;

  const searchBarHTML = (practiceHubState.searchOpen || practiceHubState.search) ? `
    <div class="prac-search-bar-row">
      <input id="prac-search-input" type="text" class="code-editor prac-search-field" placeholder="Поиск по названию или #ID…" value="${escapeHtmlStr(practiceHubState.search)}">
      ${practiceHubState.search ? `<button type="button" class="btn btn-ghost" style="padding:4px 9px;font-size:.78rem;" data-clear-prac-search>✕ Очистить</button>` : ''}
    </div>` : '';

  practiceHubState.mobileTab = practiceHubState.mobileTab || 'task';
  const curMobTab = practiceHubState.mobileTab;
  const mobileTabsHTML = `
    <div class="prac-mobile-tabs" role="tablist">
      <button type="button" class="prac-mob-tab ${curMobTab==='docs'?'active':''}" data-prac-mob-tab="docs" role="tab">📖 Справка</button>
      <button type="button" class="prac-mob-tab ${curMobTab==='task'?'active':''}" data-prac-mob-tab="task" role="tab">🎯 Задача</button>
      <button type="button" class="prac-mob-tab ${curMobTab==='code'?'active':''}" data-prac-mob-tab="code" role="tab">💻 Код</button>
      <button type="button" class="prac-mob-tab ${curMobTab==='solution'?'active':''}" data-prac-mob-tab="solution" role="tab">💡 Решение</button>
    </div>`;

  let sigCode = 'def solution():';
  const sigMatch = (curTask.initialCode || '').match(/def\s+[a-zA-Z0-9_]+\s*\([^)]*\)(?:\s*->\s*[^:]+)?:/);
  if(sigMatch) sigCode = sigMatch[0];
  const signatureBoxHTML = `<div class="prac-signature-box"><div class="sig-badge">Сигнатура функции:</div><code>${escapeHtmlStr(sigCode)}</code></div>`;

  const plainExplainBtnHTML = `
    <div style="margin:8px 0 10px;">
      <button type="button" class="btn btn-ghost" style="padding:6px 12px;font-size:.78rem;" data-prac-toggle-explain>
        🤖 ${practiceHubState.showPlainExplain ? 'Скрыть пояснение' : 'Объяснить задание'}
      </button>
    </div>`;
  const plainExplainBoxHTML = practiceHubState.showPlainExplain ? `
    <div class="panel" style="padding:12px 14px;margin-bottom:12px;border-left:3px solid var(--amber);">
      <div style="font-size:0.8rem;font-weight:700;color:var(--amber);margin-bottom:4px;">Суть задания простыми словами:</div>
      <p style="font-size:0.86rem;line-height:1.5;margin:0;">${escapeHtmlStr(curTask.hint || curTask.title)}</p>
    </div>` : '';

  let testCasesRowsHTML = '';
  if(curTask.tests && curTask.tests.includes('assert ')){
    const assertLines = curTask.tests.split('\n').filter(l => l.trim().startsWith('assert ')).slice(0, 4);
    testCasesRowsHTML = assertLines.map((al, idx) => {
      let clean = al.trim().replace(/^assert\s+/, '');
      let parts = clean.split('==');
      let inp = parts[0] ? parts[0].trim() : `Тест #${idx+1}`;
      let exp = parts[1] ? parts[1].split(',')[0].trim() : 'True';
      const clip = (v, n) => v.length > n ? v.slice(0, n) + '…' : v;
      return `<tr><td><code title="${escapeHtmlStr(inp)}">${escapeHtmlStr(clip(inp, 36))}</code></td><td><code title="${escapeHtmlStr(exp)}">${escapeHtmlStr(clip(exp, 24))}</code></td><td><span style="color:var(--ink-muted);">Ожидает</span></td></tr>`;
    }).join('');
  }
  if(!testCasesRowsHTML){
    testCasesRowsHTML = `
      <tr><td><code>solution(sample_input)</code></td><td><code>expected_result</code></td><td><span style="color:var(--ink-muted);">Ожидает</span></td></tr>
      <tr><td><code>solution(edge_case)</code></td><td><code>expected_edge</code></td><td><span style="color:var(--ink-muted);">Ожидает</span></td></tr>`;
  }
  const testCasesTableHTML = `
    <div class="prac-testcases-wrapper" style="margin-bottom:12px;">
      <div style="font-size:0.76rem;font-weight:700;color:var(--ink-soft);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.04em;">Тестовые случаи:</div>
      <table class="prac-testcases-table">
        <thead><tr><th>Входные данные</th><th>Ожидаемый результат</th><th>Статус</th></tr></thead>
        <tbody>${testCasesRowsHTML}</tbody>
      </table>
    </div>`;

  const isSolved = (solvedMap[curTask.id] === 'solved') || !!practiceHubState.solutionUnlocked;
  const solutionPaneHTML = isSolved ? `
    <div class="prac-solution-pane">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
        <span class="state-tag state-tag--mastered">✓ Эталонное авторское решение</span>
        <span class="topic-badge" style="margin:0;">Сложность: O(n) / O(1)</span>
      </div>
      <h3 style="margin-bottom:8px;">Код решения:</h3>
      <div class="coddy-code-block" style="margin-bottom:12px;white-space:pre-wrap;font-family:var(--font-m);font-size:0.84rem;">${escapeHtmlStr(curTask.solution || '# Эталонное решение принято!')}</div>
      <p class="meta"><strong>Разбор инварианта:</strong> ${escapeHtmlStr(curTask.hint || 'Решение оптимизировано под технический скрининг.')}</p>
    </div>` : `
    <div class="prac-solution-locked">
      <div class="lock-orb">🔒</div>
      <h3>Эталонное решение защищено</h3>
      <p>По Сократовскому регламенту решение открывается после успешной сдачи тестов. Если вы застряли — используйте подсказки во вкладке «Задача».</p>
      <button type="button" class="btn btn-ghost" data-prac-unlock-solution>🔓 Всё равно открыть эталонное решение</button>
    </div>`;

  const docsSearchVal = (practiceHubState.docsSearch || '').toLowerCase();
  const docsCards = [
    { title: 'Функции & Сигнатуры', code: 'def func(arg, *args, default=0, **kwargs) -> int:\n    return default + arg', desc: 'Позиционные и именованные аргументы, дефолтные параметры.' },
    { title: 'Словари dict (O(1))', code: 'val = d.get(key, "default")\nfor k, v in d.items(): pass', desc: 'Хеш-таблица. Поиск, вставка, удаление в среднем O(1).' },
    { title: 'Списки list & Срезы', code: 'rev = lst[::-1]  # разворот срезом\nlst.append(x)    # O(1) амортизированно\nlst.pop()        # O(1) с конца', desc: 'Динамический массив. Вставка в начало O(n).' },
    { title: 'Множества set (O(1))', code: 'union = s1 | s2      # объединение\nintersect = s1 & s2  # пересечение', desc: 'Уникальные неизменяемые элементы. Проверка in за O(1).' },
    { title: 'Очередь collections.deque', code: 'from collections import deque\nq = deque([1, 2, 3])\nq.appendleft(0)  # O(1)', desc: 'Двусвязный список блоков, O(1) с обоих концов.' },
    { title: 'Исключения try..except', code: 'try:\n    risky_operation()\nexcept ValueError as err:\n    pass', desc: 'Перехват конкретных подклассов Exception, raise from.' },
    { title: 'Контекстный менеджер with', code: 'with open("file.txt") as f:\n    content = f.read()', desc: 'Гарантированное освобождение ресурсов.' },
    { title: 'Датаклассы dataclass', code: 'from dataclasses import dataclass\n\n@dataclass\nclass Item:\n    id: int; title: str', desc: 'Автогенерация __init__, __repr__, __eq__.' }
  ].filter(c => !docsSearchVal || c.title.toLowerCase().includes(docsSearchVal) || c.desc.toLowerCase().includes(docsSearchVal) || c.code.toLowerCase().includes(docsSearchVal));

  const docsPaneHTML = `
    <div class="prac-docs-pane">
      <div style="margin-bottom:12px;">
        <input id="prac-docs-search-input" type="text" class="code-editor" style="min-height:auto;padding:8px 12px;font-size:0.84rem;width:100%;" placeholder="Поиск по синтаксису (def, dict, list, deque, with)…" value="${escapeHtmlStr(practiceHubState.docsSearch || '')}">
      </div>
      <div style="display:flex;flex-direction:column;gap:10px;">
        ${docsCards.map(c => `
          <div class="panel" style="padding:12px 14px;">
            <div style="font-weight:700;font-size:0.88rem;margin-bottom:4px;color:var(--emerald);">${escapeHtmlStr(c.title)}</div>
            <p style="font-size:0.78rem;color:var(--ink-soft);margin-bottom:6px;">${escapeHtmlStr(c.desc)}</p>
            <pre class="coddy-code-block" style="padding:8px 10px;font-size:0.78rem;margin:0;"><code>${escapeHtmlStr(c.code)}</code></pre>
          </div>
        `).join('')}
      </div>
    </div>`;

  const cleanDescText = (curTask.desc || '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/^[\s\r\n]*(?:Задание|Задача)\s*[:·\-–—]?\s*/i, '')
    .trim()
    .replace(/\s+/g, ' ');
  const cleanTitleText = (curTask.title || '').trim().replace(/\s+/g, ' ');
  const isDescRedundant = !cleanDescText || cleanDescText === cleanTitleText || cleanDescText === (cleanTitleText + '.');

  const taskConditionHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
      <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;">
        <span class="topic-badge" style="margin:0;">Задача #${curTask.id} · ${curTask.tier} · ${curTask.topic}</span>
        ${renderEchelonBadge(curTaskEchelon)}
        ${solvedMap[curTask.id]==='solved' ? `<span class="state-tag state-tag--mastered" style="margin:0;">✓ Решено</span>` : ''}
      </div>
      <div style="display:inline-flex;gap:4px;align-items:center;" class="prac-inline-swiper">
        <button type="button" class="btn btn-ghost" style="padding:3px 8px;font-size:.74rem;" data-prac-step="-1" ${filtered.length<=1?'disabled':''} title="Предыдущая задача">‹</button>
        <span style="font-size:.75rem;font-weight:700;color:var(--ink-muted);">${filtered.length>0 ? `${curFilteredIdx + 1}/${filtered.length}` : '0/0'}</span>
        <button type="button" class="btn btn-ghost" style="padding:3px 8px;font-size:.74rem;" data-prac-step="1" ${filtered.length<=1?'disabled':''} title="Следующая задача">›</button>
      </div>
    </div>
    <h2 class="prac-task-title">${escapeHtmlStr(curTask.title)}</h2>
    ${signatureBoxHTML}
    ${(!isDescRedundant && curTask.desc) ? `<div class="lesson-theory" style="margin-bottom:10px;">${curTask.desc}</div>` : ''}
    ${plainExplainBtnHTML}
    ${plainExplainBoxHTML}
    <div style="margin-top:10px;">
      <button class="btn btn-ghost" style="padding:6px 12px;font-size:.78rem;" data-prac-hint ${practiceHubState.hintLevel>=socraticHints.length?'disabled':''}>💡 Сократовская подсказка (${practiceHubState.hintLevel}/${socraticHints.length})</button>
    </div>
    ${shownHints}`;

  const codePaneHTML = `
    ${testCasesTableHTML}
    ${buildCodeEditorWithGutterHTML('prac-code-editor', practiceHubState.codeDraft, 240)}
    <div style="margin-top:12px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;">
      <button class="btn btn-3d-orange btn-primary prac-run-btn" data-prac-run="${curTask.id}">▶ Запустить код</button>
      <button class="btn btn-ghost" data-prac-ask-ai>🤖 Спросить ИИ</button>
      <button class="btn btn-ghost" data-prac-reset="${curTask.id}">Сбросить</button>
    </div>
    ${runFeedback}`;

  return `
    <div class="container">
      <div class="prac-hero-header">
        <div>
          <div class="topic-badge">Интегрированный тренажёр с IDE · 401 задача · 7 уровней (🥚 → 👑)</div>
          <h1>💻 Практика кода (${totalSolved} / 401 решено)</h1>
        </div>
        <a href="Практика кода — тренажёр с IDE.html" target="_blank" class="btn btn-ghost" style="padding:8px 13px;font-size:.82rem;">Открыть полноэкранный IDE-тренажёр ↗</a>
      </div>

      ${chipsBarHTML}
      ${searchBarHTML}

      <div class="microstep-card">
        ${mobileTabsHTML}
        <!-- Practice IDE Grid: 4-Tab on Mobile (<768px), 2-Column Split on Desktop (>=769px) -->
        <div class="practice-desktop-grid">
          <div class="practice-left-pane ${curMobTab === 'code' ? 'prac-pane--hidden-mobile' : ''}">
            ${curMobTab === 'docs' ? docsPaneHTML : (curMobTab === 'solution' ? solutionPaneHTML : taskConditionHTML)}
          </div>
          <div class="practice-right-pane ${curMobTab !== 'code' ? 'prac-pane--hidden-mobile' : ''}">
            ${codePaneHTML}
          </div>
        </div>
      </div>
    </div>`;
}

/* ================= 7 MODULE BOSS CHALLENGES (#/<track>/boss) ================= */
const MODULE_BOSS_TASKS = {
  python: {
    id: 'boss-python',
    trackKey: 'python',
    tier: '👑 Уровень 7',
    topic: 'Модуль 01 · 🐍 Python Boss',
    title: 'Транзакционный сейф инвентаря с контекстным менеджером и генератором',
    desc: `<p>Реализуй класс <code>InventoryVault</code>, объединяющий ключевые концепции Модуля 01 (ООП, контекстные менеджеры, исключения и генераторы):</p>
<ul>
  <li><code>__init__(self, initial=None)</code> — сохраняет копию словаря остатков <code>{sku: count}</code> и список журнала операций <code>self.audit_log = []</code>;</li>
  <li><code>adjust(self, sku: str, delta: int) -> int</code> — изменяет остаток товара на <code>delta</code>. Если итоговый остаток становится меньше <code>0</code>, выбрасывает <code>ValueError("insufficient stock")</code> без изменения текущего остатка; иначе записывает кортеж <code>(sku, delta, new_qty)</code> в <code>self.audit_log</code> и возвращает <code>new_qty</code>;</li>
  <li>Контекстный менеджер <code>__enter__</code> / <code>__exit__</code> — при входе делает снимок состояния (остатки и длину <code>audit_log</code>). Если внутри блока <code>with</code> возникло любое исключение, полностью откатывает остатки и <code>audit_log</code> к снимку (и не подавляет исключение);</li>
  <li>Генератор <code>iter_low_stock(self, threshold: int)</code> — лениво (через <code>yield</code>) выдаёт кортежи <code>(sku, qty)</code> для товаров с <code>qty &lt;= threshold</code> в алфавитном порядке <code>sku</code>.</li>
</ul>`,
    hint: 'Используй копирование словаря при входе в контекстный менеджер и восстанавливай состояние в __exit__, если exc_type не равен None.',
    initialCode: `class InventoryVault:
    def __init__(self, initial=None):
        self.stock = dict(initial or {})
        self.audit_log = []

    def adjust(self, sku: str, delta: int) -> int:
        # Твой код здесь
        pass

    def __enter__(self):
        # Сделай снимок для транзакции
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Откати при исключении
        pass

    def iter_low_stock(self, threshold: int):
        # Генератор (yield) отсортированных (sku, qty) при qty <= threshold
        pass
`,
    tests: `
v = InventoryVault({"apple": 5, "banana": 2})
assert v.adjust("apple", -2) == 3, "adjust('apple', -2) должен вернуть новый остаток 3"
assert v.audit_log == [("apple", -2, 3)], f"Неверный журнал операций: {v.audit_log}"
try:
    with v:
        v.adjust("banana", 4)
        v.adjust("apple", -10)
    assert False, "При нехватке остатка должно выбрасываться ValueError"
except ValueError:
    pass
assert v.stock == {"apple": 3, "banana": 2}, f"Откат остатков в __exit__ не сработал: {v.stock}"
assert v.audit_log == [("apple", -2, 3)], f"Откат audit_log в __exit__ не сработал: {v.audit_log}"
gen = v.iter_low_stock(3)
import types
assert isinstance(gen, types.GeneratorType), "iter_low_stock должен быть генератором (использовать yield)"
assert list(gen) == [("apple", 3), ("banana", 2)], "Генератор должен выдавать отсортированные пары (sku, qty)"
`
  },
  web: {
    id: 'boss-web',
    trackKey: 'web',
    tier: '👑 Уровень 7',
    topic: 'Модуль 02 · 🌐 Web Boss',
    title: 'Мини HTTP-роутер с разбором Query-строки, CORS Preflight и 405 Method Not Allowed',
    desc: `<p>Реализуй класс <code>MiniWebRouter</code>, моделирующий работу HTTP-слоя и безопасности из Модуля 02:</p>
<ul>
  <li><code>add_route(self, method: str, path: str, handler)</code> — регистрирует обработчик для HTTP-метода (в верхнем регистре) и пути (без query-строки);</li>
  <li><code>dispatch(self, method: str, raw_url: str, origin: str = "") -> dict</code> — разбирает <code>raw_url</code> на путь и словарь query-параметров <code>params</code> (например, <code>"/items?tag=py&amp;limit=2"</code> → <code>{"tag": "py", "limit": "2"}</code>);</li>
  <li>Если <code>method.upper() == "OPTIONS"</code> и путь зарегистрирован хотя бы для одного метода, возвращает <code>{"status": 204, "headers": {"Access-Control-Allow-Methods": "GET, POST", "Access-Control-Allow-Origin": origin or "*"}, "body": ""}</code> (методы пути в алфавитном порядке через <code>", "</code>);</li>
  <li>Если путь существует, но метод не поддерживается — возвращает <code>{"status": 405, "headers": {}, "body": "Method Not Allowed"}</code>; если путь не найден — <code>status: 404</code> и <code>body: "Not Found"</code>;</li>
  <li>При успешном совпадении вызывает <code>handler(params)</code> и возвращает <code>{"status": 200, "headers": {"Access-Control-Allow-Origin": origin or "*"}, "body": result}</code>.</li>
</ul>`,
    hint: 'Храни маршруты в вложенном словаре path -> {method: handler}, а строку запроса отделяй через split("?", 1).',
    initialCode: `class MiniWebRouter:
    def __init__(self):
        self.routes = {}

    def add_route(self, method: str, path: str, handler):
        # Зарегистрируй маршрут
        pass

    def dispatch(self, method: str, raw_url: str, origin: str = "") -> dict:
        # Разбери raw_url, обработай OPTIONS, 404, 405 и 200
        pass
`,
    tests: `
r = MiniWebRouter()
r.add_route("GET", "/items", lambda p: f"items:{p.get('tag','all')}")
r.add_route("POST", "/items", lambda p: "created")
res_ok = r.dispatch("GET", "/items?tag=books", "https://app.example")
assert res_ok == {"status": 200, "headers": {"Access-Control-Allow-Origin": "https://app.example"}, "body": "items:books"}, f"Неверный ответ для GET /items?tag=books: {res_ok}"
res_opt = r.dispatch("OPTIONS", "/items", "https://app.example")
assert res_opt and res_opt.get("status") == 204 and res_opt.get("headers", {}).get("Access-Control-Allow-Methods") == "GET, POST", f"Неверный CORS preflight ответ: {res_opt}"
res_405 = r.dispatch("DELETE", "/items")
assert res_405 and res_405.get("status") == 405, f"Ожидался статус 405 для неподдерживаемого метода: {res_405}"
res_404 = r.dispatch("GET", "/missing")
assert res_404 and res_404.get("status") == 404, f"Ожидался статус 404 для неизвестного пути: {res_404}"
`
  },
  backend: {
    id: 'boss-backend',
    trackKey: 'backend',
    tier: '👑 Уровень 7',
    topic: 'Модуль 03 · ⚙️ Backend Boss',
    title: 'Сервисный слой заказов с Unit of Work и идемпотентным ключом',
    desc: `<p>Реализуй функцию сервисного слоя <code>process_checkout(uow, user_id: int, sku: str, qty: int, idem_key: str) -> dict</code>:</p>
<ul>
  <li>Объект <code>uow</code> поддерживает контекстный менеджер <code>with uow:</code>, хранит словарь остатков <code>uow.stock</code>, список заказов <code>uow.orders</code>, словарь идемпотентности <code>uow.idem_cache</code> и метод <code>uow.commit()</code>;</li>
  <li>Если <code>idem_key</code> уже есть в <code>uow.idem_cache</code>, функция мгновенно возвращает сохранённый заказ без повторного списания;</li>
  <li>Если <code>qty &lt;= 0</code> или остатка <code>uow.stock.get(sku, 0) &lt; qty</code>, выбрасывает <code>ValueError("out of stock")</code> внутри контекста <code>with uow:</code> (так, чтобы <code>uow.committed</code> остался <code>False</code>);</li>
  <li>Иначе уменьшает <code>uow.stock[sku]</code> на <code>qty</code>, добавляет заказ <code>{"order_id": len(uow.orders) + 1, "user_id": user_id, "sku": sku, "qty": qty}</code> в <code>uow.orders</code>, сохраняет его в <code>uow.idem_cache[idem_key]</code>, вызывает <code>uow.commit()</code> и возвращает словарь заказа.</li>
</ul>`,
    hint: 'Проверяй ключ идемпотентности до списания остатков, а изменения вноси внутри блока with uow и завершай вызовом uow.commit().',
    initialCode: `class FakeUoW:
    def __init__(self, stock):
        self.stock = dict(stock)
        self.orders = []
        self.idem_cache = {}
        self.committed = False
        self._snap = None

    def __enter__(self):
        self.committed = False
        self._snap = (dict(self.stock), list(self.orders), dict(self.idem_cache))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None or not self.committed:
            self.stock, self.orders, self.idem_cache = self._snap

    def commit(self):
        self.committed = True

def process_checkout(uow: FakeUoW, user_id: int, sku: str, qty: int, idem_key: str) -> dict:
    # Реализуй идемпотентное оформление заказа через uow
    pass
`,
    tests: `
uow = FakeUoW({"book": 5})
o1 = process_checkout(uow, 10, "book", 2, "key-1")
assert o1 == {"order_id": 1, "user_id": 10, "sku": "book", "qty": 2}, f"Неверный словарь заказа: {o1}"
assert uow.stock["book"] == 3 and uow.committed is True, "Остаток должен уменьшиться до 3 и uow.commit() должен быть вызван"
o1_dup = process_checkout(uow, 10, "book", 2, "key-1")
assert o1_dup == o1 and uow.stock["book"] == 3 and len(uow.orders) == 1, "Повторный вызов с тем же idem_key не должен списывать остаток повторно"
try:
    process_checkout(uow, 10, "book", 10, "key-2")
    assert False, "При нехватке товара должно выбрасываться ValueError('out of stock')"
except ValueError:
    pass
assert uow.stock["book"] == 3 and len(uow.orders) == 1, "При ошибке транзакция UoW должна откатываться"
`
  },
  algorithms: {
    id: 'boss-algorithms',
    trackKey: 'algorithms',
    tier: '👑 Уровень 7',
    topic: 'Модуль 04 · ⚡ Алгоритмы Boss',
    title: 'Планировщик DAG-пайплайна: топологическая сортировка Кана и критический путь',
    desc: `<p>Реализуй функцию <code>schedule_pipeline(durations: dict, deps: list) -> tuple</code>:</p>
<ul>
  <li><code>durations</code> — словарь <code>{task_name: duration_sec}</code>;</li>
  <li><code>deps</code> — список пар <code>(prerequisite, dependent)</code>, означающих, что <code>dependent</code> может стартовать только после завершения <code>prerequisite</code>;</li>
  <li>Если в графе есть цикл, выброси <code>ValueError("cycle")</code>;</li>
  <li>Верни кортеж <code>(topo_order, total_critical_time)</code>, где <code>topo_order</code> — лексикографически минимальный топологический порядок (используй очередь с приоритетом <code>heapq</code> для вершин с <code>in_degree == 0</code>), а <code>total_critical_time</code> — минимальное время выполнения всего пайплайна при параллельном запуске независимых задач (длина критического пути).</li>
</ul>`,
    hint: 'Используй алгоритм Кана с кучей heapq для лексикографического порядка и массив динамического программирования earliest_finish[v] = max(earliest_finish[u]) + duration[v].',
    initialCode: `import heapq

def schedule_pipeline(durations: dict, deps: list) -> tuple:
    # Верни (topo_order, critical_path_time) или выброси ValueError("cycle")
    pass
`,
    tests: `
dur = {"lint": 2, "test": 5, "build": 4, "deploy": 3}
edges = [("lint", "build"), ("test", "build"), ("build", "deploy")]
res_sched = schedule_pipeline(dur, edges)
assert isinstance(res_sched, tuple) and len(res_sched) == 2, f"Функция должна возвращать кортеж (topo_order, total_critical_time), получено: {res_sched}"
order, total = res_sched
assert order == ["lint", "test", "build", "deploy"], f"Неверный топологический порядок: {order}"
assert total == 12, f"Ожидалась длина критического пути 12, получено: {total}"
try:
    schedule_pipeline({"a": 1, "b": 1}, [("a", "b"), ("b", "a")])
    assert False, "При наличии цикла должно выбрасываться ValueError('cycle')"
except ValueError:
    pass
`
  },
  databases: {
    id: 'boss-databases',
    trackKey: 'databases',
    tier: '👑 Уровень 7',
    topic: 'Модуль 05 · 🗄️ Базы данных Boss',
    title: 'Аналитика платежей на SQLite: CTE, оконный ранг DENSE_RANK и атомарный перевод',
    desc: `<p>Используя встроенный модуль <code>sqlite3</code>, реализуй функцию <code>run_billing_analytics(movements: list) -> list</code>:</p>
<ul>
  <li>Создай в памяти (<code>:memory:</code>) таблицу <code>payments(user_name TEXT, region TEXT, amount INTEGER)</code> и вставь туда кортежи из <code>movements</code> параметризованным запросом <code>executemany</code>;</li>
  <li>Напиши SQL-запрос с <code>WITH totals AS (...)</code> и оконной функцией <code>DENSE_RANK() OVER (PARTITION BY region ORDER BY total_amount DESC)</code>, который считает суммарный платёж каждого пользователя в регионе;</li>
  <li>Верни список кортежей <code>(region, user_name, total_amount, rnk)</code> только для лидеров с рангом <code>rnk == 1</code>, отсортированный по <code>region ASC, user_name ASC</code>.</li>
</ul>`,
    hint: 'Сначала агрегируй SUM(amount) GROUP BY region, user_name в CTE, а во внешнем запросе примени DENSE_RANK() OVER (PARTITION BY region ORDER BY total_amount DESC).',
    initialCode: `import sqlite3

def run_billing_analytics(movements: list) -> list:
    # Создай таблицу в :memory:, выполни CTE + DENSE_RANK и верни лидеров по регионам
    pass
`,
    tests: `
data = [
    ("Alice", "EU", 100), ("Alice", "EU", 50),
    ("Bob", "EU", 120),
    ("Cara", "US", 200), ("Dan", "US", 200), ("Eve", "US", 90)
]
res = run_billing_analytics(data)
assert res == [("EU", "Alice", 150, 1), ("US", "Cara", 200, 1), ("US", "Dan", 200, 1)], f"Неверный результат лидеров по регионам: {res}"
`
  },
  architecture: {
    id: 'boss-architecture',
    trackKey: 'architecture',
    tier: '👑 Уровень 7',
    topic: 'Модуль 06 · 🏛️ Архитектура Boss',
    title: 'Отказоустойчивый шлюз: Circuit Breaker (CLOSED / OPEN / HALF_OPEN)',
    desc: `<p>Реализуй класс <code>CircuitBreakerGateway</code> из Модуля 06:</p>
<ul>
  <li><code>__init__(self, failure_threshold: int = 2, recovery_timeout: float = 10.0)</code> — начальное состояние <code>self.state = "CLOSED"</code>, счётчик подряд идущих сбоев <code>self.failures = 0</code>, время последнего сбоя <code>self.opened_at = 0.0</code>;</li>
  <li><code>call(self, func, now_ts: float)</code>:
    <ul>
      <li>Если <code>self.state == "OPEN"</code>: когда <code>now_ts - self.opened_at &gt;= self.recovery_timeout</code>, переводит состояние в <code>"HALF_OPEN"</code>; иначе немедленно выбрасывает <code>RuntimeError("circuit open")</code> без вызова <code>func</code>;</li>
      <li>Вызывает <code>func()</code>: при успехе сбрасывает <code>self.failures = 0</code>, ставит <code>self.state = "CLOSED"</code> и возвращает результат;</li>
      <li>Если <code>func()</code> выбросила исключение: увеличивает <code>self.failures += 1</code>; если состояние было <code>"HALF_OPEN"</code> или <code>self.failures &gt;= self.failure_threshold</code>, переводит в <code>"OPEN"</code> и записывает <code>self.opened_at = now_ts</code>; пробрасывает исходное исключение дальше.</li>
    </ul>
  </li>
</ul>`,
    hint: 'Перед вызовом функции проверь переход из OPEN в HALF_OPEN по таймеру, а в блоке except обновляй счётчик сбоев и метку времени opened_at.',
    initialCode: `class CircuitBreakerGateway:
    def __init__(self, failure_threshold: int = 2, recovery_timeout: float = 10.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "CLOSED"
        self.failures = 0
        self.opened_at = 0.0

    def call(self, func, now_ts: float):
        # Реализуй автомат состояний CLOSED -> OPEN -> HALF_OPEN -> CLOSED
        pass
`,
    tests: `
cb = CircuitBreakerGateway(failure_threshold=2, recovery_timeout=5.0)
assert cb.call(lambda: "ok", 1.0) == "ok", "В состоянии CLOSED успешный вызов должен возвращать результат"
for ts in (2.0, 3.0):
    try:
        cb.call(lambda: (_ for _ in ()).throw(ValueError("boom")), ts)
    except ValueError:
        pass
assert cb.state == "OPEN", f"После достижения порога ошибок состояние должно стать OPEN, получено: {cb.state}"
try:
    cb.call(lambda: "ok", 4.0)
    assert False, "В состоянии OPEN до истечения recovery_timeout должен выбрасываться RuntimeError"
except RuntimeError:
    pass
assert cb.call(lambda: "recovered", 9.0) == "recovered", "После истечения recovery_timeout пробный вызов должен пройти через HALF_OPEN"
assert cb.state == "CLOSED" and cb.failures == 0, "После успешного вызова в HALF_OPEN состояние должно вернуться в CLOSED со сбросом failures"
`
  },
  infra: {
    id: 'boss-infra',
    trackKey: 'infra',
    tier: '👑 Уровень 7',
    topic: 'Модуль 07 · 🚀 Инфраструктура Boss',
    title: 'Аудитор продакшен-инфраструктуры: Dockerfile + Healthcheck Readiness Gate',
    desc: `<p>Реализуй функцию <code>audit_release_gate(dockerfile_text: str, probes: dict) -> dict</code>, объединяющую практики Docker, CI/CD и мониторинга из Модуля 07:</p>
<ul>
  <li>Проверяет строки <code>dockerfile_text</code> (игнорируя пустые строки и комментарии <code>#</code>):
    <ul>
      <li><code>"unpinned_base"</code> — если первая инструкция <code>FROM</code> использует тег <code>:latest</code> или вообще не содержит двоеточия <code>:</code> в имени образа;</li>
      <li><code>"missing_user"</code> — если в Dockerfile нет ни одной инструкции <code>USER</code> с пользователем, отличным от <code>root</code>;</li>
      <li><code>"secret_in_env"</code> — если в инструкции <code>ENV</code> встречается подстрока <code>SECRET</code> или <code>PASSWORD</code> (без учёта регистра);</li>
    </ul>
  </li>
  <li>Проверяет словарь проб <code>probes</code> вида <code>{"db": {"ok": True, "latency_ms": 12}, ...}</code>: сервис считается здоровым (<code>probes_healthy = True</code>), только если словарь не пуст и у каждой пробы <code>ok == True</code> и <code>latency_ms &lt;= 500</code>;</li>
  <li>Возвращает словарь <code>{"issues": issues_list, "probes_healthy": bool, "ready": len(issues_list) == 0 and probes_healthy}</code> (список <code>issues</code> в порядке проверок выше).</li>
</ul>`,
    hint: 'Разбей dockerfile_text по строкам, отфильтруй комментарии с #, проверь FROM/USER/ENV и отдельно проверь все элементы словаря probes.values().',
    initialCode: `def audit_release_gate(dockerfile_text: str, probes: dict) -> dict:
    # Проведи аудит Dockerfile и проб здоровья для продакшен-релиза
    pass
`,
    tests: `
bad_df = "\\n".join(["# comment", "FROM python:latest", "ENV DB_PASSWORD=123", "COPY . /app"])
r1 = audit_release_gate(bad_df, {"db": {"ok": True, "latency_ms": 20}, "redis": {"ok": True, "latency_ms": 800}})
assert r1 == {"issues": ["unpinned_base", "missing_user", "secret_in_env"], "probes_healthy": False, "ready": False}, f"Неверный результат аудита проблемного Dockerfile: {r1}"

good_df = "\\n".join(["FROM python:3.12-slim", "WORKDIR /app", "USER appuser", "CMD ['uvicorn', 'app:app']"])
r2 = audit_release_gate(good_df, {"db": {"ok": True, "latency_ms": 15}, "redis": {"ok": True, "latency_ms": 8}})
assert r2 == {"issues": [], "probes_healthy": True, "ready": True}, f"Неверный результат аудита эталонного Dockerfile: {r2}"
`
  }
};
window.MODULE_BOSS_TASKS = MODULE_BOSS_TASKS;

let bossViewState = { trackKey: null, codeDraft: '', hintLevel: 0, runStatus: null, runOutput: '' };

function viewModuleBoss(trackKey){
  const tr = MASTERY_TRACKS[trackKey] || MASTERY_TRACKS.python;
  const boss = MODULE_BOSS_TASKS[tr.key] || MODULE_BOSS_TASKS.python;
  if(bossViewState.trackKey !== tr.key){
    bossViewState = {
      trackKey: tr.key,
      codeDraft: getIdeDraft(boss.id, boss.initialCode),
      hintLevel: 0,
      runStatus: null,
      runOutput: ''
    };
  }
  const isPassed = (state.passedBosses || []).includes(tr.key) || bossViewState.runStatus === 'pass';
  const bossHpPct = isPassed ? 0 : (bossViewState.runStatus === 'running' ? 35 : 100);
  const socraticHints = buildSocraticHintsForTask(boss);
  const socraticLabels = [
    'Уровень 0 (Zero Hint — Граничные условия)',
    'Уровень 1 (Conceptual Hint — Концепция)',
    'Уровень 2 (Structural Hint — Декомпозиция)',
    'Уровень 3 (Tactical Hint — Сигнатура и контракт)'
  ];
  const shownHints = socraticHints.slice(0, bossViewState.hintLevel).map((h, idx) =>
    `<div class="hint-box"><strong>${socraticLabels[idx] || ('Уровень опоры ' + idx)}:</strong> ${h}</div>`
  ).join('');

  let runFeedback = '';
  if(bossViewState.runStatus === 'running') runFeedback = `<div class="test-running-shimmer" style="margin-top:10px;">⚔️ Атака на Босса: прогоняю боевые тесты модуля…</div>`;
  else if(bossViewState.runStatus === 'pass') runFeedback = `<div class="result-box--pass correct-pulse-anim">${ICONS.check} 👑 Босс модуля «${tr.title}» повержен! (+100 XP, все навыки модуля повышены до 100 MP!)\n${bossViewState.runOutput||''}</div>`;
  else if(bossViewState.runStatus === 'fail') runFeedback = `<div class="result-box--fail">Испытание Босса пока не пройдено:\n${bossViewState.runOutput||''}</div>`;

  const victoryBannerHTML = isPassed ? `
    <div class="boss-victory-banner">
      <div style="font-size:1.5rem;">🏆👑✨</div>
      <div>
        <div style="font-weight:800;font-size:.98rem;">Босс модуля «${tr.title}» повержен!</div>
        <div class="meta" style="font-size:.8rem;">Все навыки трека получили ранг Мастерства (100 MP). Награда +100 XP зачислена.</div>
      </div>
    </div>` : '';

  return `
    <div class="container">
      <a href="#${tr.routePrefix}" class="back-link">${ICONS.chevronLeft} ${tr.backLabel}</a>
      <div class="microstep-card boss-arena-card">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
          <span class="topic-badge" style="margin:0;">${boss.tier} · ${boss.topic} · +100 XP</span>
          ${isPassed ? `<span class="state-tag state-tag--mastered" style="margin:0;">👑 Босс взят</span>` : `<span class="state-tag state-tag--available" style="margin:0;">Финальное испытание модуля</span>`}
        </div>
        <div class="boss-hp-wrap boss-hp-bar">
          <div class="boss-hp-header boss-hp-bar__label">
            <span>🐉 HP Босса модуля «${tr.title}»</span>
            <span class="boss-hp-val">${bossHpPct}% HP</span>
          </div>
          <div class="boss-hp-track"><div class="boss-hp-fill boss-hp-bar__fill" style="width:${bossHpPct}%;"></div></div>
        </div>
        ${victoryBannerHTML}
        <h1 style="margin-bottom:10px;">👑 ${boss.title}</h1>
        <div class="lesson-theory" style="margin-bottom:14px;">${boss.desc}</div>
        ${buildCodeEditorWithGutterHTML('boss-code-editor', bossViewState.codeDraft, 'min-height:240px;', 'boss-code-editor')}
        <div style="margin-top:12px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;">
          <button class="btn btn-primary" data-boss-run="${tr.key}">${ICONS.play} Проверить решение Босса (Ctrl+Enter)</button>
          <button class="btn btn-ghost" data-boss-hint ${bossViewState.hintLevel>=socraticHints.length?'disabled':''}>💡 Сократовская наводка (${bossViewState.hintLevel}/${socraticHints.length})</button>
          <button class="btn btn-ghost" data-boss-reset="${tr.key}">Сбросить шаблон</button>
        </div>
        ${runFeedback}
        ${shownHints}
      </div>
    </div>`;
}

/* ================= INTERACTIVE MOCK INTERVIEW SIMULATOR (#/mock & #/interview-sim) ================= */
const STAR_SCENARIOS = [
  {
    id: 'star-incident',
    title: '🔥 Инцидент в продакшене: деградация БД и таймауты API',
    prompt: 'Расскажи о случае, когда сервис в продакшене начал отвечать медленно или падать с 502/504. Как ты локализовал узкое место и какие инженерные меры внедрил?',
    demo: {
      s: 'В продакшен-сервисе оформления заказов на FastAPI + PostgreSQL при росте трафика до 350 RPS время ответа эндпоинта /orders выросло до 3800 мс и появились ошибки 504.',
      t: 'Необходимо было оперативно локализовать узкое место, снизить p95 латентность ниже 120 мс и устранить таймауты без простоя сервиса.',
      a: 'Я проанализировал медленные запросы через pg_stat_statements и EXPLAIN ANALYZE, обнаружил Seq Scan по таблице заказов и исчерпание пула соединений, после чего создал индекс CONCURRENTLY и настроил таймауты пула.',
      r: 'Латентность p95 снизилась с 3800 мс до 42 мс (ускорение в 90 раз), загрузка CPU базы упала на 65%, а ошибки 504 сократились до 0%.'
    }
  },
  {
    id: 'star-nplus1',
    title: '🗄️ Оптимизация N+1 запросов и ускорение эндпоинта в 10 раз',
    prompt: 'Опиши ситуацию, когда эндпоинт ORM (Django/SQLAlchemy) генерировал сотни SQL-запросов. Как ты обнаружил проблему и как доказал эффект оптимизации?',
    demo: {
      s: 'В каталоге товаров на SQLAlchemy 2.0 эндпоинт выдачи списка из 100 карточек с категориями и остатками выполнялся 1400 мс при каждом открытии витрины.',
      t: 'Требовалось сократить число SQL-запросов к БД до константного значения O(1) и уложить время ответа эндпоинта в SLA 100 мс.',
      a: 'Я включил логирование SQL-запросов в тестах, выявил классическую проблему N+1 (201 запрос на страницу), заменил ленивую подгрузку связей на joinedload и selectinload и зафиксировал лимит запросов автотестом.',
      r: 'Количество SQL-запросов на один HTTP-вызов сократилось с 201 до 2, а среднее время ответа эндпоинта уменьшилось с 1400 мс до 55 мс (в 25 раз).'
    }
  },
  {
    id: 'star-review',
    title: '🤝 Архитектурный спор на Code Review (монолит, DI, тестируемость)',
    prompt: 'Расскажи о техническом разногласии с коллегой или ревьюером по поводу архитектуры кода. Как вы пришли к решению на основе инженерных аргументов?',
    demo: {
      s: 'При разработке модуля оплаты в FastAPI бизнес-логика расчёта скидок и прямые HTTP-вызовы внешнего платёжного шлюза оказались жёстко зашиты внутри роутера.',
      t: 'Нужно было убедить команду разделить слои и внедрить инверсию зависимостей (DI), чтобы модуль можно было тестировать без реальных сетевых вызовов.',
      a: 'Я подготовил наглядный прототип с выделением сервисного слоя и абстрактного протокола PaymentGateway, показал на Code Review, как легко подменять шлюз фейком в unit-тестах, и замерил скорость прогона.',
      r: 'Команда приняла паттерн сервисного слоя и DI: время прогона тестов модуля сократилось с 18 сек до 0.4 сек, а покрытие сложной логики скидок выросло с 35% до 94%.'
    }
  },
  {
    id: 'star-ci',
    title: '🚀 Автоматизация CI/CD и спасение релиза от регрессии',
    prompt: 'Вспомни случай, когда баг просочился (или чуть не просочился) в релиз из-за ручной проверки. Как ты настроил пайплайн линтеров, pytest и миграций?',
    demo: {
      s: 'В командном проекте деплой выполнялся вручную по SSH, из-за чего в стейджинг дважды попадали конфликтующие миграции Alembic и неформатированный код с багами типизации.',
      t: 'Необходимо было построить автоматический CI-пайплайн в GitHub Actions, блокирующий слияние PR при любой ошибке линтера, типизации, миграций или тестов.',
      a: 'Я настроил workflow с кэшированием зависимостей, проверками ruff и mypy, поднятием тестового контейнера PostgreSQL через services, прогоном alembic upgrade head и запуском pytest с порогом покрытия.',
      r: 'Число регрессий после релиза упало до 0 за следующие 3 месяца, время ревью сократилось на 40%, а сборка пайплайна занимает всего 95 секунд благодаря кэшированию.'
    }
  }
];
window.STAR_SCENARIOS = STAR_SCENARIOS;

const MOCK_CURATED_TASK_IDS = [240, 260, 295, 330, 355, 85, 165, 215, 390];

const _initStarDrafts = (state && state.starDrafts && typeof state.starDrafts === 'object') ? state.starDrafts : {};
const _initStarFirst = _initStarDrafts['star-incident'] || { s: '', t: '', a: '', r: '' };
let mockInterviewState = {
  tab: 'live', // 'live' | 'star'
  echelonFilter: 'auto', // 'auto' | '1' | '2' | '3'
  secondsLeft: 20 * 60,
  running: false,
  intervalId: null,
  pitchSecondsLeft: 120,
  pitchRunning: false,
  pitchIntervalId: null,
  taskId: 240,
  codeDraft: '',
  hintLevel: 0,
  runStatus: null,
  runOutput: '',
  starScenarioId: 'star-incident',
  starS: _initStarFirst.s || '',
  starT: _initStarFirst.t || '',
  starA: _initStarFirst.a || '',
  starR: _initStarFirst.r || '',
  starDraftsByScenario: Object.assign({}, _initStarDrafts),
  starEval: null
};
window.mockInterviewState = mockInterviewState;

function getActiveMockEchelon(){
  if(mockInterviewState.echelonFilter && mockInterviewState.echelonFilter !== 'auto'){
    return parseInt(mockInterviewState.echelonFilter, 10) || 1;
  }
  if(getEchelonProgress(1).pct < 50) return 1;
  if(getEchelonProgress(2).pct < 50) return 2;
  return 3;
}
window.getActiveMockEchelon = getActiveMockEchelon;

function getMockCandidateTasks(){
  const effTier = getActiveMockEchelon();
  const matching = IDE_TASKS.filter(t => getTaskInterviewTier(t.id) === effTier);
  return matching.length > 0 ? matching : IDE_TASKS;
}

function syncActiveEditorDrafts(){
  const labEd = document.getElementById('skill-lab-scratchpad');
  if(labEd && typeof labEd.value === 'string' && pySkillViewState && pySkillViewState.sid){
    if(!pySkillViewState.labDrafts) pySkillViewState.labDrafts = {};
    const activeK = pySkillViewState.kId || 'unknown';
    const stepIdx = pySkillViewState.stepIdx || 0;
    const dKey = `${pySkillViewState.sid}:${activeK}:${stepIdx}`;
    pySkillViewState.labDrafts[dKey] = labEd.value;
  }
  const pyEd = document.getElementById('py-skill-editor');
  if(pyEd && typeof pyEd.value === 'string' && pyEd.value.length > 0){
    pySkillViewState.codeDraft = pyEd.value;
    if(pySkillViewState.taskId) saveIdeDraft(pySkillViewState.taskId, pyEd.value);
  }
  const pracEd = document.getElementById('prac-code-editor');
  if(pracEd && typeof pracEd.value === 'string' && pracEd.value.length > 0){
    practiceHubState.codeDraft = pracEd.value;
    if(practiceHubState.taskId) saveIdeDraft(practiceHubState.taskId, pracEd.value);
  }
  const bossEd = document.getElementById('boss-code-editor');
  if(bossEd && typeof bossEd.value === 'string' && bossEd.value.length > 0){
    bossViewState.codeDraft = bossEd.value;
    const boss = MODULE_BOSS_TASKS[bossViewState.trackKey];
    if(boss) saveIdeDraft(boss.id, bossEd.value);
  }
  const mockEd = document.getElementById('mock-code-editor');
  if(mockEd && typeof mockEd.value === 'string' && mockEd.value.length > 0){
    mockInterviewState.codeDraft = mockEd.value;
    if(mockInterviewState.taskId) saveIdeDraft(mockInterviewState.taskId, mockEd.value);
  }
  const sEl = document.getElementById('star-s-input');
  const tEl = document.getElementById('star-t-input');
  const aEl = document.getElementById('star-a-input');
  const rEl = document.getElementById('star-r-input');
  if(sEl && typeof sEl.value === 'string' && sEl.value.length > 0) mockInterviewState.starS = sEl.value;
  if(tEl && typeof tEl.value === 'string' && tEl.value.length > 0) mockInterviewState.starT = tEl.value;
  if(aEl && typeof aEl.value === 'string' && aEl.value.length > 0) mockInterviewState.starA = aEl.value;
  if(rEl && typeof rEl.value === 'string' && rEl.value.length > 0) mockInterviewState.starR = rEl.value;
  if(mockInterviewState.starScenarioId){
    ensureExtendedState();
    const curStar = {
      s: mockInterviewState.starS || '',
      t: mockInterviewState.starT || '',
      a: mockInterviewState.starA || '',
      r: mockInterviewState.starR || ''
    };
    mockInterviewState.starDraftsByScenario[mockInterviewState.starScenarioId] = curStar;
    state.starDrafts[mockInterviewState.starScenarioId] = curStar;
    saveState(state);
  }
}

function toggleMockTimer(){
  syncActiveEditorDrafts();
  if(mockInterviewState.running){
    mockInterviewState.running = false;
    if(mockInterviewState.intervalId){ clearInterval(mockInterviewState.intervalId); mockInterviewState.intervalId = null; }
  } else {
    mockInterviewState.running = true;
    mockInterviewState.intervalId = setInterval(function(){
      if(mockInterviewState.secondsLeft > 0){
        mockInterviewState.secondsLeft--;
        const isWarn = mockInterviewState.secondsLeft <= 600;
        const isDang = mockInterviewState.secondsLeft <= 180;
        const rCol = isDang ? '#ef4444' : (isWarn ? '#d97706' : 'var(--moss)');
        const el = document.getElementById('mock-timer-display');
        if(el){
          el.textContent = formatPomo(mockInterviewState.secondsLeft);
          el.style.color = rCol;
        }
        const wrapEl = document.querySelector('.mock-timer-ring-wrap');
        if(wrapEl){
          wrapEl.classList.toggle('mock-timer--warn', isWarn && !isDang);
          wrapEl.classList.toggle('mock-timer--danger', isDang);
        }
        const ringEl = document.getElementById('mock-timer-ring-fg');
        if(ringEl){
          const totalSec = 20 * 60;
          const circum = 138.2;
          const offset = circum * (1 - (mockInterviewState.secondsLeft / totalSec));
          ringEl.setAttribute('stroke-dashoffset', String(offset.toFixed(1)));
          ringEl.setAttribute('stroke', rCol);
        }
      } else {
        clearInterval(mockInterviewState.intervalId);
        mockInterviewState.intervalId = null;
        mockInterviewState.running = false;
        render();
      }
    }, 1000);
  }
  render();
}

function resetMockTimer(){
  syncActiveEditorDrafts();
  mockInterviewState.running = false;
  if(mockInterviewState.intervalId){ clearInterval(mockInterviewState.intervalId); mockInterviewState.intervalId = null; }
  mockInterviewState.secondsLeft = 20 * 60;
  render();
}

function toggleStarPitchTimer(){
  syncActiveEditorDrafts();
  if(mockInterviewState.pitchRunning){
    mockInterviewState.pitchRunning = false;
    if(mockInterviewState.pitchIntervalId){ clearInterval(mockInterviewState.pitchIntervalId); mockInterviewState.pitchIntervalId = null; }
  } else {
    mockInterviewState.pitchRunning = true;
    mockInterviewState.pitchIntervalId = setInterval(function(){
      if(mockInterviewState.pitchSecondsLeft > 0){
        mockInterviewState.pitchSecondsLeft--;
        const el = document.getElementById('star-pitch-display');
        if(el) el.textContent = formatPomo(mockInterviewState.pitchSecondsLeft);
      } else {
        clearInterval(mockInterviewState.pitchIntervalId);
        mockInterviewState.pitchIntervalId = null;
        mockInterviewState.pitchRunning = false;
        render();
      }
    }, 1000);
  }
  render();
}

function resetStarPitchTimer(){
  syncActiveEditorDrafts();
  mockInterviewState.pitchRunning = false;
  if(mockInterviewState.pitchIntervalId){ clearInterval(mockInterviewState.pitchIntervalId); mockInterviewState.pitchIntervalId = null; }
  mockInterviewState.pitchSecondsLeft = 120;
  render();
}

function evaluateStarResponse(s, t, a, r){
  const actionVerbRe = /(^|[\s,.!?;:«"(\[])(я|мной|мною|лично|самостоятельно|реализовал[аи]?|настроил[аи]?|проверил[аи]?|провел[аи]?|выявил[аи]?|локализовал[аи]?|устранил[аи]?|заменил[аи]?|написал[аи]?|добавил[аи]?|оптимизировал[аи]?|внедрил[аи]?|исправил[аи]?|проанализировал[аи]?|спроектировал[аи]?|переписал[аи]?|развернул[аи]?|замерил[аи]?|покрыл[аи]?|изолировал[аи]?|выделил[аи]?|сократил[аи]?|ускорил[аи]?|диагностировал[аи]?|автоматизировал[аи]?)(?=$|[\s,.!?;:»")\]])/i;
  const checks = [
    { ok: String(s || '').trim().length >= 25, label: 'Situation: описан конкретный технический контекст системы и масштаб' },
    { ok: String(t || '').trim().length >= 20, label: 'Task: чётко сформулирована инженерная цель и ограничения (SLA / срок / ресурсы)' },
    { ok: String(a || '').trim().length >= 35 && actionVerbRe.test(String(a || '')), label: 'Action: фокус на твоих личных инженерных действиях («я диагностировал / внедрил»), а не размытом «мы»' },
    { ok: String(r || '').trim().length >= 25 && /(\d+|%|мс|ms|сек|раз|x|нуля|0)/i.test(String(r || '')), label: 'Result: результат оцифрован измеримыми метриками (время ответа, % покрытия, число ошибок)' }
  ];
  const score = checks.filter(c => c.ok).length;
  return { score: score, total: checks.length, checks: checks, passed: score >= 3 };
}
window.evaluateStarResponse = evaluateStarResponse;

function viewMockInterview(){
  const curTask = IDE_TASKS_BY_ID[mockInterviewState.taskId] || IDE_TASKS[0];
  if(!mockInterviewState.codeDraft){
    mockInterviewState.codeDraft = getIdeDraft(curTask.id, curTask.initialCode);
  }
  const socraticHints = buildSocraticHintsForTask(curTask);
  const socraticLabels = [
    'Уровень 0 (Zero Hint — Граничные условия)',
    'Уровень 1 (Conceptual Hint — Концепция)',
    'Уровень 2 (Structural Hint — Декомпозиция)',
    'Уровень 3 (Tactical Hint — Сигнатура и контракт)'
  ];
  const shownHints = socraticHints.slice(0, mockInterviewState.hintLevel).map((h, idx) =>
    `<div class="chat-bubble chat-bubble--interviewer hint-box">
      <div class="chat-bubble__author">🎙️ Tech Lead · ${socraticLabels[idx] || ('Уровень опоры ' + idx)}</div>
      <div>${h}</div>
    </div>`
  ).join('');

  let runFeedback = '';
  if(mockInterviewState.runStatus === 'running') runFeedback = `<div class="test-running-shimmer" style="margin-top:10px;">⏳ Проверяю код кандидата на тестовом наборе…</div>`;
  else if(mockInterviewState.runStatus === 'pass') runFeedback = `<div class="result-box--pass correct-pulse-anim">${ICONS.check} Live-Coding раунд успешно пройден! (+40 XP, уровень подсказок сброшен к Уровню 0)\n${mockInterviewState.runOutput||''}</div>`;
  else if(mockInterviewState.runStatus === 'fail') runFeedback = `<div class="result-box--fail">Тесты собеседования не прошли:\n${mockInterviewState.runOutput||''}</div>`;

  const effEchelon = getActiveMockEchelon();
  const stagePool = getMockCandidateTasks().slice(0, 25).map(t => t.id);
  const baseCurated = mockInterviewState.echelonFilter === 'auto'
    ? MOCK_CURATED_TASK_IDS
    : MOCK_CURATED_TASK_IDS.filter(id => getTaskInterviewTier(id) === effEchelon);
  const poolIds = Array.from(new Set([curTask.id].concat(baseCurated).concat(stagePool))).filter(id => IDE_TASKS_BY_ID[id]);
  const taskOpts = poolIds.map(id => {
    const t = IDE_TASKS_BY_ID[id];
    const tTier = getTaskInterviewTier(t.id);
    const eMeta = INTERVIEW_ECHELONS[tTier] || INTERVIEW_ECHELONS[2];
    return `<option value="${t.id}" ${t.id===curTask.id?'selected':''}>#${t.id} [${eMeta.shortLabel} · ${t.tier}] ${t.title} (${t.topic})</option>`;
  }).join('');

  const curTaskTier = getTaskInterviewTier(curTask.id);
  const curEchMeta = INTERVIEW_ECHELONS[curTaskTier] || INTERVIEW_ECHELONS[2];
  // V24: desc вида «Задание: <заголовок>» дословно дублирует h2 — не выводим такой дубль.
  // desc приходит HTML-ом (<p><strong>Задание:</strong> …</p>) — сравниваем очищенный текст.
  const mockDescRaw = String(curTask.desc || '');
  const mockDescText = mockDescRaw.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  const mockDescClean = mockDescText.replace(/^(?:Задание|Задача)\s*[:·\-–—]?\s*/i, '').replace(/[.]\s*$/, '');
  const mockTitleClean = String(curTask.title || '').replace(/[.]\s*$/, '');
  const mockDescRedundant = !mockDescClean || mockDescClean === mockTitleClean;

  const curScen = STAR_SCENARIOS.find(x => x.id === mockInterviewState.starScenarioId) || STAR_SCENARIOS[0];
  const starOpts = STAR_SCENARIOS.map(sc =>
    `<button class="btn ${sc.id===curScen.id?'btn-primary':'btn-ghost'}" style="padding:7px 12px;font-size:.82rem;" data-star-scenario="${sc.id}">${sc.title}</button>`
  ).join('');

  let starEvalHTML = '';
  if(mockInterviewState.starEval){
    const ev = mockInterviewState.starEval;
    const rows = ev.checks.map(c => `<div style="margin:4px 0;">${c.ok ? '✓' : '✗'} ${c.label}</div>`).join('');
    starEvalHTML = `
      <div class="${ev.passed ? 'result-box--pass correct-pulse-anim' : 'result-box--fail'}" style="margin-top:12px;">
        <strong>Оценка STAR-ответа: ${ev.score} из ${ev.total} критериев Senior-интервьюера ${ev.passed ? '(+30 XP!)' : ''}</strong>
        <div style="margin-top:6px;">${rows}</div>
      </div>`;
  }

  const totalSec = 20 * 60;
  const ringCircum = 138.2;
  const ringOffset = (ringCircum * (1 - (mockInterviewState.secondsLeft / totalSec))).toFixed(1);
  const isWarningTime = mockInterviewState.secondsLeft <= 600;
  const isDangerTime = mockInterviewState.secondsLeft <= 180;
  const ringColor = isDangerTime ? '#ef4444' : (isWarningTime ? '#d97706' : 'var(--moss)');
  const timerStateCls = isDangerTime ? ' mock-timer--danger' : (isWarningTime ? ' mock-timer--warn' : '');

  const bodyHTML = mockInterviewState.tab === 'live' ? `
    <div class="panel" style="padding:14px 18px;margin-bottom:16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
      <div class="mock-timer-ring-wrap mock-timer-wrap${timerStateCls}">
        <svg class="mock-timer-svg circular-progress-ring" width="54" height="54" viewBox="0 0 54 54" aria-hidden="true">
          <circle class="mock-timer-ring-bg mock-timer-circle-bg" cx="27" cy="27" r="22" fill="none" stroke-width="4"></circle>
          <circle id="mock-timer-ring-fg" class="mock-timer-ring-fg mock-timer-circle-fg" cx="27" cy="27" r="22" fill="none" stroke="${ringColor}" stroke-width="4" stroke-dasharray="${ringCircum}" stroke-dashoffset="${ringOffset}"></circle>
        </svg>
        <div>
          <div class="meta">Таймер Live-Coding секции (регламент 20 минут)</div>
          <div id="mock-timer-display" style="font-family:var(--font-d);font-size:1.85rem;font-weight:700;color:${ringColor};">${formatPomo(mockInterviewState.secondsLeft)}</div>
        </div>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
        <select id="mock-echelon-select" class="code-editor" style="min-height:auto;padding:8px 10px;width:auto;">
          <option value="auto" ${mockInterviewState.echelonFilter==='auto'?'selected':''}>🎯 Авто-подбор раунда (сейчас: Эшелон ${effEchelon})</option>
          <option value="1" ${mockInterviewState.echelonFilter==='1'?'selected':''}>🚨 Раунд 1: Тех-скрининг (Эшелон 1)</option>
          <option value="2" ${mockInterviewState.echelonFilter==='2'?'selected':''}>🔥 Раунд 2: Ядро и стек (Эшелон 2)</option>
          <option value="3" ${mockInterviewState.echelonFilter==='3'?'selected':''}>⚡ Раунд 3: Продакшен и System Design (Эшелон 3)</option>
        </select>
        <button class="btn ${mockInterviewState.running?'btn-clay':'btn-primary'}" data-mock-timer-toggle>${mockInterviewState.running ? '⏸ Пауза' : '▶ Старт 20:00'}</button>
        <button class="btn btn-ghost" data-mock-timer-reset>↺ Сброс таймера</button>
        <button class="btn btn-clay" data-mock-random-task>🎲 Случайная задача раунда</button>
      </div>
    </div>
    <div style="margin-bottom:14px;">
      <select id="mock-task-select" class="code-editor" style="min-height:auto;padding:10px 12px;font-weight:600;">${taskOpts}</select>
    </div>
    <div class="microstep-card">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
        <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;">
          <span class="topic-badge" style="margin:0;">Live-Coding #${curTask.id} · ${curTask.tier} · ${curTask.topic}</span>
          <span class="echelon-badge ${curEchMeta.badgeClass}">${curEchMeta.shortLabel}</span>
        </div>
        <span class="meta">Сократический интервьюер (4 уровня опор · 0 спойлеров кода)</span>
      </div>
      <h2 style="margin-bottom:10px;">${curTask.title}</h2>
      ${!mockDescRedundant ? `<div class="lesson-theory" style="margin-bottom:14px;">${curTask.desc}</div>` : ''}
      ${buildCodeEditorWithGutterHTML('mock-code-editor', mockInterviewState.codeDraft, 220)}
      <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;">
        <button class="btn btn-primary" data-mock-run="${curTask.id}">${ICONS.play} Запустить решение (Ctrl+Enter)</button>
        <button class="btn btn-ghost" data-mock-hint ${mockInterviewState.hintLevel>=socraticHints.length?'disabled':''}>💡 Запросить наводку интервьюера&nbsp;(${mockInterviewState.hintLevel}/${socraticHints.length})</button>
        <button class="btn btn-ghost" data-mock-reset="${curTask.id}">Сбросить код</button>
      </div>
      ${runFeedback}
      <div class="socratic-chat-stream" style="margin-top:12px;">
        <div class="socratic-chat-header">
          <span>💬 Лента Сократического диалога</span>
          <span class="meta" style="font-size:.73rem;">Использовано опор: ${mockInterviewState.hintLevel}/${socraticHints.length}</span>
        </div>
        <div class="chat-bubble chat-bubble--interviewer">
          <div class="chat-bubble__author">🎙️ Tech Lead · Сократический интервьюер</div>
          <div>Прочитай контракт функции, оцени граничные случаи и асимптотику <span class="math-formula">O(n)</span> перед написанием кода. Если застрянешь — запроси сократовскую наводку (до 4 уровней).</div>
        </div>
        ${shownHints}
      </div>
    </div>
  ` : `
    <div class="microstep-card">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px;">
        <div class="topic-badge" style="margin:0;">Поведенческое интервью · Методика STAR (Situation · Task · Action · Result)</div>
        <div class="star-pitch-bar">
          <span class="meta">🎤 Таймер устного питча (2 мин):</span>
          <strong id="star-pitch-display" class="pitch-timer-display" style="font-family:var(--font-m);color:var(--moss-deep);">${formatPomo(mockInterviewState.pitchSecondsLeft || 120)}</strong>
          <button class="btn btn-ghost" style="padding:4px 10px;font-size:.76rem;" data-star-pitch-toggle>${mockInterviewState.pitchRunning ? '⏸ Пауза' : '▶ Репетиция 02:00'}</button>
          <button class="btn btn-ghost" style="padding:4px 8px;font-size:.75rem;" data-star-pitch-reset>↺</button>
        </div>
      </div>
      <h2 style="margin-bottom:10px;">Выбери сценарий и собери сильный инженерный ответ</h2>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">${starOpts}</div>
      <div class="notice" style="margin-bottom:14px;"><strong>Вопрос интервьюера:</strong> ${curScen.prompt}</div>
      <div class="star-matrix-grid">
        <div class="star-quadrant-card">
          <label class="meta" style="font-weight:700;display:flex;justify-content:space-between;margin-bottom:4px;"><span>S — Situation (Контекст, трафик, стек)</span><span>${String(mockInterviewState.starS||'').trim().length >= 25 ? '✓' : '≥25 симв.'}</span></label>
          <textarea id="star-s-input" class="code-editor" style="min-height:76px;" placeholder="Например: В сервисе заказов на FastAPI + PostgreSQL при пиковой нагрузке 300 RPS время ответа выросло до 4 секунд…">${escapeHtmlStr(mockInterviewState.starS)}</textarea>
        </div>
        <div class="star-quadrant-card">
          <label class="meta" style="font-weight:700;display:flex;justify-content:space-between;margin-bottom:4px;"><span>T — Task (Инженерная цель и SLA)</span><span>${String(mockInterviewState.starT||'').trim().length >= 20 ? '✓' : '≥20 симв.'}</span></label>
          <textarea id="star-t-input" class="code-editor" style="min-height:76px;" placeholder="Например: Нужно было снизить p95 латентность ниже 150 мс без остановки приёма платежей…">${escapeHtmlStr(mockInterviewState.starT)}</textarea>
        </div>
        <div class="star-quadrant-card">
          <label class="meta" style="font-weight:700;display:flex;justify-content:space-between;margin-bottom:4px;"><span>A — Action (Личный вклад: «Я диагностировал…»)</span><span>${String(mockInterviewState.starA||'').trim().length >= 35 ? '✓' : 'глагол «Я»'}</span></label>
          <textarea id="star-a-input" class="code-editor" style="min-height:84px;" placeholder="Например: Я снял план через EXPLAIN ANALYZE, обнаружил Seq Scan и N+1, добавил составной индекс и selectinload…">${escapeHtmlStr(mockInterviewState.starA)}</textarea>
        </div>
        <div class="star-quadrant-card">
          <label class="meta" style="font-weight:700;display:flex;justify-content:space-between;margin-bottom:4px;"><span>R — Result (Метрики: мс, %, RPS, 0 ошибок)</span><span>${/(\d+|%|мс|ms|сек|раз|x)/i.test(String(mockInterviewState.starR||'')) ? '✓' : 'числа/%'}</span></label>
          <textarea id="star-r-input" class="code-editor" style="min-height:76px;" placeholder="Например: Время ответа упало с 4000 мс до 45 мс (в 88 раз), нагрузка на CPU БД снизилась на 65%…">${escapeHtmlStr(mockInterviewState.starR)}</textarea>
        </div>
      </div>
      <div style="margin-top:12px;display:flex;gap:10px;flex-wrap:wrap;">
        <button class="btn btn-primary" data-star-evaluate>✓ Проверить ответ по чек-листу Senior-интервьюера</button>
        <button class="btn btn-ghost" data-star-fill-demo>Заполнить эталонный пример</button>
      </div>
      ${starEvalHTML}
    </div>
  `;

  return `
    <div class="container">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;margin-bottom:12px;">
        <div>
          <div class="topic-badge">Тренажёр технического и поведенческого собеседования · Успешных раундов: ${state.mockCompletedCount || 0}</div>
          <h1>🎙️ Симулятор собеседования (Live-Coding + STAR)</h1>
        </div>
      </div>
      <div class="subtabs">
        <button class="subtab ${mockInterviewState.tab==='live'?'active':''}" data-mock-tab="live">⏱ Live-Coding с таймером (20 мин)</button>
        <button class="subtab ${mockInterviewState.tab==='star'?'active':''}" data-mock-tab="star">⭐ Поведенческое интервью (STAR)</button>
      </div>
      ${bodyHTML}
    </div>`;
}

/* ================= CALIBRATION DIAGNOSTIC & BI-DIRECTIONAL SKILL TREE ================= */
(function enrichDiagnosticQuestions(){
  if(CORE_QUESTIONS.length === 23){
    CORE_QUESTIONS.push(
      {
        cat: 'py-basics',
        text: 'Какова средняя асимптотическая сложность проверки x in seen для множества (set) или словаря (dict) по сравнению со списком (list)?',
        options: [
          'O(n) для обоих',
          'O(1) в среднем для set/dict за счёт хеш-таблицы и O(n) для list',
          'O(log n) для set и O(1) для list',
          'O(1) для list и O(n) для dict'
        ],
        correct: 1,
        explain: 'set и dict основаны на хеш-таблицах (O(1) в среднем), а поиск по списку list требует линейного перебора O(n).'
      },
      {
        cat: 'py-basics',
        text: 'Как работает GIL (Global Interpreter Lock) в стандартном CPython при использовании потоков (threading)?',
        options: [
          'Запрещает создавать больше одного потока в программе',
          'Разрешает исполнять байткод Python только одному потоку одновременно, но освобождается на операциях ввода-вывода (I/O)',
          'Автоматически распределяет CPU-bound циклы по всем ядрам процессора',
          'Отключает сборщик мусора при работе с сетью'
        ],
        correct: 1,
        explain: 'В CPython GIL сериализует исполнение байткода в рамках одного процесса (поэтому CPU-bound задачи не ускоряются потоками), но освобождается при ожидании сети/диска (I/O).'
      }
    );
  }
  const coreSkillMap = [
    ['1.1.3', '1.1.4'],
    ['1.1.4'],
    ['1.3.1'],
    ['1.4.1'],
    ['1.2.3'],
    ['1.1.1', '1.1.2'],
    ['1.4.1'],
    ['1.3.2', '1.2.1'],
    ['7.1.1'],
    ['7.1.2'],
    ['7.1.3'],
    ['7.1.1', '7.3.1'],
    ['7.1.1'],
    ['5.2.1'],
    ['5.1.1'],
    ['5.2.2'],
    ['5.3.1'],
    ['5.2.1', '5.1.2'],
    ['2.2.2'],
    ['2.2.1'],
    ['2.3.1', '1.4.3'],
    ['2.2.2', '2.3.2'],
    ['2.2.3', '2.3.1'],
    ['4.1.1', '4.4.1', '1.2.3'],
    ['1.9.3', '1.9.1', '1.9.2']
  ];
  CORE_QUESTIONS.forEach((q, idx) => {
    q.skillIds = coreSkillMap[idx] || ['1.1.1'];
  });
  const advSkillMap = [
    ['1.5.1', '1.5.2'],
    ['1.5.3'],
    ['1.7.1'],
    ['4.1.1', '4.4.2'],
    ['4.4.1', '1.2.3'],
    ['4.1.1', '4.3.1']
  ];
  ADVANCED_QUESTIONS.forEach((q, idx) => {
    q.skillIds = advSkillMap[idx] || ['1.5.1'];
  });
})();

function applyDiagnosticCalibration(){
  ensureExtendedState();
  const passedSkills = new Set();
  const missedSkills = new Set();
  let score = 0;
  let total = 0;
  if(diagState){
    CORE_QUESTIONS.forEach((q, idx) => {
      const ans = diagState.coreAnswers ? diagState.coreAnswers[idx] : undefined;
      if(ans === undefined || ans === null) return;
      total++;
      if(ans === q.correct){
        score++;
        (q.skillIds || []).forEach(sid => passedSkills.add(sid));
      } else {
        (q.skillIds || []).forEach(sid => missedSkills.add(sid));
      }
    });
    ADVANCED_QUESTIONS.forEach((q, idx) => {
      const ans = diagState.advAnswers ? diagState.advAnswers[idx] : undefined;
      if(ans === undefined || ans === null) return;
      total++;
      if(ans === q.correct){
        score++;
        (q.skillIds || []).forEach(sid => passedSkills.add(sid));
      } else {
        (q.skillIds || []).forEach(sid => missedSkills.add(sid));
      }
    });
  }
  // If a skill was missed in any question of this diagnostic, revoke any prior 50 MP diagnostic auto-credit
  missedSkills.forEach(sid => {
    if(state.skillMastery && state.skillMastery[sid] === 50){
      delete state.skillMastery[sid];
    }
  });
  // If a skill was passed and not missed in any question of this diagnostic, auto-credit it to 50 MP
  passedSkills.forEach(sid => {
    if(!missedSkills.has(sid)){
      setSkillMP(sid, 50);
    }
  });
  const nextGaps = [];
  missedSkills.forEach(sid => {
    if(PY_SKILLS_BY_ID[sid] && getSkillMP(sid) < 100 && !nextGaps.includes(sid)){
      nextGaps.push(sid);
    }
  });
  // Keep previous unresolved gaps unless they were just passed in this calibration
  (state.diagnosticGaps || []).forEach(sid => {
    if(!passedSkills.has(sid) && PY_SKILLS_BY_ID[sid] && getSkillMP(sid) < 100 && !nextGaps.includes(sid)){
      nextGaps.push(sid);
    }
  });
  state.diagnosticGaps = nextGaps;
  if(total > 0){
    state.diagCompleted = true;
    state.diagScore = score;
    state.diagTotal = total;
  }
  saveState(state);
  return {
    score: score,
    total: total,
    passedSkills: Array.from(passedSkills).filter(sid => !missedSkills.has(sid)),
    missedSkills: Array.from(missedSkills),
    gaps: state.diagnosticGaps
  };
}
window.applyDiagnosticCalibration = applyDiagnosticCalibration;

diagIntroHTML = function(){
  ensureExtendedState();
  const branch = state.stackBranch || 'fastapi';
  return `
    <div class="container">
      <div class="diag-header-row">
        <a href="#/" class="back-link">${ICONS.chevronLeft} К результатам</a>
        <div class="topic-badge">Этап 0 · Калибровочная диагностика Эшелона 1 (Скрининг)</div>
      </div>
      <h1 style="margin-bottom:10px;">Калибровка приоритетов перед стартом</h1>
      <p>${CORE_QUESTIONS.length} вопросов по темам <b>🚨 Эшелона 1 (Скрининг и база)</b> — Python Core, словари/хеширование, типизация/GIL, Git, базовый SQL/JOIN, HTTP/REST и Big-O. Это не экзамен, а умная калибровка твоего маршрута:</p>
      <ul style="margin:8px 0 16px 20px;line-height:1.55;">
        <li>За каждый верный блок связанные навыки автоматически получают <b>50 MP (Знакомство)</b> — ты не тратишь время на очевидное;</li>
        <li>Вопросы с ошибками формируют <b>Очередь приоритета №1 («Пробелы скрининга»)</b> на Дашборде и в модулях;</li>
        <li>В конце по желанию можно открыть продвинутый блок (${ADVANCED_QUESTIONS.length} вопросов по ООП и алгоритмам).</li>
      </ul>
      <div class="panel" style="margin-bottom:18px;padding:14px 16px;">
        <div style="font-weight:700;margin-bottom:6px;">Выбери целевую ветку веб-стека (Этап 2 параллельных веток):</div>
        <p class="meta" style="margin-bottom:10px;">Выбранный стек остаётся в <b>🔥 Эшелоне 2</b>, а альтернативный фреймворк переносится в <b>👑 Эшелон 4 (Резерв)</b>, чтобы не распылять фокус перед оффером:</p>
        <div class="stack-branch-bar">
          <button class="btn ${branch==='fastapi'?'btn-primary':'btn-ghost'}" style="padding:7px 14px;font-size:.84rem;" data-stack-branch="fastapi">⚡ FastAPI + SQLAlchemy (Рекомендуется)</button>
          <button class="btn ${branch==='django'?'btn-primary':'btn-ghost'}" style="padding:7px 14px;font-size:.84rem;" data-stack-branch="django">🎸 Django + DRF</button>
          <button class="btn ${branch==='both'?'btn-primary':'btn-ghost'}" style="padding:7px 14px;font-size:.84rem;" data-stack-branch="both">🔥 Оба стека</button>
        </div>
      </div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px;">
        <button class="btn btn-primary" data-diag-start>Начать калибровку (${CORE_QUESTIONS.length} вопросов)</button>
        <a href="#/" class="btn btn-ghost">Пропустить, вернусь позже</a>
      </div>
    </div>`;
};

function saveDiagDraftState(){
  ensureExtendedState();
  if(!diagState){
    state.diagDraft = null;
  } else {
    state.diagDraft = {
      stage: diagState.stage || 'core',
      idx: typeof diagState.idx === 'number' ? diagState.idx : 0,
      coreAnswers: Array.isArray(diagState.coreAnswers) ? diagState.coreAnswers.slice() : [],
      advAnswers: Array.isArray(diagState.advAnswers) ? diagState.advAnswers.slice() : [],
      revealed: !!diagState.revealed,
      updatedAt: Date.now()
    };
  }
  saveState(state);
}

const _origViewDiagnostic = viewDiagnostic;
viewDiagnostic = function(){
  ensureExtendedState();
  if(!diagState && state.diagDraft && typeof state.diagDraft === 'object' && state.diagDraft.stage){
    diagState = {
      stage: state.diagDraft.stage,
      idx: typeof state.diagDraft.idx === 'number' ? state.diagDraft.idx : 0,
      coreAnswers: Array.isArray(state.diagDraft.coreAnswers) ? state.diagDraft.coreAnswers.slice() : [],
      advAnswers: Array.isArray(state.diagDraft.advAnswers) ? state.diagDraft.advAnswers.slice() : [],
      revealed: !!state.diagDraft.revealed
    };
  }
  return _origViewDiagnostic();
};

const _origStartDiag = startDiag;
startDiag = function(){
  _origStartDiag();
  saveDiagDraftState();
};

diagQuestionHTML = function(pool, label){
  const q = pool[diagState.idx];
  const pct = Math.round(((diagState.idx+1)/pool.length)*100);
  const ansArr = diagState.stage === 'advanced' ? diagState.advAnswers : diagState.coreAnswers;
  const chosen = (ansArr && typeof ansArr[diagState.idx] === 'number') ? ansArr[diagState.idx] : undefined;
  const hasSelection = (chosen !== undefined && chosen !== null);
  const isRevealed = !!diagState.revealed;
  const isCorrect = (chosen === q.correct);

  const optsHTML = q.options.map(function(opt, i){
    let cls = 'quiz-opt';
    if(isRevealed){
      if(i === q.correct) cls += ' quiz-opt--correct';
      else if(i === chosen) cls += ' quiz-opt--wrong';
    } else if(i === chosen){
      cls += ' quiz-opt--selected';
    }
    return `<button class="${cls}" data-diag-answer="${i}" ${isRevealed ? 'disabled' : ''}><b>${String.fromCharCode(65+i)}.</b> ${formatRichInlineText(opt)}</button>`;
  }).join('');

  const idkSelected = (chosen === -1);
  const idkBtnHTML = `<button class="quiz-opt ${isRevealed && idkSelected ? 'quiz-opt--wrong' : (idkSelected ? 'quiz-opt--selected' : '')}" style="margin-top:4px;border-style:dashed;opacity:.92;" data-diag-answer="-1" ${isRevealed ? 'disabled' : ''}><b>🤷</b> Не знаю — разобрать эту тему с нуля (без угадывания)</button>`;

  const prevBtnHTML = diagState.idx > 0
    ? `<button class="btn btn-ghost" data-diag-prev>← Предыдущий вопрос</button>`
    : `<span></span>`;

  const actionRowHTML = hasSelection
    ? `<div style="margin-top:16px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
        ${prevBtnHTML}
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-left:auto;">
          ${!isRevealed ? `<button class="btn btn-clay" data-diag-confirm>✓ Проверить ответ</button>` : ''}
          <button class="btn btn-primary" data-diag-next>${diagState.idx+1<pool.length ? 'Следующий вопрос' : 'Завершить блок'} ${ICONS.arrowRight}</button>
        </div>
      </div>`
    : `<div style="margin-top:16px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
        ${prevBtnHTML}
        <span class="meta">Выбери вариант ответа (можно изменить выбор до перехода дальше)</span>
      </div>`;

  const bottomSheetHTML = isRevealed ? `
    <div class="academy-bottom-sheet ${isCorrect ? 'academy-bottom-sheet--correct' : 'academy-bottom-sheet--wrong'}">
      <div class="bs-title-row">
        <span>${isCorrect ? '✓ Правильно! (Ответ уровня Senior)' : (chosen === -1 ? '🤷 Честный выбор — тема добавлена в маршрут' : '✕ Не совсем.')}</span>
        <span class="bs-badge">${isCorrect ? '⚡ +15 XP' : 'Диагностика'}</span>
      </div>
      <div class="bs-explain-text">${formatRichInlineText(q.explain)}</div>
      <div style="display:flex;gap:10px;align-items:center;width:100%;">
        ${diagState.idx > 0 ? `<button class="btn btn-ghost" style="padding:12px 16px;color:var(--ink-soft);" data-diag-prev>← Назад</button>` : ''}
        <button class="${isCorrect ? 'btn-coddy-emerald' : 'btn-coddy-ruby'} btn-sprint-cta" style="flex:1;" data-diag-next>
          ${diagState.idx+1 < pool.length ? 'Следующий вопрос ➔' : 'Завершить блок ➔'}
        </button>
      </div>
    </div>` : '';

  return `
    <div class="container" style="padding-bottom:${isRevealed ? '200px' : '32px'};">
      <div class="diag-header-row">
        <a href="#/" class="back-link">${ICONS.chevronLeft} К результатам</a>
        <div class="topic-badge">${label} · вопрос ${diagState.idx+1} из ${pool.length}</div>
      </div>
      <div class="progress-bar"><div class="progress-bar__fill" style="width:${pct}%"></div></div>
      <div class="panel">
        <div class="quiz-question-prompt">${formatQuizQuestionPromptHTML(q.text)}</div>
        <div>${optsHTML}${idkBtnHTML}</div>
        ${!isRevealed ? actionRowHTML : ''}
      </div>
      ${bottomSheetHTML}
    </div>`;
};

selectDiagAnswer = function(i){
  if(!diagState || diagState.revealed) return;
  const arr = diagState.stage === 'advanced' ? diagState.advAnswers : diagState.coreAnswers;
  arr[diagState.idx] = i;
  diagState.selectedOption = i;
  saveDiagDraftState();
  render();
};

function confirmDiagAnswer(){
  if(!diagState || diagState.revealed) return;
  const pool = diagState.stage === 'advanced' ? (typeof DIAGNOSTIC_ADV_POOL !== 'undefined' ? DIAGNOSTIC_ADV_POOL : []) : (typeof DIAGNOSTIC_CORE_POOL !== 'undefined' ? DIAGNOSTIC_CORE_POOL : []);
  const q = pool[diagState.idx];
  const ansArr = diagState.stage === 'advanced' ? diagState.advAnswers : diagState.coreAnswers;
  const chosen = (ansArr && typeof ansArr[diagState.idx] === 'number') ? ansArr[diagState.idx] : undefined;
  const isCorrect = q ? (chosen === q.correct) : false;
  if(navigator && navigator.vibrate) try{ navigator.vibrate(isCorrect ? [15] : [30, 40, 30]); }catch(e){}
  diagState.revealed = true;
  saveDiagDraftState();
  render();
}

function prevDiagQuestion(){
  if(!diagState || diagState.idx <= 0) return;
  diagState.idx--;
  diagState.revealed = false;
  saveDiagDraftState();
  render();
}

const _origGoAdvancedDiag = goAdvancedDiag;
goAdvancedDiag = function(){
  _origGoAdvancedDiag();
  saveDiagDraftState();
};

const _origRestartDiag = restartDiag;
restartDiag = function(){
  _origRestartDiag();
  saveDiagDraftState();
};

nextDiagQuestion = function(){
  if(!diagState) return;
  diagState.idx++;
  diagState.revealed = false;
  if(diagState.stage === 'core' && diagState.idx >= CORE_QUESTIONS.length){
    applyDiagnosticCalibration();
    diagState.stage = 'offer';
    diagState.idx = 0;
  } else if(diagState.stage === 'advanced' && diagState.idx >= ADVANCED_QUESTIONS.length){
    applyDiagnosticCalibration();
    diagState.stage = 'results';
    toggleMastered('diag', true);
  }
  saveDiagDraftState();
  render();
};

skipAdvancedDiag = function(){
  if(!diagState) return;
  applyDiagnosticCalibration();
  diagState.stage = 'results';
  toggleMastered('diag', true);
  saveDiagDraftState();
  render();
};

diagResultsHTML = function(){
  const cal = applyDiagnosticCalibration();
  const cats = diagCategories();
  const totalScore = cats.reduce(function(a,c){ return a+c.score; },0);
  const totalQ = cats.reduce(function(a,c){ return a+c.total; },0);
  const catsHTML = cats.map(function(c){
    const pctCat = c.total > 0 ? Math.round((c.score / c.total) * 100) : 0;
    let action;
    if(c.perfect && isMastered(c.id)) action = `<p class="meta" style="color:var(--moss-deep);">${ICONS.check} Подтверждено (100% без ошибок)</p>`;
    else if(c.perfect) action = `<p class="meta" style="color:var(--moss-deep);">✓ Отличный результат (${c.score}/${c.total}). Базовое знакомство (50 MP) зачтено, практика кода впереди.</p>`;
    else if(c.score === 0) action = `<p class="meta" style="color:var(--Danger);">🚨 Тема не пройдена (${c.score}/${c.total}) — добавлена в приоритет №1 с самого начала.</p>`;
    else if(c.optional) action = `<p class="meta">Частичное знакомство (${pctCat}%) — тема включена в программу с разбором пробелов.</p>`;
    else action = `<p class="meta">Есть пробелы (${c.score}/${c.total}) — добавлено в персональный маршрут Эшелона 1.</p>`;
    return `<div class="panel" style="margin-bottom:0;"><h3>${c.title}</h3><p class="meta">${c.score} из ${c.total} верно (${pctCat}%)</p>${action}</div>`;
  }).join('');

  const gapButtons = (cal.gaps || []).slice(0, 8).map(sid => {
    const sk = PY_SKILLS_BY_ID[sid];
    if(!sk) return '';
    return `<button class="btn btn-clay" style="padding:6px 11px;font-size:.8rem;" data-py-open-skill="${sid}">🚨 ${sid.replace('s-','')} · ${sk.title}</button>`;
  }).join('');

  const calibratedNotice = `
    <div class="panel" style="margin-top:18px;border-left:4px solid var(--moss);">
      <div class="topic-badge">Калибровка Матрицы Мастерства выполнена</div>
      <h3 style="margin-bottom:6px;">Зачтено базовое знакомство (50 MP): ${cal.passedSkills.length} · Пробелов в Очереди №1: ${cal.gaps.length}</h3>
      <p class="meta" style="margin-bottom:10px;">${cal.gaps.length > 0 ? 'Темы с ошибками или ответом «Не знаю» НЕ зачтены и поставлены в приоритет №1:' : 'Все проверенные навыки скрининга получили базовые 50 MP! Для полного мастерства (100 MP) нужно пройти практику кода и тесты.'}</p>
      ${gapButtons ? `<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px;">${gapButtons}</div>` : ''}
      <button class="btn-quick-start" data-quick-microstep="">⚡ Начать закрывать пробелы по шагам</button>
    </div>`;

  return `
    <div class="container">
      <div class="diag-header-row">
        <a href="#/" class="back-link">${ICONS.chevronLeft} К результатам</a>
        <div class="topic-badge">Диагностика · результат калибровки</div>
      </div>
      <h1 style="margin-bottom:6px;">Результат: ${totalScore} из ${totalQ} верно</h1>
      <p class="meta" style="margin-bottom:18px;">Честная калибровка: зачтены только темы со 100% верными ответами (на базовый уровень 50 MP), а все ошибки вынесены в очередь изучения.</p>
      <div class="node-grid">${catsHTML}</div>
      ${calibratedNotice}
      <div style="display:flex;gap:10px;margin-top:22px;flex-wrap:wrap;">
        <a href="#/" class="btn btn-primary">К результатам ${ICONS.arrowRight}</a>
        <button class="btn btn-ghost" data-diag-restart>Пройти ещё раз</button>
      </div>
    </div>`;
};

nodeCardHTML = function(n){
  const st = nodeState(n);
  const icon = st==='mastered' ? ICONS.check : st==='locked' ? ICONS.lock : ICONS.dot;
  const prereqNames = n.prereqs.map(p=>NODES_BY_ID[p] ? NODES_BY_ID[p].title : p);
  const unitIds = NODE_TO_UNITS_MAP[n.id] || [];
  let minTier = 2;
  if(unitIds.length > 0){
    minTier = Math.min.apply(null, unitIds.map(uid => getEffectiveUnitTier(uid)));
  } else if(n.id === 'diag'){
    minTier = 1;
  }
  const eMeta = INTERVIEW_ECHELONS[minTier] || INTERVIEW_ECHELONS[2];
  const parallelBadge = (n.stage === 1) ? `<span class="node-parallel-badge">🔀 Параллельная ветка</span>` : '';
  return `
    <button class="node-card node-card--${st}" data-open="${n.id}">
      <div class="node-card__top">
        <span class="node-card__num">${n.bonus ? 'бонус' : ('№ '+n.num)}</span>
        <span class="echelon-badge ${eMeta.badgeClass}" style="margin-left:auto;margin-right:6px;">${eMeta.shortLabel}</span>
        ${icon}
      </div>
      <h3 class="node-card__title">${n.title}</h3>
      <p class="node-card__summary">${n.summary}</p>
      ${parallelBadge}
      ${unitIds.length ? `<p class="node-card__prereq" style="color:var(--moss-deep);font-weight:600;">Связанные юниты: ${unitIds.join(', ')}</p>` : ''}
      ${prereqNames.length ? `<p class="node-card__prereq">Требует: ${prereqNames.join(', ')}</p>` : ''}
    </button>`;
};

let mapViewState = { mode: 'tree' };

const cleanUnitTitle = function(id, title){
  if(!title) return '';
  return String(title).replace(new RegExp(`^(?:Юнит\\s*)?${String(id).replace('.', '\\.')}\\s*[:·\\-–—]?\\s*`, 'i'), '').trim();
};

function renderPathModeSwitcherHTML(){
  const mode = (state && state.pathViewMode === 'pro') ? 'pro' : 'game';
  return `
    <div class="path-mode-switcher" role="radiogroup" aria-label="Режим плана обучения">
      <button type="button" class="path-mode-btn ${mode==='game'?'active':''}" data-set-path-mode="game" role="radio" aria-checked="${mode==='game'}" title="Игровой режим с 3D-тропой">🎮 Игровой</button>
      <button type="button" class="path-mode-btn ${mode==='pro'?'active':''}" data-set-path-mode="pro" role="radio" aria-checked="${mode==='pro'}" title="Профессиональный режим со списком глав">💼 Профессиональный</button>
    </div>
  `;
}

function getPathChaptersMeta(allUnits){
  return [
    { num: 1, title: 'Python Core', units: allUnits.slice(0, 9) },
    { num: 2, title: 'Web & HTTP', units: allUnits.slice(9, 13) },
    { num: 3, title: 'Backend & Архитектура', units: allUnits.slice(13, 21) },
    { num: 4, title: 'Алгоритмы и структуры данных', units: allUnits.slice(21, 27) },
    { num: 5, title: 'Базы данных и SQL', units: allUnits.slice(27, 33) },
    { num: 6, title: 'Системный дизайн', units: allUnits.slice(33, 39) },
    { num: 7, title: 'Инфраструктура и DevOps', units: allUnits.slice(39, 45) }
  ];
}

function isUnitCompleted(u){
  return (state.passedUnitTests || []).includes(u.id) || ((u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80));
}

function renderPathMobileStatsHTML(totalCompletedUnits, streakText, curTier){
  const tierNum = curTier || 1;
  return `
    <div class="path-mobile-stats" role="status" aria-label="Статистика обучения">
      <span class="pms-item pms-echelon" title="Текущий эшелон подготовки">🎯 <b>Эшелон ${tierNum}</b></span>
      <span class="pms-item" title="Пройдено юнитов">📘 <b>${totalCompletedUnits}/45</b></span>
      <span class="pms-item" title="Стрик активности">🔥 <b>${state.streak || 0}</b> ${streakText}</span>
      <span class="pms-item" title="Накопленный опыт">💎 <b>${state.xp || 0} XP</b></span>
    </div>`;
}

function renderCoddyRightRail(totalCompletedUnits, streakText, activeChapterNum){
  const chaptersMeta = getPathChaptersMeta(ALL_UNITS_COMBINED);
  const e1 = (typeof getEchelonProgress === 'function') ? getEchelonProgress(1) : null;
  const e1Pct = e1 ? e1.pct : 0;
  const e1Remaining = e1 ? e1.skills.filter(s => getSkillMP(s.id) < 100).length : 0;
  const dailyGoal = Math.max(1, Number(state.dailyGoal) || 50);
  const dailyXp = (typeof todayXp === 'function') ? todayXp() : 0;
  const dailyPct = Math.min(100, Math.round(dailyXp / dailyGoal * 100));
  const chaptersListHTML = chaptersMeta.map(ch => {
    const chCompleted = ch.units.filter(isUnitCompleted).length;
    const chPct = Math.round(chCompleted / ch.units.length * 100);
    const route = (typeof getTrackForUnit === 'function' && ch.units[0]) ? getTrackForUnit(ch.units[0].id).routePrefix : 'python';
    const isCurrent = (ch.num === activeChapterNum);
    return `
      <a class="crc-row ${isCurrent ? 'crc-row--current' : 'crc-row--compact'}" href="#/${route}" ${isCurrent ? 'aria-current="location"' : ''} title="Глава ${ch.num}: ${escapeHtmlStr(ch.title)} — перейти к модулю">
        <span class="crc-num">${ch.num}</span>
        <span class="crc-body">
          <span class="crc-title">${escapeHtmlStr(ch.title)}</span>
          ${isCurrent ? `<span class="crc-bar"><span class="crc-bar-fill" style="width:${chPct}%;"></span></span>` : ''}
        </span>
        <span class="crc-pct">${chCompleted}/${ch.units.length}</span>
      </a>`;
  }).join('');

  return `
    <aside class="coddy-right-rail">
      <!-- Top Stats Row (Coddy style) -->
      <div class="coddy-rail-stats-row">
        <div class="coddy-rail-stat" title="Пройдено юнитов">
          <span class="coddy-rail-stat-icon">📘</span>
          <span class="coddy-rail-stat-val">${totalCompletedUnits}/45</span>
        </div>
        <div class="coddy-rail-stat" title="Стрик активности">
          <span class="coddy-rail-stat-icon">🔥</span>
          <span class="coddy-rail-stat-val">${state.streak || 0} ${streakText}</span>
        </div>
        <div class="coddy-rail-stat" title="Накопленный опыт">
          <span class="coddy-rail-stat-icon">💎</span>
          <span class="coddy-rail-stat-val">${state.xp || 0} XP</span>
        </div>
      </div>

      <!-- Widget 1: Screening Readiness — мотивирующая графа «До 1-го скрининга %» (по ТЗ) -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-card-head">
          <div class="coddy-rail-badge">🎯 До 1-го скрининга</div>
          <a href="#/mock" class="coddy-rail-link">Симулятор →</a>
        </div>
        <div class="coddy-rail-meter">
          <span class="coddy-rail-meter-value">${e1Pct}%</span>
          <span class="meta">готовности к тех-скринингу</span>
        </div>
        <div class="cd-bar cd-bar-track" role="progressbar" aria-label="Готовность к техническому скринингу" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${e1Pct}"><div class="cd-fill cd-bar-fill" style="width:${Math.max(6, e1Pct)}%;"></div></div>
        <div class="meta" style="font-size:.75rem;margin-top:7px;">⏳ Осталось ${e1Remaining} ${pluralRuTopics(e1Remaining)} Эшелона 1</div>
      </div>

      <!-- Widget: Radar Screening Themes (Replaces duplicate chapter tree) -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-card-head">
          <div class="coddy-rail-badge">🎯 Радар скрининга</div>
          <span class="coddy-rail-link">14 тем</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:7px;margin-top:8px;">
          <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;">
            <span style="color:#f8fafc;">Сложность O(n) & срезы</span>
            <span style="color:var(--emerald);font-weight:700;">85%</span>
          </div>
          <div class="cd-bar cd-bar-track" style="height:4px;"><div class="cd-fill cd-bar-fill" style="width:85%;"></div></div>
          
          <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;margin-top:2px;">
            <span style="color:var(--ink-muted);">Хеш-таблицы & dict/set</span>
            <span style="color:var(--amber);font-weight:700;">40%</span>
          </div>
          <div class="cd-bar cd-bar-track" style="height:4px;"><div class="cd-fill cd-bar-fill" style="width:40%;background:var(--amber);"></div></div>

          <div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;margin-top:2px;">
            <span style="color:var(--ink-muted);">SQL JOIN & индексы</span>
            <span style="color:var(--ink-muted);font-weight:600;">0%</span>
          </div>
          <div class="cd-bar cd-bar-track" style="height:4px;"><div class="cd-fill cd-bar-fill" style="width:0%;"></div></div>
        </div>
      </div>

      <!-- Widget: SRS Flashcards Queue -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-card-head">
          <div class="coddy-rail-badge">🧠 Очередь SRS</div>
          <a href="#/cards" class="coddy-rail-link">12 карточек →</a>
        </div>
        <div style="font-size:0.78rem;color:var(--ink-muted);line-height:1.45;margin-top:6px;">
          Интервальное повторение ключевых определений перед собеседованием: <span style="color:#f8fafc;font-weight:600;">GIL, MRO, Дескрипторы</span>.
        </div>
      </div>

      <!-- Widget 3: Daily goal (streak lives in the topbar pill, no duplicate) -->
      <div class="panel coddy-rail-card">
        <div class="coddy-rail-badge">🎯 Цель дня</div>
        <div class="progress-bar-wrap" style="height:6px;margin:10px 0 8px;">
          <div class="progress-bar-fill" style="width:${dailyPct}%;background:linear-gradient(90deg,#fbbf24,#f59e0b);"></div>
        </div>
        <div class="coddy-rail-daily-summary"><span>Сегодня: <strong>${dailyXp}/${dailyGoal} XP</strong></span><span>${dailyXp >= dailyGoal ? 'Цель выполнена' : `Осталось ${dailyGoal - dailyXp} XP`}</span></div>
      </div>
      <!-- Widget 2: SRS Cards Review (compact one-row card) -->
      <div class="panel coddy-rail-card coddy-rail-card--row">
        <div class="coddy-rail-badge">🃏 Повторение карточек</div>
        <a href="#/cards" class="coddy-rail-link">Повторить →</a>
      </div>
    </aside>`;
}

// Набор контурных иконок для узлов тропы (референс: тёмно-серый гекс + светлая иконка вместо замка)
const TRAIL_ICON_PATHS = {
  star: '<path d="M12 3l2.7 5.5 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.8 1-6.1L3.2 9.4l6.1-.9z"/>',
  book: '<path d="M6.5 3H20v18H6.5A2.5 2.5 0 0 1 4 18.5v-13A2.5 2.5 0 0 1 6.5 3z"/><path d="M4 18.5A2.5 2.5 0 0 1 6.5 16H20"/>',
  code: '<path d="M8 7l-5 5 5 5"/><path d="M16 7l5 5-5 5"/>',
  terminal: '<path d="M4 17l6-5-6-5"/><path d="M12 19h8"/>',
  globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15.3 15.3 0 0 1 0 18 15.3 15.3 0 0 1 0-18z"/>',
  layers: '<path d="M12 2l10 6-10 6L2 8z"/><path d="M2 14l10 6 10-6"/>',
  zap: '<path d="M13 2L4 14h6l-1 8 9-12h-6z"/>',
  database: '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
  cloud: '<path d="M17.5 19a4.5 4.5 0 0 0 0-9 6.5 6.5 0 0 0-12.6 1.7A4.2 4.2 0 0 0 6.8 19z"/>',
  wrench: '<path d="M14.7 6.3a4.8 4.8 0 0 0-6 6L3 18l3 3 5.7-5.7a4.8 4.8 0 0 0 6-6L14 13l-3-3z"/>',
  branch: '<circle cx="6" cy="18" r="3"/><circle cx="18" cy="6" r="3"/><path d="M6 15V3"/><path d="M18 9a9 9 0 0 1-9 9"/>',
  shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
  trophy: '<path d="M8 21h8"/><path d="M12 17v4"/><path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 5H4v1a3 3 0 0 0 3 3"/><path d="M17 5h3v1a3 3 0 0 1-3 3"/>'
};
function trailIconCenter(x, y, name, size, color){
  const d = TRAIL_ICON_PATHS[name] || TRAIL_ICON_PATHS.star;
  return `<g transform="translate(${x - size/2} ${y - size/2}) scale(${(size/24).toFixed(3)})" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" pointer-events="none">${d}</g>`;
}
function trailPawShape(x, y, fill, stroke, strokeWidth){
  const parts = '<circle cx="-15" cy="-14" r="6.2"/><circle cx="-5" cy="-22" r="6.2"/><circle cx="5" cy="-22" r="6.2"/><circle cx="15" cy="-14" r="6.2"/><path d="M-18 6c-1-7 3-16 9-17 4-.7 6 3 9 3s5-3.7 9-3c6 1 10 10 9 17-1 7-8 11-16 6-2-1-3-1-5 0-8 5-15 1-16-6z"/>';
  return `<g class="path-node-paw" transform="translate(${x} ${y})"><g transform="translate(0 2)" fill="rgba(0,0,0,0.30)" stroke="none">${parts}</g><g class="path-paw-face" fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}" stroke-linejoin="round">${parts}</g></g>`;
}
function trailIsometricButton(x, y, fill, stroke, strokeWidth){
  const top = `M${x} ${y-25} L${x+24} ${y-12} L${x+24} ${y+10} L${x} ${y+23} L${x-24} ${y+10} L${x-24} ${y-12} Z`;
  const side = `M${x-24} ${y+10} L${x} ${y+23} L${x+24} ${y+10} L${x+24} ${y+18} L${x} ${y+31} L${x-24} ${y+18} Z`;
  const shadow = `M${x} ${y-19} L${x+24} ${y-6} L${x+24} ${y+16} L${x} ${y+29} L${x-24} ${y+16} L${x-24} ${y-6} Z`;
  const inset = `M${x} ${y-18} L${x+17} ${y-9} L${x+17} ${y+7} L${x} ${y+16} L${x-17} ${y+7} L${x-17} ${y-9} Z`;
  return `<path d="${shadow}" fill="rgba(0,0,0,0.34)" transform="translate(0 4)"/><g class="path-button-face"><path d="${side}" fill="url(#pathButtonSide)" stroke="rgba(255,255,255,0.12)" stroke-width="1" stroke-linejoin="round"/><path d="${top}" fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}" stroke-linejoin="round"/><path d="${inset}" fill="none" stroke="rgba(255,255,255,0.14)" stroke-width="1" stroke-linejoin="round"/><path d="M${x-15} ${y-12} L${x} ${y-20} L${x+15} ${y-12}" fill="none" stroke="rgba(255,255,255,0.28)" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></g>`;
}
// Тематические иконки по главам (циклятся внутри главы)
const TRAIL_CHAPTER_ICONS = [
  ['terminal', 'code', 'star', 'book'],
  ['globe', 'code', 'book', 'star'],
  ['layers', 'code', 'shield', 'book'],
  ['branch', 'zap', 'code', 'book'],
  ['database', 'terminal', 'book', 'star'],
  ['cloud', 'layers', 'book', 'star'],
  ['wrench', 'cloud', 'shield', 'book']
];

function viewPathSerpentine(options){
  options = options || {};
  ensureExtendedState();
  const allUnits = ALL_UNITS_COMBINED;
  const usePawNodes = state.pathNodeStyle !== 'button';
  
  // Find which units are completed vs active vs locked
  let activeUnitIndex = -1;
  allUnits.forEach((u, idx) => {
    const isUnitTestPassed = (state.passedUnitTests || []).includes(u.id);
    const allSkillsMastered = (u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80);
    const isCompleted = isUnitTestPassed || allSkillsMastered;
    if(!isCompleted && activeUnitIndex === -1){
      activeUnitIndex = idx;
    }
  });
  if(activeUnitIndex === -1) activeUnitIndex = allUnits.length - 1;

  // Track coordinates for each of the 45 nodes
  // Account for chapter spacing: Chapter 1 starts at y=130 (with Chapter 1 ribbon at y=48)
  // Each chapter transition adds +150px of breathing room for Coddy-style Section Gate Cards!
  const chapterStartSet = new Set([9, 13, 21, 27, 33, 39]);
  let curY = 130;
  const coords = allUnits.map((u, i) => {
    if(i > 0){
      curY += 115;
      if(chapterStartSet.has(i)){
        curY += 150; // Dedicated gap for Coddy Section Gate Card (Variant C)
      }
    }
    const x = Math.round(210 + 110 * Math.sin((i * Math.PI) / 2.2));
    return { x, y: curY };
  });

  const totalH = coords[coords.length - 1].y + 120;

  // Build smooth Bezier path
  let dPath = `M ${coords[0].x} ${coords[0].y}`;
  for(let i = 0; i < coords.length - 1; i++){
    const p1 = coords[i];
    const p2 = coords[i+1];
    const midY = (p1.y + p2.y) / 2;
    dPath += ` C ${p1.x} ${midY}, ${p2.x} ${midY}, ${p2.x} ${p2.y}`;
  }

  // Build progress sub-path up to active unit
  let dProgress = '';
  if(activeUnitIndex > 0){
    dProgress = `M ${coords[0].x} ${coords[0].y}`;
    for(let i = 0; i < Math.min(activeUnitIndex, coords.length - 1); i++){
      const p1 = coords[i];
      const p2 = coords[i+1];
      const midY = (p1.y + p2.y) / 2;
      dProgress += ` C ${p1.x} ${midY}, ${p2.x} ${midY}, ${p2.x} ${p2.y}`;
    }
  }

  // Dotted "path ahead" overlay from the active unit to the end (Coddy-style)
  let dFuture = '';
  if(activeUnitIndex < coords.length - 1){
    dFuture = `M ${coords[activeUnitIndex].x} ${coords[activeUnitIndex].y}`;
    for(let i = activeUnitIndex; i < coords.length - 1; i++){
      const p1 = coords[i];
      const p2 = coords[i+1];
      const midY = (p1.y + p2.y) / 2;
      dFuture += ` C ${p1.x} ${midY}, ${p2.x} ${midY}, ${p2.x} ${p2.y}`;
    }
  }

  // Active unit metadata for top chapter banner
  const curActiveUnit = allUnits[activeUnitIndex] || allUnits[0];
  const activeTrack = getTrackForUnit(curActiveUnit.id);
  const chapterUnits = allUnits.filter(u => getTrackForUnit(u.id).routePrefix === activeTrack.routePrefix);
  const totalInChapter = chapterUnits.length;
  const completedInChapter = chapterUnits.filter(u => (state.passedUnitTests || []).includes(u.id) || ((u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80))).length;
  const chapterSegmentsHTML = chapterUnits.map(u => {
    const isPassed = (state.passedUnitTests || []).includes(u.id) || ((u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80));
    const isActive = u.id === curActiveUnit.id;
    return `<div class="path-seg-bar ${isPassed ? 'done' : (isActive ? 'active' : '')}" title="Юнит ${u.id}: ${escapeHtmlStr(u.title)}"></div>`;
  }).join('');
  const chapterProgressLabel = completedInChapter === 0
    ? `Начни · ${totalInChapter}`
    : `${completedInChapter} / ${totalInChapter}`;

  // Chapter markers: Chapter 1 has top ribbon, Chapters 2..7 have Coddy Section Gate Cards (Variant C, Hard Gate)
  const chapterBreakpoints = [
    { startIdx: 0, title: 'Глава 1: Python Core', chapterNum: 1, track: 'python', shortTitle: 'Python Core', unitsCount: 9 },
    { startIdx: 9, title: 'Глава 2: Web & HTTP', chapterNum: 2, track: 'web', shortTitle: 'Web & HTTP', unitsCount: 4 },
    { startIdx: 13, title: 'Глава 3: Backend & Архитектура', chapterNum: 3, track: 'backend', shortTitle: 'Backend & Архитектура', unitsCount: 8 },
    { startIdx: 21, title: 'Глава 4: Алгоритмы и структуры данных', chapterNum: 4, track: 'algorithms', shortTitle: 'Алгоритмы и структуры', unitsCount: 6 },
    { startIdx: 27, title: 'Глава 5: Базы данных и SQL', chapterNum: 5, track: 'databases', shortTitle: 'Базы данных и SQL', unitsCount: 6 },
    { startIdx: 33, title: 'Глава 6: Системный дизайн', chapterNum: 6, track: 'architecture', shortTitle: 'Системный дизайн', unitsCount: 6 },
    { startIdx: 39, title: 'Глава 7: Инфраструктура и DevOps', chapterNum: 7, track: 'infra', shortTitle: 'Инфраструктура и DevOps', unitsCount: 6 }
  ];
  // Последний юнит главы получает отдельную иконку трофея.
  const chapterLastIdxSet = new Set(chapterBreakpoints.slice(1).map(cb => cb.startIdx - 1));
  chapterLastIdxSet.add(allUnits.length - 1);

  let markersSVG = '';
  chapterBreakpoints.forEach((cb, ci) => {
    if(coords[cb.startIdx]){
      if(cb.startIdx === 0){
        // Chapter 1 retains clean top ribbon
        const cy = 48;
        markersSVG += `
          <g class="path-chapter-ribbon" transform="translate(210, ${cy})">
            <line x1="-190" y1="0" x2="-130" y2="0" stroke="rgba(190, 18, 60, 0.40)" stroke-width="1.5" stroke-dasharray="4 4"/>
            <line x1="130" y1="0" x2="190" y2="0" stroke="rgba(190, 18, 60, 0.40)" stroke-width="1.5" stroke-dasharray="4 4"/>
            <rect x="-120" y="-14" width="240" height="28" rx="14" fill="rgba(22, 27, 36, 0.88)" stroke="rgba(190, 18, 60, 0.50)" stroke-width="1.2"/>
            <text x="0" y="4" text-anchor="middle" font-size="11" font-weight="800" fill="#fbbf24" letter-spacing="0.04em">${escapeHtmlStr(cb.title)}</text>
          </g>`;
      } else {
        // Chapters 2..7 get Coddy-style Section Gate Cards (Variant C, Hard Gate)
        const prevCb = chapterBreakpoints[ci - 1];
        const prevUnits = allUnits.slice(prevCb.startIdx, cb.startIdx);
        const isPrevChapterDone = prevUnits.length > 0 && prevUnits.every(isUnitCompleted);

        const nextStartIdx = (ci + 1 < chapterBreakpoints.length) ? chapterBreakpoints[ci + 1].startIdx : allUnits.length;
        const curUnits = allUnits.slice(cb.startIdx, nextStartIdx);
        const curCompletedCount = curUnits.filter(isUnitCompleted).length;
        const isCurChapterDone = curUnits.length > 0 && curCompletedCount === curUnits.length;
        const isCurChapterActive = isPrevChapterDone && !isCurChapterDone;

        const gateStatus = !isPrevChapterDone ? 'locked' : (isCurChapterDone ? 'completed' : 'active');
        const isLocked = (gateStatus === 'locked');

        const prevY = coords[cb.startIdx - 1].y;
        const nextY = coords[cb.startIdx].y;
        const cy = Math.round((prevY + nextY) / 2);

        let hexFill = 'url(#pathButtonActive)';
        let hexStroke = 'rgba(251, 191, 36, 0.95)';
        let hexGlow = 'filter="drop-shadow(0 0 10px rgba(245, 158, 11, 0.65))"';
        let hexText = `<text x="0" y="-48" text-anchor="middle" font-size="14" font-weight="900" fill="#ffffff">${cb.chapterNum}</text>`;

        if(isLocked){
          hexFill = 'url(#pathButtonLocked)';
          hexStroke = 'rgba(190, 18, 60, 0.60)';
          hexGlow = '';
          hexText = `<text x="0" y="-49" text-anchor="middle" font-size="12" font-weight="900" fill="#fda4af">🔒</text>`;
        } else if(isCurChapterDone){
          hexFill = 'url(#pathButtonCompleted)';
          hexStroke = 'rgba(52, 211, 153, 0.85)';
          hexGlow = 'filter="drop-shadow(0 0 10px rgba(16, 185, 129, 0.55))"';
          hexText = `<text x="0" y="-48" text-anchor="middle" font-size="15" font-weight="900" fill="#ffffff">✓</text>`;
        }

        const hexBadge = `
          <g class="path-gate-hex-badge" ${hexGlow}>
            <polygon points="0,-72 16,-63 16,-44 0,-35 -16,-44 -16,-63" fill="${hexFill}" stroke="${hexStroke}" stroke-width="1.8" stroke-linejoin="round"/>
            <polygon points="0,-68 13,-60 13,-46 0,-38 -13,-46 -13,-60" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="1" stroke-linejoin="round"/>
            ${hexText}
          </g>`;

        let subText = '';
        if(isLocked){
          subText = `<text class="path-gate-sub" x="0" y="5" text-anchor="middle" font-size="10.5" font-weight="600" fill="#fda4af">🔒 ${cb.unitsCount} ${pluralizeRu(cb.unitsCount, 'юнит', 'юнита', 'юнитов')} · Откроется после «${escapeHtmlStr(prevCb.shortTitle)}»</text>`;
        } else if(isCurChapterDone){
          subText = `<text class="path-gate-sub" x="0" y="5" text-anchor="middle" font-size="10.5" font-weight="600" fill="#6ee7b7">✓ Все ${cb.unitsCount} из ${cb.unitsCount} юнитов сданы · 100%</text>`;
        } else {
          const pct = Math.round(curCompletedCount / cb.unitsCount * 100);
          subText = `<text class="path-gate-sub" x="0" y="5" text-anchor="middle" font-size="10.5" font-weight="600" fill="#fcd34d">${curCompletedCount} из ${cb.unitsCount} ${pluralizeRu(cb.unitsCount, 'юнита', 'юнитов', 'юнитов')} сдано · ${pct}%</text>`;
        }

        let btnContent = '';
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
        }

        markersSVG += `
          <g class="path-section-gate path-chapter-ribbon path-section-gate--${gateStatus}" transform="translate(210, ${cy})">
            <line x1="-195" y1="0" x2="-160" y2="0" stroke="rgba(190, 18, 60, 0.40)" stroke-width="1.5" stroke-dasharray="4 4"/>
            <line x1="160" y1="0" x2="195" y2="0" stroke="rgba(190, 18, 60, 0.40)" stroke-width="1.5" stroke-dasharray="4 4"/>
            <rect class="path-section-gate-bg" x="-155" y="-53" width="310" height="112" rx="18" fill="rgba(19, 24, 34, 0.94)" stroke="${isLocked ? 'rgba(190, 18, 60, 0.45)' : (isCurChapterDone ? 'rgba(16, 185, 129, 0.50)' : 'rgba(245, 158, 11, 0.60)')}" stroke-width="1.5" filter="drop-shadow(0 12px 28px rgba(0,0,0,0.65))"/>
            ${hexBadge}
            <text class="path-gate-title" x="0" y="-14" text-anchor="middle" font-size="12" font-weight="900" fill="#f8fafc" letter-spacing="0.08em">РАЗДЕЛ ${cb.chapterNum}: ${escapeHtmlStr(cb.shortTitle.toUpperCase())}</text>
            ${subText}
            ${btnContent}
          </g>`;
      }
    }
  });

  // Flat-topped hexagon SVG points calculation
  let nodesSVG = '';
  allUnits.forEach((u, i) => {
    const { x, y } = coords[i];
    let status = 'locked';
    if(i < activeUnitIndex || (state.passedUnitTests || []).includes(u.id) || ((u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80))){
      status = 'completed';
    } else if(i === activeUnitIndex){
      status = 'active';
    }

    const isCompleted = (status === 'completed');
    const isActive = (status === 'active');

    const topGrad = isCompleted ? 'url(#hexGradCompleted)' : (isActive ? 'url(#hexGradActive)' : 'url(#hexGradLocked)');
    const buttonGrad = isCompleted ? 'url(#pathButtonCompleted)' : (isActive ? 'url(#pathButtonActive)' : 'url(#pathButtonLocked)');
    const strokeColor = isCompleted ? 'rgba(255,255,255,0.3)' : (isActive ? '#fef08a' : 'rgba(148,163,184,0.28)');
    const strokeWidth = isActive ? 2 : 1.5;

    let centerIcon = '';
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
    const showUnderLabel = (i >= activeUnitIndex && i <= activeUnitIndex + 2);
    const underTitleFull = cleanUnitTitle(u.id, u.title);
    const shortTitle = (underTitleFull.length > 24) ? underTitleFull.slice(0, 22) + '…' : underTitleFull;
    // у финишных юнитов главы снизу-сбоку висит ветка челленджа — уводим подпись в противоположную сторону
    const hasBranchBelow = chapterLastIdxSet.has(i);
    const branchDir = (x >= 210) ? 1 : -1;
    const underLabelX = hasBranchBelow ? (x - branchDir * 44) : x;
    const underLabelAnchor = hasBranchBelow ? (branchDir === 1 ? 'end' : 'start') : 'middle';
    const nodeStateLabel = isCompleted ? 'Пройден' : (isActive ? 'Текущий юнит, доступен для продолжения' : 'Заблокирован: сначала пройдите предыдущие юниты');
    const nodeAccessibleLabel = `Юнит ${u.id}: ${cleanUnitTitle(u.id, u.title)}. ${nodeStateLabel}. Нажмите Enter или пробел, чтобы открыть.`;

    nodesSVG += `
      <g class="hex-3d-node hex-node--${status}" data-unit-id="${u.id}" data-node-idx="${i}" data-cx="${x}" data-cy="${y}" role="button" tabindex="0" aria-label="${escapeHtmlStr(nodeAccessibleLabel)}" aria-keyshortcuts="Enter Space ArrowUp ArrowDown Home End" title="${escapeHtmlStr(nodeAccessibleLabel)}">
        ${pulseHalo}
        <circle cx="${x}" cy="${y}" r="34" fill="transparent" pointer-events="all"/>
        ${nodeShape}
        ${buttonContent}
        ${showUnderLabel ? `<text class="hex-node-underlabel" x="${underLabelX}" y="${y + 52}" text-anchor="${underLabelAnchor}">${escapeHtmlStr(shortTitle)}</text>` : ''}
        ${activeBubble}
      </g>`;
  });

  // «Челлендж мастерства» — боковые ветви-гексагоны на финишных юнитах глав (по референсу Coddy)
  let branchesSVG = '';
  chapterBreakpoints.forEach((cb, cIdx) => {
    const endIdx = (cIdx < chapterBreakpoints.length - 1) ? (chapterBreakpoints[cIdx + 1].startIdx - 1) : (allUnits.length - 1);
    const u = allUnits[endIdx];
    if(!u) return;
    const { x, y } = coords[endIdx];
    const track = getTrackForUnit(u.id);
    const chDone = (state.passedUnitTests || []).includes(u.id);
    const chUnlocked = endIdx <= activeUnitIndex;
    const chStatus = chDone ? 'done' : (chUnlocked ? 'open' : 'locked');
    const offsetDir = (x >= 210) ? 1 : -1;
    const bx = Math.max(60, Math.min(360, x + offsetDir * 84));
    const by = y + 54;
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
      </g>`;
  });

  const totalCompletedUnits = allUnits.filter(isUnitCompleted).length;
  const streakText = (typeof pluralizeRu === 'function') ? pluralizeRu(state.streak || 0, 'день', 'дня', 'дней') : 'дн.';
  const activeChapterNum = (getPathChaptersMeta(allUnits).find(c => c.units.some(u => u.id === curActiveUnit.id)) || { num: 1 }).num;
  const e1Top = (typeof getEchelonProgress === 'function') ? getEchelonProgress(1) : null;
  const e1PctTop = e1Top ? e1Top.pct : 0;

  return `
    <div class="coddy-path-layout">
      <div class="container path-serpentine-wrap">
        <!-- Переключатель режимов game/pro перенесён в «⚙️ Настройки платформы» (по ТЗ — тех.информация не в топбаре) -->

        <!-- Mobile compact stats strip (visible when the right rail is hidden) -->
        ${renderPathMobileStatsHTML(totalCompletedUnits, streakText, curActiveUnit.tier || 1)}

        <!-- Top Chapter Banner -->
        <div class="path-chapter-banner">
          <div class="path-chapter-banner-main">
            <div class="path-chapter-banner-left">
              <div class="path-chapter-breadcrumb">
                <span class="path-echelon-pill echelon-pill--t${curActiveUnit.tier || 1}">${curActiveUnit.tierLabel || `Эшелон ${curActiveUnit.tier || 1}`}</span>
                <span class="path-crumb-sep">›</span>
                <span>ГЛАВА ${activeChapterNum}</span>
                <span class="path-screening-badge" title="Готовность к 1-му техническому скринингу">⚡ Готовность к тех-скринингу: ${e1PctTop}%</span>
              </div>
              <div class="path-chapter-title">Юнит ${curActiveUnit.id} · ${escapeHtmlStr(cleanUnitTitle(curActiveUnit.id, curActiveUnit.title))}</div>
            </div>
          </div>
          <div class="path-chapter-banner-right">
            <div class="path-chapter-progress-row">
              <span class="path-chapter-target-icon">🎯</span>
              <div class="path-chapter-segments">
                ${chapterSegmentsHTML}
              </div>
              <span class="path-chapter-count" title="${completedInChapter === 0 ? `Начни главу: в ней ${totalInChapter} ${pluralizeRu(totalInChapter, 'юнит', 'юнита', 'юнитов')}` : `Завершено юнитов: ${completedInChapter} из ${totalInChapter}`}" aria-label="${completedInChapter === 0 ? `Начни главу: ${totalInChapter} ${pluralizeRu(totalInChapter, 'юнит', 'юнита', 'юнитов')}` : `Завершено юнитов: ${completedInChapter} из ${totalInChapter}`}">${chapterProgressLabel}</span>
            </div>
          </div>
        </div>

        <!-- S-Curve SVG Trail -->
        <div class="path-serpentine" style="position:relative;">
          <svg class="path-serpentine-svg" viewBox="0 0 420 ${totalH}" xmlns="http://www.w3.org/2000/svg" role="group" aria-label="Путь обучения: ${allUnits.length} юнитов и челленджи">
            <defs>
              <linearGradient id="hexGradCompleted" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#34d399"/>
                <stop offset="100%" stop-color="#059669"/>
              </linearGradient>
              <linearGradient id="hexGradActive" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#fbbf24"/>
                <stop offset="100%" stop-color="#d97706"/>
              </linearGradient>
              <linearGradient id="hexGradLocked" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#3a4150"/>
                <stop offset="100%" stop-color="#15181f"/>
              </linearGradient>
              <linearGradient id="hexGradChallenge" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#fb7185"/>
                <stop offset="100%" stop-color="#be123c"/>
              </linearGradient>
              <linearGradient id="pathButtonActive" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffd166"/><stop offset="0.52" stop-color="#f59e0b"/><stop offset="1" stop-color="#c65a08"/></linearGradient>
              <linearGradient id="pathButtonCompleted" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#6ee7b7"/><stop offset="0.52" stop-color="#10b981"/><stop offset="1" stop-color="#047857"/></linearGradient>
              <linearGradient id="pathButtonLocked" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#566174"/><stop offset="0.55" stop-color="#303949"/><stop offset="1" stop-color="#1b2230"/></linearGradient>
              <linearGradient id="pathButtonSide" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#303a4b"/><stop offset="1" stop-color="#111722"/></linearGradient>
              <linearGradient id="pathButtonChallenge" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fda4af"/><stop offset="0.55" stop-color="#e11d48"/><stop offset="1" stop-color="#9f1239"/></linearGradient>
              <linearGradient id="pathProgressGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#10b981"/>
                <stop offset="100%" stop-color="#f59e0b"/>
              </linearGradient>
            </defs>

            <!-- Outer trail shadow -->
            <path d="${dPath}" fill="none" stroke="rgba(0,0,0,0.35)" stroke-width="22" stroke-linecap="round"/>
            <!-- Burgundy under-glow of the trail -->
            <path d="${dPath}" fill="none" stroke="rgba(190,18,60,0.12)" stroke-width="30" stroke-linecap="round"/>
            <!-- Background trail -->
            <path class="path-track-bg" d="${dPath}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="14" stroke-linecap="round"/>
            ${dProgress ? `<path class="path-track-progress" d="${dProgress}" fill="none" stroke="url(#pathProgressGrad)" stroke-width="8" stroke-linecap="round"/>` : ''}
            ${dFuture ? `<path class="path-track-future" d="${dFuture}" fill="none" stroke="rgba(154,161,175,0.45)" stroke-width="4" stroke-linecap="round" stroke-dasharray="0.1 16"/>` : ''}

            <!-- Chapter ribbons -->
            ${markersSVG}

            <!-- 45 3D Hexagonal Nodes -->
            ${nodesSVG}

            <!-- «Челлендж мастерства» side branches -->
            ${branchesSVG}
          </svg>

          <!-- Anchored Popover Modal -->
          <div id="path-anchored-popover" class="path-popover" style="display:none;" role="dialog" tabindex="-1" aria-labelledby="popover-title" aria-describedby="popover-status">
            <div class="path-popover-arrow path-popover-arrow--down" id="popover-arrow"></div>
            <div class="path-popover-content">
              <div class="path-popover-header">
                <div class="path-popover-badge" id="popover-badge">🎯 Модуль 1 · Python</div>
                <button type="button" class="path-popover-close" id="popover-close-btn" aria-label="Закрыть">✕</button>
              </div>
              <h3 class="path-popover-title" id="popover-title">Юнит 1.1: Переменные и память</h3>
              <div class="path-popover-status" id="popover-status">В процессе изучения</div>
              <div class="path-popover-skills" id="popover-skills"></div>
              <div class="path-popover-actions">
                <button type="button" class="btn-3d-orange path-popover-cta" id="popover-cta-btn">НАЧАТЬ ➔</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Floating Jump Button to active lesson -->
        <button type="button" class="path-jump-btn" id="path-jump-btn" title="Перейти к текущему уроку" aria-label="Перейти к текущему уроку">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
        </button>
      </div>

      ${renderCoddyRightRail(totalCompletedUnits, streakText, activeChapterNum)}
    </div>`;
}

let proCollapsedChapters = new Set();

function viewProPath(options){
  options = options || {};
  ensureExtendedState();
  const allUnits = ALL_UNITS_COMBINED;

  // Find active unit
  let activeUnitIndex = -1;
  allUnits.forEach((u, idx) => {
    const isUnitTestPassed = (state.passedUnitTests || []).includes(u.id);
    const allSkillsMastered = (u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80);
    const isCompleted = isUnitTestPassed || allSkillsMastered;
    if(!isCompleted && activeUnitIndex === -1){
      activeUnitIndex = idx;
    }
  });
  if(activeUnitIndex === -1) activeUnitIndex = allUnits.length - 1;

  const curActiveUnit = allUnits[activeUnitIndex] || allUnits[0];
  const activeTrack = getTrackForUnit(curActiveUnit.id);
  const totalCompletedUnits = allUnits.filter(isUnitCompleted).length;
  const streakText = (typeof pluralizeRu === 'function') ? pluralizeRu(state.streak || 0, 'день', 'дня', 'дней') : 'дн.';

  // 7 Chapters
  const chapters = getPathChaptersMeta(allUnits);

  const activeChap = chapters.find(c => c.units.some(u => u.id === curActiveUnit.id)) || chapters[0];
  const activeChapCompleted = activeChap.units.filter(u => (state.passedUnitTests || []).includes(u.id) || ((u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80))).length;
  const activeChapTotal = activeChap.units.length;
  const activeChapPct = Math.round(activeChapCompleted / activeChapTotal * 100);
  const activeChapSummary = activeChapCompleted === 0
    ? `Начни главу · ${activeChapTotal} ${pluralizeRu(activeChapTotal, 'юнит', 'юнита', 'юнитов')}`
    : `Глава ${activeChap.num}: ${escapeHtmlStr(activeChap.title)} · ${activeChapCompleted}/${activeChapTotal} уроков · ${activeChapPct}%`;

  // Segments for active chapter
  const activeChapSegmentsHTML = activeChap.units.map(u => {
    const isPassed = (state.passedUnitTests || []).includes(u.id) || ((u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80));
    const isActive = u.id === curActiveUnit.id;
    return `<div class="path-seg-bar ${isPassed ? 'done' : (isActive ? 'active' : '')}" title="Юнит ${u.id}: ${escapeHtmlStr(u.title)}"></div>`;
  }).join('');

  // Hero Card HTML (exactly matching Coddy screenshot #2)
  const heroCardHTML = `
    <div class="pro-hero-card">
      <div class="pro-hero-card-head">
        <div class="pro-hero-card-left">
          <div class="pro-hero-breadcrumb">ПРОГРАММА › РАЗДЕЛ ${activeChap.num} · ГЛАВА ${activeChap.num}</div>
          <h2 class="pro-hero-title">Юнит ${curActiveUnit.id} · ${escapeHtmlStr(cleanUnitTitle(curActiveUnit.id, curActiveUnit.title))}</h2>
          <div class="pro-hero-meta">${activeChapSummary}</div>
        </div>
        <button type="button" class="btn-3d-orange pro-hero-cta" data-pro-start="${curActiveUnit.id}">ПРОДОЛЖИТЬ</button>
      </div>

      <div class="pro-hero-progress-track">
        <div class="pro-hero-progress-fill" style="width:${activeChapPct}%;"></div>
      </div>

      <div class="path-chapter-progress-row" style="margin-top:4px;">
        <span class="path-chapter-target-icon">🎯</span>
        <div class="path-chapter-segments">
          ${activeChapSegmentsHTML}
        </div>
        <span class="path-chapter-count" title="${activeChapCompleted === 0 ? `Начни главу: в ней ${activeChapTotal} ${pluralizeRu(activeChapTotal, 'юнит', 'юнита', 'юнитов')}` : `Завершено юнитов: ${activeChapCompleted} из ${activeChapTotal}`}" aria-label="${activeChapCompleted === 0 ? `Начни главу: ${activeChapTotal} ${pluralizeRu(activeChapTotal, 'юнит', 'юнита', 'юнитов')}` : `Завершено юнитов: ${activeChapCompleted} из ${activeChapTotal}`}">${activeChapCompleted === 0 ? `Начни · ${activeChapTotal}` : `${activeChapCompleted} / ${activeChapTotal}`}</span>
      </div>
    </div>
  `;

  // Chapters list HTML (structured chapter box and lesson rows with icons and badges)
  const chaptersHTML = chapters.map(ch => {
    const isCurChap = (ch.num === activeChap.num);
    const chCompleted = ch.units.filter(u => (state.passedUnitTests || []).includes(u.id) || ((u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80))).length;
    const chTotal = ch.units.length;
    const chPct = Math.round(chCompleted / chTotal * 100);
    const isExpanded = isCurChap ? !proCollapsedChapters.has(ch.num) : proCollapsedChapters.has(ch.num);

    const lessonsListHTML = ch.units.map(u => {
      const isUnitTestPassed = (state.passedUnitTests || []).includes(u.id);
      const allSkillsMastered = (u.skills && u.skills.length > 0) && u.skills.every(s => getSkillMP(s.id) >= 80);
      const isCompleted = isUnitTestPassed || allSkillsMastered;
      const globalIdx = allUnits.findIndex(x => x.id === u.id);
      const isActive = (globalIdx === activeUnitIndex);
      const isLocked = (globalIdx > activeUnitIndex && !isCompleted);

      let statusClass = isCompleted ? 'pro-lesson-row--completed' : (isActive ? 'pro-lesson-row--active' : 'pro-lesson-row--locked');
      let iconHtml = '';
      if(isActive){
        iconHtml = '<div class="pro-icon-play" aria-label="Текущий урок">▶</div>';
      } else if(isCompleted){
        iconHtml = '<div class="pro-icon-done" aria-label="Пройден">✓</div>';
      } else {
        iconHtml = '<div class="pro-icon-locked" aria-label="Заблокирован">🔒</div>';
      }

      const isChallenge = u.id.endsWith('.9') || u.id.endsWith('.6') || u.id.endsWith('.8');
      const badgeClass = isChallenge ? 'pro-lesson-badge pro-lesson-badge--challenge' : 'pro-lesson-badge';
      const badgeText = isChallenge ? 'Испытание' : 'Теория + Практика';
      
      const unitSkills = (u.skills || []).map(s => s.title.split('(')[0].trim());
      const previewPills = unitSkills.slice(0, 3).map(skillName => 
        `<span style="font-size:0.68rem;padding:2px 7px;border-radius:6px;background:rgba(255,255,255,0.05);color:var(--ink-muted);border:1px solid rgba(255,255,255,0.06);white-space:nowrap;">${escapeHtmlStr(skillName)}</span>`
      ).join(' ');

      return `
        <div class="pro-lesson-row ${statusClass}" data-unit-id="${u.id}" role="button" tabindex="${isLocked ? '-1' : '0'}" style="${isActive ? 'box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.4), 0 8px 24px rgba(0,0,0,0.4); background: rgba(245, 158, 11, 0.05);' : ''}">
          <div class="pro-lesson-status-icon">${iconHtml}</div>
          <div class="pro-lesson-info" style="display:flex;flex-direction:column;gap:5px;">
            <div class="pro-lesson-title" style="font-weight:${isActive ? '700' : '600'}; color:${isActive ? '#f8fafc' : (isCompleted ? 'var(--ink)' : 'var(--ink-muted)')};">
              Юнит ${u.id}: ${escapeHtmlStr(cleanUnitTitle(u.id, u.title))}
            </div>
            <div class="pro-lesson-tags" style="display:flex;flex-wrap:wrap;gap:5px;align-items:center;">
              <span class="${badgeClass}">${badgeText}</span>
              ${previewPills}
            </div>
          </div>
          <div class="pro-lesson-tail">
            ${isActive ? '<span class="pro-arrow" style="font-weight:bold;color:var(--amber);">→</span>' : (isLocked ? '<span style="font-size:0.75rem;color:var(--ink-muted);opacity:0.6;">4 темы</span>' : '')}
          </div>
        </div>
      `;
    }).join('');

    return `
      <div class="pro-chapter-box ${isCurChap ? 'pro-chapter-box--active' : ''}">
        <div class="pro-chapter-header" data-toggle-chapter="${ch.num}">
          <div class="pro-chapter-header-left">
            <div class="pro-chapter-num">ГЛАВА ${ch.num}</div>
            <div class="pro-chapter-title">${escapeHtmlStr(ch.title)}</div>
          </div>
          <div class="pro-chapter-header-right">
            <span class="pro-chapter-stat" style="white-space:nowrap;">${chCompleted}/${chTotal} · ${chPct}%</span>
            <span class="pro-chapter-chevron" style="transform:${isExpanded ? 'rotate(180deg)' : 'none'};">▼</span>
          </div>
        </div>
        ${isExpanded ? `<div class="pro-lesson-list">${lessonsListHTML}</div>` : ''}
      </div>
    `;
  }).join('');

  return `
    <div class="coddy-path-layout">
      <div class="container path-pro-wrap">
        <!-- Переключатель режимов game/pro перенесён в «⚙️ Настройки платформы» (по ТЗ — тех.информация не в топбаре) -->

        <!-- Mobile compact stats strip (visible when the right rail is hidden) -->
        ${renderPathMobileStatsHTML(totalCompletedUnits, streakText, curActiveUnit.tier || 1)}

        <!-- Top Hero Card of Current Lesson -->
        ${heroCardHTML}

        <!-- Structured Chapters List -->
        ${chaptersHTML}
      </div>

      ${renderCoddyRightRail(totalCompletedUnits, streakText, activeChap.num)}
    </div>
  `;
}
window.viewPathSerpentine = viewPathSerpentine;
window.viewProPath = viewProPath;

viewMap = function(){
  const stagesHTML = STAGES.map((s,i)=>{
    const nodes = NODES.filter(n=>n.stage===i);
    const isLast = i===STAGES.length-1;
    return `
      <div class="stage" style="${isLast?'':''}">
        <div class="stage__spine">
          <div class="stage__dot">${i+1}</div>
        </div>
        <div class="stage__body">
          <h2 class="stage__title">${s.title}</h2>
          <p class="stage__desc meta">${s.desc}</p>
          <div class="node-grid">${nodes.map(nodeCardHTML).join('')}</div>
        </div>
      </div>`;
  }).join('');

  const mode = (mapViewState && mapViewState.mode) ? mapViewState.mode : 'tree';

  const modeSwitcherHTML = `
    <div class="subtabs subtabs--compact" style="margin-bottom:16px;">
      <button class="subtab ${mode==='path'?'active':''}" data-map-mode="path">🏔 3D-Тропа курса (Serpentine)</button>
      <button class="subtab ${mode==='tree'?'active':''}" data-map-mode="tree">🗺 Дерево и Эшелоны собеседования</button>
    </div>`;

  if(mode === 'path'){
    return `
      <div class="container" style="padding-bottom:10px;">
        <h1 style="margin-bottom:6px;">Карта навыков: Интерактивная 3D-Тропа обучения</h1>
        <p class="meta" style="margin-bottom:14px;">Математическая извилистая S-трасса соединяет все 45 юнитов курса в единое непрерывное приключение.</p>
        ${modeSwitcherHTML}
      </div>
      ${(state.pathViewMode === 'pro') ? viewProPath() : viewPathSerpentine()}`;
  }

  return `
    <div class="container">
      <h1 style="margin-bottom:6px;">Карта навыков и Эшелоны собеседования</h1>
      <p class="meta" style="margin-bottom:14px;">Единая архитектура: 4 сквозных эшелона приоритета (от 100% обязательного тех-скрининга до архитектурного резерва) синхронизированы с 18 узлами дерева навыков и 45 юнитами в 7 модулях.</p>
      ${modeSwitcherHTML}
      ${buildPriorityRoadmapWidgetHTML({ compact: false })}
      ${stagesHTML}
    </div>`;
};

const _origViewTopic = viewTopic;
viewTopic = function(id){
  if(id === 'diag') return viewDiagnostic();
  const baseHtml = _origViewTopic(id);
  const unitIds = NODE_TO_UNITS_MAP[id] || [];
  if(!unitIds.length) return baseHtml;

  const unitCards = unitIds.map(uid => {
    const u = UNITS_BY_ID[uid];
    if(!u) return '';
    const tr = getTrackForUnit(uid);
    const effTier = getEffectiveUnitTier(uid);
    const eMeta = INTERVIEW_ECHELONS[effTier] || INTERVIEW_ECHELONS[2];
    const uMp = u.skills.reduce((a, s) => a + getSkillMP(s.id), 0);
    const uMax = u.skills.length * 100;
    const firstSkill = u.skills[0];
    return `
      <div class="panel" style="margin:0;padding:12px 14px;display:flex;flex-direction:column;justify-content:space-between;gap:8px;">
        <div>
          <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:4px;">
            <span class="echelon-badge ${eMeta.badgeClass}">${eMeta.shortLabel}</span>
            <span class="meta">${uMp}/${uMax} MP</span>
          </div>
          <div style="font-weight:700;font-size:.92rem;">Юнит ${u.id}: ${u.title}</div>
          <div class="meta" style="font-size:.78rem;">Навыков: ${u.skills.length} · Тренажёр + К-конспекты + Ф-карточки</div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;">
          ${firstSkill ? `<button class="btn btn-primary" style="padding:6px 10px;font-size:.78rem;" data-py-open-skill="${firstSkill.id}">Открыть юнит ${u.id}</button>` : ''}
          <a href="#${tr.routePrefix}/unittest/${u.id}" class="btn btn-ghost" style="padding:6px 10px;font-size:.78rem;">Unit Test ${u.id}</a>
        </div>
      </div>`;
  }).join('');

  const bridgeBlock = `
    <div class="panel" style="margin-top:18px;">
      <div class="topic-badge">Двусторонняя синхронизация с 7 модулями Мастерства</div>
      <h3 style="margin-bottom:8px;">Связанные юниты (К-конспекты, 3D-карточки Ф-xxx и задачи IDE)</h3>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;">
        ${unitCards}
      </div>
    </div>`;

  return baseHtml.replace(/<\/div>\s*$/, bridgeBlock + '</div>');
};


/* ================= ANTI-PROCRASTINATION DASHBOARD, LESSON MICRO-STEPS & HANDOVER ================= */
let lessonMicroState = { lessonId: null, stepIdx: 0, chunkIdx: 0, fullMode: false };
let dashStage = 1;

function saveLessonDraftState(){
  ensureExtendedState();
  if(!lessonState || !lessonState.lessonId) return;
  const lid = lessonState.lessonId;
  const ta = document.getElementById('lesson-code');
  if(ta && typeof ta.value === 'string' && lessonState.stage && ['practice','task','practice2','task2','debug'].includes(lessonState.stage)){
    lessonState[lessonState.stage + 'Code'] = ta.value;
  }
  const prev = (state.lessonDrafts && state.lessonDrafts[lid]) || {};
  state.lessonDrafts[lid] = Object.assign({}, prev, {
    stage: lessonState.stage || 'theory',
    checkIdx: lessonState.checkIdx || 0,
    checkAnswers: Array.isArray(lessonState.checkAnswers) ? lessonState.checkAnswers.slice() : [],
    checkRevealed: !!lessonState.checkRevealed,
    practiceCode: lessonState.practiceCode,
    practiceHintLevel: lessonState.practiceHintLevel || 0,
    practiceStatus: lessonState.practiceStatus || null,
    taskCode: lessonState.taskCode,
    taskHintLevel: lessonState.taskHintLevel || 0,
    taskStatus: lessonState.taskStatus || null,
    practice2Code: lessonState.practice2Code,
    practice2HintLevel: lessonState.practice2HintLevel || 0,
    practice2Status: lessonState.practice2Status || null,
    task2Code: lessonState.task2Code,
    task2HintLevel: lessonState.task2HintLevel || 0,
    task2Status: lessonState.task2Status || null,
    debugCode: lessonState.debugCode,
    debugHintLevel: lessonState.debugHintLevel || 0,
    debugStatus: lessonState.debugStatus || null,
    stepIdx: (lessonMicroState && lessonMicroState.lessonId === lid) ? (lessonMicroState.stepIdx || 0) : (prev.stepIdx || 0),
    chunkIdx: (lessonMicroState && lessonMicroState.lessonId === lid) ? (lessonMicroState.chunkIdx || 0) : (prev.chunkIdx || 0),
    fullMode: (lessonMicroState && lessonMicroState.lessonId === lid) ? !!lessonMicroState.fullMode : !!prev.fullMode,
    updatedAt: Date.now()
  });
  saveState(state);
}

const _origEnsureLessonState = ensureLessonState;
ensureLessonState = function(id){
  const wasDifferent = (!lessonState || lessonState.lessonId !== id);
  _origEnsureLessonState(id);
  if(wasDifferent && lessonState && lessonState.lessonId === id){
    ensureExtendedState();
    const saved = state.lessonDrafts && state.lessonDrafts[id];
    if(saved && typeof saved === 'object'){
      if(saved.stage && ['theory','check','practice','task','practice2','task2','debug','done'].includes(saved.stage)){
        lessonState.stage = saved.stage;
      }
      if(typeof saved.checkIdx === 'number') lessonState.checkIdx = saved.checkIdx;
      if(Array.isArray(saved.checkAnswers)) lessonState.checkAnswers = saved.checkAnswers.slice();
      if(typeof saved.checkRevealed === 'boolean') lessonState.checkRevealed = saved.checkRevealed;
      ['practice','task','practice2','task2','debug'].forEach(st => {
        if(typeof saved[st + 'Code'] === 'string' && saved[st + 'Code'].length > 0){
          lessonState[st + 'Code'] = saved[st + 'Code'];
        }
        if(typeof saved[st + 'HintLevel'] === 'number'){
          lessonState[st + 'HintLevel'] = saved[st + 'HintLevel'];
        }
        if(saved[st + 'Status'] === 'pass'){
          lessonState[st + 'Status'] = 'pass';
        }
      });
      lessonMicroState = {
        lessonId: id,
        stepIdx: typeof saved.stepIdx === 'number' ? saved.stepIdx : 0,
        chunkIdx: typeof saved.chunkIdx === 'number' ? saved.chunkIdx : 0,
        fullMode: !!saved.fullMode
      };
    } else {
      lessonMicroState = { lessonId: id, stepIdx: 0, chunkIdx: 0, fullMode: false };
    }
  }
};

const _origAnswerLessonCheck = answerLessonCheck;
answerLessonCheck = function(i){
  if(!lessonState || lessonState.checkRevealed) return;
  const l = (typeof LESSONS !== 'undefined' && lessonState) ? LESSONS[lessonState.lessonId] : null;
  const checks = (l && l.checks) ? l.checks : [];
  const c = checks[lessonState ? (lessonState.checkIdx || 0) : 0];
  const isCorrect = c ? (i === c.correct) : false;
  if(navigator && navigator.vibrate) try{ navigator.vibrate(isCorrect ? [15] : [30, 40, 30]); }catch(e){}
  _origAnswerLessonCheck(i);
  if(isCorrect){
    awardXp(15);
  }
  saveLessonDraftState();
};

const _origLessonHint = lessonHint;
lessonHint = function(stage){
  _origLessonHint(stage);
  saveLessonDraftState();
};

function splitHtmlIntoMicroSteps(htmlStr, fallbackTitle){
  let str = String(htmlStr || '').trim();
  str = str.replace(/^<div\s+class=["']lesson-theory["'][^>]*>/i, '').replace(/<\/div>\s*$/, '').trim();
  const parts = str.split(/(?=<h4[^>]*>)/i).map(s => s.trim()).filter(Boolean);
  if(parts.length > 1 && !/^<h4\b/i.test(parts[0])){
    parts[1] = parts[0] + '\n' + parts[1];
    parts.shift();
  }
  if(parts.length <= 1){
    return [{ title: fallbackTitle || 'Теория', html: str }];
  }
  return parts.map((p, idx) => {
    const m = p.match(/<h4[^>]*>([\s\S]*?)<\/h4>/i);
    const title = m ? m[1].replace(/<[^>]+>/g, '').trim() : ('Шаг ' + (idx + 1));
    return { title: title, html: p };
  });
}

// Override lessonTheoryHTML so every lesson on the Skill Tree has interactive micro-step cards + Coddy-style chunk feed + inline Python runner!
lessonTheoryHTML = function(){
  const l = LESSONS[lessonState.lessonId];
  if(lessonMicroState.lessonId !== lessonState.lessonId){
    const saved = (state.lessonDrafts && state.lessonDrafts[lessonState.lessonId]) || {};
    lessonMicroState = {
      lessonId: lessonState.lessonId,
      stepIdx: typeof saved.stepIdx === 'number' ? saved.stepIdx : 0,
      chunkIdx: typeof saved.chunkIdx === 'number' ? saved.chunkIdx : 0,
      fullMode: !!saved.fullMode
    };
  }
  const steps = splitHtmlIntoMicroSteps(l.theory, l.title);
  const sIdx = Math.min(lessonMicroState.stepIdx, Math.max(0, steps.length - 1));
  const curStep = steps[sIdx];

  const dots = steps.map((st, i) =>
    `<button class="microstep-dot ${i===sIdx?'active':(i<sIdx?'done':'')}" data-lstep-jump="${i}" title="${escapeHtmlStr(st.title)}"></button>`
  ).join('');

  const chunks = splitStepHtmlIntoChunks(curStep.html);
  const totalChunks = chunks.length;
  const curChunkIdx = Math.min(lessonMicroState.chunkIdx || 0, Math.max(0, totalChunks - 1));
  const sprintPct = Math.min(100, Math.max(10, Math.round(((sIdx + (curChunkIdx + 1) / Math.max(1, totalChunks)) / Math.max(1, steps.length)) * 100)));

  const feedHTML = `<div class="scroll-feed" id="lesson-theory-text">` + chunks.slice(0, curChunkIdx + 1).map((ch, ci) =>
    `<div class="feed-chunk ${ci < curChunkIdx ? 'feed-chunk-prev' : 'feed-chunk-new'} lesson-theory" data-chunk-idx="${ci}">${ch}</div>`
  ).join('') + `</div>`;

  const hasMoreChunks = (curChunkIdx + 1 < totalChunks);
  const canGoBack = (curChunkIdx > 0 || sIdx > 0);
  const backBtnHTML = `<button type="button" class="btn btn-ghost" data-chunk-prev="lesson" style="padding:11px 16px;border-radius:14px;font-size:.88rem;white-space:nowrap;${canGoBack ? 'display:inline-flex;' : 'display:none;'}" ${canGoBack ? '' : 'disabled aria-hidden="true"'}>← Назад</button>`;

  let primaryActionHTML = '';
  if(hasMoreChunks){
    primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-chunk-more="lesson">Понятно, дальше (+10 XP) ➔</button>`;
  } else if(sIdx + 1 < steps.length){
    primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-lstep-jump="${sIdx+1}">Следующий шаг (${sIdx+2}/${steps.length}) (+10 XP) ➔</button>`;
  } else {
    primaryActionHTML = `<button type="button" class="btn-glass-emerald btn-sprint-cta" style="flex:1;" data-lesson-next="check">Дальше: мини-проверка (+10 XP) ${ICONS.arrowRight}</button>`;
  }

  const isLastStepAndChunk = (sIdx + 1 >= steps.length) && !hasMoreChunks;
  const e1 = getEchelonProgress(1);
  const remE1 = e1.skills.filter(s => getSkillMP(s.id) < 100).length;
  const streakVal = (typeof state !== 'undefined' && state && state.streak) ? state.streak : 1;
  const activeCount = Math.min(6, Math.max(1, streakVal % 6 || 6));
  const finishSprintBanner = isLastStepAndChunk ? `
    <div class="sprint-finish-card" style="margin-top:12px;">
      <div class="sprint-finish-orb">👑</div>
      <h3 style="margin-bottom:6px;">Минус 1 тема до скрининга!</h3>

      <div class="daily-activity-strip">
        <div class="daily-activity-head">
          <span>✓ Дневная активность выполнена!</span>
          <span class="active-accent">${activeCount} / 6</span>
        </div>
        <div class="daily-week-segments">
          ${[1,2,3,4,5,6].map(i => `<div class="day-seg ${i <= activeCount ? 'done' : ''}"></div>`).join('')}
        </div>
      </div>

      <div class="stats-grid-2x2">
        <div class="stat-card">
          <div class="stat-head">XP ЗАРАБОТАНО</div>
          <div class="stat-val">+10 XP</div>
        </div>
        <div class="stat-card emerald">
          <div class="stat-head">ДО СКРИНИНГА</div>
          <div class="stat-val">${remE1} ${pluralRuTopics(remE1)} (-1)</div>
        </div>
        <div class="stat-card emerald">
          <div class="stat-head">ТОЧНОСТЬ</div>
          <div class="stat-val">100 %</div>
        </div>
        <div class="stat-card">
          <div class="stat-head">ВРЕМЯ СЕССИИ</div>
          <div class="stat-val">01:45</div>
        </div>
      </div>

      <div class="countdown-shift-card">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;font-weight:800;font-size:.9rem;">
          <span>🎯 Готовность: ${e1.pct}% ➔ ${Math.min(100, e1.pct + 2)}%</span>
          <span style="color:var(--moss);">⏳ Осталось ${remE1} ${pluralRuTopics(remE1)}!</span>
        </div>
        <div class="cd-bar cd-bar-track"><div class="cd-fill cd-bar-fill" style="width:${Math.max(8, Math.min(100, e1.pct + 2))}%;"></div></div>
      </div>
    </div>` : '';

  const primaryLessonActionHTML = `
    <div class="floating-step-nav" style="display:flex;align-items:center;gap:10px;margin-top:18px;padding-top:14px;border-top:1px solid var(--glass-border);flex-wrap:nowrap;flex:none;box-shadow:none;background:transparent;border-left:none;border-right:none;border-bottom:none;border-radius:0;padding-left:0;padding-right:0;">
      ${backBtnHTML}
      <div style="display:flex;gap:10px;align-items:center;flex:1;justify-content:center;">
        ${primaryActionHTML}
      </div>
    </div>`;

  const navDrawerHTML = `
    <details class="cocoon-details cocoon-details--compact" style="margin-top:12px;">
      <summary><span>🧭 Навигация: ${escapeHtmlStr(NODES_BY_ID[l.nodeId].title)}</span><span class="meta">Все шаги (${steps.length}) ▾</span></summary>
      <div class="sprint-step-header">
        <div class="microstep-dots">${dots}</div>
        <span class="meta" style="font-size:.73rem;white-space:nowrap;">Шаг ${sIdx+1}/${steps.length}<span class="sr-only"> Микро-шаг ${sIdx+1} из ${steps.length}</span></span>
      </div>
      ${lessonBackLink()}
      <h1 style="font-size:1.15rem;margin:6px 0 8px;">${l.title}</h1>
      <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
        <button class="link-quiet" data-lstep-toggle-full>${lessonMicroState.fullMode ? 'По шагам' : 'Показать весь текст'}</button>
        <button class="btn btn-primary" style="padding:7px 12px;font-size:.82rem;" data-lesson-next="check">Дальше: мини-проверка ${ICONS.arrowRight}</button>
      </div>
    </details>`;

  const body = lessonMicroState.fullMode
    ? `${navDrawerHTML}<div class="microstep-card"><div class="lesson-theory">${decorateCodeBlocksWithRunBtn(l.theory)}</div></div>`
    : `<div class="card coddy-lesson-card" style="margin-top:0;display:flex;flex-direction:column;justify-content:space-between;min-height:280px;">
        <div style="flex:1;">${feedHTML}</div>
        ${primaryLessonActionHTML}
      </div>
      ${finishSprintBanner}${navDrawerHTML}`;

  return `
    <div class="container">
      <div class="sprint-focus-topbar sprint-topbar">
        <a href="#/topic/${l.nodeId}" class="sprint-close-btn" title="${escapeHtmlStr(NODES_BY_ID[l.nodeId].title)}">✕</a>
        <div class="sprint-progress-wrap">
          <div class="sprint-progress-meta">
            <span>${escapeHtmlStr(l.title)}</span>
            <span>Шаг ${sIdx+1}/${steps.length}<span class="sr-only"> Микро-шаг ${sIdx+1} из ${steps.length}</span></span>
          </div>
          <div class="sprint-progress-track"><div class="sprint-progress-fill" style="width:${sprintPct}%;"></div></div>
        </div>
        <span class="sprint-xp-pill">⚡ +10 XP</span>
      </div>
      <div id="theory-audio-bar" class="theory-audio-bar" style="display:${state.audioBarOpen ? 'flex' : 'none'};">
        <button type="button" class="theory-audio-btn" data-audio-play title="Воспроизвести / Пауза">▶</button>
        <button type="button" class="theory-audio-btn" data-audio-rewind title="Перемотка назад на 10 сек">⏪ -10с</button>
        <button type="button" class="theory-audio-btn" data-audio-rate title="Скорость чтения">1.0x</button>
        <span class="audio-status-text">Аудио-компаньон</span>
        <button type="button" class="theory-audio-btn" data-audio-close style="margin-left:auto;" title="Скрыть аудио-бар">✕</button>
      </div>
      ${body}
    </div>`;
};

const _origAdvanceLessonStage = advanceLessonStage;
advanceLessonStage = function(next){
  if(lessonState && lessonState.stage === 'theory' && next === 'check'){
    awardXp(10);
  }
  _origAdvanceLessonStage(next);
  saveLessonDraftState();
};

function buildLessonStageTopbarHTML(l, rightLabel, pct, xpLabel){
  return `
    <div class="sprint-focus-topbar sprint-topbar">
      <a href="#/topic/${l.nodeId}" class="sprint-close-btn" title="${escapeHtmlStr(NODES_BY_ID[l.nodeId].title)}">✕</a>
      <div class="sprint-progress-wrap">
        <div class="sprint-progress-meta">
          <span>${escapeHtmlStr(l.title)}</span>
          <span>${rightLabel}</span>
        </div>
        <div class="sprint-progress-track"><div class="sprint-progress-fill" style="width:${pct}%;"></div></div>
      </div>
      <span class="sprint-xp-pill">${xpLabel}</span>
    </div>
    <div id="theory-audio-bar" class="theory-audio-bar" style="display:${state.audioBarOpen ? 'flex' : 'none'};">
      <button type="button" class="theory-audio-btn" data-audio-play title="Воспроизвести / Пауза">▶</button>
      <button type="button" class="theory-audio-btn" data-audio-rewind title="Перемотка назад на 10 сек">⏪ -10с</button>
      <button type="button" class="theory-audio-btn" data-audio-rate title="Скорость чтения">1.0x</button>
      <span class="audio-status-text">Аудио-компаньон</span>
      <button type="button" class="theory-audio-btn" data-audio-close style="margin-left:auto;" title="Скрыть аудио-бар">✕</button>
    </div>`;
}

const _origLessonCheckHTML = lessonCheckHTML;
lessonCheckHTML = function(){
  const l = LESSONS[lessonState.lessonId];
  const checks = l.checks || [];
  const idx = lessonState.checkIdx || 0;
  const c = checks[idx] || { q: '', options: [], correct: 0, explain: '' };
  const sel = (lessonState.checkAnswers && typeof lessonState.checkAnswers[idx] === 'number') ? lessonState.checkAnswers[idx] : undefined;
  const revealed = !!lessonState.checkRevealed;
  const isCorrect = (sel === c.correct);

  const pct = Math.min(95, Math.max(45, Math.round(45 + ((idx + 1) / Math.max(1, checks.length)) * 20)));
  const topbar = buildLessonStageTopbarHTML(l, `Мини-проверка ${idx+1}/${checks.length}`, pct, '⚡ +10 XP');

  const isTokenChips = (c.chips || (c.options.length <= 6 && c.options.every(o => o.length <= 22 && !o.includes('\n')) && (/\[|\`|%|==|\+=|def|hash|len|index/.test(c.q) || c.options.length <= 4)));

  let questionBodyHTML = '';
  if(isTokenChips){
    const slotValue = (sel !== undefined) ? c.options[sel] : null;
    const slotClass = (sel !== undefined) ? (revealed ? (isCorrect ? 'filled selected-correct' : 'filled selected-wrong') : 'filled') : 'empty';
    const slotText = slotValue ? escapeHtmlStr(slotValue) : '[ ? ]';

    let promptText = c.q;
    if(promptText.includes('`')){
      promptText = promptText.replace(/`([^`]+)`/g, '<span class="inline-code-pill">$1</span>');
    }

    const chipsHTML = c.options.map(function(opt, i){
      let cls = 'tap-chip';
      if(revealed){
        if(i === c.correct) cls += ' selected-correct';
        else if(i === sel) cls += ' selected-wrong';
      } else if(i === sel){
        cls += ' selected';
      }
      return `<button type="button" class="${cls}" data-lesson-check="${i}" ${revealed?'disabled':''}>${escapeHtmlStr(opt)}</button>`;
    }).join('');

    questionBodyHTML = `
      <div class="tap-chip-card">
        <p style="font-size:1.02rem;line-height:1.52;margin-bottom:12px;color:var(--ink);">${promptText}</p>
        <div class="tap-code-slot-container">
          <span style="color:var(--ink-soft);font-size:.84rem;">Подстановка: </span>
          <span class="tap-code-slot ${slotClass}">${slotText}</span>
        </div>
        <div class="tap-chips-bank-label">Банк токенов (Zero-Keyboard Scaffolding):</div>
        <div class="tap-chips-row">${chipsHTML}</div>
      </div>`;
  } else {
    const optsHTML = c.options.map(function(opt, i){
      let cls = 'quiz-opt';
      if(revealed){
        if(i === c.correct) cls += ' quiz-opt--correct';
        else if(i === sel) cls += ' quiz-opt--wrong';
      } else if(i === sel){
        cls += ' quiz-opt--selected';
      }
      return `<button class="${cls}" data-lesson-check="${i}" ${revealed?'disabled':''}>${formatRichInlineText(opt)}</button>`;
    }).join('');

    questionBodyHTML = `
      <h2 style="margin-bottom:16px;">${formatRichInlineText(c.q)}</h2>
      <div style="display:flex;flex-direction:column;gap:9px;">${optsHTML}</div>`;
  }

  const isLast = idx + 1 >= checks.length;
  const nextTarget = isLast ? 'practice' : 'next-check';
  const nextLabel = isLast ? 'Дальше: практика' : 'Следующий вопрос';

  const bottomSheetHTML = revealed ? `
    <div class="academy-bottom-sheet lesson-drawer ${isCorrect ? 'academy-bottom-sheet--correct' : 'academy-bottom-sheet--wrong'}">
      <div class="bs-title-row">
        <span>${isCorrect ? '✓ Правильно! +15 XP' : '✕ Не совсем.'}</span>
        <span class="bs-badge">${isCorrect ? '⚡ +15 XP' : 'Разбор'}</span>
      </div>
      <div class="bs-explain-text">${formatRichInlineText(c.explain)}</div>
      <button class="${isCorrect ? 'btn-3d-emerald btn-coddy-emerald' : 'btn-3d-ruby btn-coddy-ruby'} btn-sprint-cta" data-lesson-next="${nextTarget}">
        ${isCorrect ? 'ПРОДОЛЖИТЬ ➔' : (isLast ? 'ПРОДОЛЖИТЬ (ПРАКТИКА) ➔' : 'ПРОДОЛЖИТЬ ➔')}
      </button>
    </div>` : '';

  return `
    <div class="container" style="padding-bottom:${revealed ? '200px' : '32px'};">
      ${topbar}
      ${lessonBackLink()}
      <div class="topic-badge">Урок · мини-проверка ${idx+1} из ${checks.length}</div>
      ${questionBodyHTML}
      ${bottomSheetHTML}
    </div>`;
};

const _origLessonStageHTML = lessonStageHTML;
lessonStageHTML = function(stage){
  const l = LESSONS[lessonState.lessonId];
  const seq = lessonStageSequence(l);
  const seqIdx = Math.max(0, seq.indexOf(stage));
  const pct = Math.min(98, Math.round(70 + ((seqIdx + 1) / Math.max(1, seq.length)) * 25));
  const labels = {practice:'Практика', task:'Задание', practice2:'Практика 2', task2:'Задание 2', debug:'Отладка'};
  const topbar = buildLessonStageTopbarHTML(l, labels[stage] || 'Практика', pct, '⚡ +20 XP');
  let raw = _origLessonStageHTML(stage).replace('<div class="container">', '<div class="container">\n      ' + topbar);
  raw = raw.replace(/<textarea id="lesson-code"[^>]*>([\s\S]*?)<\/textarea>/, function(_, inner){
    const unesc = inner.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&amp;/g,'&');
    return buildCodeEditorWithGutterHTML('lesson-code', unesc, 200);
  });
  return raw;
};

const _origLessonDoneHTML = lessonDoneHTML;
lessonDoneHTML = function(){
  const l = LESSONS[lessonState.lessonId];
  const topbar = buildLessonStageTopbarHTML(l, 'Завершено', 100, '✨ Готово');
  const streakVal = (state && state.streak) ? state.streak : 1;
  const activeCount = Math.min(6, Math.max(1, streakVal % 6 || 6));
  const finishCard = `
    <div class="sprint-finish-card" style="margin-top:16px;">
      <div class="sprint-finish-orb">👑</div>
      <h2 style="font-size:1.45rem;font-weight:800;margin-bottom:8px;">Урок завершён!</h2>
      <div class="daily-activity-strip">
        <div class="daily-activity-head">
          <span>✓ Дневная активность выполнена!</span>
          <span class="active-accent">${activeCount} / 6</span>
        </div>
        <div class="daily-week-segments">
          ${[1,2,3,4,5,6].map(i => `<div class="day-seg ${i<=activeCount?'done':''}"></div>`).join('')}
        </div>
      </div>
      <div class="stats-grid-2x2">
        <div class="stat-card">
          <div class="stat-head">XP ЗАРАБОТАНО</div>
          <div class="stat-val">+30 XP</div>
        </div>
        <div class="stat-card emerald">
          <div class="stat-head">ДО СКРИНИНГА</div>
          <div class="stat-val">-1 урок</div>
        </div>
        <div class="stat-card emerald">
          <div class="stat-head">ТОЧНОСТЬ</div>
          <div class="stat-val">100 %</div>
        </div>
        <div class="stat-card">
          <div class="stat-head">ВРЕМЯ СЕССИИ</div>
          <div class="stat-val">03:20</div>
        </div>
      </div>
    </div>`;
  const base = _origLessonDoneHTML();
  return base
    .replace('<div class="container">', '<div class="container">\n      ' + topbar)
    .replace('<p>Теория, мини-проверка, практика и итоговое задание — всё пройдено.</p>', '<p>Теория, мини-проверка, практика и итоговое задание — всё пройдено.</p>\n' + finishCard);
};

// Upgrade verifyLessonStage and verifyCommandStage to use fast Brython/Pyodide runner & award XP & mark complete on last stage
verifyLessonStage = async function(stage){
  if(!lessonState) return;
  const ta = document.getElementById('lesson-code');
  const code = ta ? ta.value : lessonState[stage+'Code'];
  lessonState[stage+'Status'] = 'running';
  lessonState[stage+'Output'] = '';
  saveLessonDraftState();
  render();
  const l = LESSONS[lessonState.lessonId];
  const block = l[stage];
  let output = '', passed = false, message = '';
  try{
    const runner = await getFastPythonRunner();
    runner.setStdout({batched:function(s){ output += s + '\n'; }});
    runner.setStderr({batched:function(s){ output += s + '\n'; }});
    runner.runPython(code + '\n' + block.test);
    passed = !!runner.globals.get('__result__');
    const m = runner.globals.get('__message__');
    message = m ? String(m) : '';
  }catch(err){
    passed = false;
    message = String(err);
  }
  lessonState[stage+'Status'] = passed ? 'pass' : 'fail';
  lessonState[stage+'Output'] = output.trim();
  lessonState[stage+'Message'] = message;
  const seq = lessonStageSequence(l);
  if(passed){
    awardXp(20);
    if(stage === 'task' || stage === seq[seq.length - 1]){
      markLessonComplete(lessonState.lessonId);
    }
  }
  saveLessonDraftState();
  render();
};

const _origVerifyCommandStage = verifyCommandStage;
verifyCommandStage = function(stage){
  _origVerifyCommandStage(stage);
  if(lessonState && lessonState[stage+'Status'] === 'pass'){
    awardXp(15);
    const seq = lessonStageSequence(LESSONS[lessonState.lessonId]);
    if(stage === 'task' || stage === seq[seq.length - 1]){
      markLessonComplete(lessonState.lessonId);
    }
  }
  saveLessonDraftState();
};

// Build 7-day heatmap data
function buildSevenDayHeatmapHTML(){
  const days = ['Вс','Пн','Вт','Ср','Чт','Пт','Сб'];
  let html = '';
  const hasActiveStreak = (state.streak || 0) > 0;
  for(let i=6; i>=0; i--){
    const d = new Date();
    d.setDate(d.getDate() - i);
    const k = dateIsoKey(d);
    const xp = (state.dailyXpByDate && state.dailyXpByDate[k]) || 0;
    const isToday = (i === 0);
    const isHigh = xp >= (state.dailyGoal || 50);
    const isActive = xp > 0;
    const isFrozen = !isActive && hasActiveStreak && !isToday;
    const cls = isHigh ? 'heat-cell high' : (isActive ? 'heat-cell active' : (isToday ? 'heat-cell today' : (isFrozen ? 'heat-cell frozen' : 'heat-cell')));
    const valText = isHigh ? `✓ ${xp}` : (isActive ? `${xp}` : (isToday ? '🔥 0' : (isFrozen ? '🧊' : '—')));
    const frozenHint = isFrozen ? ' (заморозка стрика 🧊)' : '';
    html += `<div class="${cls}" role="button" tabindex="0" data-heat-day="${k}" data-heat-xp="${xp}" data-heat-today="${isToday ? '1' : '0'}" title="${k}: ${xp} XP ${isToday ? '(сегодня)' : ''}${frozenHint}" aria-label="${k}: ${xp} XP ${isToday ? '(сегодня)' : ''}${frozenHint}"><span>${days[d.getDay()]}</span><b>${valText}</b></div>`;
  }
  return `<div class="heat-row">${html}</div>`;
}


// ================= REMNOTE SPACED REPETITION ENGINE (SRS) =================
function addDaysToDateKey(baseDateKey, days){
  try{
    const base = String(baseDateKey || dateIsoKey());
    const parts = base.split('-').map(Number);
    const dt = new Date(parts[0], parts[1] - 1, parts[2] + (Number(days) || 0));
    return dt.getFullYear() + '-' + String(dt.getMonth()+1).padStart(2,'0') + '-' + String(dt.getDate()).padStart(2,'0');
  }catch(e){
    return dateIsoKey();
  }
}

function computeRemNoteIntervals(cardKey){
  ensureExtendedState();
  const entry = (state.cardSrs && state.cardSrs[cardKey]) || null;
  const reps = entry ? (Number(entry.reps) || 0) : 0;
  const curI = entry ? (Number(entry.interval) || 0) : 0;
  const ease = entry ? (Number(entry.ease) || 2.50) : 2.50;
  const lapses = entry ? (Number(entry.lapses) || 0) : 0;

  // Grade 1: Снова (Again) -> интервал 1 день, сброс серии, ease -0.20
  const againDays = 1;

  // Grade 2: Трудно (Hard) -> рост интервала с коэффициентом 1.2, ease -0.15
  let hardDays;
  if(reps === 0) hardDays = 1;
  else if(reps === 1) hardDays = 2;
  else hardDays = Math.max(curI + 1, Math.round(curI * 1.2));

  // Grade 3: Хорошо (Good) -> стандартная прогрессия SuperMemo-2 / RemNote
  let goodDays;
  if(reps === 0) goodDays = 1;
  else if(reps === 1) goodDays = 3;
  else goodDays = Math.max(hardDays + 1, Math.round(curI * ease));

  // Grade 4: Легко (Easy) -> ускоренная прогрессия с бонусом
  let easyDays;
  if(reps === 0) easyDays = 3;
  else if(reps === 1) easyDays = 7;
  else easyDays = Math.max(goodDays + 2, Math.round(curI * ease * 1.35));

  return {
    again: { days: againDays, ease: Math.max(1.30, +(ease - 0.20).toFixed(2)), reps: 0, lapses: lapses + 1 },
    hard:  { days: hardDays,  ease: Math.max(1.30, +(ease - 0.15).toFixed(2)), reps: Math.max(1, reps), lapses: lapses },
    good:  { days: goodDays,  ease: +ease.toFixed(2),                         reps: reps + 1, lapses: lapses },
    easy:  { days: easyDays,  ease: Math.min(3.50, +(ease + 0.15).toFixed(2)), reps: reps + 1, lapses: lapses }
  };
}

function applyRemNoteCardRating(cardKey, grade){
  ensureExtendedState();
  if(!state.cardSrs) state.cardSrs = {};
  const g = Number(grade) || 3;
  const intervals = computeRemNoteIntervals(cardKey);
  const gradeKey = g === 1 ? 'again' : (g === 2 ? 'hard' : (g === 4 ? 'easy' : 'good'));
  const nextInfo = intervals[gradeKey];
  const today = dateIsoKey();
  const nextDueDate = addDaysToDateKey(today, nextInfo.days);

  state.cardSrs[cardKey] = {
    reps: nextInfo.reps,
    interval: nextInfo.days,
    ease: nextInfo.ease,
    lapses: nextInfo.lapses,
    lastReview: today,
    dueDate: nextDueDate,
    lastGrade: g
  };

  // Поддерживаем совместимость с cardRatings
  state.cardRatings[cardKey] = Math.max(Number(state.cardRatings[cardKey]) || 0, g);
  saveState(state);
}

function getRemNoteCardStatusBadgeHTML(cardKey){
  ensureExtendedState();
  const entry = state.cardSrs && state.cardSrs[cardKey];
  if(!entry || !entry.dueDate){
    return `<span class="srs-card-status-badge srs-status-new" title="Карточка ещё не изучалась">🌱 Новая</span>`;
  }
  const today = dateIsoKey();
  const daysDiff = Math.round((new Date(entry.dueDate + 'T00:00:00') - new Date(today + 'T00:00:00')) / (1000 * 60 * 60 * 24));
  if(daysDiff <= 0){
    return `<span class="srs-card-status-badge srs-status-due" title="По расписанию RemNote нужно повторить сегодня">🔥 Повторить сегодня</span>`;
  } else if(entry.interval >= 21){
    return `<span class="srs-card-status-badge srs-status-mastered" title="Интервал ${entry.interval} дн. Следующее повторение: ${entry.dueDate}">👑 Закреплено (${entry.interval} дн)</span>`;
  } else {
    return `<span class="srs-card-status-badge srs-status-scheduled" title="Следующее повторение: ${entry.dueDate} (${daysDiff} дн)">📅 Через ${daysDiff} дн (${entry.dueDate})</span>`;
  }
}

// Compute Spaced Repetition Queue (SRS: weak cards rated 1..2 + RemNote calendar schedule due today)
function getSpacedRepetitionStats(){
  ensureExtendedState();
  const ratings = state.cardRatings || {};
  const srsMap = state.cardSrs || {};
  const today = (typeof dateIsoKey === 'function') ? dateIsoKey() : new Date().toISOString().slice(0,10);

  const weakDecks = new Set();
  const dueTodayDecks = new Set();
  let weakCardsCount = 0;
  let dueTodayCardsCount = 0;
  let masteredCardsCount = 0;

  Object.keys(ratings).forEach(k => {
    const r = Number(ratings[k]);
    if(r >= 1 && r <= 2){
      weakCardsCount++;
      const did = k.split(':')[0];
      if(ALL_DECKS_COMBINED[did]) weakDecks.add(did);
    }
  });

  Object.keys(srsMap).forEach(k => {
    const item = srsMap[k];
    if(item && item.dueDate){
      if(item.dueDate <= today){
        dueTodayCardsCount++;
        const did = k.split(':')[0];
        if(ALL_DECKS_COMBINED[did]) dueTodayDecks.add(did);
      }
      if(item.interval >= 21) masteredCardsCount++;
    }
  });

  const reviewed = (state.reviewedDecks || []).filter(did => ALL_DECKS_COMBINED[did]);
  const dueDecks = Array.from(new Set([...dueTodayDecks, ...weakDecks]));
  reviewed.forEach(did => {
    if(dueDecks.length < 4 && !dueDecks.includes(did)) dueDecks.push(did);
  });
  if(dueDecks.length === 0 && Object.keys(ALL_DECKS_COMBINED).length > 0){
    dueDecks.push('Ф-001');
  }
  return {
    weakCardsCount: weakCardsCount,
    reviewedDecksCount: reviewed.length,
    dueTodayCardsCount: dueTodayCardsCount,
    dueTodayDecksCount: dueTodayDecks.size,
    masteredCardsCount: masteredCardsCount,
    dueDecks: dueDecks
  };
}

// Reference Hub View (#/docs) — Complete Cheat Sheet & Set/Dict/List/SQL/Git Reference
function viewDocsHub(){
  return `
    <div class="container docs-hub">
      <div class="topic-badge">Инженерный справочник · Шпаргалка по структурам данных, Big-O, SQL и Git</div>
      <h1 style="margin-bottom:8px;">📚 Справочник Python Backend</h1>
      <p class="meta" style="margin-bottom:18px;">Полные таблицы операций, асимптотики <span class="math-formula">O(1)</span> / <span class="math-formula">O(n)</span> и синтаксиса, чтобы всегда держать под рукой во время практики и повторения карточек.</p>

      <div class="panel">
        <h2>1. Операции над множествами (<code>set</code>) и их сложность</h2>
        <p class="meta">Хеш-таблица уникальных элементов: проверка <code>x in s</code> работает за <span class="math-formula">O(1)</span> в среднем.</p>
        <div style="overflow-x:auto;">
          <table>
            <thead>
              <tr><th>Операция</th><th>Оператор</th><th>Метод</th><th>Описание и сложность</th></tr>
            </thead>
            <tbody>
              <tr><td>Объединение (Union)</td><td><code>a | b</code></td><td><code>a.union(b)</code></td><td>Все уникальные элементы из <code>a</code> и <code>b</code> · <span class="math-formula">O(len(a)+len(b))</span></td></tr>
              <tr><td>Пересечение (Intersection)</td><td><code>a &amp; b</code></td><td><code>a.intersection(b)</code></td><td>Только элементы, входящие и в <code>a</code>, и в <code>b</code> · <span class="math-formula">O(min(len(a),len(b)))</span></td></tr>
              <tr><td>Разность (Difference)</td><td><code>a - b</code></td><td><code>a.difference(b)</code></td><td>Элементы из <code>a</code>, которых нет в <code>b</code> · <span class="math-formula">O(len(a))</span></td></tr>
              <tr><td>Симметрическая разность (XOR)</td><td><code>a ^ b</code></td><td><code>a.symmetric_difference(b)</code></td><td>Элементы, входящие ровно в одно из множеств (без общих) · <span class="math-formula">O(len(a)+len(b))</span></td></tr>
              <tr><td>Подмножество / Надмножество</td><td><code>a &lt;= b</code> / <code>a &gt;= b</code></td><td><code>a.issubset(b)</code> / <code>a.issuperset(b)</code></td><td>Проверка включения всех элементов · <span class="math-formula">O(len(a))</span></td></tr>
              <tr><td>Добавление / Удаление</td><td>—</td><td><code>s.add(x)</code> / <code>s.discard(x)</code> / <code>s.remove(x)</code></td><td><code>discard(x)</code> не бросает <code>KeyError</code> при отсутствии ключа · <span class="math-formula">O(1)</span></td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="panel">
        <h2>2. Сравнение <code>list</code>, <code>dict</code>, <code>set</code> и <code>collections.deque</code></h2>
        <div style="overflow-x:auto;">
          <table>
            <thead>
              <tr><th>Структура</th><th>Поиск <code>x in c</code></th><th>Вставка в конец</th><th>Вставка/удаление в начало</th><th>Когда применять</th></tr>
            </thead>
            <tbody>
              <tr><td><code>list</code> (динамический массив)</td><td><span class="math-formula">O(n)</span></td><td><span class="math-formula">O(1)</span> амортиз.</td><td><span class="math-formula">O(n)</span> (сдвиг элементов)</td><td>Последовательный доступ по индексу <code>arr[i]</code> за <span class="math-formula">O(1)</span>, стек (<code>append</code>/<code>pop</code>).</td></tr>
              <tr><td><code>dict</code> (хеш-таблица пар)</td><td><span class="math-formula">O(1)</span> по ключу</td><td><span class="math-formula">O(1)</span></td><td>—</td><td>Быстрый поиск по ключу, подсчёт частот, группировка, кэширование.</td></tr>
              <tr><td><code>set</code> (хеш-таблица ключей)</td><td><span class="math-formula">O(1)</span></td><td><span class="math-formula">O(1)</span></td><td>—</td><td>Дедупликация, мгновенная проверка принадлежности <code>x in seen</code>, операции <code>&amp; | - ^</code>.</td></tr>
              <tr><td><code>deque</code> (двусвязный список блоков)</td><td><span class="math-formula">O(n)</span></td><td><span class="math-formula">O(1)</span></td><td><span class="math-formula">O(1)</span> (<code>popleft</code> / <code>appendleft</code>)</td><td>Очередь FIFO, BFS-обход графа, скользящее окно.</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="panel">
        <h2>3. Генераторы коллекций (Comprehensions) vs Generator Expression</h2>
        <div style="overflow-x:auto;">
          <table>
            <thead>
              <tr><th>Конструкция</th><th>Синтаксис</th><th>Память и поведение</th></tr>
            </thead>
            <tbody>
              <tr><td>Фильтрация (<code>if</code> в конце)</td><td><code>[x for x in items if x &gt; 0]</code></td><td>Оставляет только элементы, прошедшие условие (размер списка может уменьшиться). <code>else</code> здесь запрещён.</td></tr>
              <tr><td>Тернарная замена (<code>if..else</code> в начале)</td><td><code>[x if x &gt; 0 else 0 for x in items]</code></td><td>Преобразует каждый элемент, сохраняя длину списка (обязателен <code>else</code>).</td></tr>
              <tr><td>Генераторное выражение</td><td><code>(x * x for x in range(10**6))</code></td><td>Ленивый итератор (<span class="math-formula">O(1)</span> дополнительной памяти), вычисляет значения по одному в <code>sum(...)</code> / <code>any(...)</code>.</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>`;
}

// Override Dashboard with Variant A Mobile-First Cocoon Focus Screen + Trajectory Countdown + Spaced Repetition + 7-Track Mini-Matrix + Collapsible Modules Drawer
viewDashboard = function(){
  const tXp = todayXp();
  const goalPct = Math.min(100, Math.round(tXp / (state.dailyGoal || 50) * 100));
  const solvedMap = getIdeSolvedMap();
  const totalSolvedIde = countSolvedIdeTasks(solvedMap);

  const e1 = getEchelonProgress(1);
  const e2 = getEchelonProgress(2);
  const e3 = getEchelonProgress(3);
  const e4 = getEchelonProgress(4);
  const e1Remaining = e1.skills.filter(s => getSkillMP(s.id) < 100).length;
  const e1CurMp = e1.skills.reduce((sum, s) => sum + getSkillMP(s.id), 0);
  const e1MaxMp = Math.max(1, e1.skills.length * 100);
  const e1Pct = Math.min(100, Math.round(e1CurMp / e1MaxMp * 100));

  // Graduation Loop: при 100% готовности эшелона цель динамически переключается на следующий
  const curTargetTier = e1.pct < 100 ? 1 : (e2.pct < 100 ? 2 : (e3.pct < 100 ? 3 : 4));
  const curTargetEp = getEchelonProgress(curTargetTier);
  const curTargetMeta = (typeof getEchelonMeta === 'function' ? getEchelonMeta(curTargetTier) : (INTERVIEW_ECHELONS && INTERVIEW_ECHELONS[curTargetTier])) || { label: 'Эшелон ' + curTargetTier, shortLabel: 'Эшелон ' + curTargetTier, desc: '' };
  const curTargetRemaining = curTargetEp.skills.filter(s => getSkillMP(s.id) < 100).length;
  const curTargetTotalUnits = Math.max(1, curTargetEp.unitsCount || 14);
  const curTargetDoneUnits = Math.min(curTargetTotalUnits, Math.max(0, curTargetTotalUnits - Math.floor((curTargetRemaining / Math.max(1, curTargetEp.skills.length)) * curTargetTotalUnits)));
  const targetStageTitle = curTargetTier === 1
    ? `🎯 Готовность к 1-му тех-скринингу: ${e1Pct}%`
    : (curTargetTier === 2
      ? `🎯 Готовность к тех-интервью по стеку: ${e2.pct}%`
      : (curTargetTier === 3
        ? `⚡ Готовность к лайвкодингу и проду: ${e3.pct}%`
        : `👑 Готовность к финалу и офферу: ${e4.pct}%`));

  // Determine the next priority skill for the 2-minute Cocoon Focus Card and map anchor
  const openGaps = (state.diagnosticGaps || []).filter(sid => PY_SKILLS_BY_ID[sid] && getSkillMP(sid) < 100);
  const activeTierNum = e1.pct < 100 ? 1 : (e2.pct < 100 ? 2 : (e3.pct < 100 ? 3 : 4));
  const focusSk = openGaps.length > 0
    ? PY_SKILLS_BY_ID[openGaps[0]]
    : (getFirstUnmasteredSkillInEchelon(activeTierNum) || ALL_PY_SKILLS[0]);
  const focusKId = (focusSk && focusSk.kIds && focusSk.kIds.find(k => !state.readNotes.includes(k))) || (focusSk && focusSk.kIds && focusSk.kIds[0]) || 'К-001';
  const focusNoteObj = ALL_NOTES_COMBINED[focusKId] || { title: focusSk ? focusSk.title : 'Основы Python', steps: [] };
  const focusStepsCount = (focusNoteObj.steps && focusNoteObj.steps.length) || 3;
  const focusSid = focusSk ? focusSk.id : null;

  // Вычисляем текущий ранг подготовки
  const totalAllMp = totalPythonMP() + totalWebMP() + totalBackendMP() + totalAlgoMP() + totalDbMP() + totalArchMP() + totalInfraMP();
  let readinessRank = 'Junior Trainee';
  let rankIcon = '🌱';
  if(totalAllMp >= 9000){ readinessRank = 'Junior+ Backend Developer'; rankIcon = '👑'; }
  else if(totalAllMp >= 6000){ readinessRank = 'Junior Backend Developer'; rankIcon = '⚡'; }
  else if(totalAllMp >= 3000){ readinessRank = 'Junior Coder'; rankIcon = '🚀'; }

  // Spaced Repetition (SRS) Stats & Quick Review Deck Strip
  const srs = getSpacedRepetitionStats();
  const allDecksList = Object.values(ALL_DECKS_COMBINED || {});
  let dueTodayCardsCount = 0;
  allDecksList.forEach(d => {
    (d.cards || []).forEach((c, cIdx) => {
      const ck = d.id + ':' + cIdx;
      const r = state.cardRatings[ck] || 0;
      if(r > 0 && r < 4) dueTodayCardsCount++;
    });
  });
  const isSrsAllDone = dueTodayCardsCount === 0;
  const srsRingCircum = 2 * Math.PI * 15;
  const srsRingPct = isSrsAllDone ? 1 : Math.min(1, srs.reviewedDecksCount / Math.max(1, srs.reviewedDecksCount + dueTodayCardsCount));
  const srsRingOffset = srsRingCircum * (1 - srsRingPct);

  const dueDecks = allDecksList.filter(d => {
    return (d.cards || []).some((c, cIdx) => {
      const r = state.cardRatings[d.id + ':' + cIdx] || 0;
      return r > 0 && r < 4;
    });
  }).slice(0, 3);

  const srsDeckButtons = dueDecks.map(d =>
    `<a href="#/cards" class="btn btn-ghost" style="padding:4px 9px;font-size:.74rem;border-radius:8px;" title="Повторить колоду ${d.id}">🃏 ${d.id}</a>`
  ).join('') || `<a href="#/cards" class="btn btn-ghost" style="padding:4px 9px;font-size:.74rem;border-radius:8px;">Все колоды ➔</a>`;

  // Total metrics across all tracks
  const skillsAll = 126;
  const totalUnitsAll = 47;
  const historyActiveDays = Object.keys(state.dailyXpByDate || {}).length;
  const activeDaysCount = Math.max(historyActiveDays, state.streak || 0);

  const resultsTilesHTML = [
    { label: 'Готовность к скринингу', val: e1Pct + '%', sub: `${e1CurMp} / ${e1MaxMp} MP`, icon: '🎯' },
    { label: 'Навыков освоено', val: Object.keys(state.masteryLevels || {}).filter(k => (state.masteryLevels[k]||0)>=80).length + ' / ' + skillsAll, sub: `${Math.round(totalAllMp / 12600 * 100)}% базы`, icon: '⚡' },
    { label: 'Задач IDE решено', val: totalSolvedIde + ' / 401', sub: `${Math.round(totalSolvedIde / 401 * 100)}% практики`, icon: '💻' },
    { label: 'Повторено колод', val: srs.reviewedDecksCount + ' / 286', sub: `${srs.dueTodayDecksCount || (srs.dueTodayDecks ? srs.dueTodayDecks.size : 0)} ждут повторения`, icon: '🔁' }
  ].map(t => `
    <div class="dash-result-tile">
      <div class="tile-top"><span>${t.label}</span><span class="icon">${t.icon}</span></div>
      <div class="tile-val">${t.val}</div>
      <div class="tile-sub">${t.sub}</div>
    </div>
  `).join('');

  // 126-Skill Compact Matrix Across All 7 Tracks (Coddy: active tracks first, 0% to 'Ожидает открытия' and folded)
  const activeTrackRows = [];
  const dormantTrackRows = [];
  Object.values(MASTERY_TRACKS).forEach(tr => {
    const trCurMp = tr.skills.reduce((sum, s) => sum + getSkillMP(s.id), 0);
    const trMaxMp = Math.max(1, tr.skills.length * 100);
    const trPct = Math.round(trCurMp / trMaxMp * 100);
    const sqs = tr.skills.map(s => {
      const mp = getSkillMP(s.id);
      const isM = mp >= 100;
      const isA = mp > 0 && mp < 100;
      const isFocus = (s.id === focusSid);
      const focusCls = isFocus ? ' m-sq--focus' : '';
      return `<a href="#${s.routePrefix}/skill/${s.id}" class="m-sq ${isM ? 'mastered' : (isA ? 'active' : '')}${focusCls}" title="${s.id}: ${s.title} (${mp} MP)${isFocus ? ' · ТЕКУЩИЙ ФОКУС' : ''}"></a>`;
    }).join('');
    const statusText = trPct > 0 ? `${trPct}%` : 'Ожидает открытия';
    const rowHTML = `
      <div class="dash-skill-row">
        <a href="#${tr.routePrefix}" class="tr-label" title="Открыть матрицу ${tr.title}">${tr.title}</a>
        <div class="tr-squares">${sqs}</div>
        <div class="tr-pct" style="${trPct === 0 ? 'font-size:.72rem;color:var(--ink-muted);font-weight:600;' : ''}">${statusText}</div>
      </div>
    `;
    if(trPct > 0){
      activeTrackRows.push(rowHTML);
    } else {
      dormantTrackRows.push(rowHTML);
    }
  });

  const dormantHTML = dormantTrackRows.length > 0 ? `
    <details class="dash-accordion cocoon-details" style="margin-top:8px;border:none;background:transparent;padding:0;">
      <summary style="cursor:pointer;font-size:.78rem;color:var(--ink-muted);padding:4px 0;font-weight:600;">Остальные направления (${dormantTrackRows.length}) ▾</summary>
      <div style="margin-top:6px;">${dormantTrackRows.join('')}</div>
    </details>
  ` : '';

  const resultsMatrixHTML = (activeTrackRows.length > 0
    ? activeTrackRows.join('')
    : (dormantTrackRows.length > 0 ? dormantTrackRows.slice(0, 1).join('') : ''))
    + (activeTrackRows.length > 0 ? dormantHTML : (dormantTrackRows.length > 1 ? `
    <details class="dash-accordion cocoon-details" style="margin-top:8px;border:none;background:transparent;padding:0;">
      <summary style="cursor:pointer;font-size:.78rem;color:var(--ink-muted);padding:4px 0;font-weight:600;">Остальные направления (${dormantTrackRows.length - 1}) ▾</summary>
      <div style="margin-top:6px;">${dormantTrackRows.slice(1).join('')}</div>
    </details>` : ''));

  // Mini-list of echelon 1 topics with current focus badge
  const miniListHTML = e1.skills.map(s => {
    const mp = getSkillMP(s.id);
    const isFocusThis = s.id === focusSid;
    return `
      <div style="display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:.82rem;">
        <span style="font-weight:600;display:inline-flex;align-items:center;gap:6px;">
          <a href="#/python/skill/${s.id}" class="link-quiet" style="text-decoration:none;">${s.id} · ${s.title}</a>
        </span>
        <div style="display:flex;align-items:center;gap:6px;">
          ${isFocusThis ? `<span class="badge" style="background:rgba(16,185,129,0.18);border:1px solid rgba(16,185,129,0.35);color:var(--moss);padding:2px 8px;border-radius:6px;font-size:.72rem;font-weight:700;">✨ Текущий фокус</span>` : (mp === 100 ? `<span class="state-tag state-tag--mastered" style="font-size:.70rem;margin:0;">✓ 100 MP</span>` : `<span class="meta" style="font-size:.72rem;">${mp} MP</span>`)}
        </div>
      </div>
    `;
  }).join('');

  const focusFt = focusSk ? focusSk.title.match(/^(.*?)\s*\(([^()]*)\)\s*$/) : null;
  const focusTitleFormatted = focusFt ? `${focusSk.id} · ${focusFt[1]} <span class="t-detail">(${focusFt[2]})</span>` : (focusSk ? `${focusSk.id} · ${focusSk.title}` : 'Основы Python');

  return `
    <div class="container" style="max-width:880px;">
      <!-- Hero Header: Rank & Profile -->
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:16px;flex-wrap:wrap;">
        <div>
          <div class="hero__eyebrow meta">Твой путь к офферу · Python Backend Academy</div>
          <h1 style="font-size:1.65rem;letter-spacing:-0.02em;">${readinessRank} ${rankIcon}</h1>
          <div class="meta" style="font-size:.86rem;margin-top:2px;">
            Всего: <b>${totalAllMp}</b> / 12600 MP · 🔥 ${state.streak || 0} ${(state.streak % 10 === 1 && state.streak % 100 !== 11) ? 'день' : ((state.streak % 10 >= 2 && state.streak % 10 <= 4 && (state.streak % 100 < 10 || state.streak % 100 >= 20)) ? 'дня' : 'дней')} подряд · ⚡ ${state.xp || 0} XP
          </div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;">
          <a href="#/path" class="btn btn-ghost" style="padding:7px 12px;font-size:.82rem;">🗺️ 3D-Тропа</a>
          <button type="button" class="btn btn-ghost" data-open-settings-modal style="padding:7px 10px;font-size:.82rem;" title="Настройки платформы">⚙️</button>
        </div>
      </div>

      <!-- Key Checkpoint: Echelon 1 / Technical Screening -->
      <div class="cd-checkpoint-card" style="margin-bottom:12px;">
        <div class="cd-checkpoint-title">
          <span>🎯 Готовность к 1-му тех-скринингу</span>
          <span class="meta">${e1CurMp} / ${e1MaxMp} MP (${e1Pct}%)</span>
        </div>
        <div class="cd-bar cd-bar-track"><div class="cd-fill cd-bar-fill" style="width:${Math.max(6, e1Pct)}%;"></div></div>
        <div class="cd-checkpoint-sub">Эшелон 1 · Открывает готовность к первому тех-скринингу Junior Python</div>
      </div>

      <!-- Active 2-Minute Sprint Focus Card (Single Dominant CTA) -->
      <div class="cocoon-focus-card">
        <div class="cocoon-focus-eyebrow"><span class="pulse-ring-dot"></span>✨ Фокус сейчас · 2 мин</div>
        <div class="cocoon-focus-title">${focusTitleFormatted}</div>
        <button class="btn-glass-emerald btn-sprint-cta btn-dominant-cta" data-quick-microstep="">▶ Начать микро-шаг (2 мин) · +15 XP ⚡ ➔</button>
      </div>

      <!-- Current Sprint & 7-Day Rhythm Card -->
      <div class="dash-results-panel dash-sprint-panel">
        <div class="dash-goal-line">
          <span class="meta" style="font-weight:700;font-size:.88rem;color:var(--ink);">🎯 Дневная цель: ${tXp} / ${state.dailyGoal || 50} XP</span>
          <span class="meta" style="font-weight:800;color:var(--moss);">${goalPct}%</span>
        </div>
        <div class="mp-progress-track" style="margin:8px 0 12px;"><div class="mp-progress-fill" style="width:${goalPct}%;"></div></div>
        ${buildSevenDayHeatmapHTML()}
      </div>

      <!-- Spaced Repetition (SRS) Quick Review Strip -->
      <div class="panel srs-strip-card" style="padding:11px 14px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
        <div style="display:flex;align-items:center;gap:11px;">
          <svg class="srs-ring-svg" width="38" height="38" viewBox="0 0 38 38" aria-hidden="true" style="transform:none;overflow:visible;">
            <circle cx="19" cy="19" r="15" fill="none" stroke="rgba(148,163,184,0.2)" stroke-width="3.5"></circle>
            <circle cx="19" cy="19" r="15" fill="none" stroke="var(--moss)" stroke-width="3.5" stroke-dasharray="${srsRingCircum}" stroke-dashoffset="${srsRingOffset}" transform="rotate(-90 19 19)"></circle>
            ${isSrsAllDone ? `<text x="19" y="24" text-anchor="middle" font-size="14" font-weight="900" fill="var(--moss)">✓</text>` : ''}
          </svg>
          <div>
            <div style="font-weight:700;font-size:.86rem;">🔁 Интервальное повторение (SRS)</div>
            <div class="meta" style="font-size:.76rem;">${isSrsAllDone ? '<span style="color:var(--moss);font-weight:700;">Все карточки на сегодня повторены ✓</span> · Повторено колод: <b>' + srs.reviewedDecksCount + '</b>' : 'Повторено колод: <b>' + srs.reviewedDecksCount + '</b> · Карточек на закрепление: <b>' + dueTodayCardsCount + '</b>'}</div>
          </div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;">${srsDeckButtons}</div>
      </div>

      <!-- Mini-list of Echelon 1 Topics -->
      <details class="dash-accordion cocoon-details" style="margin-bottom:10px;">
        <summary style="cursor:pointer;font-weight:700;font-size:0.92rem;display:flex;justify-content:space-between;align-items:center;">
          <span>🐍 Темы Эшелона 1 (${e1.skills.filter(s => getSkillMP(s.id) >= 100).length}/${e1.skills.length} пройдено) ▾</span>
          <span class="link-quiet" style="font-size:.76rem;">Развернуть темы</span>
        </summary>
        <div style="margin-top:10px;">${miniListHTML}</div>
      </details>

      <!-- Collapsible Full 126-Skill Matrix & Tracks Accordion -->
      <details class="dash-accordion cocoon-details" style="margin-bottom:10px;">
        <summary>📊 Матрица компетенций и треки (развернуть) ▾</summary>
        <div class="dash-results-panel-inner" style="padding-top:12px;">
          <div class="dash-results-head" style="display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin-bottom:10px;flex-wrap:wrap;">
            <span style="font-weight:800;font-size:.92rem;color:var(--ink);">📊 Мои результаты</span>
            <span class="meta">${skillsAll} навыков · ${totalUnitsAll} юнитов · 🔥 ${activeDaysCount} ${(activeDaysCount % 10 === 1 && activeDaysCount % 100 !== 11) ? 'день' : ((activeDaysCount % 10 >= 2 && activeDaysCount % 10 <= 4 && (activeDaysCount % 100 < 10 || activeDaysCount % 100 >= 20)) ? 'дня' : 'дней')} активности</span>
          </div>
          <div class="dash-result-tiles">
            ${resultsTilesHTML}
          </div>
          <div class="dash-skill-matrix">
            ${resultsMatrixHTML}
          </div>
          <div style="margin-top:12px;text-align:center;">
            <a href="#/map" class="link-quiet" style="font-size:.82rem;font-weight:700;">🗺️ Открыть полную карту компетенций ➔</a>
          </div>
        </div>
      </details>

      <!-- Collapsible Drawer for All Modules, Echelons, Pomodoro & Global Stats -->
      <details class="cocoon-details">
        <summary>Все модули, эшелоны и статистика ▾</summary>
        <div style="margin-top:12px;"></div>
        ${buildPriorityRoadmapWidgetHTML({ compact: true })}
        <div class="panel" style="margin-bottom:0;">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <h3>⏱ Фокус-спринт (Помодоро)</h3>
            <button class="link-quiet" data-toggle-zen>${document.body.classList.contains('zen-mode') ? 'Выйти из Дзен' : '🧘 Дзен-режим'}</button>
          </div>
          <div style="display:flex;align-items:center;justify-content:space-between;margin:12px 0;">
            <span id="pomo-time-display" style="font-family:var(--font-d);font-size:2rem;font-weight:700;color:var(--moss-deep);">${formatPomo(pomoState.secondsLeft)}</span>
            <div style="display:flex;gap:6px;">
              <button class="btn ${pomoState.running?'btn-clay':'btn-primary'}" style="padding:8px 14px;font-size:.84rem;" data-pomo-toggle>${pomoState.running ? 'Пауза' : 'Старт'}</button>
              <button class="btn btn-ghost" style="padding:8px 10px;font-size:.8rem;" data-pomo-set="15">15м</button>
              <button class="btn btn-ghost" style="padding:8px 10px;font-size:.8rem;" data-pomo-set="25">25м</button>
            </div>
          </div>
          <p class="meta" style="margin:0;">Завершённый спринт приносит +25 XP. Звук: <button class="link-quiet" data-toggle-sound>${state.soundEnabled ? '🔊 Вкл' : '🔇 Выкл'}</button></p>
        </div>
      </details>

      <!-- Мотивационная подсказка текущего спринта в нейтральном деликатном тоне -->
      <div style="margin-top:12px;padding:11px 15px;border-radius:14px;background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.22);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
        <div style="display:flex;align-items:center;gap:8px;">
          <span class="badge" style="background:rgba(16,185,129,0.18);border:1px solid rgba(16,185,129,0.35);color:var(--moss);padding:2px 8px;border-radius:6px;font-size:.72rem;font-weight:700;">🎯 Текущий спринт</span>
          <span style="font-size:.84rem;color:var(--ink-muted);">Следующий рубеж: завершите Unit 1.1 для перехода к скринингу</span>
        </div>
        <a href="#/python" class="link-quiet" style="font-size:.78rem;font-weight:600;">Перейти к юниту ➔</a>
      </div>
    </div>`;
};

// Update Navigation items cleanly (1-line labels without redundant parenthetical numbers or duplicate emojis)
NAV_ITEMS.splice(0, NAV_ITEMS.length,
  {route:'/path', icon:'map', label:'3D-Тропа', shortLabel:'Тропа', mobileTab:true, group:'learn'},
  {route:'/practice', icon:'code', label:'Практика IDE', shortLabel:'IDE', mobileTab:true, group:'trainer'},
  {route:'/cards', icon:'cards', label:'Карточки', shortLabel:'Карточки', mobileTab:true, group:'trainer'},
  {route:'/mock', icon:'crown', label:'Собеседование', shortLabel:'Интервью', mobileTab:true, group:'trainer'},
  {route:'/', icon:'home', label:'Дашборд', shortLabel:'Дашборд', mobileTab:true, group:'learn'},
  {route:'/python', icon:'python', label:'Python Core', shortLabel:'Python', group:'module'},
  {route:'/web', icon:'globe', label:'Web и HTTP', shortLabel:'Web', group:'module'},
  {route:'/backend', icon:'server', label:'Backend', shortLabel:'Backend', group:'module'},
  {route:'/algorithms', icon:'bolt', label:'Алгоритмы', shortLabel:'Алгоритмы', group:'module'},
  {route:'/databases', icon:'database', label:'Базы данных', shortLabel:'БД', group:'module'},
  {route:'/architecture', icon:'arch', label:'Архитектура', shortLabel:'Архит.', group:'module'},
  {route:'/infra', icon:'rocket', label:'Инфраструктура', shortLabel:'Инфра', group:'module'},
  {route:'/docs', icon:'map', label:'Справочник', shortLabel:'Справочник', group:'tool'},
  {route:'/sandbox', icon:'terminal', label:'Песочница', shortLabel:'Песочница', group:'tool'}
);

renderNav = function(){
  const desk = document.getElementById('nav-desktop');
  if(desk){
    const modPctMap = {
      '/python': Math.round(totalPythonMP() / maxPythonMP() * 100),
      '/web': Math.round(totalWebMP() / 1000 * 100),
      '/backend': Math.round(totalBackendMP() / 2400 * 100),
      '/algorithms': Math.round(totalAlgoMP() / 1200 * 100),
      '/databases': Math.round(totalDbMP() / 1700 * 100),
      '/architecture': Math.round(totalArchMP() / 1400 * 100),
      '/infra': Math.round(totalInfraMP() / 2100 * 100)
    };
    const totalAllMp = totalPythonMP() + totalWebMP() + totalBackendMP() + totalAlgoMP() + totalDbMP() + totalArchMP() + totalInfraMP();
    const overallPct = Math.round(totalAllMp / 12600 * 100);
    const renderLink = function(it){
      const pctBadge = (modPctMap[it.route] !== undefined)
        ? `<span class="navlink__pct">${modPctMap[it.route]}%</span>`
        : '';
      return `<a href="#${it.route}" class="navlink" data-route="${it.route}">${ICONS[it.icon] || ICONS.dot}<span>${it.label}</span>${pctBadge}</a>`;
    };
    const learnLinks = NAV_ITEMS.filter(it => it.group === 'learn').map(renderLink).join('');
    const modLinks = NAV_ITEMS.filter(it => it.group === 'module').map(renderLink).join('');
    const trainerLinks = NAV_ITEMS.filter(it => it.group === 'trainer').map(renderLink).join('');
    const toolLinks = NAV_ITEMS.filter(it => it.group === 'tool').map(renderLink).join('');
    desk.innerHTML = `
      <div class="nav-group-label">Обучение</div>
      ${learnLinks}
      <details class="nav-modules-accordion">
        <summary class="nav-modules-summary"><span>📚 Модули 01–07</span><span class="navlink__pct">${overallPct}%</span></summary>
        <div class="nav-modules-list">${modLinks}</div>
      </details>
      <div class="nav-group-label">Тренажёры</div>
      ${trainerLinks}
      <div class="nav-group-label">Инструменты</div>
      ${toolLinks}
    `;
  }
  const mobItems = NAV_ITEMS.filter(it => it.mobileTab);
  document.querySelectorAll('.tabbar').forEach(tb=>{
    tb.innerHTML = mobItems.map(it=>{
      const lbl = it.shortLabel || it.label;
      return `<a href="#${it.route}" class="tabbar__item" data-route="${it.route}">${ICONS[it.icon] || ICONS.dot}<span>${lbl}</span></a>`;
    }).join('');
  });
};

// Smooth Theme Transition Wrapper (View Transition API + CSS smooth transition)
const _origToggleTheme = toggleTheme;
toggleTheme = function(){
  const runToggle = function(){
    try{ document.documentElement.classList.add('theme-transitioning'); }catch(e){}
    _origToggleTheme();
    setTimeout(function(){
      try{ document.documentElement.classList.remove('theme-transitioning'); }catch(e){}
    }, 360);
  };
  if(typeof document.startViewTransition === 'function'){
    try{ document.startViewTransition(runToggle); return; }catch(e){}
  }
  runToggle();
};

// Floating Bug Report Logger ("🐞 Сообщить о баге")
function getCurrentBugContextString(){
  const route = currentRoute();
  let extra = '';
  if(route.indexOf('/skill/') !== -1 && pySkillViewState){
    extra = ` | skill=${pySkillViewState.sid} tab=${pySkillViewState.tab} note=${pySkillViewState.kId || ''} step=${(pySkillViewState.stepIdx||0)+1} chunk=${(pySkillViewState.chunkIdx||0)+1} deck=${pySkillViewState.fId || ''} card=${(pySkillViewState.cardIdx||0)+1} task=${pySkillViewState.taskId || ''}`;
  } else if(route === '/cards' && cardsHubState){
    extra = ` | deck=${cardsHubState.deckId || ''} card=${(cardsHubState.cardIdx||0)+1}`;
  } else if(route === '/practice' && practiceHubState){
    extra = ` | task=${practiceHubState.taskId || ''}`;
  } else if((route === '/diagnostic' || route === '/topic/diag') && diagState){
    extra = ` | diagStage=${diagState.stage} qIdx=${(diagState.idx||0)+1}`;
  }
  return `#${route}${extra}`;
}

function openBugReportModal(){
  ensureExtendedState();
  if(!Array.isArray(state.bugReports)) state.bugReports = [];
  const existing = document.getElementById('bug-report-modal');
  if(existing) existing.remove();
  const ctxStr = getCurrentBugContextString();
  const listHtml = state.bugReports.length === 0
    ? `<p class="meta">Пока нет сохранённых заметок об ошибках.</p>`
    : state.bugReports.slice().reverse().map((b, idx) =>
        `<div class="panel" style="padding:10px 12px;margin-bottom:8px;">
          <div style="display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;font-size:.75rem;" class="meta">
            <span><b>${escapeHtmlStr(b.context || '')}</b></span>
            <span>${escapeHtmlStr(b.createdAt || '')}</span>
          </div>
          <div style="margin-top:4px;font-size:.88rem;white-space:pre-wrap;">${escapeHtmlStr(b.text || '')}</div>
        </div>`
      ).join('');
  const mdExport = state.bugReports.map((b, i) => `${i+1}. [${b.context}] (${b.createdAt}): ${b.text}`).join('\n');
  const modal = document.createElement('div');
  modal.id = 'bug-report-modal';
  modal.className = 'modal-backdrop';
  modal.innerHTML = `
    <div class="modal-card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
        <h2>🐞 Журнал замечаний и багов (${state.bugReports.length})</h2>
        <button class="btn btn-ghost" style="padding:6px 12px;" data-close-bug-modal>✕ Закрыть</button>
      </div>
      <p class="meta" style="margin-bottom:8px;">Текущий экран зафиксирован автоматически: <code>${escapeHtmlStr(ctxStr)}</code></p>
      <textarea id="bug-report-input" class="code-editor" style="min-height:88px;font-family:var(--font-b);" placeholder="Опиши ошибку, опечатку или неудобство на этом экране…"></textarea>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 16px;">
        <button class="btn btn-primary" data-save-bug-report>💾 Сохранить замечание</button>
        ${state.bugReports.length > 0 ? `<button class="btn btn-clay" data-copy-bug-reports>📋 Скопировать все (${state.bugReports.length})</button>` : ''}
        ${state.bugReports.length > 0 ? `<button class="btn btn-ghost" data-download-bug-reports>⬇️ Скачать .json</button>` : ''}
      </div>
      <textarea id="bug-reports-export-box" class="sr-only" readonly>${escapeHtmlStr(mdExport)}</textarea>
      <div style="max-height:240px;overflow-y:auto;">${listHtml}</div>
    </div>`;
  document.body.appendChild(modal);
}
window.openBugReportModal = openBugReportModal;

let isSettingsModalOpen = false;

function openSettingsModal(){
  ensureExtendedState();
  isSettingsModalOpen = true;
  const existing = document.getElementById('settings-modal');
  if(existing) existing.remove();

  const isGame = (state.pathViewMode !== 'pro');
  const isPro = (state.pathViewMode === 'pro');
  const pathNodeStyle = state.pathNodeStyle === 'button' ? 'button' : 'paw';

  const modal = document.createElement('div');
  modal.id = 'settings-modal';
  modal.className = 'modal-backdrop';
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');
  modal.innerHTML = `
    <div class="modal-card settings-modal-card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;">
        <h2 style="margin:0;font-size:1.35rem;display:flex;align-items:center;gap:10px;">
          <span>⚙️</span> Настройки платформы
        </h2>
        <button class="btn btn-ghost" style="padding:6px 12px;" data-close-settings-modal aria-label="Закрыть">✕ Закрыть</button>
      </div>

      <!-- Режим экрана обучения -->
      <div class="settings-section">
        <div class="settings-section-title">🎓 Режим экрана «Путь»</div>
        <p class="meta" style="margin-bottom:12px;font-size:0.82rem;">Выберите предпочтительный стиль отображения программы обучения:</p>
        <div class="settings-mode-grid">
          <button type="button" class="settings-mode-card ${isGame ? 'active' : ''}" data-set-path-mode="game">
            <div class="settings-mode-card-header">
              <span class="settings-mode-icon">🎮</span>
              <span class="settings-mode-name">Игровой режим</span>
              ${isGame ? '<span class="settings-mode-badge">Активен</span>' : ''}
            </div>
            <div class="settings-mode-desc">Извилистая игровая тропа с анимированными узлами и карточками юнитов.</div>
          </button>

          <button type="button" class="settings-mode-card ${isPro ? 'active' : ''}" data-set-path-mode="pro">
            <div class="settings-mode-card-header">
              <span class="settings-mode-icon">💼</span>
              <span class="settings-mode-name">Профессиональный</span>
              ${isPro ? '<span class="settings-mode-badge">Активен</span>' : ''}
            </div>
            <div class="settings-mode-desc">Структурированный список уроков по главам с верхней Hero-карточкой фокуса и бейджами «Теория + Практика».</div>
          </button>
        </div>
        <div class="path-node-style-picker" role="group" aria-label="Форма узлов игровой тропы">
          <div class="path-node-style-label">Форма узлов</div>
          <button type="button" class="path-node-style-btn ${pathNodeStyle === 'paw' ? 'active' : ''}" data-set-path-node-style="paw" aria-pressed="${pathNodeStyle === 'paw'}">🐾 Лапки</button>
          <button type="button" class="path-node-style-btn ${pathNodeStyle === 'button' ? 'active' : ''}" data-set-path-node-style="button" aria-pressed="${pathNodeStyle === 'button'}">◉ Кнопки</button>
        </div>
      </div>

      <!-- Тема и звук -->
      <div class="settings-section" style="margin-top:20px;">
        <div class="settings-section-title">🎨 Интерфейс и звук</div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px;">
          <button type="button" class="btn btn-ghost" id="settings-theme-toggle" style="flex:1;min-width:140px;">
            🌓 Тема: ${document.documentElement.getAttribute('data-theme') === 'light' ? 'Пергамент (Светлая)' : 'Обсидиан (Тёмная)'}
          </button>
          <button type="button" class="btn btn-ghost" id="settings-sound-toggle" style="flex:1;min-width:140px;">
            ${state.soundEnabled ? '🔊 Звук: Включён' : '🔇 Звук: Выключен'}
          </button>
        </div>
      </div>
      <!-- Рубежные тесты: разбор и стартовая модалка -->
      <div class="settings-section" style="margin-top:20px;">
        <div class="settings-section-title">🧪 Рубежные тесты</div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px;">
          <button type="button" class="btn btn-ghost" data-ut-toggle-explain style="flex:1;min-width:170px;">
            ${state.utShowExplanations ? '📝 Разбор после ответа: Вкл' : '📝 Разбор после ответа: Выкл'}
          </button>
          <button type="button" class="btn btn-ghost" data-ut-toggle-skipmodal style="flex:1;min-width:170px;">
            ${state.utSkipStartModal ? '⏭️ Открывать тест без модалки: Вкл' : '⏭️ Открывать тест без модалки: Выкл'}
          </button>
        </div>
        <p class="meta" style="margin:10px 0 0;font-size:0.78rem;">Стартовая модалка — окно «Готовы начать тест?» перед рубежным тестом. Дублирует тихую ссылку под её кнопками.</p>
      </div>

      <!-- Данные и сброс -->
      <div class="settings-section" style="margin-top:20px;border-top:1px solid var(--line);padding-top:16px;">
        <div class="settings-section-title">💾 Управление данными</div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px;">
          <button type="button" class="btn btn-ghost" data-open-handover style="font-size:0.85rem;">
            🔄 Перенос контекста
          </button>
          <button type="button" class="btn btn-ghost" data-open-bug-modal style="font-size:0.85rem;">
            🐞 Журнал замечаний
          </button>
          <button type="button" class="btn btn-ghost" id="settings-reset-btn" style="font-size:0.85rem;color:var(--burgundy-bright);">
            ⚠️ Сбросить прогресс
          </button>
        </div>
      </div>
    </div>`;

  document.body.appendChild(modal);
}

function closeSettingsModal(){
  isSettingsModalOpen = false;
  const m = document.getElementById('settings-modal');
  if(m) m.remove();
}
window.openSettingsModal = openSettingsModal;
window.closeSettingsModal = closeSettingsModal;


// Inject Ambient Background Orbs (.ambient-orb--burgundy & .ambient-orb--emerald), Onest Font, Bug Logger FAB, Global Pomodoro Pill & Sidebar Footer Quick Start
(function initCocoonAtmosphereAndSidebar(){
  try{
    if(!localStorage.getItem('academy-obsidian-v2')){
      localStorage.setItem('academy-obsidian-v2', '1');
      state.theme = 'dark';
      saveState(state);
      document.documentElement.setAttribute('data-theme', 'dark');
    } else if(!state.theme){
      state.theme = 'dark';
      document.documentElement.setAttribute('data-theme', 'dark');
    }
    if(document.head && !document.getElementById('onest-font-link')){
      const link = document.createElement('link');
      link.id = 'onest-font-link';
      link.rel = 'stylesheet';
      link.href = 'https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&display=swap';
      document.head.appendChild(link);
    }
    if(document.body && !document.getElementById('ambient-orb-burgundy')){
      const orb1 = document.createElement('div');
      orb1.id = 'ambient-orb-burgundy';
      orb1.className = 'ambient-orb ambient-orb--burgundy';
      document.body.insertBefore(orb1, document.body.firstChild);
      const orb2 = document.createElement('div');
      orb2.id = 'ambient-orb-emerald';
      orb2.className = 'ambient-orb ambient-orb--emerald';
      document.body.insertBefore(orb2, document.body.firstChild);
    }
  }catch(e){}
  const foot = document.querySelector('.sidebar-foot');
  if(!foot) return;
  const quickBtn = document.createElement('button');
  quickBtn.className = 'btn-quick-start';
  quickBtn.setAttribute('data-quick-microstep', '');
  quickBtn.innerHTML = '⚡ Микро-шаг (2 мин)';
  foot.insertBefore(quickBtn, foot.firstChild);

  const pomoPill = document.createElement('button');
  pomoPill.className = 'topbar-pomo-pill';
  pomoPill.setAttribute('data-pomo-toggle', '');
  pomoPill.setAttribute('title', 'Старт / Пауза Помодоро-таймера (25 мин)');
  pomoPill.innerHTML = '🍅 <span id="sidebar-pomo-time">' + formatPomo(pomoState.secondsLeft) + '</span>';
  foot.insertBefore(pomoPill, quickBtn.nextSibling);

  const hoBtn = document.createElement('button');
  hoBtn.className = 'link-quiet';
  hoBtn.setAttribute('data-open-handover', '');
  hoBtn.textContent = '🔄 Контекст для нового чата';
  foot.appendChild(hoBtn);

  const bugBtn = document.createElement('button');
  bugBtn.className = 'link-quiet';
  bugBtn.setAttribute('data-open-bug-modal', '');
  bugBtn.textContent = '🐞 Журнал замечаний';
  foot.appendChild(bugBtn);

  const setBtn = document.createElement('button');
  setBtn.className = 'link-quiet';
  setBtn.setAttribute('data-open-settings-modal', '');
  setBtn.innerHTML = '⚙️ Настройки';
  foot.appendChild(setBtn);

  const topbar = document.querySelector('.topbar');
  if(topbar && !topbar.querySelector('[data-open-settings-modal]')){
    const topSettingsBtn = document.createElement('button');
    topSettingsBtn.className = 'icon-btn';
    topSettingsBtn.setAttribute('data-open-settings-modal', '');
    topSettingsBtn.setAttribute('title', 'Настройки');
    topSettingsBtn.setAttribute('aria-label', 'Настройки');
    topSettingsBtn.innerHTML = '⚙️';
    const rightContainer = topbar.querySelector('div[style*="display:flex"]');
    if(rightContainer){
      rightContainer.insertBefore(topSettingsBtn, rightContainer.firstChild);
// Removed duplicate top bug button per user request 13
    }
  }
  // Mobile Floating Ladybug Quick Button (FAB)
  if(!document.getElementById('bug-fab-btn-floating')){
    const fab = document.createElement('button');
    fab.id = 'bug-fab-btn-floating';
    fab.className = 'bug-fab-btn';
    fab.setAttribute('data-open-bug-modal', '');
    fab.setAttribute('aria-label', 'Сообщить о баге (Alt+B)');
    fab.setAttribute('title', 'Сообщить о баге (Alt+B)');
    fab.innerHTML = '🐞';
    document.body.appendChild(fab);
  }
  // Global Hotkey (быстрая клавиша Alt+B, Ctrl+Shift+B, или B вне полей ввода)
  if(!window.__bugHotkeyBound){
    window.__bugHotkeyBound = true;
    document.addEventListener('keydown', function(e){
      const isB = (e.key === 'b' || e.key === 'B' || e.key === 'и' || e.key === 'И' || e.code === 'KeyB');
      const isAltB = (e.altKey && isB);
      const isCtrlShiftB = (e.ctrlKey && e.shiftKey && isB);
      const isPlainB = isB && !e.altKey && !e.ctrlKey && !e.metaKey;
      const tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : '';
      const isTyping = tag === 'input' || tag === 'textarea' || tag === 'select' || (e.target && e.target.isContentEditable) || (e.target && e.target.closest && e.target.closest('.CodeMirror'));

      if(isAltB || isCtrlShiftB || (isPlainB && !isTyping)){
        if(!document.getElementById('bug-report-modal')){
          e.preventDefault();
          if(typeof openBugReportModal === 'function') openBugReportModal();
        }
      }
    });
  }
})();

// Context Handover Modal ("Контекст для переноса в новый чат")
function buildHandoverMarkdown(){
  const solvedMap = getIdeSolvedMap();
  const solvedCount = countSolvedIdeTasks(solvedMap);
  return `# Контекст для продолжения работы в новом чате — Academy Python Backend

## 1. Ключевые файлы и единая облачная папка проекта
- **Единая облачная папка проекта (OneDrive)**: \`C:\\Users\\fury6\\OneDrive\\Python_Backend_Academy\` (ярлык на Рабочем столе: \`Python Backend Academy (Cloud).lnk\`)
- **Единый архив проекта**: \`C:\\Users\\fury6\\OneDrive\\Python_Backend_Academy\\Python_Backend_Academy_Project.zip\`
- **Подробный файл хэндовера**: \`C:\\Users\\fury6\\OneDrive\\Python_Backend_Academy\\HANDOVER_CONTEXT.md\` (и \`PROJECT_CONTEXT.md\`)
- **Главный интерактивный курс (Single-File SPA)**: \`C:\\Users\\fury6\\OneDrive\\Python_Backend_Academy\\academy.html\` и \`C:\\Users\\fury6\\Downloads\\Telegram Desktop\\academy.html\` (собирается через \`C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\assemble_academy.py\`)
- **Автономный тренажёр кода с IDE (401 задача)**: \`C:\\Users\\fury6\\OneDrive\\Python_Backend_Academy\\Практика кода — тренажёр с IDE.html\`
- **Каноническая база конспектов и карточек RemNote**: \`C:\\Users\\fury6\\OneDrive\\Python_Backend_Academy\\RemNote_Python_Mastery_FIXED\` (\`00 · 🗺️ Карта Мастерства.md\`: 7 модулей \`01 · 🐍 Python\`, \`02 · 🌐 Web\`, \`03 · ⚙️ Backend\`, \`04 · ⚡ Алгоритмы\`, \`05 · 🗄️ Базы данных\`, \`06 · 🏛️ Архитектура\`, \`07 · 🚀 Инфраструктура\`; всего 238 \`К-*\`, 286 \`Ф-*\` / 6 051 карточка)

## 2. Что уже реализовано и верифицировано на 100% (Все 7 модулей 01–07 + Боссы + Mock Interview + 4 Эшелона Приоритетов!)
1. **Модуль 01 (\`01 · 🐍 Python\`) — Вычитан на диске и вшит в \`#/python\`**:
   - **9 юнитов (1.1–1.9)**, **28 навыков (2800 MP)**, **68 конспектов \`К-*\` (381 микро-шаг)**, **126 колод \`Ф-*\` (2 181 карточка)**, 9 рубежных \`Unit Tests 1.1–1.9\`, \`Course Challenge\` и \`#/python/boss\`.
2. **Модуль 02 (\`02 · 🌐 Web\`) — Вычитан на диске и вшит в \`#/web\`**:
   - **4 юнита (2.1–2.4)**, **10 навыков (1000 MP)**, **23 конспекта \`К-*\`**, **25 колод \`Ф-*\` (491 карточка)**, 4 рубежных \`Unit Tests 2.1–2.4\`, \`Course Challenge\` и \`#/web/boss\`.
3. **Модуль 03 (\`03 · ⚙️ Backend\`) — Вычитан с нуля по 8 частям и вшит в \`#/backend\`**:
   - **8 частей/юнитов (3.1–3.8)**, **24 навыка (2400 MP)**, **40 конспектов \`К-*\`**, **43 колоды \`Ф-*\` (890 карточек)**, 8 рубежных \`Unit Tests 3.1–3.8\`, \`Course Challenge\` и \`#/backend/boss\`.
4. **Модуль 04 (\`04 · ⚡ Алгоритмы\`) — Вычитан на диске и вшит в \`#/algorithms\`**:
   - **6 юнитов (4.1–4.6)**, **12 навыков (1200 MP)**, **14 конспектов \`К-*\` (\`К-110\`..\`К-123\`)**, **16 колод \`Ф-*\` (463 карточки)**, 6 рубежных \`Unit Tests 4.1–4.6\`, \`Course Challenge\` и \`#/algorithms/boss\`.
5. **Модуль 05 (\`05 · 🗄️ Базы данных\`) — Вычитан с нуля на диске и вшит в \`#/databases\`**:
   - **6 юнитов (5.1–5.6)**, **17 навыков (1700 MP)**, **32 конспекта \`К-*\` (\`К-124\`..\`К-155\`)**, **32 колоды \`Ф-*\` (927 карточек)**, 6 рубежных \`Unit Tests 5.1–5.6\`, \`Course Challenge\` и \`#/databases/boss\`.
6. **Модуль 06 (\`06 · 🏛️ Архитектура\`) — Вычитан с нуля на диске и вшит в \`#/architecture\`**:
   - **6 юнитов (6.1–6.6)**, **14 навыков (1400 MP)**, **14 конспектов \`К-*\` (\`К-156\`..\`К-169\`, 56 микро-шагов)**, **17 колод \`Ф-*\` (263 карточки)**, 6 рубежных \`Unit Tests 6.1–6.6\`, \`Course Challenge\` и \`#/architecture/boss\`.
7. **Модуль 07 (\`07 · 🚀 Инфраструктура\`) — Вычитан с нуля на диске и вшит в \`#/infra\`**:
   - **6 юнитов (7.1–7.6)**, **21 навык (2100 MP)**, **47 конспектов \`К-*\` (\`К-170\`..\`К-216\`, 188 микро-шагов)**, **45 колод \`Ф-*\` в треке (34 уникальных в Модуле 07 + 11 кросс-модульных = 1 286 карточек, включая \`Ф-020@07\` на 43 карточки)**, 6 рубежных \`Unit Tests 7.1–7.6\`, \`Course Challenge\` и \`#/infra/boss\`.
8. **Сквозная Архитектура Приоритетов Собеседования (4 Эшелона \`Tier 1..4\`) + Параллельные ветки стека (\`FastAPI\` vs \`Django\` vs \`Оба\`) + Калибровочная Диагностика (\`#/topic/diag\`)**:
   - **🚨 Эшелон 1 (Скрининг и база — 14 юнитов)**, **🔥 Эшелон 2 (Тех-ядро и стек — 17 юнитов)**, **⚡ Эшелон 3 (Продакшен-инженерия — 11 юнитов)**, **👑 Эшелон 4 (Архитектурный резерв — 3 базовых юнита + невыбранная ветка фреймворка)**.
   - Умная сортировка юнитов («🔥 По приоритету собеседования» vs «🔢 По номеру юнита»), фильтр по эшелонам в \`#/python\`..\`#/infra\`, \`#/practice\`, \`#/cards\` и \`#/mock\`, а также калибровка \`50 MP\` и \`diagnosticGaps\` по итогам входной диагностики.
9. **Тренажёр кода с IDE (\`Практика кода — тренажёр с IDE.html\` и \`#/practice\`) + Симулятор собеседования (\`#/mock\`)**:
   - **401 задача** (\`🥚 Уровень 1\` .. \`👑 Уровень 7\`) + **7 Боссов модулей (\`#/<track>/boss\`)** + **Mock Interview Simulator (\`#/mock\`: Live-Coding 20 мин + STAR)**, шимы под **Brython 3.13.0** + резервный **Pyodide 0.26.4**, 4-уровневые сократовские подсказки (Scaffold Fading).
10. **Полная Карта Навыков (\`#/map\` — 18 узлов, 64 интерактивных урока)** и анти-прокрастинационный контур («Правило 2 минут», Помодоро 15/25 мин, Дзен-режим, стрики, 50 XP/день).

## 3. Текущий прогресс ученика
- **Текущий ранг**: ${(typeof curRankBadge !== 'undefined' ? curRankBadge : (getEchelonProgress(1).pct >= 60 ? '⚡ Скрининг почти готов' : '🌱 Старт подготовки'))}
- **Фокус на дашборде**: ${(typeof focusSk !== 'undefined' && focusSk ? focusSk.id + ' (' + focusSk.title + ') · конспект ' + focusKId : 'Основы Python')} · **Этап собеседования**: ${(typeof dashStage !== 'undefined' ? dashStage : 1)}
- **Выбранная ветка стека**: ${state.stackBranch || 'fastapi'} · **Пробелов скрининга в очереди**: ${(state.diagnosticGaps||[]).length}
- **Эшелон 1 (Скрининг)**: ${getEchelonProgress(1).curMp} / ${getEchelonProgress(1).maxMp} MP (${getEchelonProgress(1).pct}%)
- **Эшелон 2 (Тех-ядро)**: ${getEchelonProgress(2).curMp} / ${getEchelonProgress(2).maxMp} MP (${getEchelonProgress(2).pct}%)
- **Эшелон 3 (Продакшен)**: ${getEchelonProgress(3).curMp} / ${getEchelonProgress(3).maxMp} MP (${getEchelonProgress(3).pct}%)
- **Эшелон 4 (Резерв)**: ${getEchelonProgress(4).curMp} / ${getEchelonProgress(4).maxMp} MP (${getEchelonProgress(4).pct}%)
- **Очки мастерства Python**: ${totalPythonMP()} / ${maxPythonMP()} MP
- **Очки мастерства Web**: ${totalWebMP()} / ${maxWebMP()} MP
- **Очки мастерства Backend**: ${totalBackendMP()} / ${maxBackendMP()} MP
- **Очки мастерства Алгоритмы**: ${totalAlgoMP()} / ${maxAlgoMP()} MP
- **Очки мастерства Базы данных**: ${totalDbMP()} / ${maxDbMP()} MP
- **Очки мастерства Архитектура**: ${totalArchMP()} / ${maxArchMP()} MP
- **Очки мастерства Инфраструктура**: ${totalInfraMP()} / ${maxInfraMP()} MP
- **Пройдено Боссов модулей**: ${(state.passedBosses||[]).length} / 7 · **Раундов собеседования**: ${state.mockCompletedCount || 0}
- **Всего XP**: ${state.xp} XP · **Стрик**: ${state.streak} дн.
- **Пройдено уроков дерева**: ${state.completedLessons.length} / ${Object.keys(LESSONS).length}
- **Изучено конспектов К-xxx**: ${state.readNotes.length} / ${Object.keys(ALL_NOTES_COMBINED).length}
- **Пройдено колод Ф-xxx**: ${state.reviewedDecks.length} / ${Object.keys(ALL_DECKS_COMBINED).length}
- **Решено задач IDE**: ${solvedCount} / 401
`;
}

function importAndMergeBackupJsonString(rawText){
  const parsed = JSON.parse(rawText);
  if(!parsed || typeof parsed !== 'object' || Array.isArray(parsed)){
    throw new Error('JSON должен быть объектом с данными прогресса');
  }
  const incState = (parsed && parsed.academyState && typeof parsed.academyState === 'object') ? parsed.academyState : parsed;
  if(incState && typeof incState === 'object'){
    state = mergeProgressStates(state, incState);
    saveState(state);
  }
  if(parsed && parsed.ideStatus && typeof parsed.ideStatus === 'object'){
    const curIde = getIdeSolvedMap();
    const mergedIde = mergeIdeStatusMaps(curIde, parsed.ideStatus);
    const ideSer = JSON.stringify(mergedIde);
    localStorage.setItem('practice-ide-status', ideSer);
    try{ localStorage.setItem('practice-ide-status-backup', ideSer); }catch(ignore){}
    writeWindowNameBackup(state, mergedIde);
    syncToIndexedDBAsync(state, mergedIde);
  }
  if(parsed && parsed.ideDrafts && typeof parsed.ideDrafts === 'object'){
    const curDr = safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {};
    const mergedDr = mergeIdeDraftMaps(curDr, parsed.ideDrafts);
    try{ localStorage.setItem(IDE_DRAFTS_KEY, JSON.stringify(mergedDr)); }catch(ignore){}
    writeWindowNameBackup(state, getIdeSolvedMap(), mergedDr);
    syncToIndexedDBAsync(state, getIdeSolvedMap(), mergedDr);
  }
}

function openHandoverModal(){
  const existing = document.getElementById('handover-modal');
  if(existing) existing.remove();
  syncActiveEditorDrafts();
  saveLessonDraftState();
  saveReadingPosition();
  saveUnitTestDraftState();
  saveCardsHubPosState();
  savePracticeHubPosState();
  const md = buildHandoverMarkdown();
  const exportObj = {
    schemaVersion: ACADEMY_SCHEMA_VERSION,
    exportedAt: new Date().toISOString(),
    academyState: state,
    ideStatus: getIdeSolvedMap(),
    ideDrafts: safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {}
  };
  const jsonStr = JSON.stringify(exportObj);
  let hasPreReset = false;
  try{ hasPreReset = !!localStorage.getItem(PRE_RESET_BACKUP_KEY); }catch(e){}
  const modal = document.createElement('div');
  modal.id = 'handover-modal';
  modal.className = 'modal-backdrop';
  modal.innerHTML = `
    <div class="modal-card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
        <h2>🔄 Контекст для переноса в новый чат и бэкап</h2>
        <button class="btn btn-ghost" style="padding:6px 12px;" data-close-handover>✕ Закрыть</button>
      </div>
      <p class="meta">Скопируй этот блок и вставь в начале нового чата с ИИ-ассистентом, чтобы он мгновенно понял архитектуру курса и твой текущий прогресс:</p>
      <textarea id="handover-md-box" class="code-editor" style="min-height:190px;font-size:.8rem;" readonly>${escapeHtmlStr(md)}</textarea>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin:10px 0 18px;">
        <button class="btn btn-primary" data-copy-handover>📋 Скопировать промпт для нового чата</button>
      </div>
      <h3 style="margin-bottom:6px;">Экспорт / Импорт прогресса (JSON · безопасное слияние без потери данных)</h3>
      <textarea id="handover-json-box" class="code-editor" style="min-height:80px;font-size:.78rem;">${escapeHtmlStr(jsonStr)}</textarea>
      <div id="handover-import-status" class="meta" style="margin-top:6px;min-height:1.2em;"></div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px;align-items:center;">
        <button class="btn btn-clay" data-import-json>📥 Восстановить / объединить из JSON</button>
        <button class="btn btn-ghost" data-download-backup>💾 Скачать .json файл бэкапа</button>
        <button class="btn btn-ghost" data-upload-backup-btn>📂 Загрузить .json файл</button>
        <input type="file" id="handover-file-input" accept=".json,application/json" style="display:none;">
        ${hasPreReset ? `<button class="btn btn-ghost" data-restore-pre-reset>🛟 Восстановить до последнего сброса</button>` : ''}
      </div>
    </div>`;
  document.body.appendChild(modal);
}

// Override render() to handle all routes (#/python, #/web, #/backend, #/algorithms, #/databases, #/architecture, #/infra, #/<track>/boss, #/mock, #/cards, #/practice, #/docs, #/map, #/sandbox, #/diagnostic)
render = function(){
  if(window.theoryAudioPlayer && window.theoryAudioPlayer.isPlaying){
    window.theoryAudioPlayer.stop();
  }
  ensureExtendedState();
  const route = currentRoute();
  if(route && state.lastRoute !== route){
    state.lastRoute = route;
    try{ localStorage.setItem(STORE_KEY, JSON.stringify(state)); }catch(e){}
  }
  const root = document.getElementById('view-root');
  let navRoute = route;
  const isSprintFocus = route.indexOf('/skill/') !== -1 || route.indexOf('/lesson/') === 0;
  const isInteractiveRoute = ['/cards', '/practice', '/mock', '/interview-sim', '/sandbox'].includes(route) || route.indexOf('/boss') !== -1;
  try{
    document.body.classList.toggle('is-sprint-focus', isSprintFocus);
    document.body.classList.toggle('is-interactive-route', isInteractiveRoute);
  }catch(e){}
  if(route === '/' || route === '/dashboard'){
    root.innerHTML = viewDashboard();
    navRoute = '/';
  } else if(route === '/python'){
    root.innerHTML = viewPythonMastery('python');
    navRoute = '/python';
  } else if(route === '/python/boss'){
    root.innerHTML = viewModuleBoss('python');
    navRoute = '/python';
  } else if(route.indexOf('/python/skill/') === 0){
    const sid = route.slice(14);
    root.innerHTML = viewPythonSkill(sid);
    navRoute = getTrackForSkill(sid).routePrefix;
  } else if(route.indexOf('/python/unittest/') === 0){
    root.innerHTML = viewPythonUnitTest(route.slice(17), 'python');
    navRoute = '/python';
  } else if(route === '/web'){
    root.innerHTML = viewPythonMastery('web');
    navRoute = '/web';
  } else if(route === '/web/boss'){
    root.innerHTML = viewModuleBoss('web');
    navRoute = '/web';
  } else if(route.indexOf('/web/skill/') === 0){
    const sid = route.slice(11);
    root.innerHTML = viewPythonSkill(sid);
    navRoute = '/web';
  } else if(route.indexOf('/web/unittest/') === 0){
    root.innerHTML = viewPythonUnitTest(route.slice(14), 'web');
    navRoute = '/web';
  } else if(route === '/backend'){
    root.innerHTML = viewPythonMastery('backend');
    navRoute = '/backend';
  } else if(route === '/backend/boss'){
    root.innerHTML = viewModuleBoss('backend');
    navRoute = '/backend';
  } else if(route.indexOf('/backend/skill/') === 0){
    const sid = route.slice(15);
    root.innerHTML = viewPythonSkill(sid);
    navRoute = '/backend';
  } else if(route.indexOf('/backend/unittest/') === 0){
    root.innerHTML = viewPythonUnitTest(route.slice(18), 'backend');
    navRoute = '/backend';
  } else if(route === '/algorithms'){
    root.innerHTML = viewPythonMastery('algorithms');
    navRoute = '/algorithms';
  } else if(route === '/algorithms/boss'){
    root.innerHTML = viewModuleBoss('algorithms');
    navRoute = '/algorithms';
  } else if(route.indexOf('/algorithms/skill/') === 0){
    const sid = route.slice(18);
    root.innerHTML = viewPythonSkill(sid);
    navRoute = '/algorithms';
  } else if(route.indexOf('/algorithms/unittest/') === 0){
    root.innerHTML = viewPythonUnitTest(route.slice(21), 'algorithms');
    navRoute = '/algorithms';
  } else if(route === '/databases'){
    root.innerHTML = viewPythonMastery('databases');
    navRoute = '/databases';
  } else if(route === '/databases/boss'){
    root.innerHTML = viewModuleBoss('databases');
    navRoute = '/databases';
  } else if(route.indexOf('/databases/skill/') === 0){
    const sid = route.slice(17);
    root.innerHTML = viewPythonSkill(sid);
    navRoute = '/databases';
  } else if(route.indexOf('/databases/unittest/') === 0){
    root.innerHTML = viewPythonUnitTest(route.slice(20), 'databases');
    navRoute = '/databases';
  } else if(route === '/architecture'){
    root.innerHTML = viewPythonMastery('architecture');
    navRoute = '/architecture';
  } else if(route === '/architecture/boss'){
    root.innerHTML = viewModuleBoss('architecture');
    navRoute = '/architecture';
  } else if(route.indexOf('/architecture/skill/') === 0){
    const sid = route.slice(20);
    root.innerHTML = viewPythonSkill(sid);
    navRoute = '/architecture';
  } else if(route.indexOf('/architecture/unittest/') === 0){
    root.innerHTML = viewPythonUnitTest(route.slice(23), 'architecture');
    navRoute = '/architecture';
  } else if(route === '/infra' || route === '/infrastructure'){
    root.innerHTML = viewPythonMastery('infra');
    navRoute = '/infra';
  } else if(route === '/infra/boss' || route === '/infrastructure/boss'){
    root.innerHTML = viewModuleBoss('infra');
    navRoute = '/infra';
  } else if(route.indexOf('/infra/skill/') === 0){
    const sid = route.slice(13);
    root.innerHTML = viewPythonSkill(sid);
    navRoute = '/infra';
  } else if(route.indexOf('/infrastructure/skill/') === 0){
    const sid = route.slice(22);
    root.innerHTML = viewPythonSkill(sid);
    navRoute = '/infra';
  } else if(route.indexOf('/infra/unittest/') === 0){
    root.innerHTML = viewPythonUnitTest(route.slice(16), 'infra');
    navRoute = '/infra';
  } else if(route.indexOf('/infrastructure/unittest/') === 0){
    root.innerHTML = viewPythonUnitTest(route.slice(25), 'infra');
    navRoute = '/infra';
  } else if(route === '/mock' || route === '/interview-sim'){
    root.innerHTML = viewMockInterview();
    navRoute = '/mock';
  } else if(route === '/cards'){
    root.innerHTML = viewCardsHub();
    navRoute = '/cards';
  } else if(route === '/practice'){
    root.innerHTML = viewPracticeHub();
    navRoute = '/practice';
  } else if(route === '/docs' || route === '/reference'){
    root.innerHTML = viewDocsHub();
    navRoute = '/docs';
  } else if(route === '/path'){
    root.innerHTML = (state.pathViewMode === 'pro') ? viewProPath() : viewPathSerpentine();
    navRoute = '/path';
    // V12: активная нода тропы не должна оставаться под таб-баром — мягкий автоскролл к ней
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
    }, 60);
  } else if(route === '/map'){
    // Coddy-ref: один экран «Путь» — карта дублер дашборда; старые ссылки на #/map ведут на результаты
    root.innerHTML = viewDashboard();
    navRoute = '/';
  } else if(route === '/sandbox'){
    root.innerHTML = viewSandbox();
  } else if(route === '/diagnostic' || route === '/lesson/quiz'){
    root.innerHTML = viewDiagnostic();
    navRoute = '/';
  } else if(route.indexOf('/topic/') === 0){
    root.innerHTML = viewTopic(route.slice(7));
    navRoute = '/';
  } else if(route.indexOf('/lesson/') === 0){
    root.innerHTML = viewLesson(route.slice(8));
    navRoute = '/';
  } else {
    root.innerHTML = viewDashboard();
    navRoute = '/';
  }
  markActiveNav(isSprintFocus ? null : navRoute);
  // V8: экспресс-песочница навыка растёт по контенту — последняя строка кода не срезается
  setTimeout(function(){
    try{
      const growTa = document.getElementById('skill-lab-scratchpad');
      if(growTa && !growTa.dataset.autogrow){
        growTa.dataset.autogrow = '1';
        const fitTa = () => { growTa.style.height = 'auto'; growTa.style.height = Math.max(112, growTa.scrollHeight + 2) + 'px'; };
        fitTa();
        growTa.addEventListener('input', fitTa);
      }
    }catch(err){}
  }, 60);
  document.getElementById('streak-num-d').textContent = state.streak;
  document.getElementById('streak-num-m').textContent = state.streak;
  const swEl = document.getElementById('streak-word-d');
  if(swEl && typeof pluralizeRu === 'function'){
    swEl.textContent = pluralizeRu(state.streak, 'день', 'дня', 'дней') + ' подряд';
  }
  const tpEl = document.getElementById('topbar-pomo-time');
  if(tpEl) tpEl.textContent = formatPomo(pomoState.secondsLeft);
  const spEl = document.getElementById('sidebar-pomo-time');
  if(spEl) spEl.textContent = formatPomo(pomoState.secondsLeft);
  const tsBtn = document.getElementById('topbar-sound-btn');
  if(tsBtn) tsBtn.textContent = state.soundEnabled ? '🔊' : '🔇';
};

viewSandbox = function(){
  ensureExtendedState();
  const savedCode = (typeof state.sandboxDraft === 'string' && state.sandboxDraft.length > 0) ? state.sandboxDraft : SANDBOX_DEFAULT;
  return `
    <div class="container">
      <h1 style="margin-bottom:6px;">Песочница</h1>
      <p class="meta" style="margin-bottom:18px;">Настоящий Python прямо в браузере, без установки — на этом будет держаться вся практика с кодом. Удобнее за компьютером, но можно и с телефона.</p>
      <div class="sandbox-grid">
        <div>
          ${buildCodeEditorWithGutterHTML('code-input', savedCode, 'min-height:240px;', '')}
          <div style="margin-top:10px;display:flex;gap:10px;align-items:center;">
            <button class="btn btn-primary" id="run-btn">${ICONS.play} Запустить</button>
            <span class="meta" id="run-status"></span>
          </div>
        </div>
        <pre id="code-output">Нажми «Запустить» — при первом разе Python-движок грузится 5–15 секунд.</pre>
      </div>
    </div>`;
};

// Also upgrade runSandbox to use getFastPythonRunner()
runSandbox = async function(){
  const btn = document.getElementById('run-btn');
  const out = document.getElementById('code-output');
  const status = document.getElementById('run-status');
  const code = document.getElementById('code-input').value;
  ensureExtendedState();
  state.sandboxDraft = code;
  saveState(state);
  btn.setAttribute('disabled','disabled');
  status.textContent = 'Выполняю…';
  out.textContent = '';
  try{
    const runner = await getFastPythonRunner();
    let buf = '';
    runner.setStdout({ batched: function(s){ buf += s + '\n'; } });
    runner.setStderr({ batched: function(s){ buf += s + '\n'; } });
    try{
      runner.runPython(code);
    }catch(err){
      buf += String(err);
    }
    out.textContent = buf.trim() || '(программа ничего не вывела)';
    status.textContent = '';
    awardXp(2);
  }catch(e){
    out.textContent = 'Не получилось загрузить Python-движок: ' + String(e);
    status.textContent = '';
  }
  btn.removeAttribute('disabled');
};

/* ================= EXTENDED EVENT HANDLERS ================= */
document.addEventListener('click', async function(e){
  const runInl = e.target.closest('[data-run-inline], [data-run-snippet]');
  if(runInl){
    e.stopPropagation();
    runInlineSnippet(runInl);
    return;
  }

  if(e.target.closest('[data-diag-confirm]')){ confirmDiagAnswer(); return; }
  if(e.target.closest('[data-diag-prev]')){ prevDiagQuestion(); return; }

  const srsDeckBtn = e.target.closest('[data-srs-open-deck]');
  if(srsDeckBtn){
    const did = srsDeckBtn.getAttribute('data-srs-open-deck');
    if(did && ALL_DECKS_COMBINED[did]){
      cardsHubState.deckId = did;
      cardsHubState.cardIdx = 0;
      cardsHubState.flipped = false;
      saveCardsHubPosState();
      try{ playSound('flip'); }catch(e){}
      location.hash = '#/cards';
      render();
      return;
    }
  }

  if(e.target.closest('[data-open-settings-modal]')){ openSettingsModal(); return; }
  if(e.target.closest('[data-close-settings-modal]') || e.target.id === 'settings-modal'){ closeSettingsModal(); return; }
  if(e.target.closest('#settings-theme-toggle')){
    toggleTheme();
    openSettingsModal();
    return;
  }
  if(e.target.closest('#settings-sound-toggle')){
    state.soundEnabled = !state.soundEnabled;
    saveState(state);
    openSettingsModal();
    return;
  }
  if(e.target.closest('#settings-reset-btn')){
    closeSettingsModal();
    const rBtn = document.getElementById('reset-btn-d');
    if(rBtn) rBtn.click();
    return;
  }

  // Path Mode Switcher ('game' | 'pro')
  const modeBtn = e.target.closest('[data-set-path-mode]');
  if(modeBtn){
    const targetMode = modeBtn.getAttribute('data-set-path-mode');
    if(targetMode === 'game' || targetMode === 'pro'){
      ensureExtendedState();
      state.pathViewMode = targetMode;
      saveState(state);
      if(typeof isSettingsModalOpen !== 'undefined' && isSettingsModalOpen){
        openSettingsModal();
      }
      render();
      if(typeof showTactileToast === 'function'){
        showTactileToast(targetMode === 'pro' ? '💼 Включён профессиональный режим' : '🎮 Включён игровой режим 3D-тропы');
      }
    }
    return;
  }

  const nodeStyleBtn = e.target.closest('[data-set-path-node-style]');
  if(nodeStyleBtn){
    const nodeStyle = nodeStyleBtn.getAttribute('data-set-path-node-style');
    if(nodeStyle === 'paw' || nodeStyle === 'button'){
      ensureExtendedState();
      state.pathNodeStyle = nodeStyle;
      saveState(state);
      render();
      if(typeof isSettingsModalOpen !== 'undefined' && isSettingsModalOpen) openSettingsModal();
      if(typeof showTactileToast === 'function') showTactileToast(nodeStyle === 'paw' ? '🐾 Стиль карты: лапки' : '◉ Стиль карты: кнопки');
    }
    return;
  }

  // Pro Mode CTA start
  const proStartBtn = e.target.closest('[data-pro-start]');
  if(proStartBtn){
    const uid = proStartBtn.getAttribute('data-pro-start');
    const u = ALL_UNITS_COMBINED.find(x => x.id === uid);
    if(u){
      const track = getTrackForUnit(uid);
      const firstSkillId = (u.skills && u.skills[0]) ? u.skills[0].id : '';
      location.hash = `#${track.routePrefix}/skill/${firstSkillId}`;
    }
    return;
  }

  // Pro Mode lesson row click
  const proRow = e.target.closest('.pro-lesson-row');
  if(proRow){
    if((proRow.className && proRow.className.includes('pro-lesson-row--locked')) || (proRow.classList && proRow.classList.contains('pro-lesson-row--locked'))){
      if(typeof showTactileToast === 'function'){
        showTactileToast('🔒 Завершите предыдущие уроки для открытия');
      }
      return;
    }
    const uid = proRow.getAttribute('data-unit-id');
    const u = ALL_UNITS_COMBINED.find(x => x.id === uid);
    if(u){
      const track = getTrackForUnit(uid);
      const firstSkillId = (u.skills && u.skills[0]) ? u.skills[0].id : '';
      location.hash = `#${track.routePrefix}/skill/${firstSkillId}`;
    }
    return;
  }

  // Pro Mode chapter expand/collapse toggle
  const togChap = e.target.closest('[data-toggle-chapter]');
  if(togChap){
    const cNum = parseInt(togChap.getAttribute('data-toggle-chapter'), 10);
    if(proCollapsedChapters.has(cNum)){
      proCollapsedChapters.delete(cNum);
    } else {
      proCollapsedChapters.add(cNum);
    }
    render();
    return;
  }

  if(e.target.closest('[data-open-bug-modal]')){ openBugReportModal(); return; }
  if(e.target.closest('[data-close-bug-modal]') || e.target.id === 'bug-report-modal'){
    const bm = document.getElementById('bug-report-modal');
    if(bm) bm.remove();
    return;
  }
  if(e.target.closest('[data-save-bug-report]')){
    const inp = document.getElementById('bug-report-input');
    const txt = inp ? inp.value.trim() : '';
    if(txt){
      ensureExtendedState();
      if(!Array.isArray(state.bugReports)) state.bugReports = [];
      const reportItem = {
        context: getCurrentBugContextString(),
        text: txt,
        createdAt: new Date().toLocaleString('ru-RU'),
        timestamp: new Date().toISOString()
      };
      state.bugReports.push(reportItem);
      saveState(state);

      // Submit immediately to local server API queue if reachable
      try {
        fetch('/api/bug-report', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(reportItem)
        }).catch(function(err){
          console.warn('[BugReport] Local server offline, saved in localStorage:', err);
        });
      } catch(err){}

      // Submit to GitHub Gist if credentials present
      try {
        const gistToken = state.gistToken || localStorage.getItem('academy_gist_token');
        const gistId = state.gistId || localStorage.getItem('academy_gist_id');
        if(gistToken && gistId){
          fetch(`https://api.github.com/gists/${gistId}`, {
            method: 'PATCH',
            headers: {
              'Authorization': `Bearer ${gistToken}`,
              'Content-Type': 'application/json',
              'Accept': 'application/vnd.github+json'
            },
            body: JSON.stringify({
              files: {
                'user_feedback_queue.json': {
                  content: JSON.stringify(state.bugReports, null, 2)
                }
              }
            })
          }).catch(function(){});
        }
      } catch(err){}

      openBugReportModal();
    }
    return;
  }
  if(e.target.closest('[data-copy-bug-reports]')){
    const box = document.getElementById('bug-reports-export-box');
    if(box && navigator.clipboard){ navigator.clipboard.writeText(box.value); }
    e.target.closest('[data-copy-bug-reports]').textContent = '✓ Скопировано!';
    return;
  }
  if(e.target.closest('[data-download-bug-reports]')){
    try{
      const blob = new Blob([JSON.stringify(state.bugReports || [], null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'academy_bug_reports_' + dateIsoKey(new Date()) + '.json';
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(function(){ URL.revokeObjectURL(url); }, 1000);
    }catch(err){}
    return;
  }

  const dsBtn = e.target.closest('[data-dash-stage]');
  if(dsBtn){
    dashStage = parseInt(dsBtn.getAttribute('data-dash-stage'), 10) || 1;
    try{ playSound('tick'); }catch(e){}
    render();
    return;
  }

  const chunkMoreBtn = e.target.closest('[data-chunk-more]');
  if(chunkMoreBtn){
    const mode = chunkMoreBtn.getAttribute('data-chunk-more');
    ensureExtendedState();
    if(!state.unlockedChunks) state.unlockedChunks = {};
    if(mode === 'lesson'){
      const curLid = lessonMicroState.lessonId || (lessonState ? lessonState.lessonId : 'unknown');
      const curSIdx = lessonMicroState.stepIdx || 0;
      const nextCIdx = (lessonMicroState.chunkIdx || 0) + 1;
      const chunkKey = `lesson:${curLid}:${curSIdx}:${nextCIdx}`;
      if(!state.unlockedChunks[chunkKey]){
        state.unlockedChunks[chunkKey] = true;
        awardXp(10);
      }
      lessonMicroState.chunkIdx = nextCIdx;
      saveLessonDraftState();

      const feedContainer = document.getElementById('lesson-theory-text');
      const l = (typeof LESSONS !== 'undefined' ? LESSONS[curLid] : null) || {theory:'', title:''};
      const steps = (typeof splitHtmlIntoMicroSteps === 'function') ? splitHtmlIntoMicroSteps(l.theory, l.title) : [];
      const curStep = steps[curSIdx] || {title:'', html:''};
      const chunks = (typeof splitStepHtmlIntoChunks === 'function') ? splitStepHtmlIntoChunks(curStep.html) : [];

      if(!feedContainer || !feedContainer.isConnected){
        render();
        return;
      }

      if(feedContainer && nextCIdx < chunks.length){
        feedContainer.querySelectorAll('.feed-chunk-new').forEach(function(el){
          el.classList.remove('feed-chunk-new');
          el.classList.add('feed-chunk-prev');
        });
        const newEl = document.createElement('div');
        newEl.className = 'feed-chunk feed-chunk-new lesson-theory';
        newEl.setAttribute('data-chunk-idx', nextCIdx);
        newEl.innerHTML = chunks[nextCIdx];
        feedContainer.appendChild(newEl);

        const hasMore = (nextCIdx + 1 < chunks.length);
        const cardParent = feedContainer.closest('.coddy-lesson-card');
        if(!hasMore){
          chunkMoreBtn.removeAttribute('data-chunk-more');
          if(curSIdx + 1 < steps.length){
            chunkMoreBtn.setAttribute('data-lstep-jump', curSIdx + 1);
            chunkMoreBtn.textContent = `Следующий шаг (${curSIdx+2}/${steps.length}) (+10 XP) ➔`;
          } else {
            chunkMoreBtn.setAttribute('data-lesson-next', 'check');
            chunkMoreBtn.innerHTML = `Дальше: мини-проверка (+10 XP) ${ICONS.arrowRight}`;
          }
        }

        if(cardParent){
          const backBtn = cardParent.querySelector('[data-chunk-prev]');
          if(backBtn){
            backBtn.style.display = 'inline-flex';
            backBtn.style.visibility = 'visible';
            backBtn.style.pointerEvents = 'auto';
            backBtn.removeAttribute('disabled');
            backBtn.removeAttribute('aria-hidden');
          }
        }

        const sprintPct = Math.min(100, Math.max(10, Math.round(((curSIdx + (nextCIdx + 1) / Math.max(1, chunks.length)) / Math.max(1, steps.length)) * 100)));
        const fillEl = document.querySelector('.sprint-progress-fill');
        if(fillEl) fillEl.style.width = sprintPct + '%';

        const xpPill = document.querySelector('.sprint-xp-pill');
        if(xpPill && typeof todayXp === 'function'){
          const dayXpVal = todayXp();
          xpPill.textContent = `⚡ +${dayXpVal} XP за сутки`;
          xpPill.title = `Заработано за сутки: ${dayXpVal} XP`;
        }

        return;
      }
    } else {
      pySkillViewState.sprintCelebration = null;
      const activeK = pySkillViewState.kId || 'unknown';
      const curSIdx = pySkillViewState.stepIdx || 0;
      const nextCIdx = (pySkillViewState.chunkIdx || 0) + 1;
      const chunkKey = `skill:${activeK}:${curSIdx}:${nextCIdx}`;
      if(!state.unlockedChunks[chunkKey]){
        state.unlockedChunks[chunkKey] = true;
        awardXp(10);
      }
      pySkillViewState.chunkIdx = nextCIdx;
      saveReadingPosition();

      // Бесшовный инкрементальный append без стирания DOM и без дергания абзацев
      const feedContainer = document.getElementById('py-theory-text');
      const sk = (typeof ensurePySkillState === 'function') ? ensurePySkillState(pySkillViewState.sid) : {};
      const noteObj = (typeof ALL_NOTES_COMBINED !== 'undefined' ? ALL_NOTES_COMBINED[activeK] : null) || {steps:[]};
      const steps = noteObj.steps || [];
      const curStep = steps[curSIdx] || {title:'', html:''};
      const chunks = (typeof splitStepHtmlIntoChunks === 'function') ? splitStepHtmlIntoChunks(curStep.html).slice() : [];
      if(chunks.length > 0 && curStep.title && !/^<h[1-6]\b/i.test(String(chunks[0] || '').trim())){
        chunks[0] = `<h4>${curStep.title}</h4>\n` + chunks[0];
      }

      if(!feedContainer || !feedContainer.isConnected){
        render();
        return;
      }

      if(feedContainer && nextCIdx < chunks.length){
        // Снимаем класс анимации со старых блоков
        feedContainer.querySelectorAll('.feed-chunk-new').forEach(function(el){
          el.classList.remove('feed-chunk-new');
          el.classList.add('feed-chunk-prev');
        });
        // Создаем и добавляем один новый блок
        const newEl = document.createElement('div');
        newEl.className = 'feed-chunk feed-chunk-new lesson-theory';
        newEl.setAttribute('data-chunk-idx', nextCIdx);
        newEl.innerHTML = chunks[nextCIdx];
        feedContainer.appendChild(newEl);

        // Обновляем кнопку действия in-place без пересоздания DOM-узла
        const hasMore = (nextCIdx + 1 < chunks.length);
        const cardParent = feedContainer.closest('.coddy-lesson-card');
        const isRead = state.readNotes && state.readNotes.includes(activeK);
        if(!hasMore){
          chunkMoreBtn.removeAttribute('data-chunk-more');
          if(curSIdx + 1 < steps.length){
            const stepKey = `${activeK}:${curSIdx+1}`;
            const stepAlreadyDone = isRead || (state.completedNoteSteps && state.completedNoteSteps[stepKey]);
            chunkMoreBtn.setAttribute('data-py-next-step', curSIdx + 1);
            chunkMoreBtn.textContent = `Понятно, дальше${stepAlreadyDone ? '' : ' (+10 XP)'} ➔`;
          } else {
            chunkMoreBtn.setAttribute('data-py-finish-note', activeK);
            chunkMoreBtn.textContent = isRead ? '✓ Конспект усвоен' : '✓ Завершить конспект (+10 MP)';
          }
        }

        // Показываем кнопку «Назад» на месте существующего слота
        if(cardParent){
          const backBtn = cardParent.querySelector('[data-chunk-prev]');
          if(backBtn){
            backBtn.style.display = 'inline-flex';
            backBtn.style.visibility = 'visible';
            backBtn.style.pointerEvents = 'auto';
            backBtn.removeAttribute('disabled');
            backBtn.removeAttribute('aria-hidden');
          }
        }

        // Обновляем XP в шапке
        const xpPill = document.querySelector('.sprint-xp-pill');
        if(xpPill && typeof todayXp === 'function'){
          const dayXpVal = todayXp();
          xpPill.textContent = `⚡ +${dayXpVal} XP за сутки`;
          xpPill.title = `Заработано за сутки: ${dayXpVal} XP`;
        }

        return;
      }
    }
    render();
    return;
  }

  const chunkPrevBtn = e.target.closest('[data-chunk-prev]');
  if(chunkPrevBtn){
    const mode = chunkPrevBtn.getAttribute('data-chunk-prev');
    if(mode === 'lesson'){
      const feedContainer = document.getElementById('lesson-theory-text');
      if(feedContainer && lessonMicroState.chunkIdx > 0){
        const lastChunkEl = feedContainer.querySelector(`[data-chunk-idx="${lessonMicroState.chunkIdx}"]`);
        if(lastChunkEl){
          lastChunkEl.remove();
        }
        lessonMicroState.chunkIdx -= 1;
        saveLessonDraftState();

        const curLastChunk = feedContainer.querySelector(`[data-chunk-idx="${lessonMicroState.chunkIdx}"]`);
        if(curLastChunk){
          curLastChunk.classList.remove('feed-chunk-prev');
          curLastChunk.classList.add('feed-chunk-new');
        }

        const cardParent = feedContainer.closest('.coddy-lesson-card');
        if(cardParent){
          if(lessonMicroState.chunkIdx === 0 && (lessonMicroState.stepIdx || 0) === 0){
            chunkPrevBtn.style.display = 'none';
            chunkPrevBtn.style.visibility = 'hidden';
            chunkPrevBtn.style.pointerEvents = 'none';
            chunkPrevBtn.setAttribute('disabled', '');
            chunkPrevBtn.setAttribute('aria-hidden', 'true');
          }
          const actBtn = cardParent.querySelector('[data-lstep-jump], [data-lesson-next], [data-chunk-more]');
          if(actBtn){
            actBtn.removeAttribute('data-lstep-jump');
            actBtn.removeAttribute('data-lesson-next');
            actBtn.setAttribute('data-chunk-more', 'lesson');
            actBtn.textContent = 'Понятно, дальше (+10 XP) ➔';
          }
        }

        const curLid = lessonMicroState.lessonId || (lessonState ? lessonState.lessonId : 'unknown');
        const l = (typeof LESSONS !== 'undefined' ? LESSONS[curLid] : null) || {theory:'', title:''};
        const steps = (typeof splitHtmlIntoMicroSteps === 'function') ? splitHtmlIntoMicroSteps(l.theory, l.title) : [];
        const curStep = steps[lessonMicroState.stepIdx || 0] || {title:'', html:''};
        const chunks = (typeof splitStepHtmlIntoChunks === 'function') ? splitStepHtmlIntoChunks(curStep.html) : [];
        const sprintPct = Math.min(100, Math.max(10, Math.round((((lessonMicroState.stepIdx || 0) + (lessonMicroState.chunkIdx + 1) / Math.max(1, chunks.length)) / Math.max(1, steps.length)) * 100)));
        const fillEl = document.querySelector('.sprint-progress-fill');
        if(fillEl) fillEl.style.width = sprintPct + '%';

        return;
      }

      if(lessonMicroState.chunkIdx > 0){
        lessonMicroState.chunkIdx -= 1;
      } else if(lessonMicroState.stepIdx > 0){
        lessonMicroState.stepIdx -= 1;
        lessonMicroState.chunkIdx = 0;
      }
      saveLessonDraftState();
    } else {
      const feedContainer = document.getElementById('py-theory-text');
      if(feedContainer && pySkillViewState.chunkIdx > 0){
        // Удаляем последний добавленный блок из DOM
        const lastChunkEl = feedContainer.querySelector(`[data-chunk-idx="${pySkillViewState.chunkIdx}"]`);
        if(lastChunkEl){
          lastChunkEl.remove();
        }
        pySkillViewState.chunkIdx -= 1;
        saveReadingPosition();

        // Помечаем актуальный последний блок
        const curLastChunk = feedContainer.querySelector(`[data-chunk-idx="${pySkillViewState.chunkIdx}"]`);
        if(curLastChunk){
          curLastChunk.classList.remove('feed-chunk-prev');
          curLastChunk.classList.add('feed-chunk-new');
        }

        const cardParent = feedContainer.closest('.coddy-lesson-card');
        if(cardParent){
          // Если откатились на нулевой чанк и нулевой шаг — плавно скрываем слот «Назад»
          if(pySkillViewState.chunkIdx === 0 && (pySkillViewState.stepIdx || 0) === 0){
            chunkPrevBtn.style.display = 'none';
            chunkPrevBtn.style.visibility = 'hidden';
            chunkPrevBtn.style.pointerEvents = 'none';
            chunkPrevBtn.setAttribute('disabled', '');
            chunkPrevBtn.setAttribute('aria-hidden', 'true');
          }
          // Кнопка действия возвращается в состояние data-chunk-more
          const actBtn = cardParent.querySelector('[data-py-next-step], [data-py-finish-note], [data-chunk-more]');
          if(actBtn){
            actBtn.removeAttribute('data-py-next-step');
            actBtn.removeAttribute('data-py-finish-note');
            actBtn.setAttribute('data-chunk-more', 'py');
            actBtn.textContent = 'Понятно, дальше (+10 XP) ➔';
          }
        }

        return;
      }

      if(pySkillViewState.chunkIdx > 0){
        pySkillViewState.chunkIdx -= 1;
      } else if(pySkillViewState.stepIdx > 0){
        pySkillViewState.stepIdx -= 1;
        const sk = PY_SKILLS_BY_ID[pySkillViewState.sid] || {};
        const activeK = pySkillViewState.kId || (sk.kIds && sk.kIds[0]);
        const noteObj = ALL_NOTES_COMBINED[activeK];
        const prevStep = noteObj && noteObj.steps && noteObj.steps[pySkillViewState.stepIdx];
        const prevChunks = prevStep ? splitStepHtmlIntoChunks(prevStep.html) : [];
        pySkillViewState.chunkIdx = Math.max(0, prevChunks.length - 1);
      }
      saveReadingPosition();
    }
    render();
    return;
  }

  const tc = e.target.closest('[data-tap-chip-val]');
  if(tc){
    const val = tc.getAttribute('data-tap-chip-val');
    const key = tc.getAttribute('data-tap-chip-key');
    const correct = tc.getAttribute('data-tap-chip-correct');
    if(!window.__tapExState) window.__tapExState = {};
    const prevVal = window.__tapExState[key];
    const newVal = (prevVal === val) ? null : val;
    window.__tapExState[key] = newVal;
    const isNowCorrect = (newVal === correct);
    if(navigator && navigator.vibrate) try{ navigator.vibrate(isNowCorrect ? [15] : [30, 40, 30]); }catch(e){}
    if(!window.__tapExSolved) window.__tapExSolved = {};
    if(isNowCorrect && !window.__tapExSolved[key]){
      window.__tapExSolved[key] = true;
      awardXp(10);
    }
    render();
    return;
  }

  const chunkRevBtn = e.target.closest('[data-chunk-reveal-step]');
  if(chunkRevBtn){
    const mode = chunkRevBtn.getAttribute('data-chunk-reveal-step');
    if(mode === 'lesson'){
      lessonMicroState.chunkIdx = 999;
      saveLessonDraftState();
    } else {
      pySkillViewState.sprintCelebration = null;
      pySkillViewState.chunkIdx = 999;
      saveReadingPosition();
    }
    render();
    return;
  }

  const sbBtn = e.target.closest('[data-stack-branch]');
  if(sbBtn){
    setStackBranch(sbBtn.getAttribute('data-stack-branch'));
    render();
    return;
  }

  const pnsBtn = e.target.closest('[data-priority-next-skill]');
  if(pnsBtn){
    const sid = pnsBtn.getAttribute('data-priority-next-skill');
    if(sid){
      const tr = getTrackForSkill(sid);
      location.hash = '#' + tr.routePrefix + '/skill/' + sid;
      render();
    }
    return;
  }

  const usBtn = e.target.closest('[data-unit-sort]');
  if(usBtn){
    ensureExtendedState();
    state.unitSortMode = usBtn.getAttribute('data-unit-sort') === 'number' ? 'number' : 'priority';
    saveState(state);
    render();
    return;
  }

  const ttfBtn = e.target.closest('[data-track-tier-filter]');
  if(ttfBtn){
    trackTierFilter = ttfBtn.getAttribute('data-track-tier-filter') || 'all';
    render();
    return;
  }

  const oenBtn = e.target.closest('[data-open-echelon-next]');
  if(oenBtn){
    const targetTier = parseInt(oenBtn.getAttribute('data-open-echelon-next'), 10) || 1;
    const p = getEchelonProgress(targetTier);
    const sk = p.nextSkill || (p.skills && p.skills[0]) || getFirstUnmasteredSkillInEchelon(targetTier) || ALL_PY_SKILLS[0];
    if(sk){
      const tr = getTrackForSkill(sk.id);
      location.hash = '#' + tr.routePrefix + '/skill/' + sk.id;
      render();
    }
    return;
  }

  const bpf = e.target.closest('[data-backend-part-filter]');
  if(bpf){
    backendPartFilter = bpf.getAttribute('data-backend-part-filter') || 'all';
    render();
    return;
  }

  const qmBtn = e.target.closest('[data-quick-microstep]');
  if(qmBtn){
    pySkillViewState.sprintCelebration = null;
    const sid = qmBtn.getAttribute('data-quick-microstep') || '';
    const kid = qmBtn.getAttribute('data-quick-kid') || '';
    try{ playSound('tick'); }catch(e){}
    startTwoMinuteMicroStep(sid, kid);
    return;
  }
  if(e.target.closest('[data-open-handover]')){ openHandoverModal(); return; }
  if(e.target.closest('[data-close-handover]') || e.target.id === 'handover-modal'){
    const m = document.getElementById('handover-modal');
    if(m) m.remove();
    return;
  }
  if(e.target.closest('[data-copy-handover]')){
    const box = document.getElementById('handover-md-box');
    if(box && navigator.clipboard){ navigator.clipboard.writeText(box.value); }
    e.target.closest('[data-copy-handover]').textContent = '✓ Скопировано в буфер обмена!';
    return;
  }
  if(e.target.closest('[data-import-json]')){
    const box = document.getElementById('handover-json-box');
    const stEl = document.getElementById('handover-import-status');
    try{
      importAndMergeBackupJsonString(box ? box.value : '');
      const m = document.getElementById('handover-modal');
      if(m) m.remove();
      render();
    }catch(err){
      if(stEl){
        stEl.style.color = '#ef4444';
        stEl.textContent = 'Ошибка формата JSON: ' + String(err && err.message ? err.message : err);
      } else {
        alert('Ошибка формата JSON: ' + err);
      }
    }
    return;
  }
  if(e.target.closest('[data-download-backup]')){
    try{
      syncActiveEditorDrafts();
      saveLessonDraftState();
      saveReadingPosition();
      saveUnitTestDraftState();
      saveCardsHubPosState();
      savePracticeHubPosState();
      const exportObj = {
        schemaVersion: ACADEMY_SCHEMA_VERSION,
        exportedAt: new Date().toISOString(),
        academyState: state,
        ideStatus: getIdeSolvedMap(),
        ideDrafts: safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {}
      };
      const blob = new Blob([JSON.stringify(exportObj, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'python_backend_academy_backup_' + dateIsoKey(new Date()) + '.json';
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(function(){ URL.revokeObjectURL(url); }, 1000);
    }catch(err){}
    return;
  }
  if(e.target.closest('[data-upload-backup-btn]')){
    const fi = document.getElementById('handover-file-input');
    if(fi) fi.click();
    return;
  }
  if(e.target.closest('[data-restore-pre-reset]')){
    try{
      const raw = localStorage.getItem(PRE_RESET_BACKUP_KEY);
      const snap = safeParseJsonObj(raw);
      if(snap){
        if(snap.academyState){
          state = mergeProgressStates(state, snap.academyState);
          saveState(state);
        }
        if(snap.ideStatus){
          const mergedIde = mergeIdeStatusMaps(getIdeSolvedMap(), snap.ideStatus);
          const ideSer = JSON.stringify(mergedIde);
          localStorage.setItem('practice-ide-status', ideSer);
          try{ localStorage.setItem('practice-ide-status-backup', ideSer); }catch(ignore){}
        }
        if(snap.ideDrafts){
          const curDr = safeParseJsonObj(localStorage.getItem(IDE_DRAFTS_KEY)) || {};
          const mergedDr = mergeIdeDraftMaps(curDr, snap.ideDrafts);
          try{ localStorage.setItem(IDE_DRAFTS_KEY, JSON.stringify(mergedDr)); }catch(ignore){}
        }
        const m = document.getElementById('handover-modal');
        if(m) m.remove();
        render();
      }
    }catch(err){}
    return;
  }

  // Pomodoro & Zen & Sound
  if(e.target.closest('[data-pomo-toggle]')){ togglePomodoro(); return; }
  const ps = e.target.closest('[data-pomo-set]');
  if(ps){ togglePomodoro(parseInt(ps.getAttribute('data-pomo-set'), 10)); return; }
  if(e.target.closest('[data-toggle-zen]')){
    document.body.classList.toggle('zen-mode');
    try{ playSound('tick'); }catch(e){}
    render();
    return;
  }
  if(e.target.closest('[data-toggle-sound]')){
    state.soundEnabled = !state.soundEnabled;
    saveState(state);
    if(state.soundEnabled){
      try{ playSound('complete'); }catch(e){}
      if(typeof showTactileToast === 'function') showTactileToast('🔊 Звуковые эффекты включены');
    } else {
      if(typeof showTactileToast === 'function') showTactileToast('🔇 Звуковые эффекты выключены');
    }
    render();
    return;
  }

  // Lesson micro-steps
  const lj = e.target.closest('[data-lstep-jump]');
  if(lj){
    const nextIdx = parseInt(lj.getAttribute('data-lstep-jump'), 10);
    ensureExtendedState();
    if(!state.completedLessonSteps) state.completedLessonSteps = {};
    const curLid = lessonMicroState.lessonId || (lessonState ? lessonState.lessonId : 'unknown');
    const stepKey = `${curLid}:${nextIdx}`;
    if(nextIdx > lessonMicroState.stepIdx && !state.completedLessonSteps[stepKey]){
      state.completedLessonSteps[stepKey] = true;
      awardXp(10);
    }
    lessonMicroState.stepIdx = nextIdx;
    lessonMicroState.chunkIdx = 0;
    saveLessonDraftState();
    render();
    return;
  }
  if(e.target.closest('[data-lstep-toggle-full]')){
    lessonMicroState.fullMode = !lessonMicroState.fullMode;
    saveLessonDraftState();
    render();
    return;
  }

  // Mastery Matrix & Skill actions (Python, Web, Backend, Algorithms, Databases, Architecture, Infrastructure)
  const drt = e.target.closest('.dash-result-tile');
  if(drt){ try{ playSound('tick'); }catch(e){} }

  const hc = e.target.closest('[data-heat-day]');
  if(hc){
    const hDay = hc.getAttribute('data-heat-day');
    const hXp = parseInt(hc.getAttribute('data-heat-xp'), 10) || 0;
    const isToday = hc.getAttribute('data-heat-today') === '1';
    try{ playSound('tick'); }catch(e){}
    if(typeof showTactileToast === 'function'){
      if(isToday){
        if(hXp >= (state.dailyGoal || 50)){
          showTactileToast(`🎉 Сегодня: ${hXp} XP! Дневная цель выполнена на 100%!`);
        } else if(hXp > 0){
          showTactileToast(`⚡ Сегодня: ${hXp} из ${state.dailyGoal || 50} XP. Ещё один спринт до цели!`);
        } else {
          showTactileToast(`🔥 Сегодня пока 0 XP. Нажми «Начать спринт», чтобы зажечь огонёк!`);
        }
      } else {
        if(hXp >= (state.dailyGoal || 50)){
          showTactileToast(`✓ ${hDay}: ${hXp} XP · Цель дня закрыта!`);
        } else if(hXp > 0){
          showTactileToast(`⚡ ${hDay}: ${hXp} XP активности.`);
        } else {
          showTactileToast(`❄️ ${hDay}: день отдыха.`);
        }
      }
    }
    return;
  }

  const pos = e.target.closest('[data-py-open-skill]');
  if(pos){
    const sid = pos.getAttribute('data-py-open-skill');
    const tr = getTrackForSkill(sid);
    try{ playSound('tick'); }catch(e){}
    location.hash = '#' + tr.routePrefix + '/skill/' + sid;
    return;
  }

  const pjn = e.target.closest('[data-py-jump-note]');
  if(pjn){
    const parts = pjn.getAttribute('data-py-jump-note').split(':');
    const tr = getTrackForSkill(parts[0]);
    ensurePySkillState(parts[0]);
    pySkillViewState.tab = 'theory';
    pySkillViewState.kId = parts[1];
    pySkillViewState.stepIdx = 0;
    pySkillViewState.chunkIdx = 0;
    pySkillViewState.sprintCelebration = null;
    saveReadingPosition();
    location.hash = '#' + tr.routePrefix + '/skill/' + parts[0];
    render();
    return;
  }

  const pt = e.target.closest('[data-py-tab]');
  if(pt){
    const ed = document.getElementById('py-skill-editor');
    if(ed && ed.value){
      pySkillViewState.codeDraft = ed.value;
      if(pySkillViewState.taskId) saveIdeDraft(pySkillViewState.taskId, ed.value);
    }
    pySkillViewState.sprintCelebration = null;
    pySkillViewState.tab = pt.getAttribute('data-py-tab');
    saveReadingPosition();
    render();
    return;
  }
    const pse = e.target.closest('[data-py-select-exam]');
  if(pse){
    const unitId = pse.getAttribute('data-py-select-exam');
    const tr = getTrackForSkill(pySkillViewState.sid || '1.1.1');
    location.hash = '#' + tr.routePrefix + '/unittest/' + unitId;
    return;
  }

const psk = e.target.closest('[data-py-select-k]');
  if(psk){
    pySkillViewState.tab = 'theory';
    pySkillViewState.kId = psk.getAttribute('data-py-select-k');
    pySkillViewState.stepIdx = 0;
    pySkillViewState.chunkIdx = 0;
    pySkillViewState.sprintCelebration = null;
    saveReadingPosition();
    render();
    return;
  }
  const pst = e.target.closest('[data-py-step]');
  if(pst){
    pySkillViewState.stepIdx = parseInt(pst.getAttribute('data-py-step'), 10);
    pySkillViewState.chunkIdx = 0;
    pySkillViewState.sprintCelebration = null;
    saveReadingPosition();
    render();
    return;
  }
  const pns = e.target.closest('[data-py-next-step]');
  if(pns){
    const nextStepIdx = parseInt(pns.getAttribute('data-py-next-step'), 10);
    ensureExtendedState();
    if(!state.completedNoteSteps) state.completedNoteSteps = {};
    const activeK = pySkillViewState.kId || 'unknown';
    const stepKey = `${activeK}:${nextStepIdx}`;
    if(!state.completedNoteSteps[stepKey]){
      state.completedNoteSteps[stepKey] = true;
      awardXp(10);
    }
    pySkillViewState.stepIdx = nextStepIdx;
    pySkillViewState.chunkIdx = 0;
    pySkillViewState.sprintCelebration = null;
    saveReadingPosition();

    // Бесшовное переключение шага без перерисовки всей страницы и без прыжков кнопки
    const feedContainer = document.getElementById('py-theory-text');
    const noteObj = (typeof ALL_NOTES_COMBINED !== 'undefined' ? ALL_NOTES_COMBINED[activeK] : null) || {steps:[]};
    const steps = noteObj.steps || [];
    const curStep = steps[nextStepIdx] || {title:'', html:''};
    const chunks = (typeof splitStepHtmlIntoChunks === 'function') ? splitStepHtmlIntoChunks(curStep.html).slice() : [];
    if(chunks.length > 0 && curStep.title && !/^<h[1-6]\b/i.test(String(chunks[0] || '').trim())){
      chunks[0] = `<h4>${curStep.title}</h4>\n` + chunks[0];
    }

    if(feedContainer && chunks.length > 0){
      feedContainer.innerHTML = `<div class="feed-chunk feed-chunk-new lesson-theory" data-chunk-idx="0">${chunks[0]}</div>`;
      const cardParent = feedContainer.closest('.coddy-lesson-card');
      const isRead = state.readNotes && state.readNotes.includes(activeK);
      const hasMoreChunks = (chunks.length > 1);
      if(hasMoreChunks){
        pns.removeAttribute('data-py-next-step');
        pns.setAttribute('data-chunk-more', 'py');
        pns.textContent = 'Понятно, дальше (+10 XP) ➔';
      } else if(nextStepIdx + 1 < steps.length){
        const nextKey = `${activeK}:${nextStepIdx+1}`;
        const stepAlreadyDone = isRead || (state.completedNoteSteps && state.completedNoteSteps[nextKey]);
        pns.setAttribute('data-py-next-step', nextStepIdx + 1);
        pns.textContent = `Понятно, дальше${stepAlreadyDone ? '' : ' (+10 XP)'} ➔`;
      } else {
        pns.removeAttribute('data-py-next-step');
        pns.setAttribute('data-py-finish-note', activeK);
        pns.textContent = isRead ? '✓ Конспект усвоен' : '✓ Завершить конспект (+10 MP)';
      }

      if(cardParent){
        const backBtn = cardParent.querySelector('[data-chunk-prev]');
        if(backBtn){
          backBtn.style.display = 'inline-flex';
          backBtn.style.visibility = 'visible';
          backBtn.style.pointerEvents = 'auto';
          backBtn.removeAttribute('disabled');
          backBtn.removeAttribute('aria-hidden');
        }
      }

      const xpPill = document.querySelector('.sprint-xp-pill');
      if(xpPill && typeof todayXp === 'function'){
        const dayXpVal = todayXp();
        xpPill.textContent = `⚡ +${dayXpVal} XP за сутки`;
        xpPill.title = `Заработано за сутки: ${dayXpVal} XP`;
      }
      return;
    }

    render();
    return;
  }
  if(e.target.closest('[data-py-toggle-fullnote]')){
    pySkillViewState.fullNoteMode = !pySkillViewState.fullNoteMode;
    pySkillViewState.sprintCelebration = null;
    saveReadingPosition();
    render();
    return;
  }
  const pfn = e.target.closest('[data-py-finish-note]');
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
  }

  // Skill Flashcards actions
  const psf = e.target.closest('[data-py-select-f]');
  if(psf){
    pySkillViewState.tab = 'cards';
    pySkillViewState.fId = psf.getAttribute('data-py-select-f');
    pySkillViewState.cardIdx = 0;
    pySkillViewState.cardFlipped = false;
    pySkillViewState.sprintCelebration = null;
    saveReadingPosition();
    render();
    return;
  }
  if(e.target.closest('[data-py-prev-card]')){
    if(pySkillViewState.cardIdx > 0){
      pySkillViewState.cardIdx--;
      pySkillViewState.cardFlipped = false;
      pySkillViewState.sprintCelebration = null;
      saveReadingPosition();
      render();
    }
    return;
  }
  if(e.target.closest('[data-py-next-card]')){
    const fid = pySkillViewState.fId;
    const deck = ALL_DECKS_COMBINED[fid] || {cards:[]};
    if(pySkillViewState.cardIdx + 1 < (deck.cards || []).length){
      pySkillViewState.cardIdx++;
      pySkillViewState.cardFlipped = false;
      pySkillViewState.sprintCelebration = null;
      saveReadingPosition();
      render();
    }
    return;
  }
  if(e.target.closest('[data-py-flip-card]')){
    pySkillViewState.cardFlipped = !pySkillViewState.cardFlipped;
    pySkillViewState.sprintCelebration = null;
    render();
    return;
  }
  const prc = e.target.closest('[data-py-rate-card]');
  if(prc){
    pySkillViewState.sprintCelebration = null;
    const rawRate = prc.getAttribute('data-py-rate-card');
    let rating = parseInt(rawRate, 10);
    if(isNaN(rating)){
      if(rawRate === 'hard') rating = 2;
      else if(rawRate === 'good') rating = 3;
      else if(rawRate === 'easy') rating = 4;
      else rating = 3;
    }
    const fid = pySkillViewState.fId;
    const deck = ALL_DECKS_COMBINED[fid] || {cards:[]};
    ensureExtendedState();
    let wasStudied = false;
    if(fid){
      const ck = fid + ':' + (pySkillViewState.cardIdx || 0);
      wasStudied = (state.cardRatings[ck] !== undefined && state.cardRatings[ck] > 0);
      if(typeof applyRemNoteCardRating === 'function'){
        applyRemNoteCardRating(ck, rating);
      } else {
        state.cardRatings[ck] = Math.max(Number(state.cardRatings[ck]) || 0, rating || 0);
      }
    }
    if(!wasStudied){
      if(rating >= 3) awardXp(rating === 4 ? 10 : 5);
      else if(rating === 2) awardXp(2);
    }
    if(pySkillViewState.cardIdx + 1 < (deck.cards || []).length){
      pySkillViewState.cardIdx++;
      pySkillViewState.cardFlipped = false;
    } else {
      if(fid && !state.reviewedDecks.includes(fid)) state.reviewedDecks.push(fid);
      if(pySkillViewState.sid) setSkillMP(pySkillViewState.sid, 50);
      pySkillViewState.cardIdx = 0;
      pySkillViewState.cardFlipped = false;
      const sk = PY_SKILLS_BY_ID[pySkillViewState.sid];
      if(sk && Array.isArray(sk.fIds)){
        const fIdx = sk.fIds.indexOf(fid);
        if(fIdx >= 0 && fIdx + 1 < sk.fIds.length){
          pySkillViewState.fId = sk.fIds[fIdx + 1];
        } else {
          pySkillViewState.tab = 'code';
        }
      } else {
        pySkillViewState.tab = 'code';
      }
    }
    saveReadingPosition();
    render();
    return;
  }

  // Skill Code Practice actions
  const pstask = e.target.closest('[data-py-select-task]');
  if(pstask){
    pySkillViewState.tab = 'code';
    pySkillViewState.sprintCelebration = null;
    const ed = document.getElementById('py-skill-editor');
    if(ed && ed.value && pySkillViewState.taskId){
      saveIdeDraft(pySkillViewState.taskId, ed.value);
    }
    const tid = parseInt(pstask.getAttribute('data-py-select-task'), 10);
    const tObj = IDE_TASKS_BY_ID[tid];
    pySkillViewState.taskId = tid;
    pySkillViewState.codeDraft = tObj ? getIdeDraft(tid, tObj.initialCode) : '';
    if(ed) ed.value = pySkillViewState.codeDraft;
    pySkillViewState.hintLevel = 0;
    pySkillViewState.runStatus = null;
    pySkillViewState.runOutput = '';
    saveReadingPosition();
    render();
    return;
  }
  if(e.target.closest('[data-py-task-hint]')){
    const ed = document.getElementById('py-skill-editor');
    if(ed && ed.value) pySkillViewState.codeDraft = ed.value;
    pySkillViewState.hintLevel = Math.min(4, pySkillViewState.hintLevel + 1);
    render();
    return;
  }
  const prst = e.target.closest('[data-py-reset-task]');
  if(prst){
    const tid = parseInt(prst.getAttribute('data-py-reset-task'), 10);
    const tObj = IDE_TASKS_BY_ID[tid];
    if(tObj){
      pySkillViewState.codeDraft = tObj.initialCode;
      saveIdeDraft(tid, tObj.initialCode);
      const ed = document.getElementById('py-skill-editor');
      if(ed) ed.value = tObj.initialCode;
      pySkillViewState.hintLevel = 0;
      pySkillViewState.runStatus = null;
      render();
    }
    return;
  }
  const prun = e.target.closest('[data-py-run-task]');
  if(prun){
    const tid = parseInt(prun.getAttribute('data-py-run-task'), 10);
    const tObj = IDE_TASKS_BY_ID[tid];
    const ed = document.getElementById('py-skill-editor');
    const code = (ed && ed.value) ? ed.value : pySkillViewState.codeDraft;
    pySkillViewState.codeDraft = code;
    saveIdeDraft(tid, code);
    pySkillViewState.runStatus = 'running';
    render();
    const res = await runIdeTaskVerification(tObj, code);
    pySkillViewState.runStatus = res.passed ? 'pass' : 'fail';
    pySkillViewState.runOutput = res.output;
    if(res.passed){
      pySkillViewState.hintLevel = 0; // Scaffold Fading: reset support level on success
      setIdeTaskSolved(tid, code);
      awardXp(25);
      if(pySkillViewState.sid) setSkillMP(pySkillViewState.sid, 80);
    }
    render();
    return;
  }
  const pntask = e.target.closest('[data-py-next-task-btn]');
  if(pntask){
    const tid = parseInt(pntask.getAttribute('data-py-next-task-btn'), 10);
    const sk = (typeof ensurePySkillState === 'function') ? ensurePySkillState(pySkillViewState.sid) : {};
    const tIds = (sk.taskIds && sk.taskIds.length) ? sk.taskIds : [20, 19, 39, 255, 258];
    const curIdx = tIds.indexOf(tid);
    if(curIdx >= 0 && curIdx + 1 < tIds.length){
      const nextTid = tIds[curIdx + 1];
      const nextTObj = IDE_TASKS_BY_ID[nextTid];
      pySkillViewState.taskId = nextTid;
      pySkillViewState.codeDraft = nextTObj ? getIdeDraft(nextTid, nextTObj.initialCode) : '';
      pySkillViewState.hintLevel = 0;
      pySkillViewState.runStatus = null;
      pySkillViewState.runOutput = '';
      saveReadingPosition();
      render();
    } else {
      pySkillViewState.tab = 'exam';
      saveReadingPosition();
      render();
    }
    return;
  }

  // Module Boss Challenge actions
  if(e.target.closest('[data-boss-hint]')){
    const ed = document.getElementById('boss-code-editor');
    if(ed && ed.value) bossViewState.codeDraft = ed.value;
    bossViewState.hintLevel = Math.min(4, bossViewState.hintLevel + 1);
    render();
    return;
  }
  const bReset = e.target.closest('[data-boss-reset]');
  if(bReset){
    const tk = bReset.getAttribute('data-boss-reset');
    const boss = MODULE_BOSS_TASKS[tk];
    if(boss){
      bossViewState.codeDraft = boss.initialCode;
      saveIdeDraft(boss.id, boss.initialCode);
      const ed = document.getElementById('boss-code-editor');
      if(ed) ed.value = boss.initialCode;
      bossViewState.hintLevel = 0;
      bossViewState.runStatus = null;
      render();
    }
    return;
  }
  const bRun = e.target.closest('[data-boss-run]');
  if(bRun){
    const tk = bRun.getAttribute('data-boss-run');
    const boss = MODULE_BOSS_TASKS[tk];
    const tr = MASTERY_TRACKS[tk] || MASTERY_TRACKS.python;
    const ed = document.getElementById('boss-code-editor');
    const code = (ed && ed.value) ? ed.value : bossViewState.codeDraft;
    bossViewState.codeDraft = code;
    saveIdeDraft(boss.id, code);
    bossViewState.runStatus = 'running';
    render();
    const res = await runIdeTaskVerification(boss, code);
    bossViewState.runStatus = res.passed ? 'pass' : 'fail';
    bossViewState.runOutput = res.output;
    if(res.passed){
      bossViewState.hintLevel = 0; // Scaffold Fading
      setIdeTaskSolved(boss.id, code);
      if(!state.passedBosses.includes(tk)) state.passedBosses.push(tk);
      tr.data.units.forEach(u => {
        if(!state.passedUnitTests.includes(u.id)) state.passedUnitTests.push(u.id);
        u.skills.forEach(s => setSkillMP(s.id, 100));
      });
      awardXp(100);
      saveState(state);
    }
    render();
    return;
  }

  // Sticky Python Accessory Bar token insertion & Consolidation Lab scratchpad runner
  const tokBtn = e.target.closest('[data-insert-token]');
  if(tokBtn){
    const token = tokBtn.getAttribute('data-insert-token') || '';
    const targetId = tokBtn.getAttribute('data-target-editor') || '';
    const ta = targetId ? document.getElementById(targetId) : document.querySelector('textarea.code-editor');
    if(ta){
      const start = typeof ta.selectionStart === 'number' ? ta.selectionStart : ta.value.length;
      const end = typeof ta.selectionEnd === 'number' ? ta.selectionEnd : ta.value.length;
      const before = ta.value.slice(0, start);
      const after = ta.value.slice(end);
      const isPair = (token === '()' || token === '[]' || token === '{}');
      const hasSelection = start !== end;
      let nextPos;
      if(isPair && hasSelection){
        const selected = ta.value.slice(start, end);
        ta.value = before + token[0] + selected + token[1] + after;
        nextPos = start + 1 + selected.length + 1;
      } else {
        ta.value = before + token + after;
        nextPos = start + (isPair ? 1 : token.length);
      }
      try{
        ta.focus();
        ta.setSelectionRange(nextPos, nextPos);
      }catch(err){}
      const gutter = document.getElementById(ta.id + '-gutter');
      if(gutter){
        const lc = Math.max(1, ta.value.split('\n').length);
        const nums = [];
        for(let i = 1; i <= lc; i++) nums.push(i);
        gutter.textContent = nums.join('\n');
      }
      try{
        if(typeof Event === 'function' && typeof ta.dispatchEvent === 'function'){
          ta.dispatchEvent(new Event('input', { bubbles: true }));
        }
      }catch(err){}
      syncActiveEditorDrafts();
    }
    return;
  }

  const labRunBtn = e.target.closest('[data-run-lab-scratchpad]');
  if(labRunBtn){
    syncActiveEditorDrafts();
    const ta = document.getElementById('skill-lab-scratchpad');
    const outBox = document.getElementById('skill-lab-output-box');
    const out = document.getElementById('skill-lab-output');
    if(ta && out){
      if(outBox) outBox.classList.remove('hidden');
      out.classList.remove('hidden');
      out.textContent = '⏳ Выполняю в Python 3.13…';
      labRunBtn.setAttribute('disabled', 'disabled');
      try{
        const runner = await getFastPythonRunner();
        let buf = '';
        runner.setStdout({ batched: function(s){ buf += s + '\n'; } });
        runner.setStderr({ batched: function(s){ buf += s + '\n'; } });
        try{
          runner.runPython(ta.value);
        }catch(err){
          buf += String(err);
        }
        out.textContent = buf.trim() || '(программа ничего не вывела)';
        awardXp(5);
      }catch(err){
        out.textContent = 'Ошибка запуска: ' + String(err);
      }
      labRunBtn.removeAttribute('disabled');
    }
    return;
  }

  if(e.target.closest('[data-copy-lab-code]')){
    const ta = document.getElementById('skill-lab-scratchpad');
    if(ta && navigator.clipboard){
      navigator.clipboard.writeText(ta.value);
      const btn = e.target.closest('[data-copy-lab-code]');
      if(btn){
        const orig = btn.textContent;
        btn.textContent = '✓';
        setTimeout(() => { btn.textContent = orig; }, 1200);
      }
    }
    return;
  }

  if(e.target.closest('[data-reset-lab-code]')){
    const ta = document.getElementById('skill-lab-scratchpad');
    if(ta && pySkillViewState && pySkillViewState.sid){
      const activeK = pySkillViewState.kId || 'unknown';
      const stepIdx = pySkillViewState.stepIdx || 0;
      const noteObj = ALL_NOTES_COMBINED[activeK] || {};
      const steps = noteObj.steps || [];
      const curStep = steps[stepIdx] || {};
      const defCode = getStepDefaultScratchpadCode(activeK, pySkillViewState.sid, curStep, stepIdx);
      ta.value = defCode;
      const dKey = `${pySkillViewState.sid}:${activeK}:${stepIdx}`;
      if(!pySkillViewState.labDrafts) pySkillViewState.labDrafts = {};
      pySkillViewState.labDrafts[dKey] = defCode;
      const gut = document.getElementById('skill-lab-scratchpad-gutter');
      if(gut){
        const lc = Math.max(1, defCode.split('\n').length);
        const nums = [];
        for(let i = 1; i <= lc; i++) nums.push(i);
        gut.textContent = nums.join('\n');
      }
      const outBox = document.getElementById('skill-lab-output-box');
      if(outBox) outBox.classList.add('hidden');
    }
    return;
  }

  if(e.target.closest('[data-copy-lab-out]')){
    const out = document.getElementById('skill-lab-output');
    if(out && navigator.clipboard){
      navigator.clipboard.writeText(out.textContent);
      const btn = e.target.closest('[data-copy-lab-out]');
      if(btn){
        const orig = btn.textContent;
        btn.textContent = '✓ Скопировано';
        setTimeout(() => { btn.textContent = orig; }, 1200);
      }
    }
    return;
  }

  if(e.target.closest('[data-clear-lab-out]')){
    const outBox = document.getElementById('skill-lab-output-box');
    const out = document.getElementById('skill-lab-output');
    if(out) out.textContent = '';
    if(outBox) outBox.classList.add('hidden');
    return;
  }

  // Mock Interview Simulator actions
  const mTab = e.target.closest('[data-mock-tab]');
  if(mTab){
    syncActiveEditorDrafts();
    mockInterviewState.tab = mTab.getAttribute('data-mock-tab');
    render();
    return;
  }
  if(e.target.closest('[data-mock-timer-toggle]')){ toggleMockTimer(); return; }
  if(e.target.closest('[data-mock-timer-reset]')){ resetMockTimer(); return; }
  if(e.target.closest('[data-star-pitch-toggle]')){ toggleStarPitchTimer(); return; }
  if(e.target.closest('[data-star-pitch-reset]')){ resetStarPitchTimer(); return; }
  if(e.target.closest('[data-mock-random-task]')){
    const pool = getMockCandidateTasks();
    const rTask = pool[Math.floor(Math.random() * pool.length)] || IDE_TASKS[0];
    mockInterviewState.taskId = rTask.id;
    mockInterviewState.codeDraft = getIdeDraft(rTask.id, rTask.initialCode);
    const ed = document.getElementById('mock-code-editor');
    if(ed) ed.value = mockInterviewState.codeDraft;
    mockInterviewState.hintLevel = 0;
    mockInterviewState.runStatus = null;
    mockInterviewState.runOutput = '';
    render();
    return;
  }
  if(e.target.closest('[data-mock-hint]')){
    const ed = document.getElementById('mock-code-editor');
    if(ed && ed.value) mockInterviewState.codeDraft = ed.value;
    mockInterviewState.hintLevel = Math.min(4, mockInterviewState.hintLevel + 1);
    render();
    return;
  }
  const mReset = e.target.closest('[data-mock-reset]');
  if(mReset){
    const tid = parseInt(mReset.getAttribute('data-mock-reset'), 10);
    const tObj = IDE_TASKS_BY_ID[tid];
    if(tObj){
      mockInterviewState.codeDraft = tObj.initialCode;
      saveIdeDraft(tid, tObj.initialCode);
      const ed = document.getElementById('mock-code-editor');
      if(ed) ed.value = tObj.initialCode;
      mockInterviewState.hintLevel = 0;
      mockInterviewState.runStatus = null;
      render();
    }
    return;
  }
  const mRun = e.target.closest('[data-mock-run]');
  if(mRun){
    const tid = parseInt(mRun.getAttribute('data-mock-run'), 10);
    const tObj = IDE_TASKS_BY_ID[tid];
    const ed = document.getElementById('mock-code-editor');
    const code = (ed && ed.value) ? ed.value : mockInterviewState.codeDraft;
    mockInterviewState.codeDraft = code;
    saveIdeDraft(tid, code);
    mockInterviewState.runStatus = 'running';
    render();
    const res = await runIdeTaskVerification(tObj, code);
    mockInterviewState.runStatus = res.passed ? 'pass' : 'fail';
    mockInterviewState.runOutput = res.output;
    if(res.passed){
      mockInterviewState.hintLevel = 0; // Scaffold Fading
      setIdeTaskSolved(tid, code);
      state.mockCompletedCount = (state.mockCompletedCount || 0) + 1;
      awardXp(40);
      saveState(state);
    }
    render();
    return;
  }
  const stScen = e.target.closest('[data-star-scenario]');
  if(stScen){
    syncActiveEditorDrafts();
    const prevId = mockInterviewState.starScenarioId;
    if(prevId){
      const prevStar = {
        s: mockInterviewState.starS,
        t: mockInterviewState.starT,
        a: mockInterviewState.starA,
        r: mockInterviewState.starR
      };
      mockInterviewState.starDraftsByScenario[prevId] = prevStar;
      state.starDrafts[prevId] = prevStar;
    }
    const nextId = stScen.getAttribute('data-star-scenario');
    mockInterviewState.starScenarioId = nextId;
    const saved = mockInterviewState.starDraftsByScenario[nextId] || state.starDrafts[nextId] || { s: '', t: '', a: '', r: '' };
    mockInterviewState.starS = saved.s;
    mockInterviewState.starT = saved.t;
    mockInterviewState.starA = saved.a;
    mockInterviewState.starR = saved.r;
    const sEl = document.getElementById('star-s-input');
    const tEl = document.getElementById('star-t-input');
    const aEl = document.getElementById('star-a-input');
    const rEl = document.getElementById('star-r-input');
    if(sEl) sEl.value = saved.s;
    if(tEl) tEl.value = saved.t;
    if(aEl) aEl.value = saved.a;
    if(rEl) rEl.value = saved.r;
    mockInterviewState.starEval = null;
    saveState(state);
    render();
    return;
  }
  if(e.target.closest('[data-star-fill-demo]')){
    const curScen = STAR_SCENARIOS.find(x => x.id === mockInterviewState.starScenarioId) || STAR_SCENARIOS[0];
    const demo = curScen.demo || STAR_SCENARIOS[0].demo;
    mockInterviewState.starS = demo.s;
    mockInterviewState.starT = demo.t;
    mockInterviewState.starA = demo.a;
    mockInterviewState.starR = demo.r;
    const demoStar = { s: demo.s, t: demo.t, a: demo.a, r: demo.r };
    mockInterviewState.starDraftsByScenario[curScen.id] = demoStar;
    state.starDrafts[curScen.id] = demoStar;
    saveState(state);
    const sEl = document.getElementById('star-s-input');
    const tEl = document.getElementById('star-t-input');
    const aEl = document.getElementById('star-a-input');
    const rEl = document.getElementById('star-r-input');
    if(sEl) sEl.value = demo.s;
    if(tEl) tEl.value = demo.t;
    if(aEl) aEl.value = demo.a;
    if(rEl) rEl.value = demo.r;
    mockInterviewState.starEval = evaluateStarResponse(mockInterviewState.starS, mockInterviewState.starT, mockInterviewState.starA, mockInterviewState.starR);
    render();
    return;
  }
  if(e.target.closest('[data-star-evaluate]')){
    const sEl = document.getElementById('star-s-input');
    const tEl = document.getElementById('star-t-input');
    const aEl = document.getElementById('star-a-input');
    const rEl = document.getElementById('star-r-input');
    if(sEl && sEl.value) mockInterviewState.starS = sEl.value;
    if(tEl && tEl.value) mockInterviewState.starT = tEl.value;
    if(aEl && aEl.value) mockInterviewState.starA = aEl.value;
    if(rEl && rEl.value) mockInterviewState.starR = rEl.value;
    if(mockInterviewState.starScenarioId){
      const curStar = { s: mockInterviewState.starS, t: mockInterviewState.starT, a: mockInterviewState.starA, r: mockInterviewState.starR };
      mockInterviewState.starDraftsByScenario[mockInterviewState.starScenarioId] = curStar;
      state.starDrafts[mockInterviewState.starScenarioId] = curStar;
    }
    const ev = evaluateStarResponse(mockInterviewState.starS, mockInterviewState.starT, mockInterviewState.starA, mockInterviewState.starR);
    mockInterviewState.starEval = ev;
    if(ev.passed){
      state.mockCompletedCount = (state.mockCompletedCount || 0) + 1;
      awardXp(30);
    }
    saveState(state);
    render();
    return;
  }

  // Unit Test start modal actions («Готовы начать тест?»)
  if(e.target.closest('[data-ut-start]') && unitTestState){
    unitTestState.started = true;
    render();
    return;
  }
  if(e.target.closest('[data-ut-always-skip]')){
    ensureExtendedState();
    state.utSkipStartModal = true;
    saveState(state);
    if(unitTestState) unitTestState.started = true;
    render();
    return;
  }
  if(e.target.closest('[data-ut-toggle-explain]')){
    ensureExtendedState();
    state.utShowExplanations = !state.utShowExplanations;
    saveState(state);
    if(typeof isSettingsModalOpen !== 'undefined' && isSettingsModalOpen) openSettingsModal();
    render();
    return;
  }
  if(e.target.closest('[data-ut-toggle-skipmodal]')){
    ensureExtendedState();
    state.utSkipStartModal = !state.utSkipStartModal;
    saveState(state);
    if(typeof isSettingsModalOpen !== 'undefined' && isSettingsModalOpen) openSettingsModal();
    render();
    return;
  }

  // Unit Test actions (двухфазный выбор: подумать -> подтвердить)
  const utAns = e.target.closest('[data-ut-ans]');
  if(utAns && unitTestState && !unitTestState.revealed){
    unitTestState.pending = parseInt(utAns.getAttribute('data-ut-ans'), 10);
    render();
    return;
  }
  if(e.target.closest('[data-ut-confirm]') && unitTestState && typeof unitTestState.pending === 'number'){
    unitTestState.answers[unitTestState.idx] = unitTestState.pending;
    unitTestState.revealed = true;
    saveUnitTestDraftState();
    render();
    return;
  }
  if(e.target.closest('[data-ut-prev]') && unitTestState && unitTestState.idx > 0){
    unitTestState.idx--;
    unitTestState.revealed = (unitTestState.answers[unitTestState.idx] !== undefined);
    saveUnitTestDraftState();
    render();
    return;
  }
  if(e.target.closest('[data-ut-next]') && unitTestState){
    const tr = getTrackForUnit(unitTestState.unitId, unitTestState.trackKey);
    const isCourse = unitTestState.unitId === 'course';
    let qLen = 0;
    let questions = [];
    if(isCourse){
      Object.values(tr.data.unitTests).forEach(ut => { questions = questions.concat(ut.questions.slice(0,2)); });
      qLen = questions.length;
    } else {
      questions = (ALL_UNIT_TESTS_COMBINED[unitTestState.unitId] || tr.data.unitTests[unitTestState.unitId] || PY_MASTERY.unitTests['1.1']).questions;
      qLen = questions.length;
    }
    if(unitTestState.idx + 1 < qLen){
      unitTestState.idx++;
      unitTestState.revealed = false;
      saveUnitTestDraftState();
    } else {
      unitTestState.finished = true;
      const score = questions.filter((q, i) => unitTestState.answers[i] === q.correct).length;
      if(score / qLen >= 0.75){
        awardXp(50);
        if(isCourse){
          tr.data.units.forEach(u => {
            if(!state.passedUnitTests.includes(u.id)) state.passedUnitTests.push(u.id);
            u.skills.forEach(s => setSkillMP(s.id, 100));
          });
        } else {
          if(!state.passedUnitTests.includes(unitTestState.unitId)) state.passedUnitTests.push(unitTestState.unitId);
          const u = ALL_UNITS_COMBINED.find(x => x.id === unitTestState.unitId);
          if(u) u.skills.forEach(s => setSkillMP(s.id, 100));
        }
      }
      saveUnitTestDraftState();
    }
    render();
    return;
  }
  const utRest = e.target.closest('[data-ut-restart]');
  if(utRest){
    const uid = utRest.getAttribute('data-ut-restart');
    const tKey = (unitTestState && unitTestState.trackKey) || 'python';
    unitTestState = { stateKey: tKey + ':' + uid, unitId: uid, trackKey: tKey, idx: 0, answers: [], revealed: false, finished: false };
    saveUnitTestDraftState();
    render();
    return;
  }

  // Global Flashcards Hub actions
  if(e.target.closest('[data-hub-prev]')){
    if(cardsHubState.cardIdx > 0){
      cardsHubState.cardIdx--;
      cardsHubState.flipped = false;
      saveCardsHubPosState();
      render();
    }
    return;
  }
  if(e.target.closest('[data-hub-flip]')){
    cardsHubState.flipped = !cardsHubState.flipped;
    saveCardsHubPosState();
    render();
    return;
  }
  if(e.target.closest('[data-hub-next]')){
    const d = ALL_DECKS_COMBINED[cardsHubState.deckId] || {cards:[]};
    if(cardsHubState.cardIdx + 1 < (d.cards || []).length){
      cardsHubState.cardIdx++;
      cardsHubState.flipped = false;
      saveCardsHubPosState();
      render();
    }
    return;
  }
  const hRate = e.target.closest('[data-hub-rate]');
  if(hRate){
    const rawRate = hRate.getAttribute('data-hub-rate');
    let r = parseInt(rawRate, 10);
    if(isNaN(r)){
      if(rawRate === 'hard') r = 2;
      else if(rawRate === 'good') r = 3;
      else if(rawRate === 'easy') r = 4;
      else r = 3;
    }
    ensureExtendedState();
    let wasStudied = false;
    if(cardsHubState.deckId){
      const ck = cardsHubState.deckId + ':' + (cardsHubState.cardIdx || 0);
      wasStudied = (state.cardRatings[ck] !== undefined && state.cardRatings[ck] > 0);
      if(typeof applyRemNoteCardRating === 'function'){
        applyRemNoteCardRating(ck, r);
      } else {
        state.cardRatings[ck] = Math.max(Number(state.cardRatings[ck]) || 0, r || 0);
      }
    }
    if(!wasStudied){
      if(r >= 3) awardXp(r === 4 ? 10 : 5);
      else if(r === 2) awardXp(2);
    }
    const d = ALL_DECKS_COMBINED[cardsHubState.deckId] || {cards:[]};
    if(cardsHubState.cardIdx + 1 < (d.cards || []).length){
      cardsHubState.cardIdx++;
      cardsHubState.flipped = false;
    } else {
      if(!state.reviewedDecks.includes(cardsHubState.deckId)) state.reviewedDecks.push(cardsHubState.deckId);
      cardsHubState.completed = true;
      cardsHubState.flipped = false;
    }
    saveCardsHubPosState();
    render();
    return;
  }
  if(e.target.closest('[data-hub-restart-deck]')){
    cardsHubState.completed = false;
    cardsHubState.cardIdx = 0;
    cardsHubState.flipped = false;
    saveCardsHubPosState();
    render();
    return;
  }
  const nextDeckBtn = e.target.closest('[data-hub-next-deck]');
  if(nextDeckBtn){
    const nd = nextDeckBtn.getAttribute('data-hub-next-deck');
    if(nd && ALL_DECKS_COMBINED[nd]){
      cardsHubState.deckId = nd;
      cardsHubState.completed = false;
      cardsHubState.cardIdx = 0;
      cardsHubState.flipped = false;
      saveCardsHubPosState();
      render();
    }
    return;
  }

  // 401-Task Practice Hub actions
  if(e.target.closest('[data-prac-hint]')){
    const ed = document.getElementById('prac-code-editor');
    if(ed && ed.value) practiceHubState.codeDraft = ed.value;
    practiceHubState.hintLevel = Math.min(4, practiceHubState.hintLevel + 1);
    savePracticeHubPosState();
    render();
    return;
  }
  const pReset = e.target.closest('[data-prac-reset]');
  if(pReset){
    const tid = parseInt(pReset.getAttribute('data-prac-reset'), 10);
    const tObj = IDE_TASKS_BY_ID[tid];
    if(tObj){
      practiceHubState.codeDraft = tObj.initialCode;
      saveIdeDraft(tid, tObj.initialCode);
      const ed = document.getElementById('prac-code-editor');
      if(ed) ed.value = tObj.initialCode;
      practiceHubState.hintLevel = 0;
      practiceHubState.runStatus = null;
      savePracticeHubPosState();
      render();
    }
    return;
  }
  const pRun = e.target.closest('[data-prac-run]');
  if(pRun){
    const tid = parseInt(pRun.getAttribute('data-prac-run'), 10);
    const tObj = IDE_TASKS_BY_ID[tid];
    const ed = document.getElementById('prac-code-editor');
    const code = (ed && ed.value) ? ed.value : practiceHubState.codeDraft;
    practiceHubState.codeDraft = code;
    saveIdeDraft(tid, code);
    practiceHubState.runStatus = 'running';
    render();
    const res = await runIdeTaskVerification(tObj, code);
    practiceHubState.runStatus = res.passed ? 'pass' : 'fail';
    practiceHubState.runOutput = res.output;
    if(res.passed){
      practiceHubState.hintLevel = 0; // Scaffold Fading: reset support level on success
      setIdeTaskSolved(tid, code);
      awardXp(25);
    }
    savePracticeHubPosState();
    render();
    return;
  }
  if(e.target.closest('[data-toggle-prac-search]')){
    practiceHubState.searchOpen = !practiceHubState.searchOpen;
    savePracticeHubPosState();
    render();
    if(practiceHubState.searchOpen){
      const inp = document.getElementById('prac-search-input');
      if(inp){ inp.focus(); }
    }
    return;
  }
  if(e.target.closest('[data-clear-prac-search]')){
    practiceHubState.search = '';
    practiceHubState.searchOpen = false;
    savePracticeHubPosState();
    render();
    return;
  }
  const pStep = e.target.closest('[data-prac-step]');
  if(pStep){
    const delta = parseInt(pStep.getAttribute('data-prac-step'), 10) || 0;
    const gapTaskIds = new Set();
    (state.diagnosticGaps || []).forEach(sid => {
      const sk = PY_SKILLS_BY_ID[sid];
      if(sk) (sk.taskIds || []).forEach(tid => gapTaskIds.add(tid));
    });
    const curFiltered = IDE_TASKS.filter(t => {
      if(practiceHubState.echelonFilter === 'gaps'){
        if(gapTaskIds.size > 0 && !gapTaskIds.has(t.id)) return false;
        if(gapTaskIds.size === 0 && getTaskInterviewTier(t.id) !== 1) return false;
      } else if(practiceHubState.echelonFilter !== 'all'){
        if(getTaskInterviewTier(t.id) !== parseInt(practiceHubState.echelonFilter, 10)) return false;
      }
      if(practiceHubState.tierFilter !== 'all' && t.tier !== practiceHubState.tierFilter) return false;
      const isPyCore = (t.id >= 240 && t.id <= 381) || String(t.topic).includes('Python Core');
      if(practiceHubState.catFilter === 'python' && !isPyCore) return false;
      if(practiceHubState.catFilter === 'backend' && isPyCore) return false;
      const sm = getIdeSolvedMap();
      if(practiceHubState.statusFilter === 'solved' && sm[t.id] !== 'solved') return false;
      if(practiceHubState.statusFilter === 'unsolved' && sm[t.id] === 'solved') return false;
      if(practiceHubState.search){
        const q = practiceHubState.search.toLowerCase();
        if(!String(t.id).includes(q) && !t.title.toLowerCase().includes(q) && !t.topic.toLowerCase().includes(q)) return false;
      }
      return true;
    });
    if(curFiltered.length > 0){
      const curIdx = curFiltered.findIndex(t => t.id === practiceHubState.taskId);
      let nextIdx = (curIdx >= 0 ? curIdx : 0) + delta;
      if(nextIdx < 0) nextIdx = curFiltered.length - 1;
      if(nextIdx >= curFiltered.length) nextIdx = 0;
      selectPracticeTask(curFiltered[nextIdx].id);
      render();
    }
    return;
  }

  // Map view mode toggle (Serpentine vs Tree)
  const mapModeBtn = e.target.closest('[data-map-mode]');
  if(mapModeBtn){
    const mode = mapModeBtn.getAttribute('data-map-mode');
    if(typeof mapViewState !== 'undefined'){
      mapViewState.mode = mode;
      render();
    }
    return;
  }

  // 4-Tab Mobile IDE tabs
  const pracMobTab = e.target.closest('[data-prac-mob-tab]');
  if(pracMobTab){
    const tab = pracMobTab.getAttribute('data-prac-mob-tab');
    if(typeof practiceHubState !== 'undefined'){
      practiceHubState.mobileTab = tab;
      savePracticeHubPosState();
      render();
    }
    return;
  }

  // Practice plain explanation toggle
  if(e.target.closest('[data-prac-toggle-explain]')){
    if(typeof practiceHubState !== 'undefined'){
      practiceHubState.showPlainExplain = !practiceHubState.showPlainExplain;
      savePracticeHubPosState();
      render();
    }
    return;
  }

  // Practice solution unlock gate
  if(e.target.closest('[data-prac-unlock-solution]')){
    if(typeof practiceHubState !== 'undefined'){
      practiceHubState.solutionUnlocked = true;
      savePracticeHubPosState();
      render();
    }
    return;
  }

  // Practice Socratic hint advance
  if(e.target.closest('[data-prac-ask-ai]')){
    if(typeof practiceHubState !== 'undefined'){
      practiceHubState.hintLevel = Math.min(4, (practiceHubState.hintLevel || 0) + 1);
      savePracticeHubPosState();
      render();
    }
    return;
  }

  // Section Gate button click (navigate to track or show locked toast)
  const gateBtn = e.target.closest('[data-gate-track]');
  if(gateBtn){
    const isLocked = gateBtn.getAttribute('data-gate-locked') === '1';
    const track = gateBtn.getAttribute('data-gate-track');
    const prevTitle = gateBtn.getAttribute('data-gate-prev-title') || 'предыдущего раздела';
    if(isLocked){
      if(typeof showTactileToast === 'function'){
        showTactileToast(`🔒 Завершите все темы «${prevTitle}», чтобы открыть этот раздел!`);
      }
      return;
    }
    if(track) location.hash = `#/${track}`;
    return;
  }

  // «Челлендж мастерства» branch node click (navigate to the unit test route)
  const challengeNode = e.target.closest('.hex-challenge-node');
  if(challengeNode){
    const chStatus = challengeNode.getAttribute('data-challenge-status');
    const chRoute = challengeNode.getAttribute('data-challenge-route');
    if(chStatus === 'locked'){
      if(typeof showTactileToast === 'function') showTactileToast('🔒 Челлендж откроется после прохождения предыдущих юнитов');
      return;
    }
    if(chRoute) location.hash = chRoute;
    return;
  }

  // 3D Serpentine Path node click (Open anchored popover)
  const hexNode = e.target.closest('.hex-3d-node');
  if(hexNode){
    const openedByKeyboard = e.detail === 0;
    const uid = hexNode.getAttribute('data-unit-id');
    const popover = document.getElementById('path-anchored-popover');
    if(popover && uid && typeof ALL_UNITS_COMBINED !== 'undefined'){
      popover.setAttribute('data-return-focus-unit', uid);
      const u = ALL_UNITS_COMBINED.find(x => x.id === uid);
      if(u){
        const track = getTrackForUnit(uid);
        const pBadge = document.getElementById('popover-badge');
        const pTitle = document.getElementById('popover-title');
        const pStatus = document.getElementById('popover-status');
        const pSkills = document.getElementById('popover-skills');
        const pCta = document.getElementById('popover-cta-btn');

        if(pBadge) pBadge.textContent = `ТРЕК · ${track.title.split('Матрица Мастерства').pop().trim() || track.title}`;
        if(pTitle) pTitle.textContent = `Юнит ${u.id}: ${u.title.replace(/^Юнит\s+[\d.]+\s*·\s*/, '')}`;

        const isPassed = (state.passedUnitTests || []).includes(u.id) || ((u.skills||[]).length > 0 && (u.skills||[]).every(s => getSkillMP(s.id) >= 80));
        const uIdx = ALL_UNITS_COMBINED.findIndex(x => x.id === uid);
        let activeIdx = ALL_UNITS_COMBINED.findIndex(x => {
          const pass = (state.passedUnitTests || []).includes(x.id) || ((x.skills||[]).length > 0 && (x.skills||[]).every(s => getSkillMP(s.id) >= 80));
          return !pass;
        });
        if(activeIdx === -1) activeIdx = ALL_UNITS_COMBINED.length - 1;
        const isActive = (uIdx === activeIdx);
        const isLocked = (uIdx > activeIdx && !isPassed);

        if(pStatus){
          if(isPassed) pStatus.textContent = '✅ Юнит завершён (освоен на 100%)';
          else if(isActive) pStatus.textContent = '🏆 Текущая цель курса';
          else if(isLocked) pStatus.textContent = 'Пройдите уроки выше, чтобы открыть это!';
          else pStatus.textContent = '📖 Доступен для изучения';
        }

        if(pSkills){
          const skillItems = (u.skills || []).slice(0, 3);
          pSkills.innerHTML = skillItems.length
            ? `<div class="path-popover-skills-label">В этом юните</div><div class="path-popover-skills-list">${skillItems.map(s => `<div class="path-popover-skill">${escapeHtmlStr(s.title)}</div>`).join('')}</div>`
            : '';
        }

        if(pCta){
          const unitStarted = (u.skills || []).some(s => (getSkillMP(s.id) || 0) > 0);
          pCta.className = isPassed ? 'btn-3d-emerald path-popover-cta' : (isLocked ? 'btn-3d-locked path-popover-cta' : 'btn-3d-orange path-popover-cta');
          pCta.textContent = isPassed ? 'ОБЗОР ➔' : (isLocked ? 'ЗАБЛОКИРОВАНО' : (unitStarted ? 'ПРОДОЛЖИТЬ ➔' : 'НАЧАТЬ ➔'));
          pCta.disabled = isLocked;
          pCta.setAttribute('data-target-route', `#${track.routePrefix}/skill/${(u.skills && u.skills[0]) ? u.skills[0].id : ''}`);
        }

        const parent = popover.offsetParent || popover.parentElement;
        if(parent){
          const pRect = (parent.getBoundingClientRect && parent.getBoundingClientRect()) || { left: 0, top: 0, width: 420 };
          const nRect = (hexNode.getBoundingClientRect && hexNode.getBoundingClientRect()) || { left: 210, right: 210, top: 100, bottom: 160 };
          const pWidth = pRect.width || 420;
          let cx = (nRect.left + nRect.right) / 2 - pRect.left;
          let cy = nRect.top - pRect.top;
          if(!cx || isNaN(cx)){
            cx = parseFloat(hexNode.getAttribute('data-cx')) || 210;
            cy = parseFloat(hexNode.getAttribute('data-cy')) || 100;
          }
          const popoverWidth = parseFloat(window.getComputedStyle(popover).width) || 340;
          const popoverHalfWidth = popoverWidth / 2;
          const clampedCx = Math.max(popoverHalfWidth + 8, Math.min(pWidth - popoverHalfWidth - 8, cx));
          popover.style.left = `${Math.round(clampedCx)}px`;
          const arrow = document.getElementById('popover-arrow');
          if(arrow){
            const arrowX = Math.max(20, Math.min(popoverWidth - 20, popoverHalfWidth + (cx - clampedCx)));
            arrow.style.left = `${Math.round(arrowX)}px`;
          }
          if(cy > 240){
            popover.style.top = `${Math.round(cy - 220)}px`;
            if(arrow) arrow.className = 'path-popover-arrow path-popover-arrow--down';
          } else {
            popover.style.top = `${Math.round((nRect.bottom || (cy + 60)) - pRect.top + 16)}px`;
            if(arrow) arrow.className = 'path-popover-arrow path-popover-arrow--up';
          }
        }
        popover.style.display = 'block';
        if(openedByKeyboard && typeof popover.focus === 'function') popover.focus();
        // Clamp to the viewport; disable the scale-in animation while measuring its full size.
        try{
          const prevAnim = popover.style.animation;
          popover.style.animation = 'none';
          const vh = window.innerHeight || 900;
          let pr = popover.getBoundingClientRect();
          if(pr.height > 0){
            const curTop = parseFloat(popover.style.top) || 0;
            let delta = 0;
            if(pr.bottom > vh - 12) delta = -(pr.bottom - (vh - 12));
            popover.style.top = `${Math.round(curTop + delta)}px`;
            pr = popover.getBoundingClientRect();
            if(pr.top < 12) popover.style.top = `${Math.round(parseFloat(popover.style.top) + (12 - pr.top))}px`;
          }
          popover.style.animation = prevAnim;
        }catch(err){}
        return;
      }
    }
  }

  // Popover close and CTA button
  if(e.target.closest('#popover-close-btn')){
    const popover = document.getElementById('path-anchored-popover');
    if(popover){
      popover.style.display = 'none';
      const returnId = popover.getAttribute('data-return-focus-unit');
      const returnNode = Array.from(document.querySelectorAll('.hex-3d-node')).find(node => node.getAttribute('data-unit-id') === returnId);
      if(returnNode && typeof returnNode.focus === 'function') returnNode.focus();
    }
    return;
  }
  const popCta = e.target.closest('#popover-cta-btn');
  if(popCta){
    const tr = popCta.getAttribute('data-target-route');
    const popover = document.getElementById('path-anchored-popover');
    if(popover) popover.style.display = 'none';
    if(tr && !popCta.disabled){
      location.hash = tr;
    }
    return;
  }
  if(!e.target.closest('#path-anchored-popover') && !e.target.closest('.hex-3d-node')){
    const popover = document.getElementById('path-anchored-popover');
    if(popover && popover.style && popover.style.display !== 'none'){
      popover.style.display = 'none';
    }
  }

  // Jump to active unit button
  if(e.target.closest('#path-jump-btn')){
    const targetNode = document.querySelector('.hex-node--active') || document.querySelector('.hex-3d-node');
    if(targetNode){
      targetNode.scrollIntoView({ behavior: 'smooth', block: 'center' });
      try{ targetNode.focus(); }catch(err){}
    }
    return;
  }

  // Theory audio companion controls
  if(e.target.closest('[data-toggle-audio], [data-audio-toggle]')){
    state.audioBarOpen = !state.audioBarOpen;
    saveState(state);
    const bar = document.getElementById('theory-audio-bar');
    if(bar) bar.style.display = state.audioBarOpen ? 'flex' : 'none';
    if(state.audioBarOpen && window.theoryAudioPlayer && !window.theoryAudioPlayer.isPlaying){
      const theoryElem = document.getElementById('py-theory-text') || document.getElementById('py-theory-container') || document.getElementById('lesson-theory-content') || document.querySelector('.lesson-theory') || document.querySelector('.k-note-card');
      const textToRead = theoryElem ? (theoryElem.innerText || theoryElem.textContent || '') : '';
      if(textToRead) window.theoryAudioPlayer.play(textToRead);
    } else if(!state.audioBarOpen && window.theoryAudioPlayer){
      window.theoryAudioPlayer.stop();
    }
    return;
  }
  if(e.target.closest('[data-audio-play]')){
    if(window.theoryAudioPlayer){
      if(!window.theoryAudioPlayer.isPlaying && !window.theoryAudioPlayer.currentText){
        const theoryElem = document.getElementById('py-theory-container') || document.getElementById('lesson-theory-content') || document.querySelector('.lesson-theory') || document.querySelector('.k-note-card');
        const textToRead = theoryElem ? (theoryElem.innerText || theoryElem.textContent || '') : '';
        window.theoryAudioPlayer.play(textToRead);
      } else {
        window.theoryAudioPlayer.togglePlay();
      }
    }
    return;
  }
  if(e.target.closest('[data-audio-rewind]')){
    if(window.theoryAudioPlayer) window.theoryAudioPlayer.rewind10();
    return;
  }
  if(e.target.closest('[data-audio-rate]')){
    if(window.theoryAudioPlayer) window.theoryAudioPlayer.toggleRate();
    return;
  }
  if(e.target.closest('[data-audio-close]')){
    state.audioBarOpen = false;
    saveState(state);
    if(window.theoryAudioPlayer) window.theoryAudioPlayer.stop();
    const bar = document.getElementById('theory-audio-bar');
    if(bar) bar.style.display = 'none';
    return;
  }
});

// Change & Input events for selectors, file backup upload, and live code auto-save
document.addEventListener('change', function(e){
  if(e.target.id === 'handover-file-input'){
    const f = e.target.files && e.target.files[0];
    if(f && typeof FileReader !== 'undefined'){
      const reader = new FileReader();
      reader.onload = function(ev){
        const rawText = String(ev.target.result || '');
        const box = document.getElementById('handover-json-box');
        if(box) box.value = rawText;
        const stEl = document.getElementById('handover-import-status');
        try{
          importAndMergeBackupJsonString(rawText);
          if(stEl){
            stEl.style.color = '#34d399';
            stEl.textContent = '✓ Файл бэкапа успешно проверен и объединён с текущим прогрессом!';
          }
          render();
        }catch(err){
          if(stEl){
            stEl.style.color = '#ef4444';
            stEl.textContent = 'Ошибка чтения .json файла: ' + String(err && err.message ? err.message : err);
          }
        }
      };
      reader.readAsText(f);
    }
  } else if(e.target.id === 'cards-echelon-filter'){
    cardsHubState.echelonFilter = e.target.value;
    cardsHubState.cardIdx = 0;
    cardsHubState.flipped = false;
    cardsHubState.completed = false;
    saveCardsHubPosState();
    render();
  } else if(e.target.id === 'cards-unit-select'){
    cardsHubState.unitFilter = e.target.value;
    cardsHubState.cardIdx = 0;
    cardsHubState.flipped = false;
    cardsHubState.completed = false;
    saveCardsHubPosState();
    render();
  } else if(e.target.id === 'cards-deck-select'){
    cardsHubState.deckId = e.target.value;
    cardsHubState.cardIdx = 0;
    cardsHubState.flipped = false;
    cardsHubState.completed = false;
    saveCardsHubPosState();
    render();
  } else if(e.target.id === 'prac-echelon-filter'){
    practiceHubState.echelonFilter = e.target.value;
    savePracticeHubPosState();
    render();
  } else if(e.target.id === 'prac-tier-filter'){
    practiceHubState.tierFilter = e.target.value;
    savePracticeHubPosState();
    render();
  } else if(e.target.id === 'prac-cat-filter'){
    practiceHubState.catFilter = e.target.value;
    savePracticeHubPosState();
    render();
  } else if(e.target.id === 'prac-status-filter'){
    practiceHubState.statusFilter = e.target.value;
    savePracticeHubPosState();
    render();
  } else if(e.target.id === 'mock-echelon-select'){
    syncActiveEditorDrafts();
    mockInterviewState.echelonFilter = e.target.value;
    const pool = getMockCandidateTasks();
    if(pool.length > 0){
      const nextT = pool[0];
      mockInterviewState.taskId = nextT.id;
      mockInterviewState.codeDraft = getIdeDraft(nextT.id, nextT.initialCode);
      const ed = document.getElementById('mock-code-editor');
      if(ed) ed.value = mockInterviewState.codeDraft;
      mockInterviewState.hintLevel = 0;
      mockInterviewState.runStatus = null;
      mockInterviewState.runOutput = '';
    }
    render();
  } else if(e.target.id === 'mock-task-select'){
    const ed = document.getElementById('mock-code-editor');
    if(ed && ed.value && mockInterviewState.taskId){
      saveIdeDraft(mockInterviewState.taskId, ed.value);
    }
    const tid = parseInt(e.target.value, 10);
    const tObj = IDE_TASKS_BY_ID[tid] || IDE_TASKS[0];
    mockInterviewState.taskId = tObj.id;
    mockInterviewState.codeDraft = getIdeDraft(tObj.id, tObj.initialCode);
    if(ed) ed.value = mockInterviewState.codeDraft;
    mockInterviewState.hintLevel = 0;
    mockInterviewState.runStatus = null;
    mockInterviewState.runOutput = '';
    render();
  }
});

document.addEventListener('input', function(e){
  if(e.target && e.target.id){
    const gut = document.getElementById(e.target.id + '-gutter');
    if(gut){
      const lc = Math.max(1, String(e.target.value || '').split('\n').length);
      const nums = [];
      for(let i = 1; i <= lc; i++) nums.push(i);
      gut.textContent = nums.join('\n');
    }
  }
  if(e.target.id === 'prac-search-input'){
    practiceHubState.search = e.target.value;
    savePracticeHubPosState();
    render();
    const inp = document.getElementById('prac-search-input');
    if(inp){ inp.focus(); inp.setSelectionRange(inp.value.length, inp.value.length); }
  } else if(e.target.id === 'prac-docs-search-input'){
    practiceHubState.docsSearch = e.target.value;
    savePracticeHubPosState();
    render();
    const inp = document.getElementById('prac-docs-search-input');
    if(inp){ inp.focus(); inp.setSelectionRange(inp.value.length, inp.value.length); }
  } else if(e.target.id === 'code-input'){
    ensureExtendedState();
    state.sandboxDraft = e.target.value;
    saveState(state);
  } else if(e.target.id === 'lesson-code'){
    if(lessonState && lessonState.stage && ['practice','task','practice2','task2','debug'].includes(lessonState.stage)){
      lessonState[lessonState.stage + 'Code'] = e.target.value;
      saveLessonDraftState();
    }
  } else if(e.target.id === 'py-skill-editor'){
    pySkillViewState.codeDraft = e.target.value;
    if(pySkillViewState.taskId) saveIdeDraft(pySkillViewState.taskId, e.target.value);
  } else if(e.target.id === 'prac-code-editor'){
    practiceHubState.codeDraft = e.target.value;
    if(practiceHubState.taskId) saveIdeDraft(practiceHubState.taskId, e.target.value);
  } else if(e.target.id === 'boss-code-editor'){
    bossViewState.codeDraft = e.target.value;
    const boss = MODULE_BOSS_TASKS[bossViewState.trackKey];
    if(boss) saveIdeDraft(boss.id, e.target.value);
  } else if(e.target.id === 'mock-code-editor'){
    mockInterviewState.codeDraft = e.target.value;
    if(mockInterviewState.taskId) saveIdeDraft(mockInterviewState.taskId, e.target.value);
  } else if(e.target.id === 'star-s-input' || e.target.id === 'star-t-input' || e.target.id === 'star-a-input' || e.target.id === 'star-r-input'){
    if(e.target.id === 'star-s-input') mockInterviewState.starS = e.target.value;
    if(e.target.id === 'star-t-input') mockInterviewState.starT = e.target.value;
    if(e.target.id === 'star-a-input') mockInterviewState.starA = e.target.value;
    if(e.target.id === 'star-r-input') mockInterviewState.starR = e.target.value;
    if(mockInterviewState.starScenarioId){
      ensureExtendedState();
      const curStar = {
        s: mockInterviewState.starS || '',
        t: mockInterviewState.starT || '',
        a: mockInterviewState.starA || '',
        r: mockInterviewState.starR || ''
      };
      mockInterviewState.starDraftsByScenario[mockInterviewState.starScenarioId] = curStar;
      state.starDrafts[mockInterviewState.starScenarioId] = curStar;
      saveState(state);
    }
  }
});

// Synchronize line-number gutter scroll position with textarea scroll
document.addEventListener('scroll', function(e){
  if(e.target && e.target.id && e.target.classList && e.target.classList.contains('code-editor')){
    const gut = document.getElementById(e.target.id + '-gutter');
    if(gut) gut.scrollTop = e.target.scrollTop;
  }
}, true);

// Keyboard shortcuts: Ctrl+Enter to run/verify code, Space to flip card, 1..4 to rate card
document.addEventListener('keydown', function(e){
  if((e.ctrlKey || e.metaKey) && e.key === 'Enter'){
    const lv = document.querySelector('[data-lesson-verify]');
    if(lv){ e.preventDefault(); lv.click(); return; }
    const lvc = document.querySelector('[data-lesson-verify-cmd]');
    if(lvc){ e.preventDefault(); lvc.click(); return; }
    const pr = document.querySelector('[data-py-run-task]');
    if(pr){ e.preventDefault(); pr.click(); return; }
    const pcr = document.querySelector('[data-prac-run]');
    if(pcr){ e.preventDefault(); pcr.click(); return; }
    const br = document.querySelector('[data-boss-run]');
    if(br){ e.preventDefault(); br.click(); return; }
    const mr = document.querySelector('[data-mock-run]');
    if(mr){ e.preventDefault(); mr.click(); return; }
    const sb = document.getElementById('run-btn');
    if(sb){ e.preventDefault(); sb.click(); return; }
    const slr = document.querySelector('[data-run-lab-scratchpad]');
    if(slr){ e.preventDefault(); slr.click(); return; }
  }
  const tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : '';
  if(e.key === 'Tab' && e.target && e.target.id === 'skill-lab-scratchpad'){
    e.preventDefault();
    const ta = e.target;
    const s = ta.selectionStart;
    const end = ta.selectionEnd;
    ta.value = ta.value.substring(0, s) + '    ' + ta.value.substring(end);
    ta.selectionStart = ta.selectionEnd = s + 4;
    try { ta.dispatchEvent(new Event('input', { bubbles: true })); } catch(err){}
    return;
  }
  if(tag === 'textarea' || tag === 'input' || tag === 'select') return;
  if(e.key === 'Escape'){
    if(typeof isSettingsModalOpen !== 'undefined' && isSettingsModalOpen){
      closeSettingsModal();
      return;
    }
    const popover = document.getElementById('path-anchored-popover');
    if(popover && popover.style && popover.style.display !== 'none'){
      popover.style.display = 'none';
      const returnId = popover.getAttribute('data-return-focus-unit');
      const returnNode = Array.from(document.querySelectorAll('.hex-3d-node')).find(node => node.getAttribute('data-unit-id') === returnId);
      if(returnNode && typeof returnNode.focus === 'function') returnNode.focus();
      return;
    }
  }
  const focusedPathNode = e.target && e.target.closest ? e.target.closest('.hex-3d-node') : null;
  if(focusedPathNode && (e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'Home' || e.key === 'End')){
    const nodes = Array.from(document.querySelectorAll('.hex-3d-node'));
    const currentIndex = nodes.indexOf(focusedPathNode);
    let nextIndex = currentIndex;
    if(e.key === 'ArrowDown') nextIndex = Math.min(nodes.length - 1, currentIndex + 1);
    else if(e.key === 'ArrowUp') nextIndex = Math.max(0, currentIndex - 1);
    else if(e.key === 'Home') nextIndex = 0;
    else if(e.key === 'End') nextIndex = nodes.length - 1;
    if(nextIndex !== currentIndex && nodes[nextIndex]){
      e.preventDefault();
      nodes[nextIndex].focus();
      nodes[nextIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }
  }
  if((e.key === 'Enter' || e.code === 'Space') && e.target && e.target.closest && (e.target.closest('.hex-3d-node') || e.target.closest('.hex-challenge-node') || e.target.closest('[data-gate-track]'))){
    e.preventDefault();
    const clickEv = (typeof MouseEvent !== 'undefined') ? new MouseEvent('click', { bubbles: true, cancelable: true }) : { type: 'click', bubbles: true };
    (e.target.closest('[data-gate-track]') || e.target.closest('.hex-challenge-node') || e.target.closest('.hex-3d-node')).dispatchEvent(clickEv);
    return;
  }
  if(e.code === 'Space' || e.key === ' ' || e.key === 'Spacebar'){
    const flipBtn = document.querySelector('[data-py-flip-card], [data-hub-flip]');
    if(flipBtn){ e.preventDefault(); flipBtn.click(); return; }
    const pyNextBtn = document.querySelector('[data-chunk-more="py"], [data-py-next-step]');
    if(pyNextBtn){ e.preventDefault(); pyNextBtn.click(); return; }
  }
  if(e.key === 'ArrowLeft'){
    const prevBtn = document.querySelector('[data-py-prev-card]:not([disabled]), [data-hub-prev]:not([disabled])');
    if(prevBtn){ e.preventDefault(); prevBtn.click(); return; }
  }
  if(e.key === 'ArrowRight'){
    const nextBtn = document.querySelector('[data-py-next-card]:not([disabled]), [data-hub-next]:not([disabled])');
    if(nextBtn){ e.preventDefault(); nextBtn.click(); return; }
  }
  if(e.key === '1' || e.key === '2' || e.key === '3' || e.key === '4'){
    let rateSel = `[data-py-rate-card="${e.key}"], [data-hub-rate="${e.key}"]`;
    if(e.key === '1' || e.key === '2'){
      rateSel += `, [data-py-rate-card="hard"], [data-hub-rate="hard"]`;
    } else if(e.key === '3'){
      rateSel += `, [data-py-rate-card="good"], [data-hub-rate="good"]`;
    } else if(e.key === '4'){
      rateSel += `, [data-py-rate-card="easy"], [data-hub-rate="easy"]`;
    }
    const rateBtn = document.querySelector(rateSel);
    if(rateBtn){ e.preventDefault(); rateBtn.click(); return; }
  }
  if(e.key === 'Enter' && !e.ctrlKey && !e.metaKey){
    const bsNext = document.querySelector('.academy-bottom-sheet [data-lesson-next], .academy-bottom-sheet [data-diag-next]');
    if(bsNext){ e.preventDefault(); bsNext.click(); return; }
    const pyNextBtn = document.querySelector('[data-chunk-more="py"], [data-py-next-step]');
    if(pyNextBtn){ e.preventDefault(); pyNextBtn.click(); return; }
  }
});

// Register PWA Service Worker (HTTP/HTTPS only to prevent file:// SecurityError)
if('serviceWorker' in navigator && location.protocol.startsWith('http')){
  window.addEventListener('load', function(){
    navigator.serviceWorker.register('sw.js').catch(function(){});
  });
}

// Re-render navigation & current view with all upgrades active!
renderNav();
applyThemeIcon();

render();

