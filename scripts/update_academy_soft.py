import re

ACADEMY_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"
MIRROR_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\full_screen_light_mirror.html"
SW_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\sw.js"
EXTRACTED_JS_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\scripts\extracted_academy.js"

def update_file(path):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Смягчение стилей точек в светлой теме
    old_light_dots = """:root[data-theme="light"] .dot-jewel {
    background: rgba(15, 23, 42, 0.12);
    border: 1.5px solid rgba(15, 23, 42, 0.22);
  }
  :root[data-theme="light"] .dot-jewel:hover {
    background: rgba(15, 23, 42, 0.35);
  }
  :root[data-theme="light"] .dot-jewel.done {
    background: #10b981;
    border-color: #059669;
    box-shadow: 0 0 5px rgba(16, 185, 129, 0.4);
  }
  :root[data-theme="light"] .dot-jewel.active {
    background: #ffffff !important;
    border-color: #ffffff !important;
    box-shadow: 0 0 0 2px #0f172a, 0 0 10px rgba(255, 255, 255, 0.9) !important;
  }
  :root[data-theme="light"] .dots-stage-divider {
    background: rgba(15, 23, 42, 0.2);
  }
  :root[data-theme="light"] .dot-jewel.milestone {
    background: rgba(217, 119, 6, 0.2);
    border-color: var(--amber);
  }
  :root[data-theme="light"] .dot-jewel.milestone.active {
    background: #ffffff !important;
    border-color: #ffffff !important;
    box-shadow: 0 0 0 2px var(--amber), 0 0 10px rgba(255, 255, 255, 0.9) !important;
  }"""

    new_light_dots = """:root[data-theme="light"] .dot-jewel {
    background: rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(15, 23, 42, 0.12);
  }
  :root[data-theme="light"] .dot-jewel:hover {
    background: rgba(15, 23, 42, 0.22);
    transform: scale(1.3);
  }
  :root[data-theme="light"] .dot-jewel.done {
    background: rgba(16, 185, 129, 0.7);
    border: 1px solid rgba(5, 150, 105, 0.4);
    box-shadow: 0 0 3px rgba(16, 185, 129, 0.25);
  }
  :root[data-theme="light"] .dot-jewel.active {
    width: 7.5px;
    height: 7.5px;
    background: #ffffff !important;
    border: 1.5px solid rgba(20, 90, 70, 0.45) !important;
    box-shadow: 0 0 0 2px rgba(20, 90, 70, 0.18), 0 1px 3px rgba(15, 23, 42, 0.06) !important;
  }
  :root[data-theme="light"] .dots-stage-divider {
    width: 1px;
    height: 6px;
    background: rgba(15, 23, 42, 0.12);
    margin: 0 4px;
  }
  :root[data-theme="light"] .dot-jewel.milestone {
    background: rgba(217, 119, 6, 0.15);
    border: 1px solid rgba(217, 119, 6, 0.35);
  }
  :root[data-theme="light"] .dot-jewel.milestone.active {
    width: 7.5px;
    height: 7.5px;
    background: #ffffff !important;
    border: 1.5px solid rgba(217, 119, 6, 0.5) !important;
    box-shadow: 0 0 0 2px rgba(217, 119, 6, 0.2), 0 1px 3px rgba(15, 23, 42, 0.06) !important;
  }"""

    if old_light_dots in c:
        c = c.replace(old_light_dots, new_light_dots, 1)

    # 2. Обновление типографики заголовка в JS
    old_eyebrow = """          <div style="font-family:var(--font-b);font-size:0.82rem;font-weight:600;color:var(--ink-muted);letter-spacing:0.04em;text-transform:uppercase;line-height:1.2;">${escapeHtmlStr(cleanUnitTitle)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-d);font-size:1.15rem;font-weight:600;color:var(--ink);line-height:1.3;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}"""

    new_eyebrow = """          <div style="font-family:var(--font-b);font-size:0.75rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.01em;line-height:1.2;">${escapeHtmlStr(cleanUnitTitle)}</div>
          ${activeItemTitle ? `<div style="font-family:var(--font-d);font-size:0.98rem;font-weight:500;color:var(--ink-soft);line-height:1.35;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}"""

    if old_eyebrow in c:
        c = c.replace(old_eyebrow, new_eyebrow, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"Updated {path}")

update_file(ACADEMY_PATH)
update_file(MIRROR_PATH)

# Обновим версию sw.js до v30
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw = f.read()
sw = re.sub(r"const CACHE_NAME = 'academy-pwa-v\d+';", "const CACHE_NAME = 'academy-pwa-v30';", sw)
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw)
print("Updated sw.js to v30")

# Обновим extracted_academy.js
with open(ACADEMY_PATH, "r", encoding="utf-8") as f:
    html = f.read()
script_m = re.findall(r'<script\b[^>]*>([\s\S]*?)<\/script>', html)
if script_m:
    largest = max(script_m, key=len)
    with open(EXTRACTED_JS_PATH, "w", encoding="utf-8") as f:
        f.write(largest)
    print("Updated scripts/extracted_academy.js")
