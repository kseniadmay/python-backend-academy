
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const jsCode = fs.readFileSync('scripts/extracted_academy.js', 'utf-8');

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
const winListeners = {};

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
sandbox.window.addEventListener = (ev, fn) => {
  if (!winListeners[ev]) winListeners[ev] = [];
  winListeners[ev].push(fn);
};
sandbox.window.matchMedia = () => ({ matches: false });
sandbox.window.__BRYTHON__ = { builtins: true, runPythonSource: () => {} };
sandbox.window.brython = () => {};

vm.createContext(sandbox);
vm.runInContext(jsCode, sandbox);

function navigate(hash) {
  sandbox.location.hash = hash;
  (winListeners['hashchange'] || []).forEach(fn => fn());
  return elementsById['view-root'].innerHTML;
}

const html = navigate('#/python/skill/1.1.1');
console.log('Includes Шаг 1/:', html.includes('Шаг 1/'));
console.log('Includes Понятно, дальше:', html.includes('Понятно, дальше'));
console.log('Includes sprint-focus-topbar:', html.includes('sprint-focus-topbar'));
console.log('Includes btn-sprint-cta:', html.includes('btn-sprint-cta'));
