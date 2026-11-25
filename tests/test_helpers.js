'use strict';
/**
 * test_helpers.js
 * Единый модуль общих путей, кэшированного чтения артефактов и инвариантов (DRY)
 * для всех регрессионных и архитектурных сьютов в директории tests/.
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const rootDir = path.resolve(__dirname, '..');
const remnoteDir = path.join(rootDir, 'knowledge_base');
const academyPath = path.join(rootDir, 'academy.html');
const etalonyPath = path.join(rootDir, 'standards', 'standards.html');
const projectContextPath = path.join(rootDir, 'PROJECT_CONTEXT.md');
const agentsMdPath = path.join(rootDir, 'AGENTS.md');
const fixturesDir = path.join(rootDir, 'tests', 'fixtures');
const schemaSqlPath = path.join(fixturesDir, 'test_db_schema.sql');

let _cache = null;
let _pyMasteryCache = null;

function getTestContext() {
  if (!_cache) {
    assert(fs.existsSync(academyPath), `academy.html missing at ${academyPath}`);
    assert(fs.existsSync(etalonyPath), `standards.html missing at ${etalonyPath}`);
    const academyHtmlRaw = fs.readFileSync(academyPath, 'utf-8');
    const etalonyHtmlRaw = fs.readFileSync(etalonyPath, 'utf-8');
    const academyHtml = academyHtmlRaw.replace(/\r\n/g, '\n');
    const etalonyHtml = etalonyHtmlRaw.replace(/\r\n/g, '\n');
    _cache = {
      rootDir,
      remnoteDir,
      academyPath,
      etalonyPath,
      projectContextPath,
      agentsMdPath,
      fixturesDir,
      schemaSqlPath,
      academyHtmlRaw,
      etalonyHtmlRaw,
      academyHtml,
      etalonyHtml,
      projectContext: fs.existsSync(projectContextPath) ? fs.readFileSync(projectContextPath, 'utf-8') : '',
      agentsMd: fs.existsSync(agentsMdPath) ? fs.readFileSync(agentsMdPath, 'utf-8') : '',
      viewPythonSkillSlice: academyHtml.slice(
        academyHtml.indexOf('function viewPythonSkill('),
        academyHtml.indexOf('function viewCardsHub(')
      ),
      cardsDueModeSlice: academyHtml.slice(
        academyHtml.indexOf('if(cardsHubState.dueMode){'),
        academyHtml.indexOf('const allDeckIds = Object.keys(ALL_DECKS_COMBINED)')
      )
    };
  }
  return _cache;
}

function getPyMastery() {
  if (!_pyMasteryCache) {
    const { academyHtml } = getTestContext();
    const m = academyHtml.match(/const PY_MASTERY = ({[\s\S]*?});\s*(?:const|let|var|function)/);
    assert(m, 'PY_MASTERY must be present in academy.html');
    _pyMasteryCache = JSON.parse(m[1]);
  }
  return _pyMasteryCache;
}

function assertCanonicalEtalonSync(message) {
  const ctx = getTestContext();
  assert.strictEqual(
    ctx.academyHtmlRaw.length,
    ctx.etalonyHtmlRaw.length,
    `Invariant 0: academy.html (${ctx.academyHtmlRaw.length} bytes) must match standards.html (${ctx.etalonyHtmlRaw.length} bytes) length`
  );
  assert.strictEqual(
    ctx.academyHtmlRaw,
    ctx.etalonyHtmlRaw,
    message || 'academy.html и standards.html обязаны быть строго побайтово идентичны!'
  );
}

module.exports = {
  rootDir,
  remnoteDir,
  academyPath,
  etalonyPath,
  projectContextPath,
  agentsMdPath,
  fixturesDir,
  schemaSqlPath,
  getTestContext,
  getPyMastery,
  assertCanonicalEtalonSync
};
