#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/audit_content_acceptance.py

Автоматический аудитор критериев приёмки учебных материалов
(PROJECT_CONTEXT.md § 1.21 — Content Acceptance Standard).

Проверяет всю цепь обучения:
  1. Конспекты (К-*): смысловые опоры, код, оформление, 0 технических кодов и мета-ярлыков.
  2. Замкнутый контур «Конспект ↔ Карточки» (Zero Surprises): покрытие терминов >= 95%.
  3. Флеш-карточки (Ф-*): полнота полей, отсутствие дублей и техкодов.
  4. Практика (tasks.json): полнота desc/initialCode/solution/hint/tests, структура подсказок.
  5. Рубежные тесты (unitTests): 8–12 вопросов, валидный correct, наличие explain/hint.
"""

import argparse
import html as html_lib
import io
import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
STANDARDS_HTML = ROOT_DIR / 'standards' / 'standards.html'
CONTENT_DIR = ROOT_DIR / 'data' / 'content'

MASTERY_NAMES = [
    'HR_MASTERY',
    'PY_MASTERY',
    'WEB_MASTERY',
    'BACKEND_MASTERY',
    'ALGO_MASTERY',
    'DB_MASTERY',
    'ARCH_MASTERY',
    'INFRA_MASTERY',
]

TECH_CODE_RE = re.compile(r'(?<![А-Яа-яA-Za-z0-9_])(?:К-\d+|Ф-\d+|Юнит\s+\d+\.\d+)(?!\d)')
META_LABEL_RE = re.compile(
    r'(?:Ментальная модель|Аналогия|Метафора|Дидактический пример)\s*:',
    re.IGNORECASE,
)
JVS_RE = re.compile(r'(?:Junior|Senior|jvs-grid)', re.IGNORECASE)

STOP_TOKENS = {
    'str', 'int', 'float', 'bool', 'list', 'dict', 'set', 'tuple', 'bytes',
    'def', 'class', 'return', 'import', 'from', 'pass', 'true', 'false',
    'none', 'self', 'cls', 'args', 'kwargs', 'arg', 'val', 'value', 'values',
    'key', 'keys', 'item', 'items', 'user', 'users', 'name', 'names',
    'data', 'result', 'res', 'obj', 'var', 'foo', 'bar', 'baz', 'abc',
    'http', 'https', 'com', 'org', 'net', 'example', 'localhost', 'www',
    'api', 'app', 'url', 'path', 'id', 'ids', 'idx', 'num', 'nums', 'err',
    'file', 'text', 'msg', 'info', 'test', 'tests', 'func', 'fn', 'and',
    'or', 'not', 'in', 'is', 'as', 'for', 'while', 'if', 'else', 'elif',
    'try', 'except', 'finally', 'with', 'raise', 'yield', 'async', 'await',
    'print', 'len', 'range', 'type', 'isinstance', 'super', 'object',
    'python', 'sql', 'json', 'yaml', 'html', 'css', 'utf-8', 'ascii',
    'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'status',
    'order', 'orders', 'product', 'products', 'alice', 'bob', 'alex',
}

MAX_CODE_LINE_LEN = 46


def strip_html(raw: str) -> str:
    """Удаляет SVG и HTML-теги, декодирует сущности."""
    text = re.sub(r'<svg[\s\S]*?</svg>', ' ', raw)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html_lib.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()


def extract_unit_meta(html_text: str) -> dict[str, dict]:
    """Извлекает карту эшелонов юнитов (6 эшелонов / legacy fallback) из standards/standards.html."""
    result: dict[str, dict] = {}
    ech_marker = 'const ECHELONS_BY_ID ='
    ech_start = html_text.find(ech_marker)
    if ech_start != -1:
        ech_brace = html_text.find('{', ech_start)
        ech_end = html_text.find('};\n', ech_brace)
        if ech_end == -1:
            ech_end = html_text.find('};', ech_brace)
        ech_block = html_text[ech_brace:ech_end + 1]
        order = ['hr', 'screening', 'algo', 'backend', 'infra', 'system_design']
        for tier_num, ech_id in enumerate(order, start=1):
            m_units = re.search(rf'\b{ech_id}\s*:\s*\{{[\s\S]*?\bunits\s*:\s*\[([^\]]*)\]', ech_block)
            if m_units:
                uids = re.findall(r"'(\d+\.\d+)'", m_units.group(1))
                for rank_idx, uid in enumerate(uids):
                    result[uid] = {'echelonId': ech_id, 'tier': tier_num, 'rank': rank_idx, 'stackTag': 'core'}
    if result:
        return result

    marker = 'const UNIT_INTERVIEW_META ='
    start = html_text.find(marker)
    if start == -1:
        raise RuntimeError('UNIT_INTERVIEW_META и ECHELONS_BY_ID не найдены в standards/standards.html')
    brace_start = html_text.find('{', start)
    end = html_text.find('};', brace_start)
    block = html_text[brace_start:end + 1]
    pattern = re.compile(
        r"'(\d+\.\d+)'\s*:\s*\{\s*tier\s*:\s*(\d+)\s*,\s*stackTag\s*:\s*'([^']+)'\s*\}"
    )
    for m in pattern.finditer(block):
        result[m.group(1)] = {'tier': int(m.group(2)), 'stackTag': m.group(3)}
    return result


def extract_mastery_objects(html_text: str) -> dict[str, dict]:
    """Извлекает 8 объектов *_MASTERY из standards/standards.html."""
    decoder = json.JSONDecoder()
    loaded: dict[str, dict] = {}
    for name in MASTERY_NAMES:
        marker = f'const {name} ='
        idx = html_text.find(marker)
        if idx == -1:
            raise RuntimeError(f'{name} не найден в standards/standards.html')
        start = html_text.find('{', idx)
        obj, _ = decoder.raw_decode(html_text, start)
        loaded[name] = obj
    return loaded


def extract_code_tokens(raw_html: str) -> set[str]:
    """Извлекает значимые технические идентификаторы из <code>...</code>."""
    tokens: set[str] = set()
    for chunk in re.findall(r'<code>([\s\S]*?)</code>', raw_html):
        decoded = html_lib.unescape(re.sub(r'<[^>]+>', ' ', chunk))
        for tok in re.findall(r'[A-Za-z_][A-Za-z0-9_.-]{2,}', decoded):
            low = tok.lower().strip('._-')
            if len(low) < 3 or low in STOP_TOKENS:
                continue
            if re.fullmatch(r'v\d+', low):
                continue
            tokens.add(tok.strip('._-'))
    return tokens


def find_trailing_python_comment(line: str) -> bool:
    """Проверяет, есть ли в строке Python хвостовой комментарий после кода."""
    stripped = line.strip()
    if not stripped or stripped.startswith('#'):
        return False
    in_single = False
    in_double = False
    escape = False
    for idx, ch in enumerate(line):
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == '#' and not in_single and not in_double:
            return bool(line[:idx].strip())
    return False


def check_note_quality(
    kid: str,
    note: dict,
    canonical_note: dict | None,
) -> dict:
    """Проверяет один конспект на красные флаги и качественные опоры."""
    steps = note.get('steps', [])
    red_flags: list[str] = []
    warnings: list[str] = []

    if not steps:
        red_flags.append('Отсутствуют шаги конспекта (steps пуст)')
        return {
            'id': kid,
            'title': note.get('title', ''),
            'steps': 0,
            'words': 0,
            'code_blocks': 0,
            'red_flags': red_flags,
            'warnings': warnings,
        }

    if canonical_note is not None and canonical_note != note:
        red_flags.append('Рассинхронизация между standards.html и data/content/notes.json')

    all_html = '\n'.join(st.get('html', '') for st in steps)
    plain_all = strip_html(all_html)
    words = len(plain_all.split())

    # 1. Технические коды и мета-ярлыки
    for idx, st in enumerate(steps, 1):
        st_text = strip_html(st.get('title', '') + ' ' + st.get('html', ''))
        tech_hits = TECH_CODE_RE.findall(st_text)
        if tech_hits:
            red_flags.append(f'Шаг {idx}: утечка техкода ({", ".join(sorted(set(tech_hits)))})')
        meta_hits = META_LABEL_RE.findall(st_text)
        if meta_hits:
            red_flags.append(f'Шаг {idx}: мета-ярлык ({", ".join(sorted(set(meta_hits)))})')

    # 2. Проверка блоков кода
    snippet_pattern = re.compile(
        r'(?:<span class="code-lang-tag">([^<]+)</span>[\s\S]*?)?<pre><code>([\s\S]*?)</code></pre>',
        re.DOTALL,
    )
    snippets = snippet_pattern.findall(all_html)
    code_blocks = len(snippets)
    blind_prints = 0
    long_lines: list[int] = []
    trailing_comments = 0

    for lang, code_raw in snippets:
        lang_norm = (lang or 'python').strip().lower()
        code_text = html_lib.unescape(code_raw)
        lines = code_text.splitlines()
        has_doc = any('# >>>' in ln or '#' in ln for ln in lines)

        for ln in lines:
            if len(ln) > MAX_CODE_LINE_LEN:
                long_lines.append(len(ln))
            ln_s = ln.strip()
            if lang_norm == 'python':
                if 'print(' in ln_s and not ln_s.startswith('#') and not has_doc:
                    blind_prints += 1
                if find_trailing_python_comment(ln):
                    trailing_comments += 1

    if blind_prints:
        red_flags.append(f'Слепые вызовы print() без # >>> комментария вывода: {blind_prints}')
    if trailing_comments:
        warnings.append(f'Хвостовые комментарии в Python-коде: {trailing_comments}')
    if long_lines:
        warnings.append(
            f'Строки кода > {MAX_CODE_LINE_LEN} симв.: {len(long_lines)} (макс. {max(long_lines)})'
        )
    if code_blocks == 0:
        warnings.append('Нет ни одного блока кода (<pre>)')
    if not JVS_RE.search(plain_all):
        warnings.append('Отсутствует сравнение Junior vs Senior')

    return {
        'id': kid,
        'title': note.get('title', ''),
        'steps': len(steps),
        'words': words,
        'code_blocks': code_blocks,
        'red_flags': red_flags,
        'warnings': warnings,
    }


def check_closed_loop(
    skill: dict,
    unit_tier: int,
    m_notes: dict,
    m_decks: dict,
    notes_json: dict,
    cards_json: dict,
) -> dict:
    """Проверяет покрытие терминов карточек в конспектах одного навыка."""
    k_ids = skill.get('notes') or skill.get('kIds') or []
    f_ids = skill.get('decks') or skill.get('fIds') or []

    notes_parts = []
    for kid in k_ids:
        note = m_notes.get(kid) or notes_json.get(kid)
        if not note:
            continue
        for st in note.get('steps', []):
            notes_parts.append(st.get('title', ''))
            notes_parts.append(html_lib.unescape(re.sub(r'<[^>]+>', ' ', st.get('html', ''))))
    notes_corpus = ' '.join(notes_parts).lower()

    card_tokens: set[str] = set()
    total_cards = 0
    for fid in f_ids:
        deck = m_decks.get(fid) or cards_json.get(fid)
        if not deck:
            continue
        for card in deck.get('cards', []):
            total_cards += 1
            card_tokens |= extract_code_tokens(card.get('q', '') + ' ' + card.get('a', ''))

    missing: list[str] = []
    for tok in sorted(card_tokens):
        low = tok.lower()
        if low in notes_corpus:
            continue
        # Для составного имени вида obj.method допускаем наличие самого метода, если он >= 4 симв.
        if '.' in low:
            tail = low.split('.')[-1]
            if len(tail) >= 4 and tail in notes_corpus:
                continue
        missing.append(tok)

    total = len(card_tokens)
    coverage = 100.0 if total == 0 else round(100.0 * (total - len(missing)) / total, 1)
    return {
        'skill_id': skill['id'],
        'tier': unit_tier,
        'title': skill['title'],
        'k_ids': k_ids,
        'f_ids': f_ids,
        'cards': total_cards,
        'total_tokens': total,
        'missing_count': len(missing),
        'missing_tokens': missing,
        'coverage': coverage,
    }


def check_deck_quality(fid: str, deck: dict) -> dict:
    """Проверяет колоду флеш-карточек на полноту, дубли и утечку техкодов."""
    cards = deck.get('cards', [])
    red_flags: list[str] = []
    seen_q: set[str] = set()
    dup_count = 0
    empty_count = 0
    tech_hits_total = 0

    for idx, card in enumerate(cards, 1):
        q_raw = card.get('q', '')
        a_raw = card.get('a', '')
        q_plain = strip_html(q_raw)
        a_plain = strip_html(a_raw)
        if not q_plain or not a_plain:
            empty_count += 1
        q_norm = re.sub(r'\s+', ' ', q_plain.lower())
        if q_norm in seen_q:
            dup_count += 1
        seen_q.add(q_norm)
        if TECH_CODE_RE.search(q_plain + ' ' + a_plain):
            tech_hits_total += 1

    if not cards:
        red_flags.append('В колоде 0 карточек')
    if empty_count:
        red_flags.append(f'Карточки с пустым вопросом или ответом: {empty_count}')
    if dup_count:
        red_flags.append(f'Дублирующиеся вопросы в колоде: {dup_count}')
    if tech_hits_total:
        red_flags.append(f'Утечка техкодов (К-*/Ф-*/Юнит): {tech_hits_total}')

    return {
        'id': fid,
        'title': deck.get('title', ''),
        'cards': len(cards),
        'red_flags': red_flags,
    }


def check_task_quality(tid: int, task: dict | None) -> dict:
    """Проверяет задачу практики Zen IDE."""
    red_flags: list[str] = []
    warnings: list[str] = []

    if task is None:
        return {
            'id': tid,
            'title': '',
            'red_flags': ['Задача отсутствует в data/content/tasks.json'],
            'warnings': [],
        }

    for field in ('title', 'desc', 'initialCode', 'solution', 'hint', 'tests'):
        val = task.get(field)
        if not isinstance(val, str) or not val.strip():
            red_flags.append(f'Пустое или отсутствует поле {field}')

    desc_plain = strip_html(task.get('title', '') + ' ' + task.get('desc', ''))
    tech_hits = TECH_CODE_RE.findall(desc_plain)
    if tech_hits:
        red_flags.append(f'Утечка техкода в условии: {", ".join(sorted(set(tech_hits)))}')

    hint_text = task.get('hint', '')
    steps_found = len(re.findall(r'Шаг\s+\d+', hint_text))
    if steps_found < 3:
        warnings.append(f'В hint найдено {steps_found} явных шагов (рекомендуется 3–4 ступени Сократа)')

    return {
        'id': tid,
        'title': task.get('title', ''),
        'red_flags': red_flags,
        'warnings': warnings,
    }


def check_unit_test_quality(unit_id: str, unit_tier: int, utest: dict | None) -> dict:
    """Проверяет рубежный тест юнита."""
    red_flags: list[str] = []
    warnings: list[str] = []

    if not utest:
        return {
            'unit_id': unit_id,
            'tier': unit_tier,
            'title': '',
            'questions': 0,
            'red_flags': ['Отсутствует рубежный тест'],
            'warnings': [],
        }

    questions = utest.get('questions', [])
    title = utest.get('title', '')
    is_project_defense = bool(re.search(r'Защита проекта|Финальн', title, re.IGNORECASE))

    if len(questions) < 8 or len(questions) > 12:
        msg = f'Нестандартное число вопросов: {len(questions)} (норма 8–12)'
        if is_project_defense:
            warnings.append(msg + ' [проектный зачёт]')
        else:
            red_flags.append(msg)

    no_explain = 0
    bad_correct = 0
    tech_hits = 0
    for q_item in questions:
        opts = q_item.get('options', [])
        corr = q_item.get('correct')
        if not isinstance(corr, int) or corr < 0 or corr >= len(opts) or len(opts) < 2:
            bad_correct += 1
        expl = q_item.get('explain') or q_item.get('hint') or ''
        if not isinstance(expl, str) or not expl.strip():
            no_explain += 1
        q_text = strip_html(q_item.get('q', '') + ' ' + expl)
        if TECH_CODE_RE.search(q_text):
            tech_hits += 1

    if bad_correct:
        red_flags.append(f'Вопросы с некорректным correct/options: {bad_correct}')
    if no_explain:
        red_flags.append(f'Вопросы без объяснения (explain/hint): {no_explain}')
    if tech_hits:
        red_flags.append(f'Утечка техкодов в вопросах/объяснениях: {tech_hits}')

    return {
        'unit_id': unit_id,
        'tier': unit_tier,
        'title': title,
        'questions': len(questions),
        'red_flags': red_flags,
        'warnings': warnings,
    }


def run_audit(tier_filter: str, top_n: int) -> dict:
    """Выполняет полный аудит материалов по критериям § 1.21."""
    html_text = STANDARDS_HTML.read_text(encoding='utf-8')
    unit_meta = extract_unit_meta(html_text)
    masteries = extract_mastery_objects(html_text)

    notes_json = json.loads((CONTENT_DIR / 'notes.json').read_text(encoding='utf-8'))
    cards_json = json.loads((CONTENT_DIR / 'cards.json').read_text(encoding='utf-8'))
    tasks_list = json.loads((CONTENT_DIR / 'tasks.json').read_text(encoding='utf-8'))
    tasks_by_id = {t['id']: t for t in tasks_list}

    target_tier = None
    target_echelon_id = None
    if tier_filter != 'all':
        if tier_filter.isdigit():
            target_tier = int(tier_filter)
        else:
            target_echelon_id = tier_filter

    seen_notes: dict[str, dict] = {}
    seen_decks: dict[str, dict] = {}
    seen_tasks: set[int] = set()
    loop_reports: list[dict] = []
    unit_test_reports: list[dict] = []

    for m_name, obj in masteries.items():
        m_notes = obj.get('notes', {})
        m_decks = obj.get('decks', {})
        m_utests = obj.get('unitTests', {})

        for unit in obj.get('units', []):
            uid = unit['id']
            meta_u = unit_meta.get(uid, {})
            u_tier = meta_u.get('tier', unit.get('tier', 2))
            u_ech_id = meta_u.get('echelonId', unit.get('echelonId'))
            if target_tier is not None and u_tier != target_tier:
                continue
            if target_echelon_id is not None and u_ech_id != target_echelon_id:
                continue

            ut_rep = check_unit_test_quality(uid, u_tier, m_utests.get(uid))
            unit_test_reports.append(ut_rep)

            for skill in unit.get('skills', []):
                for kid in (skill.get('notes') or skill.get('kIds') or []):
                    if kid not in seen_notes:
                        note_obj = m_notes.get(kid) or notes_json.get(kid)
                        if note_obj:
                            seen_notes[kid] = check_note_quality(
                                kid,
                                note_obj,
                                notes_json.get(kid),
                            )

                for fid in (skill.get('decks') or skill.get('fIds') or []):
                    if fid not in seen_decks:
                        deck_obj = m_decks.get(fid) or cards_json.get(fid)
                        if deck_obj:
                            seen_decks[fid] = check_deck_quality(fid, deck_obj)

                for tid in skill.get('taskIds', []):
                    seen_tasks.add(tid)

                loop_reports.append(
                    check_closed_loop(skill, u_tier, m_notes, m_decks, notes_json, cards_json)
                )

    task_reports = [
        check_task_quality(tid, tasks_by_id.get(tid))
        for tid in sorted(seen_tasks)
    ]

    note_reports = sorted(seen_notes.values(), key=lambda x: x['id'])
    deck_reports = sorted(seen_decks.values(), key=lambda x: x['id'])

    summary = {
        'tier': tier_filter,
        'notes_checked': len(note_reports),
        'notes_red_flags': sum(1 for r in note_reports if r['red_flags']),
        'notes_warnings': sum(1 for r in note_reports if r['warnings']),
        'skills_checked': len(loop_reports),
        'skills_below_95': sum(1 for r in loop_reports if r['coverage'] < 95.0),
        'avg_loop_coverage': (
            round(sum(r['coverage'] for r in loop_reports) / len(loop_reports), 1)
            if loop_reports else 100.0
        ),
        'decks_checked': len(deck_reports),
        'decks_red_flags': sum(1 for r in deck_reports if r['red_flags']),
        'tasks_checked': len(task_reports),
        'tasks_red_flags': sum(1 for r in task_reports if r['red_flags']),
        'tasks_warnings': sum(1 for r in task_reports if r['warnings']),
        'unit_tests_checked': len(unit_test_reports),
        'unit_tests_red_flags': sum(1 for r in unit_test_reports if r['red_flags']),
    }

    return {
        'summary': summary,
        'notes': note_reports,
        'closed_loop': sorted(loop_reports, key=lambda x: (x['coverage'], -x['missing_count'])),
        'decks': deck_reports,
        'tasks': task_reports,
        'unit_tests': unit_test_reports,
        'top_n': top_n,
    }


def print_report(report: dict) -> None:
    """Печатает наглядную сводку результатов аудита в консоль."""
    s = report['summary']
    top_n = report['top_n']

    print('=' * 72)
    print(f'АУДИТ КРИТЕРИЕВ ПРИЁМКИ МАТЕРИАЛОВ (§ 1.21) | Фильтр: --tier {s["tier"]}')
    print('=' * 72)
    print(
        f'1. Конспекты:       {s["notes_checked"]:3d} | '
        f'Red Flags: {s["notes_red_flags"]:3d} | Предупреждений: {s["notes_warnings"]:3d}'
    )
    print(
        f'2. Замкнутый контур:{s["skills_checked"]:3d} | '
        f'Ниже 95%:  {s["skills_below_95"]:3d} | Среднее покрытие: {s["avg_loop_coverage"]}%'
    )
    print(
        f'3. Флеш-карточки:   {s["decks_checked"]:3d} | '
        f'Red Flags: {s["decks_red_flags"]:3d}'
    )
    print(
        f'4. Практика IDE:    {s["tasks_checked"]:3d} | '
        f'Red Flags: {s["tasks_red_flags"]:3d} | Предупреждений: {s["tasks_warnings"]:3d}'
    )
    print(
        f'5. Рубежные тесты:  {s["unit_tests_checked"]:3d} | '
        f'Red Flags: {s["unit_tests_red_flags"]:3d}'
    )

    notes_bad = [r for r in report['notes'] if r['red_flags'] or r['warnings']]
    if notes_bad:
        print(f'\n--- ТОП-{top_n} КОНСПЕКТОВ С ЗАМЕЧАНИЯМИ ({len(notes_bad)} всего) ---')
        notes_bad.sort(key=lambda r: (-len(r['red_flags']), -len(r['warnings']), r['id']))
        for r in notes_bad[:top_n]:
            flags = '; '.join(r['red_flags'] + r['warnings'])
            tag = 'RED' if r['red_flags'] else 'WARN'
            print(f'  [{tag}] {r["id"]} ({r["steps"]}ш, {r["words"]}сл): {flags}')

    loop_bad = [r for r in report['closed_loop'] if r['coverage'] < 95.0]
    if loop_bad:
        print(f'\n--- ТОП-{top_n} НАВЫКОВ С НЕПОЛНЫМ ЗАМКНУТЫМ КОНТУРОМ (<95%, {len(loop_bad)} всего) ---')
        for r in loop_bad[:top_n]:
            sample = ', '.join(r['missing_tokens'][:8])
            print(
                f'  [Э{r["tier"]}] {r["skill_id"]:5s} | покр: {r["coverage"]:5.1f}% '
                f'({r["missing_count"]}/{r["total_tokens"]} нет) | нет: {sample}'
            )

    decks_bad = [r for r in report['decks'] if r['red_flags']]
    if decks_bad:
        print(f'\n--- КОЛОДЫ КАРТОЧЕК С RED FLAGS ({len(decks_bad)} всего) ---')
        for r in decks_bad[:top_n]:
            print(f'  [RED] {r["id"]}: {"; ".join(r["red_flags"])}')

    tasks_bad = [r for r in report['tasks'] if r['red_flags']]
    if tasks_bad:
        print(f'\n--- ЗАДАЧИ ПРАКТИКИ С RED FLAGS ({len(tasks_bad)} всего) ---')
        for r in tasks_bad[:top_n]:
            print(f'  [RED] #{r["id"]} {r["title"][:45]}: {"; ".join(r["red_flags"])}')

    ut_bad = [r for r in report['unit_tests'] if r['red_flags'] or r['warnings']]
    if ut_bad:
        print(f'\n--- РУБЕЖНЫЕ ТЕСТЫ С ЗАМЕЧАНИЯМИ ({len(ut_bad)} всего) ---')
        for r in ut_bad[:top_n]:
            tag = 'RED' if r['red_flags'] else 'WARN'
            msgs = '; '.join(r['red_flags'] + r['warnings'])
            print(f'  [{tag}] {r["unit_id"]} (Э{r["tier"]}, {r["questions"]} вопр.): {msgs}')


def main() -> int:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(
        description='Аудит учебных материалов по критериям приёмки § 1.21',
    )
    parser.add_argument(
        '--tier',
        choices=['1', '2', '3', '4', '5', '6', 'hr', 'screening', 'algo', 'backend', 'infra', 'system_design', 'all'],
        default='all',
        help='Фильтр по эшелону подготовки (число 1..6, строковый id или all)',
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Возвращать код выхода 1 при наличии любых Red Flags',
    )
    parser.add_argument(
        '--json',
        dest='json_path',
        help='Путь для сохранения полного JSON-отчёта',
    )
    parser.add_argument(
        '--top',
        type=int,
        default=15,
        help='Максимум строк в каждой проблемной секции вывода (по умолчанию: 15)',
    )
    args = parser.parse_args()

    report = run_audit(args.tier, args.top)
    print_report(report)

    if args.json_path:
        out_path = Path(args.json_path)
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'\nПолный отчёт сохранён в: {out_path}')

    if args.strict:
        s = report['summary']
        total_red = (
            s['notes_red_flags']
            + s['decks_red_flags']
            + s['tasks_red_flags']
            + s['unit_tests_red_flags']
        )
        if total_red > 0:
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
