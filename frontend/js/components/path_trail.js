/**
 * Python Backend Academy — Unified Path & Trail Component (DRY)
 * Единый компонент интерактивной Тропы обучения (Serpentine Path) для десктопа и смартфонов.
 */

export function renderPathTrailLayout({
  echelon,
  activeNodeId = null,
  onNodeClickAttr = 'data-path-node',
  onGateClickAttr = 'data-path-gate'
}) {
  const nodes = echelon.nodes || [];
  const chapters = echelon.chapters || [];

  // Рендеринг верхней плашки эшелона
  const headerHTML = `
    <div class="path-echelon-header" style="margin-bottom:24px;text-align:center;">
      <div style="display:inline-flex;align-items:center;gap:8px;padding:4px 14px;border-radius:999px;background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.25);font-size:0.78rem;font-weight:700;color:#34d399;margin-bottom:8px;">
        <span>🎯 ${echelon.title}</span>
        <span>·</span>
        <span>${echelon.mastered_units} / ${echelon.total_units} уроков (${echelon.progress_pct}%)</span>
      </div>
      <h2 style="font-size:1.45rem;font-weight:800;color:var(--ink);margin:0 0 4px 0;">Тропа обучения</h2>
      <p style="font-size:0.86rem;color:var(--ink-muted);max-width:540px;margin:0 auto;">${echelon.subtitle}</p>
    </div>
  `;

  // Рендеринг узлов змейки
  const nodesHTML = nodes.map((node, idx) => {
    const isMastered = node.status === 'mastered';
    const isActive = node.status === 'active';
    const isLocked = node.status === 'locked';

    let nodeClass = 'hex-node';
    if (isMastered) nodeClass += ' hex-node--mastered state-mastered';
    else if (isActive) nodeClass += ' hex-node--active state-active';
    else nodeClass += ' hex-node--locked state-locked';

    const gateBadge = node.is_gate ? `<span class="gate-marker" style="position:absolute;top:-8px;right:-8px;background:var(--amber);color:#000;font-size:0.65rem;font-weight:800;padding:2px 6px;border-radius:6px;">ВОРОТА</span>` : '';

    return `
      <div class="path-node-wrapper" style="position:relative;margin:18px 0;display:flex;justify-content:center;">
        <button type="button" class="${nodeClass}" ${onNodeClickAttr}="${node.id}" style="position:relative;width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;border:2px solid ${isActive ? '#10b981' : (isMastered ? '#059669' : 'rgba(255,255,255,0.1)')};background:${isActive ? 'rgba(16,185,129,0.22)' : (isMastered ? 'rgba(16,185,129,0.12)' : 'rgba(255,255,255,0.03)')};color:#fff;font-weight:700;box-shadow:${isActive ? '0 0 24px rgba(16,185,129,0.45)' : 'none'};">
          <span>${node.unit_num}</span>
          ${gateBadge}
        </button>
        <div class="node-caption" style="position:absolute;left:calc(50% + 44px);white-space:nowrap;font-size:0.80rem;font-weight:600;color:${isActive ? '#34d399' : 'var(--ink-soft)'};">
          ${node.title}
        </div>
      </div>
    `;
  }).join('');

  return `
    <div class="path-serpentine-wrap" style="width:100%;max-width:680px;margin:0 auto;position:relative;padding-bottom:120px;">
      ${headerHTML}
      <div class="path-serpentine-track" style="position:relative;">
        ${nodesHTML}
      </div>
    </div>
  `;
}
