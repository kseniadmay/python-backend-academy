import re

ACADEMY_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"
V1_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\full_screen_v1_airy.html"
SW_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\sw.js"
EXTRACTED_JS_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\scripts\extracted_academy.js"

def soften_dark_dots(path):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    # Смягчение неонового свечения точек в тёмной теме
    old_dark_done = """  .dot-jewel.done {
    background: #10b981;
    box-shadow: 0 0 8px rgba(16, 185, 129, 1), 0 0 16px rgba(16, 185, 129, 0.65), 0 0 26px rgba(16, 185, 129, 0.35);
  }
  .dot-jewel.active {
    width: 9px;
    height: 9px;
    background: #ffffff;
    box-shadow: 0 0 10px #ffffff, 0 0 22px rgba(255, 255, 255, 0.95), 0 0 38px rgba(255, 255, 255, 0.6);
    animation: radar-breathe-white 4.4s infinite ease-in-out;
  }"""

    new_dark_done = """  .dot-jewel.done {
    background: #10b981;
    box-shadow: 0 0 4px rgba(16, 185, 129, 0.5);
  }
  .dot-jewel.active {
    width: 7.5px;
    height: 7.5px;
    background: #ffffff;
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.8), 0 0 12px rgba(255, 255, 255, 0.35);
    animation: radar-breathe-white 4.4s infinite ease-in-out;
  }"""

    if old_dark_done in c:
        c = c.replace(old_dark_done, new_dark_done, 1)

    # Смягчение ряби ripple
    old_ripple = """  @keyframes radar-ripple-white {
    0% { width: 9px; height: 9px; opacity: 1; border-color: rgba(255, 255, 255, 0.9); }
    100% { width: 32px; height: 32px; opacity: 0; border-color: rgba(255, 255, 255, 0); }
  }"""

    new_ripple = """  @keyframes radar-ripple-white {
    0% { width: 7.5px; height: 7.5px; opacity: 0.8; border-color: rgba(255, 255, 255, 0.6); }
    100% { width: 18px; height: 18px; opacity: 0; border-color: rgba(255, 255, 255, 0); }
  }"""

    if old_ripple in c:
        c = c.replace(old_ripple, new_ripple, 1)

    # Смягчение breathe white
    old_breathe = """  @keyframes radar-breathe-white {
    0%, 100% {
      box-shadow: 0 0 8px #ffffff, 0 0 16px rgba(255, 255, 255, 0.75), 0 0 26px rgba(255, 255, 255, 0.4);
    }
    50% {
      box-shadow: 0 0 14px #ffffff, 0 0 28px rgba(255, 255, 255, 1), 0 0 46px rgba(255, 255, 255, 0.7);
    }
  }"""

    new_breathe = """  @keyframes radar-breathe-white {
    0%, 100% {
      box-shadow: 0 0 4px rgba(255, 255, 255, 0.7), 0 0 8px rgba(255, 255, 255, 0.25);
    }
    50% {
      box-shadow: 0 0 6px rgba(255, 255, 255, 0.9), 0 0 14px rgba(255, 255, 255, 0.4);
    }
  }"""

    if old_breathe in c:
        c = c.replace(old_breathe, new_breathe, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"Softened dark theme dots in {path}")

soften_dark_dots(ACADEMY_PATH)
soften_dark_dots(V1_PATH)

# Обновим версию sw.js до v31
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw = f.read()
sw = re.sub(r"const CACHE_NAME = 'academy-pwa-v\d+';", "const CACHE_NAME = 'academy-pwa-v31';", sw)
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw)
print("Updated sw.js to v31")

# Обновим extracted_academy.js
with open(ACADEMY_PATH, "r", encoding="utf-8") as f:
    html = f.read()
script_m = re.findall(r'<script\b[^>]*>([\s\S]*?)<\/script>', html)
if script_m:
    largest = max(script_m, key=len)
    with open(EXTRACTED_JS_PATH, "w", encoding="utf-8") as f:
        f.write(largest)
    print("Updated scripts/extracted_academy.js")
