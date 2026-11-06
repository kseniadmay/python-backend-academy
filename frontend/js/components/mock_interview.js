/**
 * Python Backend Academy — Unified Mock Interview Simulator Component (DRY)
 * Единый компонент симулятора технического собеседования Junior+ Python Backend.
 */

export function renderMockInterviewLayout({
  session,
  codeDraft = '',
  editorId = 'mock-code-editor',
  hintsUsed = 0,
  evaluationResult = null,
  isEvaluating = false,
  onRunAttr = 'data-mock-submit',
  onHintAttr = 'data-mock-hint'
}) {
  const q = session.question;
  const socraticLevels = q.socratic_levels || [];

  const shownHintsHTML = socraticLevels.slice(0, hintsUsed).map((h, idx) => `
    <div class="chat-bubble chat-bubble--interviewer hint-box" style="margin:10px 0;padding:12px 14px;border-radius:12px;background:rgba(217,119,6,0.08);border-left:3px solid var(--amber);">
      <div style="font-size:0.75rem;font-weight:700;color:var(--amber);margin-bottom:4px;">🎙️ Tech Lead · Ступень ${idx}</div>
      <div style="font-size:0.86rem;line-height:1.5;color:var(--ink-soft);">${h}</div>
    </div>
  `).join('');

  let evalBoxHTML = '';
  if (isEvaluating) {
    evalBoxHTML = `<div class="test-running-shimmer" style="padding:14px;border-radius:12px;color:var(--amber);font-weight:700;">⏳ Тимлид проверяет код на тестовом наборе…</div>`;
  } else if (evaluationResult) {
    const isPass = evaluationResult.status === 'pass';
    const boxBg = isPass ? 'rgba(16,185,129,0.12)' : 'rgba(244,63,94,0.12)';
    const boxBorder = isPass ? 'rgba(16,185,129,0.35)' : 'rgba(244,63,94,0.35)';
    const textColor = isPass ? '#34d399' : '#fb7185';

    evalBoxHTML = `
      <div style="margin-top:14px;padding:14px;border-radius:12px;background:${boxBg};border:1px solid ${boxBorder};">
        <div style="font-size:0.95rem;font-weight:700;color:${textColor};margin-bottom:4px;">${evaluationResult.verdict}</div>
        ${isPass ? `<div style="font-size:0.82rem;color:var(--ink-muted);">Присвоенный грейд: <strong>${evaluationResult.candidate_level}</strong> (+${evaluationResult.xp_awarded} XP)</div>` : ''}
        ${evaluationResult.output ? `<pre style="margin-top:8px;font-size:0.78rem;font-family:var(--font-m, monospace);color:#cbd5e1;white-space:pre-wrap;">${evaluationResult.output}</pre>` : ''}
      </div>
    `;
  }

  return `
    <div class="mock-interview-container" style="max-width:960px;margin:0 auto;padding-bottom:100px;">
      <!-- Шапка интервью -->
      <div class="mock-topbar" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid var(--line);flex-wrap:wrap;gap:10px;">
        <div style="display:flex;align-items:center;gap:10px;">
          <span style="font-size:1.3rem;">💼</span>
          <div>
            <h2 style="font-size:1.25rem;font-weight:800;color:var(--ink);margin:0;">Live-Coding Секция: Junior+ Python Backend</h2>
            <div style="font-size:0.75rem;color:var(--ink-muted);">Эшелон ${session.echelon} · Тема: ${q.topic}</div>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
          <span class="badge" style="background:rgba(217,119,6,0.18);color:var(--amber);padding:4px 10px;border-radius:8px;font-weight:700;">⏱ 30:00</span>
          <span class="badge" style="background:rgba(16,185,129,0.18);color:#34d399;padding:4px 10px;border-radius:8px;font-weight:700;">+40 XP</span>
        </div>
      </div>

      <!-- Основной 2-колоночный сплиттер (на смартфонах вертикальная колонка) -->
      <div class="mock-split-grid" style="display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));gap:18px;">
        <!-- Левая колонка: ТЗ и диалог с Tech Lead -->
        <div class="mock-spec-panel" style="display:flex;flex-direction:column;gap:14px;">
          <div class="card" style="padding:18px;border-radius:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
              <span class="badge" style="font-size:0.75rem;background:rgba(255,255,255,0.06);color:var(--ink-soft);padding:2px 8px;border-radius:6px;">${q.tier}</span>
              <span style="font-size:0.75rem;color:var(--ink-muted);">Задача #${q.id}</span>
            </div>
            <h3 style="font-size:1.08rem;font-weight:700;color:var(--ink);margin:0 0 8px 0;">${q.title}</h3>
            <div style="font-size:0.88rem;line-height:1.55;color:var(--ink-soft);">${q.desc}</div>
          </div>

          <!-- Диалог с Tech Lead и наводки Сократа -->
          <div class="card" style="padding:16px;border-radius:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
              <span style="font-size:0.84rem;font-weight:700;color:var(--ink);">Диалог с интервьюером</span>
              <button type="button" class="btn btn-ghost" ${onHintAttr} style="font-size:0.78rem;padding:4px 10px;border-radius:8px;border:1px dashed rgba(217,119,6,0.35);color:var(--amber);" ${hintsUsed >= socraticLevels.length ? 'disabled' : ''}>
                ${hintsUsed >= socraticLevels.length ? '✓ Все наводки исчерпаны' : 'Попросить наводку'}
              </button>
            </div>
            <div class="socratic-dialog-body">
              ${shownHintsHTML || `<div style="font-size:0.80rem;color:var(--ink-muted);padding:8px 0;">Интервьюер слушает ваши рассуждения. Если зашли в тупик — запросите наводку без готового кода.</div>`}
            </div>
          </div>
        </div>

        <!-- Правая колонка: Редактор кода и сдача решения -->
        <div class="mock-code-panel" style="display:flex;flex-direction:column;gap:14px;">
          <div class="editor-wrap" style="border:1px solid var(--glass-border);border-radius:14px;overflow:hidden;background:#0d1117;">
            <div style="padding:8px 14px;background:rgba(255,255,255,0.03);border-bottom:1px solid var(--glass-border);font-size:0.75rem;color:var(--ink-muted);font-family:var(--font-m, monospace);">
              solution.py (Python 3.12)
            </div>
            <textarea id="${editorId}" style="width:100%;min-height:280px;background:transparent;color:#f0f6fc;font-family:var(--font-m, monospace);font-size:0.86rem;line-height:1.5;padding:14px;border:none;resize:vertical;outline:none;" spellcheck="false">${codeDraft || q.initial_code || ''}</textarea>
          </div>

          <button type="button" class="btn-glass-emerald" ${onRunAttr}="${q.id}" style="width:100%;justify-content:center;padding:14px;border-radius:14px;font-size:0.95rem;font-weight:700;display:inline-flex;align-items:center;gap:10px;">
            <span>Сдать решение тимлиду ➔</span>
            <span class="xp-tag" style="background:rgba(16,185,129,0.25);color:#34d399;padding:2px 8px;border-radius:8px;font-size:0.75rem;">+40 XP</span>
          </button>

          ${evalBoxHTML}
        </div>
      </div>
    </div>
  `;
}
