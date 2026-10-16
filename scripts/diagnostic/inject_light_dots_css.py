import re

ACADEMY_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"
APPLY_SCRIPT = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\scripts\apply_final_unified_dots.py"

light_dots_css = """
  /* Точки трекера для Светлой темы (Пергамент) */
  :root[data-theme="light"] .dot-jewel {
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
  }
"""

for path in [ACADEMY_PATH, APPLY_SCRIPT]:
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    if ":root[data-theme=\"light\"] .dot-jewel" not in code:
        # inject after .dot-jewel.milestone:hover
        target = ".dot-jewel.milestone:hover {"
        idx = code.find(target)
        if idx != -1:
            end_idx = code.find("}", idx) + 1
            code = code[:end_idx] + "\n" + light_dots_css + "\n" + code[end_idx:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"Injected light dots CSS into {path}")

print("Done updating CSS for light mode dots!")
