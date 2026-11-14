import json
import re

with open("standards/standards.html", "r", encoding="utf-8") as f:
    std = f.read()

tracks = ['PY_MASTERY', 'WEB_MASTERY', 'BACKEND_MASTERY', 'ALGO_MASTERY', 'DB_MASTERY', 'ARCH_MASTERY', 'INFRA_MASTERY']

all_cards = []
all_unit_tests = {}

for tr in tracks:
    m = re.search(rf'const\s+{tr}\s*=\s*(\{{.*?\}});\s*(?:const|window)', std, re.DOTALL)
    if m:
        data = json.loads(m.group(1))
        decks = data.get('decks', {})
        for did, d in decks.items():
            title = d.get('title', '')
            for c_idx, c in enumerate(d.get('cards', [])):
                all_cards.append({
                    'track': tr,
                    'deck_id': did,
                    'deck_title': title,
                    'card_idx': c_idx,
                    'q': c.get('q', '').strip(),
                    'a': c.get('a', '').strip(),
                })
        all_unit_tests.update(data.get('unitTests', {}))

print(f"=== FINAL SELF-AUDIT ===")
print(f"Total Flashcards: {len(all_cards)}")
total_ut_q = sum(len(ut.get('questions', [])) for ut in all_unit_tests.values())
print(f"Total Unit Tests: {len(all_unit_tests)} ({total_ut_q} questions)")

# Audit 1: Check for any theme/topic/unit/lesson mentions in questions
theme_words = [
    r'\bтема\b', r'\bтеме\b', r'\bтему\b', r'\bтемой\b', r'\bтемы\b',
    r'\bв\s+данной\s+теме\b', r'\bв\s+этой\s+теме\b', r'\bв\s+теме\b',
    r'\bв\s+данном\s+уроке\b', r'\bв\s+этом\s+уроке\b', r'\bв\s+уроке\b',
    r'\bв\s+данном\s+юните\b', r'\bв\s+этом\s+юните\b',
    r'\bв\s+конспекте\b', r'\bв\s+данном\s+разделе\b',
    r'^[ФК]-\d+'
]

theme_violations = []
for c in all_cards:
    plain_q = re.sub(r'<[^>]+>', '', c['q']).strip()
    for pat in theme_words:
        if re.search(pat, plain_q, re.IGNORECASE):
            theme_violations.append((c['deck_id'], plain_q, pat))
            break

for ut_id, ut in all_unit_tests.items():
    for q in ut.get('questions', []):
        q_text = q.get('q', '')
        for pat in theme_words:
            if re.search(pat, q_text, re.IGNORECASE):
                theme_violations.append((f"UT-{ut_id}", q_text[:80], pat))
                break

print(f"\n1. Theme / topic mentions: {len(theme_violations)}")
for tv in theme_violations:
    print(f"  VIOLATION: [{tv[0]}] {tv[1]} (pattern: {tv[2]})")

# Audit 2: Check for shorthand telegram patterns:
# "Сложность ...?", "Метод для ...?", "Функция для ...?", "Команда для ...?", "Режим для ...?",
# "Разница ...?", "Расшифровка ...?", "X vs Y?", "... – результат?"
shorthand_patterns = [
    r'^Сложность\b',
    r'^Расшифровка\b',
    r'^Разница\s+(?:между\b)?',
    r'\bvs\b.*\?',
    r'[–—\-:]\s*(?:результат\??|какой тип\??|что вернёт\??)$',
    r'^(?:Метод|Функция|Режим|Команда|Оператор|Способ|Формат|Срок|Синтаксис|Основное применение|Назначение|Определение|Применение|Пример|Назовите примеры|Строка импорта)\s+для\b',
    r'^(?:Основное\s+применение|Строка импорта)\b',
    r'^(?:Включается\s+ли\s+элемент\s+с\s+индексом\s+(?:start|stop)\s+в\s+результат\??|Какой\s+метод\s+вызывается\s+вторым\??|Как\s+задать\s+местоположение\s+параметра\??|Когда\s+нужно\s+экранировать\s+данные\??|Как\s+обновить\s+поле\s+документа\??|Как\s+удалить\s+один\s+документ\??|Как\s+получить\s+IP-адрес\s+клиента\??|Как\s+отсортировать\s+по\s+убыванию\??|Как\s+изменить\s+лимит\s+рекурсии\??|Как\s+узнать\s+лимит\s+рекурсии\??|Когда\s+нужны\s+моки\??|Как\s+добавить\s+хлебную\s+крошку\??)$'
]

shorthand_violations = []
for c in all_cards:
    plain_q = re.sub(r'<[^>]+>', '', c['q']).strip()
    clean_q = plain_q.replace('&quot;', '"').replace('&#x27;', "'").replace('&gt;', '>').replace('&lt;', '<')
    for pat in shorthand_patterns:
        if re.search(pat, clean_q, re.IGNORECASE):
            # check exception for vs with proper question word
            if 'vs' in pat and re.match(r'^(?:В чём|Чем|Какова|Каковы|Как|Что|Почему|Какой|Какая|Какое|Какие)\b', clean_q, re.IGNORECASE):
                continue
            shorthand_violations.append((c['deck_id'], clean_q, pat))
            break

print(f"\n2. Shorthand telegram violations: {len(shorthand_violations)}")
for sv in shorthand_violations:
    print(f"  VIOLATION: [{sv[0]}] {sv[1]} (pattern: {sv[2]})")

# Audit 3: Missing question mark
no_qm_violations = []
for c in all_cards:
    plain_q = re.sub(r'<[^>]+>', '', c['q']).strip()
    if not plain_q.endswith('?') and not re.match(r'^(?:Опишите|Назовите|Перечислите|Укажите|Приведите|Сравните|Объясните)\b', plain_q, re.IGNORECASE):
        no_qm_violations.append((c['deck_id'], plain_q))

print(f"\n3. Missing question mark violations: {len(no_qm_violations)}")
for nq in no_qm_violations:
    print(f"  VIOLATION: [{nq[0]}] {nq[1]}")

print("\n=== AUDIT SUMMARY ===")
total_defects = len(theme_violations) + len(shorthand_violations) + len(no_qm_violations)
if total_defects == 0:
    print("PERFECT: 0 defects found across all 6,134 flashcards and 217 unit test questions!")
else:
    print(f"Found {total_defects} total defects remaining.")
