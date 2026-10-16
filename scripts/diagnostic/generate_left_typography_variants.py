import re

with open('academy.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

# Подготовим скрипт генерации вариантов с левым выравниванием и единым стилем шрифта
# Вариант A: Единый чистый премиальный стиль Golos Text (var(--font-b))
html_golos = base_html.replace(
    'max-width:780px;margin:14px auto 20px;',
    'max-width:100%;margin:16px 0 22px;padding:0 2px;'
).replace(
    '''          <div style="font-family:var(--font-b);font-size:0.75rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.01em;line-height:1.2;">${escapeHtmlStr(cleanUnitTitle)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-d);font-size:0.98rem;font-weight:500;color:var(--ink-soft);line-height:1.35;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}''',
    '''          <div style="font-family:var(--font-b);font-size:0.80rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.01em;line-height:1.2;">${escapeHtmlStr(cleanUnitTitle)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-b);font-size:1.06rem;font-weight:600;color:var(--ink);line-height:1.35;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}'''
)

# Вариант B: Единый акцидентный стиль Unbounded (var(--font-d))
html_unbounded = base_html.replace(
    'max-width:780px;margin:14px auto 20px;',
    'max-width:100%;margin:16px 0 22px;padding:0 2px;'
).replace(
    '''          <div style="font-family:var(--font-b);font-size:0.75rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.01em;line-height:1.2;">${escapeHtmlStr(cleanUnitTitle)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-d);font-size:0.98rem;font-weight:500;color:var(--ink-soft);line-height:1.35;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}''',
    '''          <div style="font-family:var(--font-d);font-size:0.74rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.03em;line-height:1.2;">${escapeHtmlStr(cleanUnitTitle)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-d);font-size:0.98rem;font-weight:600;color:var(--ink);line-height:1.35;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}'''
)

with open('design_mockups/test_left_golos.html', 'w', encoding='utf-8') as f:
    f.write(html_golos)

with open('design_mockups/test_left_unbounded.html', 'w', encoding='utf-8') as f:
    f.write(html_unbounded)

print("Created test_left_golos.html and test_left_unbounded.html")
