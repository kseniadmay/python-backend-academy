import re

ACADEMY_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"
SW_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\sw.js"
EXTRACTED_JS_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\scripts\extracted_academy.js"

with open(ACADEMY_PATH, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Сдвиг левее и единый красивый стиль шрифта Golos Text (var(--font-b)) для обеих строк
target_eyebrow = """  const eyebrowDotsHTML = `
    <div class="topic-eyebrow-track" style="max-width:780px;margin:14px auto 20px;">
      <div style="display:flex;flex-direction:column;gap:12px;width:100%;">
        <div style="display:flex;flex-direction:column;align-items:flex-start;padding-left:2px;gap:2px;">
          <div style="font-family:var(--font-b);font-size:0.75rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.01em;line-height:1.2;">${escapeHtmlStr(cleanUnitTitle)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-d);font-size:0.98rem;font-weight:500;color:var(--ink-soft);line-height:1.35;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}
        </div>
        <div style="display:flex;justify-content:center;width:100%;">
          ${dotsNecklaceHTML}
        </div>
      </div>
    </div>`;"""

replacement_eyebrow = """  const eyebrowDotsHTML = `
    <div class="topic-eyebrow-track" style="max-width:100%;margin:16px 0 22px;padding:0 2px;">
      <div style="display:flex;flex-direction:column;gap:12px;width:100%;">
        <div style="display:flex;flex-direction:column;align-items:flex-start;gap:2px;">
          <div style="font-family:var(--font-b);font-size:0.80rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.01em;line-height:1.2;">${escapeHtmlStr(cleanUnitTitle)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-b);font-size:1.06rem;font-weight:600;color:var(--ink);line-height:1.35;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}
        </div>
        <div style="display:flex;justify-content:center;width:100%;">
          ${dotsNecklaceHTML}
        </div>
      </div>
    </div>`;"""

if target_eyebrow in c:
    c = c.replace(target_eyebrow, replacement_eyebrow, 1)
    print("Replaced eyebrow in academy.html")
else:
    print("Warning: target_eyebrow not found directly, trying regex...")
    c = re.sub(
        r'<div class="topic-eyebrow-track"[^>]*>[\s\S]*?<\/div>\s*<\/div>\s*<\/div>`;',
        replacement_eyebrow.strip(),
        c
    )
    print("Applied regex replacement")

with open(ACADEMY_PATH, "w", encoding="utf-8") as f:
    f.write(c)

# 2. Обновление sw.js к v32
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw = f.read()
sw = re.sub(r"const CACHE_NAME = 'academy-pwa-v\d+';", "const CACHE_NAME = 'academy-pwa-v32';", sw)
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw)
print("Updated sw.js to v32")

# 3. Обновление extracted_academy.js
script_m = re.findall(r'<script\b[^>]*>([\s\S]*?)<\/script>', c)
if script_m:
    largest = max(script_m, key=len)
    with open(EXTRACTED_JS_PATH, "w", encoding="utf-8") as f:
        f.write(largest)
    print("Updated scripts/extracted_academy.js")
