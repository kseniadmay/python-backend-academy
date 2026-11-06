/**
 * Python Backend Academy — Unified Navigation Component (DRY)
 * Единый компонент навигации для десктопного сайдбара, мобильного таббара
 * и боковой модальной шторки (drawer).
 */

/**
 * Рендеринг ссылок десктопного сайдбара с разделением на группы и бейджами
 */
export function buildDesktopNavHTML(desktopGroups = [], ICONS = {}) {
  return desktopGroups.map(group => {
    const groupLabel = `<div class="nav-group-label" style="${group.id !== 'main' ? 'margin-top:14px;' : ''}">${group.title}</div>`;
    const links = group.items.map(it => {
      let badgeHtml = '';
      if (it.badge) {
        const badgeClass = it.route === '/cards' || it.route === '/notes-review'
          ? 'navlink__pct navlink__badge-due'
          : (it.route === '/path' ? 'navlink__pct navlink__badge-emerald' : 'navlink__pct');
        badgeHtml = `<span class="${badgeClass}">${it.badge}</span>`;
      }
      const iconSvg = ICONS[it.icon] || ICONS.dot || '';
      return `<a href="#${it.route}" class="navlink" data-route="${it.route}">${iconSvg}<span>${it.label}</span>${badgeHtml}</a>`;
    }).join('');

    return `${groupLabel}\n${links}`;
  }).join('\n');
}

/**
 * Рендеринг элементов нижнего плавающего таббара смартфона (4 основных таба)
 */
export function buildMobileTabbarHTML(mobileTabs = [], ICONS = {}, cardsDueCount = 0) {
  return mobileTabs.map(it => {
    const lbl = it.short_label || it.label;
    const isCards = it.route === '/cards';
    const hasDue = isCards && (cardsDueCount > 0 || it.badge);
    const dotHtml = hasDue ? '<span class="tabbar__due-dot" aria-label="Есть карточки для повторения"></span>' : '';
    const iconSvg = ICONS[it.icon] || ICONS.dot || '';

    return `<a href="#${it.route}" class="tabbar__item" data-route="${it.route}">
      <span class="tabbar__icon-wrap">${iconSvg}${dotHtml}</span>
      <span>${lbl}</span>
    </a>`;
  }).join('');
}

/**
 * Рендеринг содержимого мобильной шторки (drawer) без жестко захардкоженных дублей
 */
export function buildMobileDrawerHTML(drawerItems = [], ICONS = {}, { streak = 0, lang = 'ru' } = {}) {
  // Группировка элементов
  const mainItems = drawerItems.filter(it => it.group === 'main');
  const trainerItems = drawerItems.filter(it => it.group === 'trainer' || it.group === 'tool');
  const moduleItems = drawerItems.filter(it => it.group === 'module');

  const renderDrawerLink = (it, isModule = false) => {
    const iconSvg = ICONS[it.icon] || '';
    const extraStyle = isModule ? 'font-size:0.80rem;padding:7px 10px;' : '';
    return `<a href="#${it.route}" class="drawer-nav-link" onclick="closeMobileDrawer();" style="${extraStyle}">
      ${iconSvg ? `<span class="drawer-link-icon" style="display:inline-flex;align-items:center;margin-right:8px;vertical-align:middle;">${iconSvg}</span>` : ''}
      <span>${it.label}</span>
      ${it.badge ? `<span class="badge" style="margin-left:auto;font-size:0.72rem;background:rgba(16,185,129,0.18);color:#34d399;padding:1px 6px;border-radius:6px;">${it.badge}</span>` : ''}
    </a>`;
  };

  return `
    <div class="mobile-side-drawer-panel">
      <!-- Header -->
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid var(--line);">
        <div>
          <div style="font-size:1.15rem;font-weight:800;color:var(--ink);display:flex;align-items:center;gap:8px;">
            <svg class="icon" viewBox="0 0 24 24" style="width:22px;height:22px;stroke:#10b981;"><circle cx="6" cy="6" r="2.2"/><circle cx="18" cy="6" r="2.2"/><circle cx="12" cy="18" r="2.2"/><path d="M7.8 7.6 10.5 16M16.2 7.6 13.5 16M8.3 6h7.4"/></svg>
            Academy
          </div>
          <div style="font-size:0.75rem;color:var(--ink-muted);font-weight:600;">Python Backend</div>
        </div>
        <button class="btn btn-ghost" style="padding:4px 8px;font-size:1.2rem;border-radius:10px;min-width:36px;min-height:36px;display:flex;align-items:center;justify-content:center;" data-close-drawer aria-label="Закрыть">✕</button>
      </div>

      <!-- Секция Главное -->
      <div class="drawer-nav-section-title">Главное</div>
      ${mainItems.map(it => renderDrawerLink(it)).join('')}

      <!-- Секция Тренажёры и практика -->
      <div class="drawer-nav-section-title" style="margin-top:10px;">Тренажёры и практика</div>
      ${trainerItems.map(it => renderDrawerLink(it)).join('')}

      <!-- Секция Модули программы -->
      <div class="drawer-nav-section-title" style="margin-top:10px;">Модули курса</div>
      <details style="margin-bottom:12px;">
        <summary style="cursor:pointer;padding:8px 10px;font-size:0.82rem;font-weight:700;color:var(--ink-muted);border-radius:8px;background:var(--surface-2);border:1px solid var(--line);">
          <span>Показать ${moduleItems.length} модулей</span>
        </summary>
        <div style="padding-top:6px;display:flex;flex-direction:column;gap:4px;">
          ${moduleItems.map(it => renderDrawerLink(it, true)).join('')}
        </div>
      </details>

      <div style="flex:1 1 auto;"></div>

      <!-- Footer / Настройки -->
      <div style="border-top:1px solid var(--line);padding-top:12px;margin-top:10px;">
        <div style="display:flex;gap:6px;margin-bottom:8px;">
          <button type="button" class="btn btn-ghost" id="drawer-theme-btn" style="flex:1;font-size:0.78rem;padding:8px 6px;border-radius:10px;background:var(--surface-2);border:1px solid var(--line);">
            🌓 Тема
          </button>
          <button type="button" class="btn btn-ghost" id="drawer-lang-btn" style="flex:1;font-size:0.78rem;padding:8px 6px;border-radius:10px;background:var(--surface-2);border:1px solid var(--line);">
            🌐 ${lang === 'en' ? 'EN' : 'RU'}
          </button>
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between;padding:6px 8px;font-size:0.78rem;color:var(--ink-muted);background:var(--surface-2);border-radius:10px;margin-bottom:8px;border:1px solid var(--line);">
          <span>Стрик дней:</span>
          <span style="font-weight:700;color:var(--ink);">⚡ ${streak}</span>
        </div>
        <button type="button" class="btn btn-ghost" onclick="closeMobileDrawer(); openSettingsModal();" style="width:100%;font-size:0.80rem;padding:8px;border-radius:10px;background:var(--surface-2);border:1px solid var(--line);margin-bottom:4px;">
          ⚙️ Все настройки
        </button>
      </div>
    </div>
  `;
}
