const fs = require('fs');
const path = require('path');
const vm = require('vm');

const jsCode = fs.readFileSync(path.join(__dirname, 'extracted_academy.js'), 'utf-8');

const elementsById = {};
function makeEl(id = '', tag = 'div') {
  const el = {
    id,
    tagName: tag.toUpperCase(),
    innerHTML: '',
    textContent: '',
    value: '',
    className: '',
    style: {},
    attributes: {},
    classList: {
      _set: new Set(),
      add(c) { this._set.add(c); },
      remove(c) { this._set.delete(c); },
      toggle(c, force) { return true; },
      contains(c) { return false; }
    },
    setAttribute(k, v) { this.attributes[k] = String(v); },
    getAttribute(k) { return this.attributes[k]; },
    removeAttribute(k) { delete this.attributes[k]; },
    appendChild(child) { return child; },
    insertBefore(child) { return child; },
    remove() {},
    addEventListener() {},
    querySelector() { return makeEl(); },
    querySelectorAll() { return []; },
    closest() { return null; },
    focus() {},
    firstChild: {}
  };
  if (id) elementsById[id] = el;
  return el;
}

['view-root', 'nav-desktop', 'theme-toggle-d', 'theme-toggle-m', 'reset-btn-d', 'streak-num-d', 'streak-num-m', 'code-input', 'code-output', 'run-btn', 'run-status', 'lesson-code', 'py-skill-editor', 'prac-code-editor'].forEach(id => makeEl(id));

const sidebarFoot = makeEl('sidebar-foot');

const sandbox = {
  console,
  setTimeout, clearTimeout, setInterval, clearInterval,
  alert: () => {},
  confirm: () => true,
  navigator: { clipboard: { writeText: () => {} } },
  localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
  location: { hash: '#/' },
  window: null,
  document: {
    body: makeEl('body', 'body'),
    head: makeEl('head', 'head'),
    documentElement: makeEl('html', 'html'),
    getElementById: id => elementsById[id] || makeEl(id),
    createElement: tag => makeEl('', tag),
    querySelector: sel => (sel === '.sidebar-foot' ? sidebarFoot : null),
    querySelectorAll: () => [],
    addEventListener: () => {}
  }
};
sandbox.window = sandbox;
sandbox.window.scrollTo = () => {};
sandbox.window.speechSynthesis = { speak: () => {}, cancel: () => {}, pause: () => {}, resume: () => {} };
sandbox.SpeechSynthesisUtterance = function(text) { this.text = text; };
sandbox.window.addEventListener = () => {};
sandbox.window.matchMedia = () => ({ matches: false });
sandbox.window.__BRYTHON__ = { builtins: true, runPythonSource: () => {} };
sandbox.window.brython = () => {};

vm.createContext(sandbox);
vm.runInContext(jsCode, sandbox);

const pyMastery = sandbox.PY_MASTERY;
const sk111 = pyMastery.units[0].skills[0];
console.log('=== НАВЫК 1.1.1 ===');
console.log('Название:', sk111.title);
console.log('\n--- 1. КОНСПЕКТЫ (kIds) ---');
(sk111.kIds || []).forEach((k, idx) => {
  const note = (pyMastery.notes && pyMastery.notes[k]) || {};
  console.log(`Точка ${idx+1} [${k}]: ${note.title || 'не найден'}`);
});

console.log('\n--- 2. КОЛОДЫ КАРТОЧЕК (fIds) ---');
(sk111.fIds || []).forEach((f, idx) => {
  const d = (pyMastery.decks && pyMastery.decks[f]) || {};
  console.log(`Точка ${idx+1} [${f}]: ${d.title || 'не найдена'} (${(d.cards||[]).length} карточек)`);
});

console.log('\n--- 3. ЗАДАЧИ ПРАКТИКИ (IDE_TASKS_BY_ID) ---');
const tasksById = sandbox.IDE_TASKS_BY_ID || {};
(sk111.taskIds || []).forEach((t, idx) => {
  const task = tasksById[t] || {};
  console.log(`Точка ${idx+1} [Задача #${t}]: ${task.title} (уровень: ${task.tier})`);
});
