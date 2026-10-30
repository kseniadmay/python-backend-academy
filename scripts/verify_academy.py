import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from quick_precommit_check import check_html_inline_scripts

HTML_PATH = os.path.normpath(os.path.join(_ROOT, 'academy.html'))
ETALON_PATH = os.path.normpath(os.path.join(_ROOT, 'standards', 'standards.html'))
INDEX_PATH = os.path.normpath(os.path.join(_ROOT, 'index.html'))

assert os.path.isfile(HTML_PATH), f'academy.html missing: {HTML_PATH}'
assert os.path.isfile(ETALON_PATH), f'standards/standards.html missing: {ETALON_PATH}'

# 0. Verify Canonical Benchmark Invariant: academy.html and standards.html must be strictly identical
with open(HTML_PATH, encoding='utf-8') as f1, open(ETALON_PATH, encoding='utf-8') as f2:
    assert f1.read() == f2.read(), 'academy.html and standards.html must be strictly identical (Canonical Benchmark Invariant)!'

# 1. Syntax check with node --check
c_acad = check_html_inline_scripts(HTML_PATH, 'academy.html', require_non_empty=True)
c_etalon = check_html_inline_scripts(ETALON_PATH, 'standards.html', require_non_empty=True)
c_idx = check_html_inline_scripts(INDEX_PATH, 'index.html', require_non_empty=True) if os.path.isfile(INDEX_PATH) else 0
print(f'1. [PASS] node --check passed with 0 syntax errors across {c_acad + c_etalon + c_idx} scripts (academy: {c_acad}, etalon: {c_etalon}, index: {c_idx})!', flush=True)

# 2. Fast in-memory Node VM runtime & router verification (< 0.8s instead of 14 heavy Chrome processes)
NODE_VM_PROBE = r"""
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');

const t0 = Date.now();
const html = fs.readFileSync(process.argv[1], 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
assert(scripts.length > 0, 'No inline <script> blocks found in academy.html');

const elementsById = {};
function makeEl(id = '') {
  const el = {
    id, innerHTML: '', textContent: '', value: '', className: '', style: {}, dataset: {}, attributes: {},
    classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
    setAttribute(k, v){ this.attributes[k] = String(v); },
    getAttribute(k){ return this.attributes[k] || null; },
    removeAttribute(k){ delete this.attributes[k]; },
    appendChild(c){ return c; }, insertBefore(c){ return c; }, remove(){},
    addEventListener(){}, querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
    closest(){ return null; }, focus(){}, scrollIntoView(){},
    getBoundingClientRect(){ return { top: 0, bottom: 100, left: 0, right: 100, width: 100, height: 100 }; }
  };
  if (id) elementsById[id] = el;
  return el;
}

[
  'view-root', 'nav-desktop', 'theme-toggle-d', 'theme-toggle-m', 'reset-btn-d',
  'streak-num-d', 'streak-num-m', 'streak-num-sidebar', 'streak-word-d',
  'topbar-pomo-time', 'sidebar-pomo-time', 'topbar-sound-btn'
].forEach(id => makeEl(id));

const runtimeErrors = [];
const sandbox = {
  console: {
    log(){}, info(){}, warn(){},
    error(...args){ runtimeErrors.push(args.join(' ')); }
  },
  Math, Date, JSON, Object, Array, String, Number, Boolean, RegExp, Set, Map, Promise, Error, TypeError,
  parseInt, parseFloat, isNaN, isFinite, encodeURIComponent, decodeURIComponent,
  setTimeout(){ return 1; }, clearTimeout(){}, setInterval(){ return 1; }, clearInterval(){},
  requestAnimationFrame(){},
  localStorage: { _s:{}, getItem(k){ return this._s[k] || null; }, setItem(k, v){ this._s[k] = String(v); }, removeItem(k){ delete this._s[k]; } },
  location: { hash: '#/', protocol: 'https:', href: 'https://localhost/#/' },
  navigator: { clipboard: { writeText(){} }, vibrate(){} },
  document: {
    body: makeEl('body'), documentElement: makeEl('html'),
    getElementById(id){ return elementsById[id] || makeEl(id); },
    querySelector(){ return makeEl(); }, querySelectorAll(){ return []; },
    createElement(t){ return makeEl('', t); }, addEventListener(){}
  },
  window: null,
  scrollTo(){}, matchMedia(){ return { matches: false, addEventListener(){} }; }
};
sandbox.window = sandbox;
sandbox.window.addEventListener = function(ev, fn){ if (ev === 'hashchange') sandbox.__onHash = fn; };

vm.createContext(sandbox);
for (const code of scripts) {
  vm.runInContext(code, sandbox);
}

const routes = [
  '#/', '#/python', '#/web', '#/backend', '#/algorithms', '#/databases',
  '#/architecture', '#/infra', '#/infra/boss', '#/mock', '#/map', '#/path',
  '#/practice', '#/cards',
  '#/python/skill/1.1.1', '#/databases/skill/5.1.1', '#/databases/skill/5.2.1', '#/databases/skill/5.3.1'
];

for (const route of routes) {
  sandbox.location.hash = route;
  sandbox.__onHash();
  const dom = elementsById['view-root'].innerHTML;
  assert(dom && dom.trim().length > 200, `Empty #view-root (${dom ? dom.length : 0} chars) for route ${route}`);
  assert(!/NaN\b/.test(dom), `Unexpected NaN rendered in DOM for route ${route}`);
}

assert.strictEqual(runtimeErrors.length, 0, `Runtime console.error calls: ${runtimeErrors.join('; ')}`);
console.log(`2. [PASS] In-memory Node VM rendered ${routes.length} routes with 0 runtime errors in ${Date.now() - t0}ms!`);
"""

res = subprocess.run(
    ['node', '-e', NODE_VM_PROBE, HTML_PATH],
    cwd=_ROOT, text=True, encoding='utf-8'
)
if res.returncode != 0:
    sys.exit(res.returncode)
