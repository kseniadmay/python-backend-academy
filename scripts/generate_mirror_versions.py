import os
import subprocess
import time

mockup_dir = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\2b320042-cd74-466b-b716-1ee73a7ff7f2"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
academy_html = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"

# 1. Снимок боевого academy.html в СВЕТЛОЙ ТЕМЕ
# Создадим обертку для открытия academy.html со светлой темой
light_wrapper_path = os.path.join(mockup_dir, "academy_light_capture.html")
with open(light_wrapper_path, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <script>
    localStorage.setItem('theme', 'light');
    window.location.replace('../academy.html#/python/skill/1.1.1');
  </script>
</head>
<body></body>
</html>
""")

light_png = os.path.join(brain_dir, "live_skill_111_light_mirror.png")
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1200,900",
    f"--screenshot={light_png}",
    f"file:///{light_wrapper_path.replace(os.sep, '/')}"
], check=True)
print("Saved light mirror screenshot:", light_png)

# 2. Создадим прототип «Зеркальный порядок строк» (Тема крупно сверху, Базовый синтаксис деликатно снизу)
proto_inverted_rows = os.path.join(mockup_dir, "mirror_inverted_rows.html")
inverted_header = """
        <div style="display:flex;flex-direction:column;align-items:flex-start;padding-left:2px;gap:2px;">
          <div id="active-title" style="font-family:var(--font-d);font-size:1.20rem;font-weight:600;color:var(--ink);line-height:1.25;letter-spacing:-0.01em;">list comprehension, dict comprehension и set</div>
          <div style="font-family:var(--font-b);font-size:0.80rem;font-weight:500;color:var(--ink-muted);letter-spacing:0.02em;line-height:1.3;">Базовый синтаксис · Юнит 1.1</div>
        </div>
"""

# 3. Создадим прототип «Горизонтальное зеркало» (Заголовок слева, трекер точек справа в одной строке)
proto_hsplit = os.path.join(mockup_dir, "mirror_horizontal_split.html")
hsplit_header = """
        <div style="display:flex;justify-content:space-between;align-items:flex-end;width:100%;gap:16px;flex-wrap:wrap;">
          <div style="display:flex;flex-direction:column;align-items:flex-start;padding-left:2px;gap:2px;">
            <div style="font-family:var(--font-b);font-size:0.82rem;font-weight:600;color:var(--ink-muted);letter-spacing:0.04em;text-transform:uppercase;line-height:1.2;">Базовый синтаксис</div>
            <div id="active-title" style="font-family:var(--font-d);font-size:1.15rem;font-weight:600;color:var(--ink);line-height:1.3;letter-spacing:-0.01em;">list comprehension, dict comprehension и set</div>
          </div>
          <div style="display:flex;align-items:center;padding-bottom:2px;">
            <div class="dots-necklace" id="dots-wrap">
              {dots_html}
            </div>
          </div>
        </div>
"""

# Функция генерации страниц
from generate_typography_variants import build_page, dots_html, items

# Вариант 1: Зеркальный порядок строк (Инверсия вертикальная)
page_inv = build_page("2A", "Зеркальный порядок строк (Тема вверху, Юнит внизу)", inverted_header)
with open(proto_inverted_rows, "w", encoding="utf-8") as f:
    f.write(page_inv)

png_inv = os.path.join(brain_dir, "mirror_inverted_rows.png")
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1080,720",
    f"--screenshot={png_inv}",
    f"file:///{proto_inverted_rows.replace(os.sep, '/')}"
], check=True)
print("Saved mirror inverted rows screenshot:", png_inv)

# Вариант 2: Горизонтальный сплит (Слева двухстрочный заголовок, Справа трекер точек)
page_hsplit_content = f"""<!DOCTYPE html>
<html lang="ru" data-theme="light">
<head>
  <meta charset="UTF-8">
  <title>Зеркальная версия: Горизонтальный сплит</title>
  <style>
    :root {{
      --bg: #faf8f5;
      --surface: rgba(255, 255, 255, 0.72);
      --ink: #0f172a;
      --ink-soft: #334155;
      --ink-muted: #64748b;
      --emerald: #145a46;
      --amber: #d97706;
      --bordeaux: #6b1d2f;
      --hairline: rgba(0, 0, 0, 0.08);
      --font-d: "Newsreader", Georgia, serif;
      --font-b: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-m: "JetBrains Mono", Consolas, monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--ink);
      font-family: var(--font-b);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 30px 20px;
    }}
    .variant-header-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      background: rgba(20, 90, 70, 0.08);
      border: 1px solid rgba(20, 90, 70, 0.2);
      border-radius: 999px;
      color: var(--emerald);
      font-size: 0.80rem;
      font-weight: 600;
      margin-bottom: 24px;
    }}
    .main-wrap {{
      width: 100%;
      max-width: 820px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .topbar-preview {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 18px;
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(16px);
      border: 1px solid var(--hairline);
      border-radius: 14px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
    }}
    .dots-necklace {{
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 8px;
      padding: 4px 0;
      position: relative;
    }}
    .dot-jewel {{
      width: 11px;
      height: 11px;
      border-radius: 50%;
      background: rgba(15, 23, 42, 0.14);
      border: 1.5px solid rgba(15, 23, 42, 0.25);
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .dot-jewel:hover {{ transform: scale(1.35); border-color: var(--ink); }}
    .dot-jewel.done {{ background: #10b981; border-color: #059669; box-shadow: 0 0 5px rgba(16, 185, 129, 0.4); }}
    .dot-jewel.active {{ background: #ffffff !important; border-color: #ffffff !important; box-shadow: 0 0 0 2px #0f172a, 0 0 10px rgba(255, 255, 255, 0.9) !important; transform: scale(1.35); }}
    .dot-jewel.milestone {{ width: 12px; height: 12px; border-radius: 2px; transform: rotate(45deg); background: rgba(217, 119, 6, 0.2); border-color: var(--amber); }}
    .dot-jewel.milestone.active {{ background: #ffffff !important; border-color: #ffffff !important; box-shadow: 0 0 0 2px var(--amber), 0 0 10px rgba(255, 255, 255, 0.9) !important; transform: rotate(45deg) scale(1.35); }}
    .dots-stage-divider {{ width: 1px; height: 14px; background: rgba(15, 23, 42, 0.2); margin: 0 3px; }}
    .card-preview {{
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(16px);
      border: 1px solid var(--hairline);
      border-radius: 18px;
      padding: 30px 32px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .card-q-box {{ font-size: 1.15rem; font-weight: 600; line-height: 1.5; color: var(--ink); min-height: 80px; }}
    .card-meta-row {{ display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid var(--hairline); font-size: 0.82rem; color: var(--ink-muted); }}
    .stage-pill {{ display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px; background: rgba(15, 23, 42, 0.05); border-radius: 999px; font-size: 0.76rem; font-weight: 600; color: var(--ink-soft); }}
  </style>
</head>
<body>

  <div class="variant-header-badge">
    <span>💎 ТЕСТОВЫЙ ПРОТОТИП</span> · <span>ГОРИЗОНТАЛЬНОЕ ЗЕРКАЛО (Слева заголовок, Справа трекер)</span>
  </div>

  <div class="main-wrap">
    <div class="topbar-preview">
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="color:var(--bordeaux);font-weight:800;font-size:0.80rem;">Эшелон 1</span>
        <span style="color:var(--ink-muted);opacity:0.6;">·</span>
        <span style="color:var(--emerald);font-weight:600;font-size:0.80rem;">35% готовности к скринингу</span>
      </div>
      <div style="display:inline-flex;align-items:center;padding:4px 10px;border-radius:999px;background:rgba(245,158,11,0.14);border:1px solid rgba(245,158,11,0.35);color:#b45309;font-size:0.75rem;font-weight:700;">
        ⚡ +55 XP за сутки
      </div>
    </div>

    <!-- Заголовок слева, трекер справа -->
    <div class="topic-eyebrow-track" style="margin: 14px 0 16px;">
      <div style="display:flex;justify-content:space-between;align-items:flex-end;width:100%;gap:16px;">
        <div style="display:flex;flex-direction:column;align-items:flex-start;padding-left:2px;gap:2px;">
          <div style="font-family:var(--font-b);font-size:0.82rem;font-weight:600;color:var(--ink-muted);letter-spacing:0.04em;text-transform:uppercase;line-height:1.2;">Базовый синтаксис</div>
          <div id="active-title" style="font-family:var(--font-d);font-size:1.15rem;font-weight:600;color:var(--ink);line-height:1.3;letter-spacing:-0.01em;">list comprehension, dict comprehension и set</div>
        </div>
        <div style="display:flex;align-items:center;padding-bottom:2px;flex:none;">
          <div class="dots-necklace" id="dots-wrap">
            {dots_html}
          </div>
        </div>
      </div>
    </div>

    <div class="card-preview">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span class="stage-pill" id="item-badge">Колода Ф-001 · 19 карт</span>
        <span style="font-size:0.82rem;color:var(--ink-muted);">Карточка 1 из 19</span>
      </div>
      <div class="card-q-box" id="item-desc">
        В чём разница между списковым включением (list comprehension) и генераторным выражением в плане потребления памяти и скорости?
      </div>
      <div class="card-meta-row">
        <span>Нажмите Пробел или карточку для ответа</span>
        <span style="font-family:var(--font-m);font-size:0.75rem;">Точка #4 / 18</span>
      </div>
    </div>
  </div>

  <script>
    const items = {items};
    const titleEl = document.getElementById('active-title');
    const badgeEl = document.getElementById('item-badge');
    const descEl = document.getElementById('item-desc');
    const dots = document.querySelectorAll('.dot-jewel');

    dots.forEach((dot, idx) => {{
      dot.addEventListener('click', () => {{
        dots.forEach(d => d.classList.remove('active'));
        dot.classList.add('active');
        const it = items[idx];
        if (titleEl) titleEl.textContent = it.title;
        if (badgeEl) badgeEl.textContent = it.badge;
      }});
    }});
  </script>
</body>
</html>
"""

with open(proto_hsplit, "w", encoding="utf-8") as f:
    f.write(page_hsplit_content)

png_hsplit = os.path.join(brain_dir, "mirror_horizontal_split.png")
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1080,720",
    f"--screenshot={png_hsplit}",
    f"file:///{proto_hsplit.replace(os.sep, '/')}"
], check=True)
print("Saved horizontal split screenshot:", png_hsplit)

print("All mirror captures completed successfully!")
