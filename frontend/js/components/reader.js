/**
 * Python Backend Academy — Unified Atomic Reader Component (DRY)
 * Единый компонент чтения атомарных конспектов (1 шаг = 1 экран, Single Dominant CTA).
 */

export function renderAtomicReaderLayout({
  note,
  currentStepIndex = 0,
  onStepChangeAttr = 'data-reader-step',
  onFinishAttr = 'data-reader-finish'
}) {
  const steps = note.steps || [];
  const total = steps.length;
  const currentStep = steps[currentStepIndex] || steps[0] || { title: '', html: '' };
  const isFinal = currentStepIndex >= total - 1;

  // Скользящее окно микро-степпера (до 7 точек)
  const windowSize = Math.min(7, total);
  let startIdx = Math.max(0, currentStepIndex - Math.floor(windowSize / 2));
  if (startIdx + windowSize > total) {
    startIdx = Math.max(0, total - windowSize);
  }
  const visibleIndices = Array.from({ length: windowSize }, (_, i) => startIdx + i);

  const dotsHTML = visibleIndices.map(idx => {
    let cls = 'sub-step-dot';
    if (idx < currentStepIndex) cls += ' is-done';
    else if (idx === currentStepIndex) cls += ' is-active';
    return `<span class="${cls}" title="Шаг ${idx + 1} из ${total}"></span>`;
  }).join('');

  // Single Dominant CTA
  let ctaHTML = '';
  if (isFinal) {
    const deckTarget = note.related_deck_id || '';
    ctaHTML = `
      <button type="button" class="btn-cta-dominant btn-glass-emerald btn-style-glass" ${onFinishAttr}="${deckTarget}" style="width:100%;max-width:440px;min-height:50px;border-radius:14px;font-size:1rem;font-weight:700;display:inline-flex;align-items:center;justify-content:center;gap:10px;">
        <span>Закрепить в карточках ➔</span>
        <span class="xp-tag" style="background:rgba(16,185,129,0.25);color:#34d399;padding:2px 8px;border-radius:8px;font-size:0.75rem;">+10 XP</span>
      </button>
    `;
  } else {
    ctaHTML = `
      <button type="button" class="btn btn-ghost" ${onStepChangeAttr}="${currentStepIndex + 1}" style="padding:12px 28px;border-radius:12px;background:rgba(255,255,255,0.06);border:1px solid var(--glass-border);font-size:0.92rem;font-weight:700;color:var(--ink);">
        Следующий шаг ➔
      </button>
    `;
  }

  return `
    <div class="reader-container" style="max-width:740px;margin:0 auto;padding-bottom:100px;">
      <!-- Шапка конспекта -->
      <div class="reader-header" style="margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
        <div>
          <span style="font-size:0.76rem;color:var(--ink-muted);font-weight:700;text-transform:uppercase;letter-spacing:0.05em;">Конспект</span>
          <h2 style="font-size:1.35rem;font-weight:800;color:var(--ink);margin:4px 0 0 0;">${note.title}</h2>
        </div>
        <div style="font-size:0.80rem;color:var(--ink-muted);font-weight:600;">
          Шаг ${currentStepIndex + 1} из ${total}
        </div>
      </div>

      <!-- Карточка микро-шага теории (1 шаг = 1 экран) -->
      <div class="card microstep-card" style="padding:24px;border-radius:18px;margin-bottom:24px;">
        <h3 style="font-size:1.15rem;font-weight:700;color:var(--ink);margin:0 0 14px 0;">${currentStep.title}</h3>
        <div class="reader-step-body" style="font-size:0.92rem;line-height:1.65;color:var(--ink-soft);">
          ${currentStep.html}
        </div>
      </div>

      <!-- Единый нижний микро-степпер и CTA-док -->
      <div class="reader-dock" style="display:flex;flex-direction:column;align-items:center;gap:16px;">
        <div class="sub-step-dots-row" style="display:flex;align-items:center;gap:6px;">
          ${currentStepIndex > 0 ? `<button type="button" class="btn btn-ghost" ${onStepChangeAttr}="${currentStepIndex - 1}" style="padding:2px 8px;font-size:0.75rem;margin-right:4px;">←</button>` : ''}
          ${dotsHTML}
        </div>
        <div style="width:100%;display:flex;justify-content:center;">
          ${ctaHTML}
        </div>
      </div>
    </div>
  `;
}
