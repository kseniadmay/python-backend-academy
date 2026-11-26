import os, re, glob, json
from extract_remnote_data import BASE_REMNOTE, TASKS_381, k_files_map, f_files_map, parse_k_note, parse_f_deck, md_inline

with open(os.path.join(BASE_REMNOTE, '00 · 🗺️ Карта Мастерства.md'), encoding='utf-8') as f:
    karta = f.read()

hr_m = re.search(r'## 📁 00 ·[^\n]*([\s\S]*?)(?=## 📁 01 ·)', karta)
mod0_hr_text = hr_m.group(1) if hr_m else ''
mod1_text = re.search(r'## 📁 01 · 🐍 Python(.*?)(?=## 📁 02 ·)', karta, re.S).group(1)
mod2_web_text = re.search(r'## 📁 02 · 🌐 Web\b(.*?)(?=## 📁 03 · ⚙️ Backend)', karta, re.S).group(1)
mod3_backend_text = re.search(r'## 📁 03 · ⚙️ Backend(.*?)(?=## 📁 04 ·)', karta, re.S).group(1)
mod4_algo_text = re.search(r'## 📁 04 · ⚡ Алгоритмы(.*?)(?=## 📁 05 ·)', karta, re.S).group(1)
mod5_db_text = re.search(r'## 📁 05 · 🗄️ Базы данных(.*?)(?=## 📁 06 ·)', karta, re.S).group(1)
mod6_arch_text = re.search(r'## 📁 06 · 🏛️ Архитектура(.*?)(?=## 📁 07 ·)', karta, re.S).group(1)
mod7_infra_text = re.search(r'## 📁 07 · 🚀 Инфраструктура(.*)', karta, re.S).group(1)

# Extra K and F attachments so 100% of files in 01 · 🐍 Python are linked
EXTRA_K_BY_SKILL = {
    '1.3.1': ['К-218'], # itertools
    '1.3.3': ['К-217'], # contextlib
    '1.6.1': ['К-219'], # enum
    '1.9.1': ['К-222'], # pathlib
    '1.9.2': ['К-221'], # imports, __all__
    '1.9.3': ['К-220', 'К-223'], # logging, pytest, fixtures, mock
}

EXTRA_F_BY_SKILL = {
    '1.1.1': ['Ф-079', 'Ф-080', 'Ф-084', 'Ф-085'],
    '1.9.2': ['Ф-078', 'Ф-257'],
}

EXPLICIT_DECKS_BY_SKILL = {
    '1.9.1': ['Ф-081', 'Ф-082', 'Ф-083', 'Ф-252', 'Ф-253', 'Ф-255'],
}

# Explicit mapping of Python, Web, Backend, Algorithms, Databases, Architecture, and Infrastructure skills to their best matching IDE task IDs from TASKS_381
SKILL_TASK_IDS = {
    # 01 · 🐍 Python (28 skills)
    '1.1.1': [20, 19, 39, 255, 258],
    '1.1.2': [253, 257, 263, 264],
    '1.1.3': [18, 72, 286, 297],
    '1.1.4': [296, 298, 301, 302],
    '1.1.5': [299, 300, 304, 305],
    '1.2.1': [66, 256, 323, 325],
    '1.2.2': [38, 93, 197, 270, 310, 313, 314, 315],
    '1.2.3': [110, 135, 262, 309, 322, 324, 326],
    '1.3.1': [265, 374, 375, 376, 377, 378, 379, 380],
    '1.3.2': [217, 266, 327, 328, 381],
    '1.3.3': [162, 331, 367, 369, 370, 373],
    '1.4.1': [151, 245, 341, 343, 345],
    '1.4.2': [9, 177, 290, 303, 317, 318, 344],
    '1.4.3': [306, 307, 308, 316, 342],
    '1.5.1': [23, 181, 233, 235, 237, 238, 240, 241, 243, 246, 251, 329],
    '1.5.2': [81, 247, 248, 249, 250, 252, 333, 348],
    '1.5.3': [92, 350],
    '1.6.1': [26, 234, 236, 239, 242, 244, 330, 368, 369],
    '1.6.2': [37, 43, 67, 268, 275, 319, 320, 321, 347, 382, 383],
    '1.7.1': [254, 259, 271, 332, 346],
    '1.7.2': [267, 311],
    '1.7.3': [312],
    '1.8.1': [273, 334, 387, 398, 399],
    '1.8.2': [40, 282, 284, 285, 288, 289, 292, 294, 338, 349],
    '1.8.3': [74, 277, 278, 336, 396, 397, 400],
    '1.9.1': [260, 261, 274, 280, 283, 287, 295, 335, 337, 366, 371, 372],
    '1.9.2': [291, 339, 340],
    '1.9.3': [10, 28, 68, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 388, 389],

    # 02 · 🌐 Web (10 skills, Units 2.1–2.4)
    '2.1.1': [2, 95, 186],
    '2.1.2': [6, 95, 186, 272, 279],
    '2.2.1': [2, 6, 74, 186],
    '2.2.2': [48, 50, 90],
    '2.2.3': [396, 397, 399],
    '2.3.1': [6, 118, 383],
    '2.3.2': [33, 142, 386],
    '2.3.3': [209, 384, 385, 386],
    '2.4.1': [90, 144, 225],
    '2.4.2': [22, 32, 395],

    # 03 · ⚙️ Backend (24 skills, Units 3.1–3.8)
    # Часть I — FastAPI и Pydantic v2
    '3.1.1': [33, 67, 382, 383],
    '3.1.2': [53, 78, 99, 216, 388],
    '3.1.3': [122, 142, 158, 397, 398, 399],
    # Часть II — Django и ORM
    '3.2.1': [44, 47, 57, 194],
    '3.2.2': [7, 104, 200, 396],
    '3.2.3': [47, 57, 194, 200],
    # Часть III — Django REST Framework (DRF)
    '3.3.1': [83, 143, 382, 383],
    '3.3.2': [83, 143, 209, 385],
    '3.3.3': [143, 172, 209, 385, 386],
    # Часть IV — Микрофреймворк Flask
    '3.4.1': [6, 33, 400],
    '3.4.2': [216, 370, 400],
    '3.4.3': [53, 142, 400],
    # Часть V — Аутентификация, авторизация и криптозащита
    '3.5.1': [112, 127, 184, 393],
    '3.5.2': [50, 90, 174, 392],
    '3.5.3': [103, 148, 172, 389, 394],
    # Часть VI — Слоистая архитектура, транзакции и кэширование
    '3.6.1': [25, 54, 56, 116, 133, 157, 206, 231],
    '3.6.2': [11, 51, 106, 149, 195, 213, 230],
    '3.6.3': [27, 70, 86, 123, 160, 171, 201],
    # Часть VII — Отказоустойчивые интеграции, очереди и Rate Limiting
    '3.7.1': [17, 41, 74, 166, 387, 401],
    '3.7.2': [121, 138, 141, 145, 175, 205, 221, 223],
    '3.7.3': [100, 384, 390, 391],
    # Часть VIII — Файлы и S3, 12-Factor, Observability и тестирование API
    '3.8.1': [35, 102, 163, 167, 189],
    '3.8.2': [38, 62, 131, 136, 146, 371, 372],
    '3.8.3': [28, 68, 96, 178, 358, 360, 388],

    # 04 · ⚡ Алгоритмы (12 skills, Units 4.1–4.6)
    '4.1.1': [16, 340, 350],
    '4.2.1': [19, 20, 73, 297],
    '4.2.2': [13, 71, 120, 150, 173, 203, 220],
    '4.3.1': [36, 64, 69, 114, 137, 179, 188, 191],
    '4.3.2': [5, 55, 82, 107, 139, 152, 170, 182, 229, 293],
    '4.4.1': [15, 75, 80, 108, 153, 161, 198, 207],
    '4.4.2': [105, 125, 185, 227],
    '4.4.3': [18, 65, 89, 164, 218],
    '4.5.1': [31, 132],
    '4.5.2': [77, 117, 128, 155, 204, 210, 222],
    '4.6.1': [14, 76, 88],
    '4.6.2': [109, 124, 310],

    # 05 · 🗄️ Базы данных (17 skills, Units 5.1–5.6)
    '5.1.1': [24, 42, 119, 129, 200],
    '5.1.2': [1, 58, 91, 199, 211],
    '5.1.3': [11, 51, 195, 230, 395],
    '5.2.1': [30, 87, 97, 168, 169],
    '5.2.2': [59, 130, 168, 208],
    '5.3.1': [4, 12, 159],
    '5.3.2': [4, 12, 79, 94, 194],
    '5.3.3': [58, 79, 94, 126],
    '5.4.1': [11, 51, 195, 213, 230],
    '5.4.2': [61, 106, 149, 165, 213],
    '5.4.3': [8, 46, 63, 115, 187, 196, 215],
    '5.5.1': [7, 44, 104, 116, 133],
    '5.5.2': [58, 116, 206, 212],
    '5.5.3': [134, 176, 212, 219],
    '5.6.1': [27, 70, 160, 201],
    '5.6.2': [27, 86, 100, 171, 223],
    '5.6.3': [123, 160, 201, 218],

    # 06 · 🏛️ Архитектура (14 skills, Units 6.1–6.6)
    '6.1.1': [26, 29, 53, 99, 101, 147, 178, 180],
    '6.1.2': [35, 49, 60],
    '6.2.1': [35, 54, 67, 118, 157],
    '6.2.2': [25, 67, 85, 133, 206],
    '6.2.3': [41, 45, 221, 400],
    '6.3.1': [40, 81],
    '6.3.2': [52, 98, 154, 167, 190, 193, 226, 400],
    '6.4.1': [21, 34, 60, 103, 140, 202],
    '6.4.2': [37, 47, 57, 145, 183, 224],
    '6.5.1': [17, 38, 62, 102, 146, 156, 158, 228],
    '6.5.2': [25, 56, 116, 133, 231],
    '6.5.3': [206, 269, 276, 281],
    '6.6.1': [295, 336, 355, 371],
    '6.6.2': [100, 123, 138, 160, 214, 384, 390, 391],

    # 07 · 🚀 Инфраструктура (21 skills, Units 7.1–7.6)
          '7.1.1': [2001, 366],
      '7.1.2': [2002, 210],
      '7.1.3': [2003, 305],
      '7.1.4': [192, 377],
    '7.2.1': [3, 111, 295],
    '7.2.2': [3, 111, 366],
    '7.2.3': [84, 113, 131],
    '7.3.1': [3, 111, 84],
    '7.3.2': [113, 232, 84],
    '7.3.3': [113, 131, 136, 336],
    '7.4.1': [192, 355, 372],
    '7.4.2': [192, 3, 111, 295],
    '7.4.3': [192, 377, 113],
    '7.5.1': [274, 280, 296, 301, 366, 381],
    '7.5.2': [336, 349, 355, 136],
    '7.5.3': [95, 272, 279, 392, 401],
    '7.6.1': [84, 121, 138, 141, 175, 205, 223],
    '7.6.2': [28, 68, 351, 352, 354, 355, 356, 358, 359, 360, 363, 388],
    '7.6.3': [38, 62, 146, 335, 337, 371, 372],
    '7.6.4': [136, 280, 340, 371, 390, 391],
    '7.6.5': [131, 136, 336],
}

def _clean_skill_title(s: str) -> str:
    s = re.sub(r'\s*\[.*?\]\s*$', '', s).strip()
    s = re.sub(r'(?<=[А-Яа-яЁёA-Za-z0-9])- (?=[А-Яа-яЁёA-Za-z])', ': ', s)
    s = (
        s.replace('I-O-bound', 'I/O-bound')
        .replace('args-kwargs', '*args, **kwargs')
        .replace('get-keys-values', 'get, keys, values')
        .replace('match-case', 'match/case')
        .replace('try-except-else-finally', 'try/except/else/finally')
        .replace('async-await', 'async/await')
        .replace('1-1, 1-N, M-N', '1:1, 1:N, M:N')
        .replace('Controller-Service-DAL', 'Controller → Service → DAL')
        .replace('Основы CI-CD', 'Основы CI/CD')
        .replace('lint -- test -- build -- deploy', 'lint → test → build → deploy')
        .replace('ps-kill', 'ps/kill')
        .replace('chmod-chown', 'chmod/chown')
    )
    return s

ECHELON_ORDER_BUILD = [
    ('hr', '🗣️ Эшелон 1 · HR-скрининг', ['0.1', '0.2', '0.3', '0.4']),
    ('screening', '⚡ Эшелон 2 · Техскрининг', ['1.1', '1.2', '1.7', '1.4', '5.1', '5.2', '2.2', '2.3', '1.8', '1.3', '7.1']),
    ('algo', '🧮 Эшелон 3 · Алгоритмическая секция', ['4.1', '4.2', '4.4', '4.3', '4.6', '4.5']),
    ('backend', '⚙️ Эшелон 4 · Backend и БД', ['3.1', '5.5', '5.4', '3.5', '5.6', '3.6', '5.3', '1.9', '6.1', '2.4', '3.2', '3.3', '1.6', '1.5', '3.4']),
    ('infra', '🚀 Эшелон 5 · Продакшен и инфраструктура', ['7.2', '7.5', '7.4', '2.1', '7.3', '3.8']),
    ('system_design', '🏛️ Эшелон 6 · Финал · Архитектура и System Design', ['6.6', '3.7', '7.6', '6.2', '6.5', '6.4', '6.3']),
]

UNIT_INTERVIEW_META = {}
for _t_idx, (_ech_id, _ech_lbl, _ech_units) in enumerate(ECHELON_ORDER_BUILD, start=1):
    for _r_idx, _uid in enumerate(_ech_units):
        UNIT_INTERVIEW_META[_uid] = {
            'echelonId': _ech_id,
            'tier': _t_idx,
            'rank': _r_idx,
            'tierLabel': _ech_lbl,
            'stackTag': 'core',
        }

PRIORITY_ARCHITECTURE_MD = """## 🎯 Приоритетная архитектура подготовки к собеседованиям (6 эшелонов и пресеты воронки)

Программа разделена на **6 эшелонов** со строковыми идентификаторами и явным порядком юнитов внутри каждого эшелона (от самых частых вопросов на собеседованиях к редким):
1. **`hr` — HR-скрининг**: `0.1`, `0.2`, `0.3`, `0.4`.
2. **`screening` — Техскрининг**: `1.1`, `1.2`, `1.7`, `1.4`, `5.1`, `5.2`, `2.2`, `2.3`, `1.8`, `1.3`, `7.1`.
3. **`algo` — Алгоритмическая секция**: `4.1`, `4.2`, `4.4`, `4.3`, `4.6`, `4.5`.
4. **`backend` — Backend и БД**: `3.1`, `5.5`, `5.4`, `3.5`, `5.6`, `3.6`, `5.3`, `1.9`, `6.1`, `2.4`, `3.2`, `3.3`, `1.6`, `1.5`, `3.4`.
5. **`infra` — Продакшен и инфраструктура**: `7.2`, `7.5`, `7.4`, `2.1`, `7.3`, `3.8`.
6. **`system_design` — Финал · Архитектура и System Design**: `6.6`, `3.7`, `7.6`, `6.2`, `6.5`, `6.4`, `6.3`.

Пресеты воронки: `BigTech (алгоритмы до Backend)` и `Продуктовый рынок (Backend и инфра до алгоритмов)`.

---"""


def ensure_priority_architecture_in_karta(karta_text: str) -> str:
    return karta_text


karta_file_path = os.path.join(BASE_REMNOTE, '00 · 🗺️ Карта Мастерства.md')


def parse_module_section(section_md: str, mod_prefix: str):
    if not section_md:
        return [], {}, {}
    units_raw = re.split(rf'### 📘 (Юнит {mod_prefix}\.\d+ · [^\n]+)', section_md)[1:]
    units = []
    linked_k = set()
    linked_f = set()
    mod_tag = f"{int(mod_prefix):02d}"

    for idx in range(0, len(units_raw), 2):
        utitle = units_raw[idx].strip().replace('Юнит 7.4 · CI CD', 'Юнит 7.4 · CI/CD')
        ubody = units_raw[idx + 1]
        uid = re.search(rf'{mod_prefix}\.\d+', utitle).group(0)
        umeta = UNIT_INTERVIEW_META.get(uid, {'echelonId': 'screening', 'tier': 2, 'rank': 0, 'tierLabel': '⚡ Эшелон 2 · Техскрининг', 'stackTag': 'core'})
        skill_blocks = re.split(rf'- \[[ x]\] ⚡ \*\*Skill ({mod_prefix}\.\d+\.\d+) · ([^\*]+)\*\*', ubody)[1:]
        skills = []
        for s_idx in range(0, len(skill_blocks), 3):
            sid = skill_blocks[s_idx]
            stitle = _clean_skill_title(skill_blocks[s_idx + 1])
            sbody = skill_blocks[s_idx + 2]
            k_ids = re.findall(r'/(К-\d+)', sbody) + EXTRA_K_BY_SKILL.get(sid, [])
            if sid in EXPLICIT_DECKS_BY_SKILL:
                raw_f_ids = list(EXPLICIT_DECKS_BY_SKILL[sid])
            else:
                raw_f_ids = re.findall(r'/(Ф-\d+)', sbody) + EXTRA_F_BY_SKILL.get(sid, [])
            f_ids = [f"{fid}@{mod_tag}" if f"{fid}@{mod_tag}" in f_files_map else fid for fid in raw_f_ids]
            k_ids = list(dict.fromkeys(k_ids))
            f_ids = list(dict.fromkeys(f_ids))
            linked_k.update(k_ids)
            linked_f.update(f_ids)
            prac_m = re.search(r'💻 \*\*Практика кодинга\*\*:\s*([^\n]+)', sbody)
            prac_txt = prac_m.group(1).strip() if prac_m else ''
            skills.append({
                'id': sid,
                'unitId': uid,
                'title': stitle,
                'echelonId': umeta['echelonId'],
                'tier': umeta['tier'],
                'tierLabel': umeta['tierLabel'],
                'stackTag': umeta['stackTag'],
                'practiceDesc': prac_txt,
                'kIds': k_ids,
                'fIds': f_ids,
                'notes': k_ids,
                'decks': f_ids,
                'taskIds': SKILL_TASK_IDS.get(sid, [])
            })
        units.append({
            'id': uid,
            'title': utitle,
            'echelonId': umeta['echelonId'],
            'tier': umeta['tier'],
            'tierLabel': umeta['tierLabel'],
            'stackTag': umeta['stackTag'],
            'desc': f'Навыков: {len(skills)} · Конспектов: {sum(len(s["kIds"]) for s in skills)} · Колод карточек: {sum(len(s["fIds"]) for s in skills)}',
            'skills': skills
        })
    notes_data = {kid: parse_k_note(kid) for kid in sorted(linked_k)}
    decks_data = {fid: parse_f_deck(fid) for fid in sorted(linked_f)}
    return units, notes_data, decks_data

HR_UNITS, HR_NOTES_DATA, HR_DECKS_DATA = parse_module_section(mod0_hr_text, '0')
PY_UNITS, PY_NOTES_DATA, PY_DECKS_DATA = parse_module_section(mod1_text, '1')
WEB_UNITS, WEB_NOTES_DATA, WEB_DECKS_DATA = parse_module_section(mod2_web_text, '2')
BACKEND_UNITS, BACKEND_NOTES_DATA, BACKEND_DECKS_DATA = parse_module_section(mod3_backend_text, '3')
ALGO_UNITS, ALGO_NOTES_DATA, ALGO_DECKS_DATA = parse_module_section(mod4_algo_text, '4')
DB_UNITS, DB_NOTES_DATA, DB_DECKS_DATA = parse_module_section(mod5_db_text, '5')
ARCH_UNITS, ARCH_NOTES_DATA, ARCH_DECKS_DATA = parse_module_section(mod6_arch_text, '6')
INFRA_UNITS, INFRA_NOTES_DATA, INFRA_DECKS_DATA = parse_module_section(mod7_infra_text, '7')

print(f"HR      -> Units: {len(HR_UNITS)}, Skills: {sum(len(u['skills']) for u in HR_UNITS)}, K: {len(HR_NOTES_DATA)}, F: {len(HR_DECKS_DATA)} ({sum(len(d['cards']) for d in HR_DECKS_DATA.values())} cards)")
print(f"Python  -> Units: {len(PY_UNITS)}, Skills: {sum(len(u['skills']) for u in PY_UNITS)}, K: {len(PY_NOTES_DATA)}, F: {len(PY_DECKS_DATA)} ({sum(len(d['cards']) for d in PY_DECKS_DATA.values())} cards)")
print(f"Web     -> Units: {len(WEB_UNITS)}, Skills: {sum(len(u['skills']) for u in WEB_UNITS)}, K: {len(WEB_NOTES_DATA)}, F: {len(WEB_DECKS_DATA)} ({sum(len(d['cards']) for d in WEB_DECKS_DATA.values())} cards)")
print(f"Backend -> Units: {len(BACKEND_UNITS)}, Skills: {sum(len(u['skills']) for u in BACKEND_UNITS)}, K: {len(BACKEND_NOTES_DATA)}, F: {len(BACKEND_DECKS_DATA)} ({sum(len(d['cards']) for d in BACKEND_DECKS_DATA.values())} cards)")
print(f"Algo    -> Units: {len(ALGO_UNITS)}, Skills: {sum(len(u['skills']) for u in ALGO_UNITS)}, K: {len(ALGO_NOTES_DATA)}, F: {len(ALGO_DECKS_DATA)} ({sum(len(d['cards']) for d in ALGO_DECKS_DATA.values())} cards)")
print(f"DB      -> Units: {len(DB_UNITS)}, Skills: {sum(len(u['skills']) for u in DB_UNITS)}, K: {len(DB_NOTES_DATA)}, F: {len(DB_DECKS_DATA)} ({sum(len(d['cards']) for d in DB_DECKS_DATA.values())} cards)")
print(f"Arch    -> Units: {len(ARCH_UNITS)}, Skills: {sum(len(u['skills']) for u in ARCH_UNITS)}, K: {len(ARCH_NOTES_DATA)}, F: {len(ARCH_DECKS_DATA)} ({sum(len(d['cards']) for d in ARCH_DECKS_DATA.values())} cards)")
print(f"Infra   -> Units: {len(INFRA_UNITS)}, Skills: {sum(len(u['skills']) for u in INFRA_UNITS)}, K: {len(INFRA_NOTES_DATA)}, F: {len(INFRA_DECKS_DATA)} ({sum(len(d['cards']) for d in INFRA_DECKS_DATA.values())} cards)")

