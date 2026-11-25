/**
 * Python Backend Academy — Unified SRS Card & Action Dock Component (DRY)
 * Единый компонент карточки интервального повторения для десктопа и смартфонов.
 * Соответствует стандартам FSRS и когнитивно скользкому UX.
 */

export const SRS_RATING_LABELS = {
  1: { label: 'Не вспомнил', sub: 'Сброс', color: '#fb7185', key: '1' },
  2: { label: 'Со скрипом', sub: '+1 д', color: '#f59e0b', key: '2' },
  3: { label: 'Вспомнил', sub: '+3 д', color: '#10b981', key: '3' },
  4: { label: 'На автомате', sub: '+7 д', color: '#38bdf8', key: '4' }
};

/**
 * Рендеринг лицевой и оборотной грани флеш-карточки
 */
export function renderUnifiedSrsCardStage({
  cardId,
  deckTitle = '',
  question = '',
  answer = '',
  isFlipped = false,
  counterLabel = '1 / 1',
  statusBadgeHTML = '',
  cardAttr = 'data-srs-flip'
}) {
  const flippedClass = isFlipped ? 'is-flipped fc-card--flipped fc-card--Answer' : '';

  return `
    <main class="srs-card-stage fc-stage" style="width:100%;max-width:700px;margin:0 auto;padding:0;perspective:1200px;box-sizing:border-box;">
      <div class="fc-card demo-card ${flippedClass}" id="srs-active-card" data-flipped="${isFlipped ? 'true' : 'false'}" ${cardAttr} style="width:100%;max-width:700px;min-height:190px;box-sizing:border-box;cursor:pointer;">
        
        <!-- Лицевая грань: Вопрос -->
        <div class="card-face card-front fc-card-front">
          <div class="fc-top-row" style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
            <div class="fc-badge-group" style="display:flex;align-items:center;gap:8px;min-width:0;flex:1;">
              <span class="srs-card-topic-chip" title="${deckTitle}">${deckTitle}</span>
              <span class="fc-card-counter-badge" style="color:var(--ink-muted);font-size:0.75rem;font-weight:600;white-space:nowrap;flex-shrink:0;">${counterLabel}</span>
              ${statusBadgeHTML}
            </div>
            <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;">
              <span class="fc-kbd-hint hide-on-mobile" style="font-size:0.68rem;opacity:0.6;">[Пробел / Enter]</span>
            </div>
          </div>

          <div class="fc-card-body" style="margin:auto 0;padding:14px 0;width:100%;">
            <div class="fc-q" style="font-size:1.14rem;font-weight:700;line-height:1.5;color:var(--ink);">${question}</div>
          </div>
        </div>

        <!-- Оборотная грань: Ответ (Mastery Emerald) -->
        <div class="card-face card-back fc-card-back">
          <div class="fc-top-row" style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
            <div class="fc-badge-group" style="display:flex;align-items:center;gap:8px;min-width:0;flex:1;">
              <span class="srs-card-topic-chip" style="color:#a7f3d0;opacity:0.9;" title="${deckTitle}">${deckTitle}</span>
              <span class="fc-card-counter-badge" style="color:#a7f3d0;opacity:0.8;font-size:0.75rem;font-weight:600;white-space:nowrap;flex-shrink:0;">${counterLabel}</span>
              ${statusBadgeHTML}
            </div>
            <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;">
              <button type="button" class="btn btn-ghost btn-hub-turn-back fc-flip-back-btn" ${cardAttr} style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.10);color:var(--ink-soft);font-size:0.78rem;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;gap:6px;padding:3px 9px;border-radius:8px;">
                ← К вопросу <span class="hide-on-mobile"><kbd class="fc-kbd-hint" style="font-size:0.68rem;padding:1px 5px;background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);border-radius:4px;color:#fff;">Esc</kbd></span>
              </button>
            </div>
          </div>

          <div class="fc-card-body" style="margin:auto 0;padding:12px 0;width:100%;">
            <div class="fc-q-sub" style="font-size:0.88rem;font-weight:600;line-height:1.4;color:#a7f3d0;opacity:0.85;margin-bottom:6px;">${question}</div>
            <div class="fc-divider" style="height:1px;background:linear-gradient(90deg, transparent, rgba(52,211,153,0.30), transparent);margin:6px 0 10px;"></div>
            <div class="fc-a-mastery" style="font-size:1.06rem;line-height:1.6;color:#ffffff;font-weight:500;">${answer}</div>
          </div>
        </div>

      </div>
    </main>
  `;
}

/**
 * Рендеринг Action Dock с когнитивно скользкими кнопками:
 * Фаза 1: «Показать ответ»
 * Фаза 2: «Не вспомнил» (1) | «Со скрипом» (2) | «Вспомнил» (3) | «На автомате» (4)
 */
export function renderUnifiedSrsActionDock({
  isFlipped = false,
  flipAttr = 'data-srs-flip',
  rateAttrPrefix = 'data-srs-rate'
}) {
  return `
    <footer class="srs-action-dock" style="margin-top:14px;max-width:700px;margin-left:auto;margin-right:auto;width:100%;">
      <!-- Фаза 1: Доминантная кнопка переворота (Показать ответ) -->
      <button type="button" class="btn-cta-dominant btn-glass-emerald btn-style-glass btn-sprint-cta ${isFlipped ? 'srs-hidden' : ''}" ${flipAttr} style="${isFlipped ? 'display:none !important;' : 'display:flex !important;'}" title="Показать ответ (Enter или Пробел)">
        <span>Показать ответ</span>
        <kbd class="fc-kbd-hint hide-on-mobile" style="margin-left:8px;">Пробел</kbd>
      </button>

      <!-- Фаза 2: Каноническая 4-кнопочная сетка FSRS (Сетка 2×2 на смартфонах, 1×4 на десктопе) -->
      <div class="srs-rating-grid card-rating-grid ${isFlipped ? '' : 'srs-hidden'}" style="${isFlipped ? 'display:grid !important;' : 'display:none !important;'}">
        <!-- Кнопка 1: Не вспомнил -->
        <button type="button" class="srs-rate-btn srs-rate-again rating-again" ${rateAttrPrefix}="1" title="Не вспомнил (хоткей 1)">
          <span class="rate-badge hide-on-mobile">1</span>
          <span class="rate-label">Не вспомнил</span>
          <span class="rate-sub">Сброс</span>
        </button>

        <!-- Кнопка 2: Со скрипом -->
        <button type="button" class="srs-rate-btn srs-rate-hard rating-hard" ${rateAttrPrefix}="2" title="Со скрипом (хоткей 2)">
          <span class="rate-badge hide-on-mobile">2</span>
          <span class="rate-label">Со скрипом</span>
          <span class="rate-sub">+1 д</span>
        </button>

        <!-- Кнопка 3: Вспомнил -->
        <button type="button" class="srs-rate-btn srs-rate-good rating-good" ${rateAttrPrefix}="3" title="Вспомнил (хоткей 3)">
          <span class="rate-badge hide-on-mobile">3</span>
          <span class="rate-label">Вспомнил</span>
          <span class="rate-sub">+3 д</span>
        </button>

        <!-- Кнопка 4: На автомате -->
        <button type="button" class="srs-rate-btn srs-rate-easy rating-easy" ${rateAttrPrefix}="4" title="На автомате (хоткей 4)">
          <span class="rate-badge hide-on-mobile">4</span>
          <span class="rate-label">На автомате</span>
          <span class="rate-sub">+7 д</span>
        </button>
      </div>
    </footer>
  `;
}
