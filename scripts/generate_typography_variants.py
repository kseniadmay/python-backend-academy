import os
import subprocess

mockup_dir = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\2b320042-cd74-466b-b716-1ee73a7ff7f2"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Точные данные по всем 18 точкам
items = [
    # Конспекты
    {"type": "theory", "id": "К-001", "title": "Структуры данных Python: list, dict, set", "badge": "Конспект К-001", "done": True},
    {"type": "theory", "id": "К-002", "title": "list vs tuple: когда что выбрать", "badge": "Конспект К-002", "done": True},
    {"type": "theory", "id": "К-003", "title": "Срезы в Python: slice и синтаксис [start:stop:step]", "badge": "Конспект К-003", "done": True},
    # Карточки
    {"type": "cards", "id": "Ф-001", "title": "list comprehension, dict comprehension и set", "badge": "Колода Ф-001 · 19 карт", "done": False, "active": True},
    {"type": "cards", "id": "Ф-002", "title": "Методы проверки вхождения подмножества", "badge": "Колода Ф-002 · 12 карт", "done": False},
    {"type": "cards", "id": "Ф-003", "title": "Отрицательные индексы", "badge": "Колода Ф-003 · 9 карт", "done": False},
    {"type": "cards", "id": "Ф-004", "title": "Последовательности", "badge": "Колода Ф-004 · 10 карт", "done": False},
    {"type": "cards", "id": "Ф-005", "title": "Список vs. кортеж", "badge": "Колода Ф-005 · 18 карт", "done": False},
    {"type": "cards", "id": "Ф-006", "title": "Срезы", "badge": "Колода Ф-006 · 24 карт", "done": False},
    {"type": "cards", "id": "Ф-007", "title": "Строковые методы split() и join()", "badge": "Колода Ф-007 · 16 карт", "done": False},
    {"type": "cards", "id": "Ф-008", "title": "Типы данных ключей словаря", "badge": "Колода Ф-008 · 10 карт", "done": False},
    {"type": "cards", "id": "Ф-009", "title": "Сложность: основные операции для list, dict, set", "badge": "Колода Ф-009 · 34 карт", "done": False},
    # Задачи практики
    {"type": "code", "id": "20", "title": "Разворот списка срезом [::-1]", "badge": "Задача #20 · Уровень 1", "done": False},
    {"type": "code", "id": "19", "title": "Главная диагональ матрицы 3x3", "badge": "Задача #19 · Уровень 1", "done": False},
    {"type": "code", "id": "39", "title": "Получите подстроку по отрицательным индексам", "badge": "Задача #39 · Уровень 1", "done": False},
    {"type": "code", "id": "255", "title": "Извлеките подсписок первых трёх и последних двух элементов через срез", "badge": "Задача #255 · Уровень 1", "done": False},
    {"type": "code", "id": "258", "title": "Создайте кортеж и список с одинаковым содержимым и сравните их возможности", "badge": "Задача #258 · Уровень 2", "done": False},
    # Рубежный зачёт
    {"type": "exam", "id": "1.1", "title": "Рубежный зачёт Юнита 1.1 (Базовый синтаксис)", "badge": "Рубежный Unit Test 1.1", "done": False, "isExam": True}
]

def generate_dots_html():
    h = []
    # 1. Конспекты
    for i in range(3):
        it = items[i]
        cls = "dot-jewel done" if it.get("done") else "dot-jewel"
        h.append(f'<span class="{cls}" data-idx="{i}" title="📖 {it["id"]}: {it["title"]}"></span>')
    h.append('<span class="dots-stage-divider" title="Переход к карточкам"></span>')
    # 2. Карточки
    for i in range(3, 12):
        it = items[i]
        cls = "dot-jewel active" if it.get("active") else ("dot-jewel done" if it.get("done") else "dot-jewel")
        h.append(f'<span class="{cls}" data-idx="{i}" title="🗂️ {it["id"]}: {it["title"]}"></span>')
    h.append('<span class="dots-stage-divider" title="Переход к практике"></span>')
    # 3. Задачи практики
    for i in range(12, 17):
        it = items[i]
        cls = "dot-jewel done" if it.get("done") else "dot-jewel"
        h.append(f'<span class="{cls}" data-idx="{i}" title="⚡ Задача #{it["id"]}: {it["title"]}"></span>')
    h.append('<span class="dots-stage-divider" title="Рубежный зачёт"></span>')
    # 4. Зачёт
    it = items[17]
    h.append(f'<span class="dot-jewel milestone" data-idx="17" title="👑 {it["title"]}"></span>')
    return "".join(h)

dots_html = generate_dots_html()

def build_page(variant_id, variant_name, header_html):
    return f"""<!DOCTYPE html>
<html lang="ru" data-theme="light">
<head>
  <meta charset="UTF-8">
  <title>Вариант {variant_id} — {variant_name}</title>
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
      justify-content: center;
      gap: 8.5px;
      padding: 6px 0;
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
      position: relative;
    }}
    .dot-jewel:hover {{
      transform: scale(1.35);
      border-color: var(--ink);
    }}
    .dot-jewel.done {{
      background: #10b981;
      border-color: #059669;
      box-shadow: 0 0 5px rgba(16, 185, 129, 0.4);
    }}
    .dot-jewel.active {{
      background: #ffffff !important;
      border-color: #ffffff !important;
      box-shadow: 0 0 0 2px #0f172a, 0 0 10px rgba(255, 255, 255, 0.9) !important;
      transform: scale(1.35);
    }}
    .dot-jewel.milestone {{
      width: 12px;
      height: 12px;
      border-radius: 2px;
      transform: rotate(45deg);
      background: rgba(217, 119, 6, 0.2);
      border-color: var(--amber);
    }}
    .dot-jewel.milestone.active {{
      background: #ffffff !important;
      border-color: #ffffff !important;
      box-shadow: 0 0 0 2px var(--amber), 0 0 10px rgba(255, 255, 255, 0.9) !important;
      transform: rotate(45deg) scale(1.35);
    }}
    .dots-stage-divider {{
      width: 1px;
      height: 14px;
      background: rgba(15, 23, 42, 0.2);
      margin: 0 3px;
    }}
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
    .card-q-box {{
      font-size: 1.15rem;
      font-weight: 600;
      line-height: 1.5;
      color: var(--ink);
      min-height: 80px;
    }}
    .card-meta-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 14px;
      border-top: 1px solid var(--hairline);
      font-size: 0.82rem;
      color: var(--ink-muted);
    }}
    .stage-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 3px 10px;
      background: rgba(15, 23, 42, 0.05);
      border-radius: 999px;
      font-size: 0.76rem;
      font-weight: 600;
      color: var(--ink-soft);
    }}
  </style>
</head>
<body>

  <div class="variant-header-badge">
    <span>💎 ТЕСТОВЫЙ ПРОТОТИП</span> · <span>ВАРИАНТ {variant_id}: {variant_name}</span>
  </div>

  <div class="main-wrap">
    <!-- Топбар -->
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

    <!-- Заголовок и трекер -->
    <div class="topic-eyebrow-track" style="margin: 10px 0 16px;">
      <div style="display:flex;flex-direction:column;gap:14px;width:100%;">
        {header_html}
        <div style="display:flex;justify-content:center;width:100%;">
          <div class="dots-necklace" id="dots-wrap">
            {dots_html}
          </div>
        </div>
      </div>
    </div>

    <!-- Карточка активного элемента -->
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
        if (descEl) {{
          if (it.type === 'theory') {{
            descEl.textContent = "Конспект: " + it.title + ". Чтение структурированных шагов теории и фундаментальных понятий Python.";
          }} else if (it.type === 'cards') {{
            descEl.textContent = "Карточка колоды: " + it.title + ". Проверка интервального повторения и глубокого понимания.";
          }} else if (it.type === 'code') {{
            descEl.textContent = "Практическая задача в IDE: " + it.title + ". Напишите чистый код с соблюдением всех тестов.";
          }} else {{
            descEl.textContent = "Рубежный зачёт (Unit Test 1.1): Комплексная проверка всех навыков юнита Базовый синтаксис.";
          }}
        }}
      }});
    }});
  </script>
</body>
</html>
"""

# Вариант 1.A: Деликатная надрубрика (Refined Eyebrow)
# Базовый синтаксис — благородный мелкий трекинговый заголовок рубрики, а активная тема — выразительный элегантный фокус
header_1a = """
        <div style="display:flex;flex-direction:column;align-items:flex-start;padding-left:2px;gap:2px;">
          <div style="font-family:var(--font-b);font-size:0.82rem;font-weight:600;color:var(--ink-muted);letter-spacing:0.04em;text-transform:uppercase;line-height:1.2;">Базовый синтаксис</div>
          <div id="active-title" style="font-family:var(--font-d);font-size:1.15rem;font-weight:600;color:var(--ink);line-height:1.3;letter-spacing:-0.01em;">list comprehension, dict comprehension и set</div>
        </div>
"""

# Вариант 1.B: Мягкая гармония (Soft Harmony Regular)
# Базовый синтаксис — нормальной плотности (не кричащий, без 700), мягкого серого оттенка, тема — аккуратный черничный сабтитл
header_1b = """
        <div style="display:flex;flex-direction:column;align-items:flex-start;padding-left:2px;gap:4px;">
          <div style="font-family:var(--font-b);font-size:0.95rem;font-weight:500;color:var(--ink-soft);line-height:1.25;">Базовый синтаксис</div>
          <div id="active-title" style="font-family:var(--font-b);font-size:0.88rem;font-weight:600;color:var(--ink);line-height:1.35;">list comprehension, dict comprehension и set</div>
        </div>
"""

# Вариант 1.C: Эфемерная капсула (Ephemeral Pill Badge)
# Базовый синтаксис вынесен в аккуратную ненавязчивую плашку-пилюлю, полностью снимая давление со шрифта
header_1c = """
        <div style="display:flex;flex-direction:column;align-items:flex-start;padding-left:2px;gap:6px;">
          <div style="display:inline-flex;align-items:center;padding:2px 10px;background:rgba(0,0,0,0.04);border:1px solid rgba(0,0,0,0.08);border-radius:999px;font-family:var(--font-b);font-size:0.76rem;font-weight:500;color:var(--ink-soft);letter-spacing:0.01em;">
            Базовый синтаксис
          </div>
          <div id="active-title" style="font-family:var(--font-b);font-size:1.02rem;font-weight:600;color:var(--ink);line-height:1.3;">list comprehension, dict comprehension и set</div>
        </div>
"""

variants = [
    ("1A", "Деликатная надрубрика (Refined Eyebrow)", header_1a, "variant_1a_refined_eyebrow.html", "variant_1a_refined_eyebrow.png"),
    ("1B", "Мягкая гармония (Soft Harmony Regular)", header_1b, "variant_1b_soft_harmony.html", "variant_1b_soft_harmony.png"),
    ("1C", "Эфемерная капсула (Ephemeral Pill Badge)", header_1c, "variant_1c_ephemeral_pill.html", "variant_1c_ephemeral_pill.png")
]

for vid, vname, hhtml, fname, pngname in variants:
    fpath = os.path.join(mockup_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(build_page(vid, vname, hhtml))
    print(f"Created HTML: {fname}")

    png_path = os.path.join(brain_dir, pngname)
    subprocess.run([
        chrome_path,
        "--headless=new", "--disable-gpu", "--window-size=1080,720",
        f"--screenshot={png_path}",
        f"file:///{fpath.replace(os.sep, '/')}"
    ], check=True)
    print(f"Saved screenshot: {pngname}")

print("All variants created and screenshotted successfully!")
