import os
import subprocess
import json

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\2b320042-cd74-466b-b716-1ee73a7ff7f2"
academy_html = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"
mockup_dir = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups"

with open(academy_html, "r", encoding="utf-8") as f:
    orig_html = f.read()

# 1. Полноценная светлая версия ВСЕГО приложения (Сайдбар + Топбар + Рабочий стол + Пергамент)
# Чтобы приложение сразу отрендерилось в светлой теме со всем окружением, пропишем в HTML:
light_full_html = orig_html.replace(
    '<html lang="ru">',
    '<html lang="ru" data-theme="light">'
).replace(
    "state.theme = 'dark';",
    "state.theme = 'light';"
).replace(
    "effectiveDark() ? 'dark' : 'light'",
    "'light'"
)

light_full_path = os.path.join(mockup_dir, "full_screen_light_mirror.html")
with open(light_full_path, "w", encoding="utf-8") as f:
    f.write(light_full_html)

png_light_full = os.path.join(brain_dir, "full_screen_light_mirror.png")
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,960",
    f"--screenshot={png_light_full}",
    f"file:///{light_full_path.replace(os.sep, '/')}#/python/skill/1.1.1"
], check=True)
print("1. Saved full_screen_light_mirror.png")

# 2. Полноценная тёмная версия ВСЕГО приложения (Сайдбар + Топбар + Рабочий стол + Обсидиан)
png_dark_full = os.path.join(brain_dir, "full_screen_dark_applied.png")
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,960",
    f"--screenshot={png_dark_full}",
    f"file:///{academy_html.replace(os.sep, '/')}#/python/skill/1.1.1"
], check=True)
print("2. Saved full_screen_dark_applied.png")

# 3. Полноценная версия ВСЕГО приложения с зеркальным порядком строк:
# Строка 1: Тема (крупно вверху)
# Строка 2: Базовый синтаксис (деликатно внизу)
# Со ВСЕМ глобальным каркасом приложения (сайдбар, меню, топбар, плеер)!
inverted_eyebrow = """
  // Зеркальный порядок строк: Тема на первом плане, Юнит вторым рядом
  const eyebrowDotsHTML = `
    <div class="topic-eyebrow-track" style="max-width:780px;margin:14px auto 20px;">
      <div style="display:flex;flex-direction:column;gap:12px;width:100%;">
        <div style="display:flex;flex-direction:column;align-items:flex-start;padding-left:2px;gap:2px;">
          ${activeItemTitle ? `<div style="font-family:var(--font-d);font-size:1.20rem;font-weight:600;color:var(--ink);line-height:1.25;letter-spacing:-0.01em;">${escapeHtmlStr(activeItemTitle)}</div>` : ''}
          <div style="font-family:var(--font-b);font-size:0.80rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.02em;line-height:1.3;">${escapeHtmlStr(cleanUnitTitle)} · Юнит ${sk.unitId}</div>
        </div>
        <div style="display:flex;justify-content:center;width:100%;">
          ${dotsNecklaceHTML}
        </div>
      </div>
    </div>`;
"""

# Найдем eyebrowDotsHTML в коде viewPythonSkill и заменим его
pos_eyebrow = orig_html.find("const eyebrowDotsHTML = `")
pos_body = orig_html.find("let bodyHTML = '';", pos_eyebrow)

full_inverted_html = orig_html[:pos_eyebrow] + inverted_eyebrow.strip() + "\n\n  " + orig_html[pos_body:]

full_inverted_path = os.path.join(mockup_dir, "full_screen_mirror_rows.html")
with open(full_inverted_path, "w", encoding="utf-8") as f:
    f.write(full_inverted_html)

png_inverted_full = os.path.join(brain_dir, "full_screen_mirror_rows.png")
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,960",
    f"--screenshot={png_inverted_full}",
    f"file:///{full_inverted_path.replace(os.sep, '/')}#/python/skill/1.1.1"
], check=True)
print("3. Saved full_screen_mirror_rows.png")

# 4. Полноценная версия со светлой темой и зеркальным порядком строк
full_inverted_light_html = full_inverted_html.replace(
    '<html lang="ru">',
    '<html lang="ru" data-theme="light">'
).replace(
    "state.theme = 'dark';",
    "state.theme = 'light';"
).replace(
    "effectiveDark() ? 'dark' : 'light'",
    "'light'"
)
full_inverted_light_path = os.path.join(mockup_dir, "full_screen_mirror_rows_light.html")
with open(full_inverted_light_path, "w", encoding="utf-8") as f:
    f.write(full_inverted_light_html)

png_inverted_light_full = os.path.join(brain_dir, "full_screen_mirror_rows_light.png")
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,960",
    f"--screenshot={png_inverted_light_full}",
    f"file:///{full_inverted_light_path.replace(os.sep, '/')}#/python/skill/1.1.1"
], check=True)
print("4. Saved full_screen_mirror_rows_light.png")

print("All 4 full-screen captures finished!")
