/**
 * Python Backend Academy — Unified Zen IDE Component (DRY)
 * Единый компонент тренажера решения задач для ПК и смартфонов.
 */

export function renderZenIdeLayout({
  task,
  codeDraft = '',
  editorId = 'py-task-editor',
  mobTab = 'spec', // 'spec' | 'code'
  runStatus = null, // 'running' | 'pass' | 'fail' | null
  runOutput = '',
  socraticHints = [],
  hintLevel = 0,
  isSolved = false,
  drawerTab = 'tests', // 'tests' | 'stdout' | 'socrates'
  drawerCollapsed = false,
  accSocratesOpen = false,
  runBtnAttr = 'data-zen-run',
  hintBtnAttr = 'data-zen-hint',
  mobTabAttr = 'data-zen-tab',
  drawerTabAttr = 'data-zen-drawer-tab'
}) {
  const tid = task.id;
  const shownHints = socraticHints.slice(0, hintLevel).map((h, i) =>
    `<div class="socratic-hint socratic-bubble" style="margin:8px 0;padding:8px 12px;border-radius:10px;background:rgba(217,119,6,0.08);border-left:3px solid var(--amber);font-size:0.82rem;line-height:1.45;color:#fef3c7;"><strong>💡 Наводка ${i+1}:</strong> ${h}</div>`
  ).join('');

  // Мобильный переключатель вкладок Условие / Код
  const mobileTabsHTML = `
    <div class="practice-mobile-tab-bar" style="display:none;margin-bottom:14px;background:rgba(255,255,255,0.03);border:1px solid var(--glass-border);border-radius:14px;padding:4px;gap:6px;">
      <button type="button" class="btn btn-ghost ${mobTab === 'spec' ? 'is-active active' : ''}" ${mobTabAttr}="spec" style="flex:1;padding:8px 12px;font-size:0.82rem;font-weight:700;border-radius:10px;justify-content:center;">📋 Условие &amp; Схемы</button>
      <button type="button" class="btn btn-ghost ${mobTab === 'code' ? 'is-active active' : ''}" ${mobTabAttr}="code" style="flex:1;padding:8px 12px;font-size:0.82rem;font-weight:700;border-radius:10px;justify-content:center;">💻 Редактор кода</button>
    </div>
  `;

  // Панель вывода тестов и терминала (Mini Drawer)
  let drawerContent = '';
  if (drawerTab === 'stdout') {
    drawerContent = `<pre style="margin:0;font-family:var(--font-m, monospace);font-size:0.78rem;white-space:pre-wrap;color:#cbd5e1;">${runOutput || '[Python 3.12 Sandboxed Session]\n>>> Готов к запуску кода.'}</pre>`;
  } else if (drawerTab === 'socrates') {
    drawerContent = shownHints ? `<div>${shownHints}</div>` : `<div style="color:var(--ink-muted);font-size:0.8rem;">Наставник Сократ готов помочь. Нажмите кнопку «Получить наводку» в левой панели.</div>`;
  } else {
    if (runStatus === 'running') {
      drawerContent = `<div class="test-running-shimmer" style="color:var(--amber);font-size:0.82rem;">⚡ Выполняю серверную проверку в FastAPI…</div>`;
    } else if (runStatus === 'pass') {
      drawerContent = `
        <div style="color:#34d399;font-weight:700;">✓ Все тесты пройдены чисто! (+15 XP)</div>
        <div style="font-size:0.75rem;opacity:0.85;margin-top:2px;">Задание успешно решено и закреплено.</div>
      `;
    } else if (runStatus === 'fail') {
      drawerContent = `
        <div style="color:#fb7185;font-weight:700;margin-bottom:4px;">✗ Проверка не пройдена:</div>
        <pre style="margin:0;font-family:var(--font-m, monospace);font-size:0.78rem;white-space:pre-wrap;color:#fca5a5;">${runOutput}</pre>
        <div style="margin-top:6px;font-size:0.74rem;color:var(--amber);">💡 Раскройте подсказки Сократа для наводки на верное решение.</div>
      `;
    } else {
      drawerContent = `<div style="color:var(--ink-muted);font-size:0.8rem;">Редактор готов к проверке. Нажмите «▷ Проверить решение».</div>`;
    }
  }

  const testsTabTitle = runStatus === 'pass'
    ? '✓ Тесты пройдены'
    : (runStatus === 'fail' ? '✗ Тесты не прошли' : (runStatus === 'running' ? '⚡ Проверка…' : 'Тесты (готов)'));
  const testsTabColor = runStatus === 'pass' ? '#34d399' : (runStatus === 'fail' ? '#fb7185' : 'inherit');

  return `
    <div class="card zen-ide-container" style="margin-top:0;">
      ${mobileTabsHTML}
      <div class="practice-layout practice-atomic-split ${mobTab === 'code' ? 'show-code' : 'show-spec'}">
        <!-- Левая панель: Спецификация и Наставник Сократ -->
        <div class="practice-left-pane practice-spec-pane" style="display:flex;flex-direction:column;justify-content:space-between;gap:12px;">
          <div>
            <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
              <div style="display:inline-flex;align-items:center;gap:6px;font-size:0.78rem;font-weight:700;">
                <span style="color:var(--ink-muted);">Практика</span>
                <span class="badge" style="background:rgba(217,119,6,0.18);color:var(--amber);padding:2px 8px;border-radius:8px;font-weight:700;">${task.tier || `Уровень ${task.level || 1}`}</span>
                <span style="color:var(--ink-muted);font-size:0.75rem;">#${tid}</span>
              </div>
              ${isSolved ? `<span class="state-tag state-tag--mastered" style="margin:0;">✓ Решено</span>` : ''}
            </div>

            <div class="lesson-theory" style="font-size:0.89rem;color:var(--ink-soft);line-height:1.55;margin-bottom:12px;">
              <h3 style="font-size:1.05rem;font-weight:700;color:var(--ink);margin:0 0 6px 0;">${task.title}</h3>
              <div>${task.desc || ''}</div>
            </div>

            <!-- Аккордеон Наставника Сократа -->
            <div class="zen-accordion ${accSocratesOpen ? 'is-open' : ''}">
              <div class="zen-accordion-header" style="cursor:pointer;padding:8px 12px;background:rgba(217,119,6,0.08);border-radius:10px;display:flex;justify-content:space-between;align-items:center;">
                <span style="color:var(--amber);font-weight:700;font-size:0.82rem;">💡 Наставник Сократ (Наводки: ${hintLevel} / ${socraticHints.length})</span>
                <span class="acc-icon">${accSocratesOpen ? '▲' : '▼'}</span>
              </div>
              <div class="zen-accordion-content" style="${accSocratesOpen ? 'display:block;padding-top:8px;' : 'display:none;'}">
                <button type="button" class="btn btn-ghost" ${hintBtnAttr} style="width:100%;justify-content:center;font-size:0.82rem;padding:9px 12px;border-radius:12px;border:1px dashed rgba(217,119,6,0.35);background:rgba(217,119,6,0.06);color:#fcd34d;font-weight:600;" ${hintLevel >= socraticHints.length ? 'disabled' : ''}>
                  ${hintLevel >= socraticHints.length ? '✓ Все наводки раскрыты' : 'Получить наводку без готового кода ➔'}
                </button>
                <div class="socrates-hints-stack" style="margin-top:8px;">${shownHints}</div>
              </div>
            </div>
          </div>

          <div style="margin-top:auto;">
            <button type="button" class="btn-glass-emerald practice-mobile-cta" ${mobTabAttr}="code" style="display:none;width:100%;justify-content:center;margin-top:14px;padding:12px 16px;border-radius:12px;font-size:0.88rem;font-weight:700;">Перейти к коду ➔</button>
          </div>
        </div>

        <!-- Правая панель: Редактор кода и Терминал проверки -->
        <div class="practice-right-pane" style="display:flex;flex-direction:column;justify-content:space-between;">
          <div>
            <div class="editor-wrap" style="position:relative;border:1px solid var(--glass-border);border-radius:12px;overflow:hidden;background:#0d1117;">
              <textarea id="${editorId}" class="code-editor" style="width:100%;min-height:240px;background:transparent;color:#f0f6fc;font-family:var(--font-m, monospace);font-size:0.86rem;line-height:1.5;padding:12px;border:none;resize:vertical;outline:none;" spellcheck="false">${codeDraft || task.initialCode || ''}</textarea>
            </div>

            <div class="practice-kbd-dock hide-on-mobile" style="display:flex;align-items:center;gap:14px;padding:6px 14px;background:rgba(0,0,0,0.25);border-radius:0 0 10px 10px;font-size:0.72rem;color:var(--ink-muted);margin-top:-2px;">
              <span><kbd>Ctrl+Enter</kbd> — проверить</span>
              <span><kbd>Tab</kbd> — 4 пробела</span>
            </div>

            <!-- Mini Drawer терминала и тестов -->
            <div class="vscode-mini-drawer ${drawerCollapsed ? 'is-collapsed' : ''}" style="margin-top:12px;border:1px solid var(--glass-border);border-radius:12px;overflow:hidden;background:#080b11;">
              <div class="drawer-nav-bar" style="display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,0.02);border-bottom:1px solid var(--glass-border);padding:4px 8px;">
                <div class="drawer-tabs-group" style="display:flex;gap:4px;">
                  <button type="button" class="drawer-tab-btn ${drawerTab === 'tests' ? 'is-active' : ''}" ${drawerTabAttr}="tests" style="padding:6px 12px;font-size:0.75rem;font-weight:600;color:${testsTabColor};border:none;background:transparent;cursor:pointer;">${testsTabTitle}</button>
                  <button type="button" class="drawer-tab-btn ${drawerTab === 'stdout' ? 'is-active' : ''}" ${drawerTabAttr}="stdout" style="padding:6px 12px;font-size:0.75rem;font-weight:600;color:var(--ink-muted);border:none;background:transparent;cursor:pointer;">Терминал (stdout)</button>
                  <button type="button" class="drawer-tab-btn ${drawerTab === 'socrates' ? 'is-active' : ''}" ${drawerTabAttr}="socrates" style="padding:6px 12px;font-size:0.75rem;font-weight:600;color:var(--ink-muted);border:none;background:transparent;cursor:pointer;">Сократ</button>
                </div>
              </div>
              <div class="drawer-body" style="padding:12px;min-height:70px;">
                ${drawerContent}
              </div>
            </div>
          </div>

          <!-- Нижний док действий с кнопкой запуска -->
          <div style="margin-top:14px;display:flex;gap:8px;align-items:center;">
            <button type="button" class="btn-glass-emerald" ${runBtnAttr}="${tid}" style="flex:1;justify-content:center;padding:12px 18px;border-radius:14px;font-size:0.92rem;font-weight:700;display:inline-flex;align-items:center;gap:10px;">
              <span>▷ Проверить решение</span>
              <span class="xp-tag" style="background:rgba(16,185,129,0.25);color:#34d399;padding:2px 8px;border-radius:8px;font-size:0.75rem;">+15 XP</span>
              <span class="hide-on-mobile" style="font-size:0.75rem;opacity:0.85;font-weight:500;">(Ctrl+Enter)</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
}
