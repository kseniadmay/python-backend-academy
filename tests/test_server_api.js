const assert = require('assert');
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const net = require('net');
const vm = require('vm');
const {
  getTestContext,
  assertCanonicalEtalonSync,
} = require('./test_helpers');

const ROOT = path.resolve(__dirname, '..');
const SERVER = path.join(ROOT, 'scripts', 'server.js');

async function getFreePort() {
  const socket = net.createServer();
  await new Promise((resolve, reject) => socket.listen(0, '127.0.0.1', resolve).once('error', reject));
  const { port } = socket.address();
  await new Promise(resolve => socket.close(resolve));
  return port;
}

async function waitForServer(baseUrl, child) {
  for (let attempt = 0; attempt < 20; attempt++) {
    if (child.exitCode !== null) throw new Error(`Server exited early with code ${child.exitCode}: ${child.__output || ''}`);
    try {
      const response = await fetch(`${baseUrl}/healthz`, { signal: AbortSignal.timeout(300) });
      if (response.ok) return;
    } catch (_) {}
    await new Promise(resolve => setTimeout(resolve, 150));
  }
  throw new Error('Server did not become healthy within 9 seconds');
}

function request(url, options = {}) {
  return fetch(url, { signal: AbortSignal.timeout(5000), ...options });
}

async function stopChild(child) {
  if (child.exitCode !== null || child.signalCode !== null) return;
  await new Promise(resolve => {
    const timer = setTimeout(resolve, 2000);
    child.once('exit', () => { clearTimeout(timer); resolve(); });
    child.kill();
  });
}

function runSrsEngineAndUiSuite() {
  assertCanonicalEtalonSync();
  const ctx = getTestContext();
  const html = ctx.academyHtml;

  // Verify helper slices remain intact
  assert.ok(ctx.viewPythonSkillSlice.includes('buildUnifiedMicroStepperHTML'));
  assert.ok(ctx.viewPythonSkillSlice.includes('buildActiveRescueScaffoldHTML'));
  assert.ok(ctx.cardsDueModeSlice.includes('collectDueCardsQueue'));

  // Extract the SRS engine block from academy.html and evaluate in isolated VM sandbox
  const flowStart = html.indexOf('function buildSrsFlowTabsHTML(');
  const flowEnd = html.indexOf('function viewCardsHub(');
  const srsStart = html.indexOf('// ================= REMNOTE SPACED REPETITION ENGINE (SRS) =================');
  const srsEnd = html.indexOf('// Reference Hub View (#/docs)');
  assert.ok(flowStart !== -1 && flowEnd > flowStart && srsStart !== -1 && srsEnd > srsStart, 'SRS engine block must exist in academy.html');
  const srsCode = html.slice(flowStart, flowEnd) + '\n' + html.slice(srsStart, srsEnd);

  let fakeToday = '2026-05-01';
  const addDaysIso = (isoStr, days) => {
    const d = new Date(isoStr + 'T00:00:00Z');
    d.setUTCDate(d.getUTCDate() + days);
    return d.toISOString().slice(0, 10);
  };

  const sandbox = {
    window: {},
    state: {
      xp: 0,
      readNotes: ['К-001', 'К-002'],
      reviewedDecks: ['Ф-001'],
      cardRatings: {},
      cardSrs: {},
      noteSrs: {},
    },
    cardsHubState: {
      hubTab: 'notes',
      notePos: 0,
      noteStepIdx: 0,
      noteFullMode: false,
      forcedNoteId: null,
      dueDoneToday: false,
      dueCompletedDate: null,
    },
    ALL_NOTES_COMBINED: {
      'К-001': {
        id: 'К-001',
        title: 'К-001: Архитектура CPython и память',
        selfCheck: ['Как устроен PyObject в памяти?', 'Когда срабатывает циклический GC?'],
        steps: [
          { title: 'Шаг 1: Ссылки и PyObject', html: '<p>В CPython любая переменная является ссылкой на структуру <code>PyObject</code> в куче.</p><pre><code>x = 42\nprint(id(x))</code></pre>' },
          { title: 'Шаг 2: Подсчёт ссылок', html: '<p>Базовый механизм освобождения памяти — <b>Reference Counting</b> плюс детектор циклов.</p>' },
        ],
      },
      'К-002': {
        id: 'К-002',
        title: 'К-002: Мутабельность и хеширование',
        selfCheck: ['Почему list нельзя использовать как ключ dict?'],
        steps: [
          { title: 'Шаг 1: Контракт __hash__ и __eq__', html: '<p>Хеш неизменяемого объекта обязан оставаться константным в течение всей жизни объекта.</p>' },
        ],
      },
    },
    ALL_DECKS_COMBINED: {
      'Ф-001': {
        id: 'Ф-001',
        title: 'Ф-001: Переменные и ссылки',
        cards: [
          { q: 'Что хранит переменная в Python?', a: 'В Python переменная хранит **ссылку (указатель)** на объект `PyObject` в куче, а не само значение.' },
          { q: 'Какой тип имеет `True`?', a: 'Тип `bool` является прямым подклассом `int`.' },
        ],
      },
    },
    ALL_PY_SKILLS: [
      { id: '1.1.1', unitId: '1.1', title: '1.1.1 · Память и ссылки', kIds: ['К-001', 'К-002'], deckIds: ['Ф-001'] },
    ],
    ensureExtendedState: () => sandbox.state,
    getTrackForSkill: () => ({ key: 'python', routePrefix: '/python' }),
    dateIsoKey: () => fakeToday,
    escapeHtmlStr: (s) => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'),
    renderRichStepContent: (h) => String(h || ''),
    decorateCodeBlocksWithRunBtn: (h) => String(h || '') + '<!--runnable-->',
    saveState: () => {},
    saveCardsHubPosState: () => {},
    awardXp: (pts) => { sandbox.state.xp += pts; },
    addDailyXp: (pts) => { sandbox.state.xp += pts; },
    showXpFloat: () => {},
    showToast: () => {},
    playSound: () => {},
  };

  vm.createContext(sandbox);
  vm.runInContext(srsCode, sandbox);

  // 1. Verify Note SRS (1/3/7/21/30) initial scheduling (+1 day, not immediately overdue)
  const infoInit = sandbox.getNoteSrsInfo('К-001');
  assert.strictEqual(infoInit.step, 0);
  assert.strictEqual(infoInit.interval, 1);
  assert.strictEqual(infoInit.dueDate, '2026-05-02', 'Newly read note must be scheduled for +1 day');
  assert.strictEqual(infoInit.isDue, false);

  // 2. Advance day to 2026-05-02: К-001 and К-002 become due
  fakeToday = '2026-05-02';
  const noteStatsDay2 = sandbox.getNoteSpacedRepetitionStats();
  assert.strictEqual(noteStatsDay2.dueCount, 1, 'К-001 must be due on 2026-05-02');
  assert.strictEqual(noteStatsDay2.dueNotes[0].noteId, 'К-001');

  // 3. Confirm stage 1 -> advances to step 1 (interval 3 days, due 2026-05-05) and awards +15 XP
  const xpBefore = sandbox.state.xp;
  sandbox.applyNoteReview('К-001', 'pass');
  const rev1 = sandbox.getNoteSrsInfo('К-001');
  assert.strictEqual(rev1.step, 1);
  assert.strictEqual(rev1.interval, 3);
  assert.strictEqual(rev1.dueDate, '2026-05-05');
  assert.strictEqual(sandbox.state.xp, xpBefore + 15, 'First review of the day awards +15 XP');

  // Anti-farming guard: repeating same note on same day does not award extra XP
  sandbox.applyNoteReview('К-001', 'pass');
  assert.strictEqual(sandbox.state.xp, xpBefore + 15, 'XP anti-farming guard must prevent duplicate XP on same day');

  // 4. Verify full 1 -> 3 -> 7 -> 21 -> 30 progression and reset on lapse
  sandbox.state.noteSrs['К-002'] = { step: 0, interval: 1, dueDate: '2026-05-01', lastReview: '2026-04-30', reviewCount: 1, mastered: false };
  const expectedProgression = [
    { step: 1, interval: 3 },
    { step: 2, interval: 7 },
    { step: 3, interval: 21 },
    { step: 4, interval: 30 },
    { step: 4, interval: 30 },
  ];
  expectedProgression.forEach((exp, idx) => {
    fakeToday = addDaysIso('2026-05-02', idx * 35);
    sandbox.applyNoteReview('К-002', 'pass');
    const res = sandbox.getNoteSrsInfo('К-002');
    assert.strictEqual(res.step, exp.step, `Step progression mismatch at index ${idx}`);
    assert.strictEqual(res.interval, exp.interval, `Interval progression mismatch at index ${idx}`);
  });

  // Resetting note returns it to step 0 (1 day)
  fakeToday = '2026-12-01';
  sandbox.applyNoteReview('К-002', false);
  const resetRes = sandbox.getNoteSrsInfo('К-002');
  assert.strictEqual(resetRes.step, 0);
  assert.strictEqual(resetRes.interval, 1);

  // 5. Verify viewNotesSrsHub renders step-by-step micro-reader, runnable code, and self-check
  fakeToday = '2026-12-02';
  const notesHubHtml = sandbox.viewNotesSrsHub();
  assert.ok(notesHubHtml.includes('data-srs-note-pass="К-002"') || notesHubHtml.includes('data-srs-note-pass="К-001"'));
  assert.ok(notesHubHtml.includes('data-srs-note-reset='));
  assert.ok(notesHubHtml.includes('srs-flow-selector'));
  assert.ok(notesHubHtml.includes('sub-step-dot'));

  // 6. Verify Flashcard FSRS intervals, Active Rescue Scaffold, and Unified Micro-Stepper (7-dot sliding window)
  const rescueHtml = sandbox.buildActiveRescueScaffoldHTML(
    'В Python переменная хранит **ссылку (указатель)** на объект `PyObject` в куче.',
    'Что хранит переменная в Python?',
    'Ф-001:0'
  );
  assert.ok(rescueHtml.includes('rescue-mask-pill'), 'Active Rescue must mask key term in .rescue-mask-pill');
  assert.ok(rescueHtml.includes('active-rescue-box'), 'Active Rescue must render .active-rescue-box');

  const stepper12 = sandbox.buildUnifiedMicroStepperHTML(5, 12, 'Шаг', 'data-test-dot', '<span>Чип</span>');
  const dotMatches = stepper12.match(/<button type="button" class="sub-step-dot/g) || [];
  assert.strictEqual(dotMatches.length, 7, 'Unified Micro-Stepper must apply 7-dot sliding window when totalCount > 8');
  assert.ok(stepper12.includes('sub-step-dot--edge'), 'Unified Micro-Stepper must mark edge dots when windowed');

  sandbox.applyRemNoteCardRating('Ф-001:0', 1);
  const card1 = sandbox.state.cardSrs['Ф-001:0'];
  assert.strictEqual(card1.interval, 1);
  assert.strictEqual(sandbox.window.__rescuePrimedCards['Ф-001:0'], true, 'Rating 1 (Не знаю) must prime card for Active Rescue');
  sandbox.applyRemNoteCardRating('Ф-001:0', 4);
  const card4 = sandbox.state.cardSrs['Ф-001:0'];
  assert.ok(card4.interval >= 3, 'Rating 4 (Легко / Назубок) must schedule card several days ahead');
  assert.strictEqual(Boolean(sandbox.window.__rescuePrimedCards['Ф-001:0']), false, 'Rating 4 clears Active Rescue prime');

  // Verify Invariant 1.9 semantic subtexts exist in academy.html
  for (const marker of ['С нуля', 'С трудом', 'Уверенно', 'Назубок', '1: Не знаю', 'Active Rescue']) {
    assert.ok(html.includes(marker), `Missing Invariant 1.9 marker in academy.html: ${marker}`);
  }
  console.log('✓ SRS Engine (Notes 1/3/7/21/30 + Flashcards FSRS + Active Rescue + 7-dot Micro-Stepper) verified');
}

async function main() {
  runSrsEngineAndUiSuite();

  const port = await getFreePort();
  const testDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'academy-api-test-'));
  const child = spawn(process.execPath, [SERVER], {
    cwd: ROOT,
    env: { ...process.env, PORT: String(port), PBA_DATA_DIR: testDataDir, NODE_ENV: 'test', DATABASE_URL: '', SYNC_TOKEN: '' },
    stdio: ['ignore', 'pipe', 'pipe']
  });
  child.__output = '';
  child.stdout.on('data', chunk => { child.__output += chunk.toString(); });
  child.stderr.on('data', chunk => { child.__output += chunk.toString(); });
  const baseUrl = `http://127.0.0.1:${port}`;
  console.log(`Starting isolated test server on ${port}`);

  try {
    await waitForServer(baseUrl, child);
    console.log('✓ server health');

    const summaryResponse = await request(`${baseUrl}/api/v1/content/summary`);
    assert.match(summaryResponse.headers.get('content-type') || '', /application\/json/);
    const summary = await summaryResponse.json();
    assert.strictEqual(summary.ok, true);
    assert.strictEqual(summary.tasksCount, 401);
    console.log('✓ content summary');

    const modules = await (await request(`${baseUrl}/api/v1/content/modules`)).json();
    assert.strictEqual(modules.length, 7);

    const note = await (await request(`${baseUrl}/api/v1/content/notes/${encodeURIComponent('К-001')}`)).json();
    assert.strictEqual(note.ok, true);
    assert.ok(note.note);
    console.log('✓ notes endpoint');

    const deck = await (await request(`${baseUrl}/api/v1/content/cards/${encodeURIComponent('Ф-001')}`)).json();
    assert.strictEqual(deck.ok, true);
    assert.ok(deck.deck);
    console.log('✓ cards endpoint');

    const taskList = await (await request(`${baseUrl}/api/v1/content/tasks?level=1&topic=Python`)).json();
    assert.ok(taskList.count > 0);
    const task = await (await request(`${baseUrl}/api/v1/content/tasks/401`)).json();
    assert.strictEqual(task.task.id, 401);
    console.log('✓ task endpoints');

    const search = await (await request(`${baseUrl}/api/v1/content/search?q=FastAPI`)).json();
    assert.strictEqual(search.ok, true);
    assert.ok(Array.isArray(search.results));

    const initialSync = await (await request(`${baseUrl}/api/v1/sync`)).json();
    assert.strictEqual(initialSync.updatedAt, 0);
    const bundle = {
      academyState: {
        xp: 12,
        completedTasks: [1],
        readNotes: ['К-001'],
        noteSrs: { 'К-001': { step: 2, interval: 7, dueDate: '2026-05-10', lastReview: '2026-05-03' } },
        cardSrs: { 'Ф-001:0': { reps: 2, interval: 4, dueDate: '2026-05-07', lastReview: '2026-05-03' } },
      },
      ideStatus: {},
      ideDrafts: {},
    };
    const push = await request(`${baseUrl}/api/v1/sync`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bundle, baseUpdatedAt: 0, device: 'api-test', clientId: 'api-test-client' })
    });
    assert.strictEqual(push.status, 200);
    const pushed = await push.json();
    assert.strictEqual(pushed.bundle.academyState.xp, 12);

    // Push from second device within TTL window with another note/card SRS entry and verify deep monotonic merge
    const bundle2 = {
      academyState: {
        xp: 25,
        completedTasks: [2],
        readNotes: ['К-002'],
        noteSrs: { 'К-002': { step: 1, interval: 3, dueDate: '2026-05-06', lastReview: '2026-05-03' } },
        cardSrs: { 'Ф-001:1': { reps: 1, interval: 2, dueDate: '2026-05-05', lastReview: '2026-05-03' } },
      },
      ideStatus: {},
      ideDrafts: {},
    };
    const push2 = await request(`${baseUrl}/api/v1/sync`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bundle: bundle2, baseUpdatedAt: pushed.updatedAt, device: 'mobile-test', clientId: 'mobile-test-client' })
    });
    assert.strictEqual(push2.status, 200);

    const pulled = await (await request(`${baseUrl}/api/v1/sync`)).json();
    assert.deepStrictEqual(pulled.bundle.academyState.completedTasks, [1, 2]);
    assert.deepStrictEqual(pulled.bundle.academyState.readNotes, ['К-001', 'К-002']);
    assert.strictEqual(pulled.bundle.academyState.noteSrs['К-001'].step, 2);
    assert.strictEqual(pulled.bundle.academyState.noteSrs['К-002'].step, 1);
    assert.strictEqual(pulled.bundle.academyState.cardSrs['Ф-001:0'].reps, 2);
    assert.strictEqual(pulled.bundle.academyState.cardSrs['Ф-001:1'].reps, 1);
    console.log('✓ sync endpoints (including deep SRS merge for cardSrs & noteSrs)');

    const feedback = await request(`${baseUrl}/api/v1/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ context: 'api-test', message: 'isolated integration test' })
    });
    assert.strictEqual(feedback.status, 200);
    assert.strictEqual((await feedback.json()).ok, true);

    const redirect = await request(`${baseUrl}/practice_ide.html`, { redirect: 'manual' });
    assert.strictEqual(redirect.status, 302);
    assert.strictEqual(redirect.headers.get('location'), '/academy.html#/practice');

    const missingApi = await request(`${baseUrl}/api/v1/missing`);
    assert.strictEqual(missingApi.status, 404);
    assert.match(missingApi.headers.get('content-type') || '', /application\/json/);
    console.log('✓ Node production server API v1, sync, feedback, and trainer route passed');
  } finally {
    await stopChild(child);
    fs.rmSync(testDataDir, { recursive: true, force: true });
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
