#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/quality_gate.py

Единая трёхуровневая система проверки качества учебных материалов (Content Quality Gate)
по стандарту PROJECT_CONTEXT.md § 1.21:
  Уровень 1 (L1): Гигиена и структура (переиспользует scripts/audit_content_acceptance.py + аудит шаблонных подсказок).
  Уровень 2 (L2): Инженерная исполняемость (позитивный и негативный прогон практики в изолированной среде,
                  статический анализ кода, AST-валидация Python-сниппетов конспектов).
  Уровень 3 (L3): Смысловой и педагогический аудит через Google Gemini API (Interactions API + Pydantic).

Результаты кэшируются в data/quality_ledger.json по SHA-256 хэшу навыка и версии рубрики,
а итоговая сводка сохраняется в data/quality_report.md.
"""

from __future__ import annotations

import argparse
import ast
import builtins
import contextlib
import copy
import datetime as dt
import hashlib
import html as html_lib
import io
import json
import os
import pathlib
import re
import statistics
import sys
import time
import types
import urllib.request
from pathlib import Path
from typing import Any, Literal

try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover - fallback для минимального Python в run_workflow
    BaseModel = None  # type: ignore[assignment]
    Field = None  # type: ignore[assignment]

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import audit_content_acceptance as aca  # noqa: E402
import test_all_401_tasks as task_runner  # noqa: E402

RUBRIC_VERSION = '1.1'
DEFAULT_MODEL = 'gemini-3.8-flash'
LEDGER_PATH = ROOT_DIR / 'data' / 'quality_ledger.json'
REPORT_PATH = ROOT_DIR / 'data' / 'quality_report.md'
ENV_PATH = ROOT_DIR / '.env'

MAX_CODE_LINE_LEN = aca.MAX_CODE_LINE_LEN

# Шаблонные фразы-заглушки в подсказках практических задач (автогенерированный шаблон вместо реальных шагов Сократа)
STUB_HINT_PATTERNS = (
    'Проверь сигнатуру и входные типы данных',
    'Обработай граничные случаи (пустые коллекции, None, неверные типы)',
    'Сформируй и верни ожидаемый результат',
    'f\'{self.__class__.__name__}(attr={self.attr})\'',
)

# Заглушки I/O Flow, указывающие на недописанный шаблон условия задачи
STUB_IO_FLOW_PATTERNS = (
    'Ожидаемый результат (int)',
    'Ожидаемый результат (result)',
    'Входная структура данных',
    'Преобразованная целевая структура',
)

# Характерные обрывы текста, возникающие при вырезании неэкранированных угловых скобок <...>
BROKEN_ANGLE_RE = re.compile(
    r'(?:Authorization:\s*(?:Bearer|Basic)|X-Real-IP:|X-Forwarded-For:\s*,|(?:Bearer|Basic)\s*\.)\s*(?:$|[.,;\n`]|<(?![\w\(\):_-]+>))',
    re.MULTILINE,
)
RAW_HTML_TAG_NAME_RE = re.compile(r'</?([a-zA-Z][a-zA-Z0-9-]*)\b[^>]*>')
SAFE_HTML_TAGS = {
    'a', 'b', 'blockquote', 'br', 'button', 'code', 'div', 'em', 'h1', 'h2',
    'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'li', 'ol', 'p', 'pre', 'span',
    'strong', 'sub', 'sup', 'svg', 'table', 'tbody', 'td', 'th', 'thead',
    'tr', 'ul',
}

ABSTRACT_IDENT_RE = re.compile(r'\b(?:foo|bar|baz)\b', re.IGNORECASE)
SNIPPET_RE = re.compile(
    r'(?:<span class="code-lang-tag">([^<]+)</span>[\s\S]*?)?<pre><code>([\s\S]*?)</code></pre>',
    re.DOTALL,
)

# Канонический системный промпт для Уровня 3 (опора на PROJECT_CONTEXT.md § 1.21)
L3_SYSTEM_PROMPT = """Ты — главный технический ревьюер и методист бэкенд-академии Python (уровень Staff Backend Engineer & Pedagogical Lead).
Твоя задача — провести строгий, предметный аудит качества ОДНОГО учебного навыка целиком по стандартам PROJECT_CONTEXT.md § 1.21.

Оценивай СМЫСЛОВОЕ и ИНЖЕНЕРНОЕ качество материалов, а не формальный объём текста или подсчёт слов.

Калибровка 5 осей оценки (от 1 до 5):
- 5 (Эталон): безупречное качество, полное раскрытие физики процессов, чистый замкнутый контур.
- 4 (Продакшен-уровень): добротный уровень, полностью пригодный для самостоятельного обучения студентов и прохождения BigTech-скрининга; концепты раскрыты, код исполняется, подсказки ведут к решению, критических блокеров нет (допустимы точечные рекомендации major/minor).
- 3 (Требует переработки): наличие критических дефектов, ломающих прохождение темы или вводящих студента в заблуждение.
- 1–2 (Брак): неработающий или оторванный от реальности материал.

Обязательные 5 осей:
1. notes_depth (Глубина конспекта):
   - Сразу ли вскрывается инженерная суть проблемы и механика под капотом (CPython, память, протоколы, СУБД, алгоритмы), без воды и канцеляризмов?
   - Есть ли вменяемые, рабочие примеры кода и корректное, честное сравнение «❌ Подход Junior vs ✅ Подход Senior»?
   - Учитывай профиль эшелона (Эшелон 1 — фундамент до уровня BigTech-скрининга Яндекса/Авито/Т-Банка/Ozon).

2. closed_loop (Смысловой замкнутый контур — Zero Surprises):
   - Сможет ли старательный студент, изучив конспекты этого навыка, уверенно ответить на флеш-карточки и решить практические задачи?
   - ВАЖНО про рубежный тест: один рубежный тест проверяет ВЕСЬ юнит целиком. Список соседних навыков этого же юнита приведён в пакете перед тестом. Вопросы рубежного теста, относящиеся к соседним навыкам этого юнита, НЕ считаются нарушением closed_loop данного навыка.
   - ВАЖНО про карточки: базовые свойства и логические следствия изучаемых типов (например, сложность среза O(k), ленивость range, неизменяемость кортежа) не считаются нарушением closed_loop, если фундаментальная механика дана в конспекте. Нарушением является лишь опрос тем, чужеродных для изучаемого материала.

3. cards_quality (Качество флеш-карточек SRS):
   - Соблюдается ли правило «1 атомарный проверяемый факт = 1 карточка»?
   - Самодостаточен ли вопрос (можно ли понять, что именно спрашивают, без телепатии)?
   - Точен ли ответ и согласован ли он с конспектом без противоречий?

4. practice_quality (Качество практики в Zen IDE):
   - Реалистичный ли это бэкенд-сценарий? Понятен ли контракт входа/выхода в условии?
   - Проверяют ли tests реальную логику и работоспособность решения?
   - Ведёт ли лестница подсказок Сократа в hint ученика к решению без шаблонных заглушек и без прямого слива готового ответа на первых шагах?

5. unit_test_quality (Качество рубежного теста юнита):
   - Сценарные ли это вопросы уровня тех-собеседования («что сломается / почему / что выбрать»)?
   - Правдоподобны ли дистракторы (не угадываются ли по длине или абсурдности)?
   - Содержат ли объяснения (explain) реальное инженерное «почему»?
   - Учитывай, что тест охватывает весь юнит целиком (включая соседние навыки юнита).

Правила фиксации дефектов (issues):
- Для КАЖДОГО замечания обязательно указывай точный target (например: 'К-001 шаг 3', 'Ф-009 карточка #4', 'Задача #20 (hint)', 'Задача #20 (tests)', 'Рубежный тест 1.1 вопрос #6', 'Замкнутый контур К-001 -> Ф-004').
- Пиши конкретно: приводи короткую цитату или факт проблемы (problem) и точное, выполнимое исправление (fix).
- Классификация severity:
  * critical — грубая ошибка в коде/фактах, ломающая решение; чужеродные материалы из других модулей; сломанная заглушка в тестах; слив решения в hint.
  * major — поверхностное объяснение, слабая формулировка дистрактора, неатомарная карточка.
  * minor — мелкая стилистическая шероховатость.
- Если материал добротный и критических дефектов нет, выставляй оценки 4 или 5 по соответствующим осям. Пиши строго на русском языке."""


L3_FALLBACK_SCHEMA: dict[str, Any] = {
    'type': 'object',
    'description': 'Структурированный результат смыслового аудита L3.',
    'properties': {
        'scores': {
            'type': 'object',
            'properties': {
                'notes_depth': {'type': 'integer', 'minimum': 1, 'maximum': 5},
                'closed_loop': {'type': 'integer', 'minimum': 1, 'maximum': 5},
                'cards_quality': {'type': 'integer', 'minimum': 1, 'maximum': 5},
                'practice_quality': {'type': 'integer', 'minimum': 1, 'maximum': 5},
                'unit_test_quality': {'type': 'integer', 'minimum': 1, 'maximum': 5},
            },
            'required': [
                'notes_depth',
                'closed_loop',
                'cards_quality',
                'practice_quality',
                'unit_test_quality',
            ],
        },
        'issues': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'severity': {'type': 'string', 'enum': ['critical', 'major', 'minor']},
                    'area': {'type': 'string', 'enum': ['note', 'card', 'practice', 'unit_test', 'closed_loop']},
                    'target': {'type': 'string'},
                    'problem': {'type': 'string'},
                    'fix': {'type': 'string'},
                },
                'required': ['severity', 'area', 'target', 'problem', 'fix'],
            },
        },
        'summary': {'type': 'string'},
    },
    'required': ['scores', 'issues', 'summary'],
}

if BaseModel is not None:

    class QualityScores(BaseModel):
        """Оценки по пяти педагогическим и инженерным критериям (1–5)."""

        notes_depth: int = Field(ge=1, le=5, description='Глубина и ясность конспекта, механика под капотом, Junior vs Senior')
        closed_loop: int = Field(ge=1, le=5, description='Смысловой замкнутый контур Zero Surprises: конспект покрывает карточки, практику и тест')
        cards_quality: int = Field(ge=1, le=5, description='Атомарность, самодостаточность и точность флеш-карточек')
        practice_quality: int = Field(ge=1, le=5, description='Инженерная ценность практики, граничные случаи в tests и подсказки Сократа')
        unit_test_quality: int = Field(ge=1, le=5, description='Сценарность вопросов рубежного теста, качество дистракторов и объяснений')

    class QualityIssue(BaseModel):
        """Конкретный выявленный дефект учебного материала."""

        severity: Literal['critical', 'major', 'minor'] = Field(description='Критичность дефекта')
        area: Literal['note', 'card', 'practice', 'unit_test', 'closed_loop'] = Field(description='Область материала')
        target: str = Field(description='Точный идентификатор: К-001 шаг 2, Ф-009 #3, Задача #20 (hint), Вопрос #5 и т.п.')
        problem: str = Field(description='Суть проблемы с конкретной цитатой или деталью')
        fix: str = Field(description='Конкретное и выполнимое исправление')

    class SkillQualityEvaluation(BaseModel):
        """Структурированный результат смыслового аудита L3."""

        scores: QualityScores
        issues: list[QualityIssue]
        summary: str = Field(description='Краткое инженерно-педагогическое резюме качества навыка (2–3 предложения)')


def get_l3_json_schema() -> dict[str, Any]:
    """Возвращает плоскую JSON Schema для L3-аудита."""
    if BaseModel is not None:
        return _inline_json_schema(SkillQualityEvaluation.model_json_schema())
    return copy.deepcopy(L3_FALLBACK_SCHEMA)


def validate_l3_evaluation(raw_eval: dict[str, Any]) -> dict[str, Any]:
    """Валидирует словарь L3-оценки через Pydantic или встроенную проверку схемы."""
    if BaseModel is not None:
        parsed = SkillQualityEvaluation.model_validate(raw_eval)
        return {
            'scores': parsed.scores.model_dump(),
            'issues': [iss.model_dump() for iss in parsed.issues],
            'summary': parsed.summary,
        }

    score_keys = ('notes_depth', 'closed_loop', 'cards_quality', 'practice_quality', 'unit_test_quality')
    scores = raw_eval.get('scores', {})
    clean_scores = {}
    for k in score_keys:
        val = int(scores[k])
        if not 1 <= val <= 5:
            raise ValueError(f'Оценка {k}={val} вне диапазона 1..5')
        clean_scores[k] = val

    clean_issues = []
    for iss in raw_eval.get('issues', []):
        sev = iss['severity']
        area = iss['area']
        if sev not in ('critical', 'major', 'minor'):
            raise ValueError(f'Некорректная критичность: {sev}')
        if area not in ('note', 'card', 'practice', 'unit_test', 'closed_loop'):
            raise ValueError(f'Некорректная область: {area}')
        clean_issues.append({
            'severity': sev,
            'area': area,
            'target': str(iss['target']),
            'problem': str(iss['problem']),
            'fix': str(iss['fix']),
        })

    return {
        'scores': clean_scores,
        'issues': clean_issues,
        'summary': str(raw_eval['summary']),
    }


def load_gemini_api_key() -> str | None:
    """Читает GEMINI_API_KEY из окружения или файла .env в корне репозитория."""
    env_key = os.environ.get('GEMINI_API_KEY', '').strip()
    if env_key:
        return env_key

    if not ENV_PATH.is_file():
        return None

    for raw_line in ENV_PATH.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line[len('export '):].strip()
        if '=' not in line:
            continue
        key, val = line.split('=', 1)
        if key.strip() == 'GEMINI_API_KEY':
            cleaned = val.strip()
            if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in ("'", '"'):
                cleaned = cleaned[1:-1]
            return cleaned or None
    return None


def collect_skill_bundles(
    tier_filter: str,
    skill_ids: set[str] | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Собирает единые пакеты материалов по каждому навыку из standards.html и data/content/."""
    html_text = aca.STANDARDS_HTML.read_text(encoding='utf-8')
    unit_meta = aca.extract_unit_meta(html_text)
    masteries = aca.extract_mastery_objects(html_text)

    notes_json = json.loads((aca.CONTENT_DIR / 'notes.json').read_text(encoding='utf-8'))
    cards_json = json.loads((aca.CONTENT_DIR / 'cards.json').read_text(encoding='utf-8'))
    tasks_list = json.loads((aca.CONTENT_DIR / 'tasks.json').read_text(encoding='utf-8'))
    tasks_by_id = {t['id']: t for t in tasks_list}

    target_tier = None if tier_filter == 'all' else int(tier_filter)
    bundles: list[dict[str, Any]] = []

    for m_name, obj in masteries.items():
        m_notes = obj.get('notes', {})
        m_decks = obj.get('decks', {})
        m_utests = obj.get('unitTests', {})

        for unit in obj.get('units', []):
            uid = unit['id']
            u_tier = unit_meta.get(uid, {}).get('tier', unit.get('tier', 2))
            if skill_ids is None and target_tier is not None and u_tier != target_tier:
                continue

            utest = m_utests.get(uid)
            unit_skills = [
                {
                    'id': s['id'],
                    'title': s.get('title', ''),
                    'notes_titles': [
                        (m_notes.get(k) or notes_json.get(k) or {}).get('title', k)
                        for k in (s.get('notes') or s.get('kIds') or [])
                    ],
                }
                for s in unit.get('skills', [])
            ]
            for skill in unit.get('skills', []):
                sid = skill['id']
                if skill_ids is not None and sid not in skill_ids:
                    continue

                sibling_skills = [s for s in unit_skills if s['id'] != sid]
                k_ids = skill.get('notes') or skill.get('kIds') or []
                f_ids = skill.get('decks') or skill.get('fIds') or []
                t_ids = skill.get('taskIds', [])

                notes_items = []
                for kid in k_ids:
                    note_obj = m_notes.get(kid) or notes_json.get(kid)
                    notes_items.append({
                        'id': kid,
                        'note': note_obj,
                        'canonical_note': notes_json.get(kid),
                    })

                decks_items = []
                for fid in f_ids:
                    deck_obj = m_decks.get(fid) or cards_json.get(fid)
                    decks_items.append({
                        'id': fid,
                        'deck': deck_obj,
                    })

                tasks_items = []
                for tid in t_ids:
                    tasks_items.append({
                        'id': tid,
                        'task': tasks_by_id.get(tid),
                    })

                bundles.append({
                    'skill_id': sid,
                    'unit_id': uid,
                    'unit_title': unit.get('title', ''),
                    'tier': u_tier,
                    'track': m_name,
                    'title': skill.get('title', ''),
                    'sibling_skills': sibling_skills,
                    'notes': notes_items,
                    'decks': decks_items,
                    'tasks': tasks_items,
                    'unit_test': utest,
                })

                if limit is not None and len(bundles) >= limit:
                    return bundles

    return bundles


def compute_bundle_hash(bundle: dict[str, Any]) -> str:
    """Вычисляет детерминированный SHA-256 хэш пакета навыка и текущей версии рубрики."""
    payload = {
        'rubric_version': RUBRIC_VERSION,
        'bundle': bundle,
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def _detect_eaten_angles(raw_html: str) -> list[str]:
    """Ищет неэкранированные псевдо-теги (<token>, <class 'tuple'>) и обрывы форматов в HTML."""
    cleaned_html = re.sub(r'<svg[\s\S]*?</svg>', '', raw_html)
    hits: list[str] = []
    for match in RAW_HTML_TAG_NAME_RE.finditer(cleaned_html):
        tag_name = match.group(1).lower()
        if tag_name not in SAFE_HTML_TAGS:
            hits.append(match.group(0))
    plain = aca.strip_html(cleaned_html)
    if BROKEN_ANGLE_RE.search(plain):
        hits.append('обрыв строки заголовка (вероятно вырезан <...>)')
    return hits


def run_level1(bundle: dict[str, Any]) -> dict[str, Any]:
    """Уровень 1: Гигиена, структура, шаблоны подсказок, битые <...> и перекос тестов."""
    red_flags: list[str] = []
    warnings: list[str] = []

    # 1. Конспекты
    for item in bundle['notes']:
        kid = item['id']
        note_obj = item['note']
        if note_obj is None:
            red_flags.append(f'[{kid}] Конспект не найден ни в standards.html, ни в data/content/notes.json')
            continue
        rep = aca.check_note_quality(kid, note_obj, item['canonical_note'])
        for msg in rep['red_flags']:
            red_flags.append(f'[{kid}] {msg}')
        for msg in rep['warnings']:
            warnings.append(f'[{kid}] {msg}')
        for idx, st in enumerate(note_obj.get('steps', []), 1):
            angle_hits = _detect_eaten_angles(st.get('html', ''))
            if angle_hits:
                red_flags.append(
                    f'[{kid} шаг {idx}] Риск потери текста в угловых скобках (<...>): {", ".join(angle_hits[:3])}'
                )

    # 2. Флеш-карточки
    for item in bundle['decks']:
        fid = item['id']
        deck_obj = item['deck']
        if deck_obj is None:
            red_flags.append(f'[{fid}] Колода карточек не найдена')
            continue
        rep = aca.check_deck_quality(fid, deck_obj)
        for msg in rep['red_flags']:
            red_flags.append(f'[{fid}] {msg}')
        for idx, card in enumerate(deck_obj.get('cards', []), 1):
            for side_name, raw_side in (('вопросе', card.get('q', '')), ('ответе', card.get('a', ''))):
                angle_hits = _detect_eaten_angles(raw_side)
                if angle_hits:
                    red_flags.append(
                        f'[{fid} #{idx}] Повреждение/риск вырезания <...> в {side_name}: {", ".join(angle_hits[:3])}'
                    )

    # 3. Практические задачи + детектор шаблонных заглушек, I/O Flow и копипаста Redis
    for item in bundle['tasks']:
        tid = item['id']
        task_obj = item['task']
        rep = aca.check_task_quality(tid, task_obj)
        for msg in rep['red_flags']:
            red_flags.append(f'[Задача #{tid}] {msg}')
        for msg in rep['warnings']:
            warnings.append(f'[Задача #{tid}] {msg}')

        if task_obj is not None:
            hint_text = task_obj.get('hint', '')
            if any(p in hint_text for p in STUB_HINT_PATTERNS):
                red_flags.append(
                    f'[Задача #{tid}] Шаблонная подсказка-заглушка в hint вместо ступеней Сократа'
                )
            desc_text = task_obj.get('desc', '')
            stub_io = [p for p in STUB_IO_FLOW_PATTERNS if p in desc_text]
            if stub_io:
                red_flags.append(
                    f'[Задача #{tid}] Шаблонная заглушка в I/O Flow условия: {", ".join(stub_io)}'
                )
            tests_text = task_obj.get('tests', '')
            context_text = ' '.join([
                task_obj.get('title', ''),
                desc_text,
                task_obj.get('solution', ''),
            ]).lower()
            if ('r._store' in tests_text or 'r.store' in tests_text) and 'redis' not in context_text:
                warnings.append(
                    f'[Задача #{tid}] Посторонний код очистки Redis (r._store/r.store) в tests'
                )

    # 4. Рубежный тест юнита + детектор перекоса ответов и длин
    ut_rep = aca.check_unit_test_quality(bundle['unit_id'], bundle['tier'], bundle['unit_test'])
    for msg in ut_rep['red_flags']:
        red_flags.append(f'[Тест {bundle["unit_id"]}] {msg}')
    for msg in ut_rep['warnings']:
        warnings.append(f'[Тест {bundle["unit_id"]}] {msg}')

    utest = bundle['unit_test']
    if utest and len(utest.get('questions', [])) >= 4:
        qs = utest['questions']
        corr_counts: dict[int, int] = {}
        corr_lens: list[int] = []
        dist_lens: list[int] = []
        for q_item in qs:
            opts = q_item.get('options', [])
            corr = q_item.get('correct')
            if isinstance(corr, int) and 0 <= corr < len(opts):
                corr_counts[corr] = corr_counts.get(corr, 0) + 1
                corr_lens.append(len(aca.strip_html(str(opts[corr]))))
                for i, opt in enumerate(opts):
                    if i != corr:
                        dist_lens.append(len(aca.strip_html(str(opt))))

        if corr_counts:
            top_idx, top_cnt = max(corr_counts.items(), key=lambda kv: kv[1])
            share = top_cnt / len(qs)
            if share >= 0.75:
                red_flags.append(
                    f'[Тест {bundle["unit_id"]}] Перекос индексов ответов: {top_cnt}/{len(qs)} '
                    f'({round(share * 100)}%) правильных ответов на индексе {top_idx}'
                )
        if corr_lens and dist_lens:
            med_corr = statistics.median(corr_lens)
            med_dist = statistics.median(dist_lens)
            if med_dist > 0 and (med_corr / med_dist) > 2.5:
                red_flags.append(
                    f'[Тест {bundle["unit_id"]}] Верный ответ угадывается по длине: '
                    f'медиана верных {med_corr:.0f} симв. vs дистракторов {med_dist:.0f} симв. '
                    f'({med_corr / med_dist:.1f}x)'
                )

    return {
        'passed': len(red_flags) == 0,
        'red_flags': red_flags,
        'warnings': warnings,
    }


@contextlib.contextmanager
def _isolated_exec_env():
    """Сохраняет и полностью восстанавливает глобальное состояние Python-процесса вокруг exec()."""
    orig_modules = dict(sys.modules)
    orig_open = builtins.open
    orig_sleep = time.sleep
    orig_urlopen = urllib.request.urlopen
    orig_model_dump = BaseModel.model_dump if BaseModel is not None else None

    path_attrs = ('read_text', 'write_text', 'mkdir', 'rglob', 'stat', 'iterdir', 'glob', 'open')
    orig_path_methods = {attr: getattr(pathlib.Path, attr) for attr in path_attrs}

    import multiprocessing as mp_mod
    orig_mp_process = mp_mod.Process
    import concurrent.futures as cf_mod
    orig_cf_process_pool = getattr(cf_mod, 'ProcessPoolExecutor', None)

    try:
        yield
    finally:
        # Восстанавливаем sys.modules строго к исходному снимку
        for mod_name in list(sys.modules.keys()):
            if mod_name not in orig_modules:
                sys.modules.pop(mod_name, None)
        for mod_name, mod_obj in orig_modules.items():
            sys.modules[mod_name] = mod_obj

        builtins.open = orig_open
        time.sleep = orig_sleep
        urllib.request.urlopen = orig_urlopen
        if BaseModel is not None and orig_model_dump is not None:
            BaseModel.model_dump = orig_model_dump

        for attr, fn in orig_path_methods.items():
            setattr(pathlib.Path, attr, fn)

        mp_mod.Process = orig_mp_process
        if orig_cf_process_pool is not None:
            cf_mod.ProcessPoolExecutor = orig_cf_process_pool


def _exec_task_in_sandbox(env_code: str, user_code: str, tests_code: str) -> tuple[bool, str]:
    """Запускает код задачи и её тесты в изолированном модуле __main__."""
    with _isolated_exec_env():
        mod = types.ModuleType('__main__')
        sys.modules['__main__'] = mod
        ns = mod.__dict__
        buf_out = io.StringIO()
        buf_err = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
                exec(env_code, ns)
                exec(user_code, ns)
                ns['__USER_CODE__'] = user_code
                exec(tests_code, ns)
            return True, ''
        except Exception as exc:
            return False, f'{type(exc).__name__}: {exc}'


def _parse_python_snippet(code_text: str) -> tuple[bool, str]:
    """Проверяет синтаксис Python-сниппета через ast.parse с поддержкой top-level await."""
    try:
        ast.parse(code_text)
        return True, ''
    except SyntaxError as exc:
        if 'await' in str(exc) or 'await ' in code_text:
            indented = '\n'.join('    ' + ln for ln in code_text.splitlines())
            wrapped = f'async def __ast_async_check__():\n{indented}\n'
            try:
                ast.parse(wrapped)
                return True, ''
            except SyntaxError as async_exc:
                return False, f'SyntaxError (строка {async_exc.lineno}): {async_exc.msg}'
        return False, f'SyntaxError (строка {exc.lineno}): {exc.msg}'


def run_level2(bundle: dict[str, Any]) -> dict[str, Any]:
    """Уровень 2: Исполняемость практики, статический анализ задач и AST-валидация сниппетов конспектов."""
    errors: list[str] = []
    warnings: list[str] = []
    tasks_checked = 0
    snippets_checked = 0

    env_code = task_runner.full_env_code

    # 1. Прогон практических задач (Positive + Negative + Static)
    for item in bundle['tasks']:
        tid = item['id']
        task = item['task']
        if task is None:
            continue
        tasks_checked += 1

        solution = task.get('solution', '')
        initial_code = task.get('initialCode', '')
        tests = task.get('tests', '')
        desc_plain = aca.strip_html(task.get('title', '') + ' ' + task.get('desc', ''))

        # Positive check: эталонное решение должно проходить тесты
        ok_pos, err_pos = _exec_task_in_sandbox(env_code, solution, tests)
        if not ok_pos:
            errors.append(f'[Задача #{tid}] Эталонное solution не прошло tests -> {err_pos}')

        # Negative check: стартовый шаблон должен падать на тестах
        ok_neg, err_neg = _exec_task_in_sandbox(env_code, initial_code, tests)
        if ok_neg:
            errors.append(f'[Задача #{tid}] Фиктивные тесты: initialCode прошёл tests без реализации')
        elif ':' in err_neg and not err_neg.split(':', 1)[1].strip():
            warnings.append(f'[Задача #{tid}] initialCode упал с пустым сообщением об ошибке ({err_neg})')

        # Статический анализ на абстрактные foo/bar/baz
        for field_name, content in (('desc', desc_plain), ('initialCode', initial_code), ('solution', solution)):
            hits = sorted(set(ABSTRACT_IDENT_RE.findall(content)))
            if hits:
                warnings.append(f'[Задача #{tid}] Абстрактный идентификатор ({", ".join(hits)}) в {field_name}')

        # Проверка длины строк кода в solution/initialCode (под 390px мобильный экран)
        for field_name, code_str in (('initialCode', initial_code), ('solution', solution)):
            long_lens = [
                len(ln)
                for ln in code_str.splitlines()
                if ln.strip() and not ln.lstrip().startswith('#') and len(ln) > MAX_CODE_LINE_LEN
            ]
            if long_lens:
                warnings.append(
                    f'[Задача #{tid}] Строки в {field_name} > {MAX_CODE_LINE_LEN} симв.: '
                    f'{len(long_lens)} шт. (макс. {max(long_lens)})'
                )

    # 2. AST-валидация Python-сниппетов в конспектах
    for item in bundle['notes']:
        kid = item['id']
        note = item['note']
        if not note:
            continue
        for idx, step in enumerate(note.get('steps', []), 1):
            step_html = step.get('html', '')
            for lang, raw_code in SNIPPET_RE.findall(step_html):
                lang_norm = (lang or '').strip().lower()
                if lang_norm not in ('python', 'py', ''):
                    continue
                code_text = html_lib.unescape(raw_code).strip()
                if not code_text:
                    continue
                if lang_norm == '' and code_text.lstrip().startswith(('<', '{', 'SELECT ', 'GET ', 'POST ', '$ ', 'git ')):
                    continue

                snippets_checked += 1
                ok_ast, err_ast = _parse_python_snippet(code_text)
                if not ok_ast:
                    # Если сниппет явно демонстрирует SyntaxError в обучающих целях
                    if 'SyntaxError' in code_text or 'синтаксическая ошибка' in aca.strip_html(step_html).lower():
                        warnings.append(f'[{kid} шаг {idx}] Сниппет с ожидаемой синтаксической ошибкой: {err_ast}')
                    else:
                        errors.append(f'[{kid} шаг {idx}] Невалидный Python-сниппет: {err_ast}')

    return {
        'passed': len(errors) == 0,
        'tasks_checked': tasks_checked,
        'snippets_checked': snippets_checked,
        'errors': errors,
        'warnings': warnings,
    }


def _html_to_readable_markdown(raw_html: str) -> str:
    """Преобразует HTML конспекта или задачи в чистый текст, сохраняя отступы в блоках кода."""
    text = re.sub(r'<svg[\s\S]*?</svg>', '', raw_html)
    code_blocks: list[str] = []

    def _repl_pre(match: re.Match[str]) -> str:
        lang = (match.group(1) or '').strip().lower()
        code = html_lib.unescape(match.group(2)).strip('\n')
        token = f'\n@@CODE_BLOCK_{len(code_blocks)}@@\n'
        code_blocks.append(f'```{lang}\n{code}\n```')
        return token

    text = re.sub(
        r'(?:<span class="code-lang-tag">([^<]+)</span>[\s\S]*?)?<pre><code>([\s\S]*?)</code></pre>',
        _repl_pre,
        text,
    )
    inline_codes: list[str] = []

    def _repl_inline(m: re.Match[str]) -> str:
        token = f'@@INLINE_CODE_{len(inline_codes)}@@'
        inline_codes.append(f'`{html_lib.unescape(m.group(1))}`')
        return token

    text = re.sub(r'<code>([\s\S]*?)</code>', _repl_inline, text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</(?:p|div|li|tr|h[1-6])>', '\n', text)
    text = re.sub(r'<(?:td|th)[^>]*>', ' | ', text)
    text = re.sub(r'</?(?:strong|em|b|i|span|a)\b[^>]*>', '', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html_lib.unescape(text)
    lines = [re.sub(r'[ \t]+', ' ', ln).strip() for ln in text.splitlines()]
    cleaned = '\n'.join(ln for ln in lines if ln)

    for idx, incode in enumerate(inline_codes):
        cleaned = cleaned.replace(f'@@INLINE_CODE_{idx}@@', incode)

    for idx, block in enumerate(code_blocks):
        cleaned = cleaned.replace(f'@@CODE_BLOCK_{idx}@@', block)
    return re.sub(r'\n{3,}', '\n\n', cleaned)


def format_bundle_for_llm(bundle: dict[str, Any]) -> str:
    """Форматирует весь пакет навыка (Конспект + Карточки + Практика + Тест) для ревьюера L3."""
    parts: list[str] = [
        f'# Навык {bundle["skill_id"]}: {bundle["title"]}',
        f'Трек: {bundle["track"]} | Юнит {bundle["unit_id"]}: {bundle["unit_title"]} | Эшелон: {bundle["tier"]}',
        '',
        '## 1. КОНСПЕКТЫ',
    ]

    for item in bundle['notes']:
        kid = item['id']
        note = item['note']
        if not note:
            parts.append(f'### {kid}: [ОТСУТСТВУЕТ]')
            continue
        parts.append(f'### {kid}: {note.get("title", "")}')
        for idx, st in enumerate(note.get('steps', []), 1):
            parts.append(f'#### Шаг {idx}: {st.get("title", "")}')
            step_html = re.sub(r'^\s*<h4[^>]*>[\s\S]*?</h4>\s*', '', st.get('html', ''), count=1)
            parts.append(_html_to_readable_markdown(step_html))
        parts.append('')

    parts.append('## 2. ФЛЕШ-КАРТОЧКИ (SRS)')
    for item in bundle['decks']:
        fid = item['id']
        deck = item['deck']
        if not deck:
            parts.append(f'### {fid}: [ОТСУТСТВУЕТ]')
            continue
        parts.append(f'### {fid}: {deck.get("title", "")} (карточек: {len(deck.get("cards", []))})')
        for idx, card in enumerate(deck.get('cards', []), 1):
            q_txt = _html_to_readable_markdown(card.get('q', ''))
            a_txt = _html_to_readable_markdown(card.get('a', ''))
            parts.append(f'- Карточка #{idx}:\n  Вопрос: {q_txt}\n  Ответ: {a_txt}')
        parts.append('')

    parts.append('## 3. ПРАКТИЧЕСКИЕ ЗАДАЧИ (ZEN IDE)')
    if not bundle['tasks']:
        parts.append('[Практические задачи отсутствуют]')
    for item in bundle['tasks']:
        tid = item['id']
        task = item['task']
        if not task:
            parts.append(f'### Задача #{tid}: [ОТСУТСТВУЕТ]')
            continue
        parts.append(f'### Задача #{tid}: {task.get("title", "")}')
        parts.append(f'Условие:\n{_html_to_readable_markdown(task.get("desc", ""))}')
        parts.append(f'initialCode:\n```python\n{task.get("initialCode", "")}\n```')
        parts.append(f'solution:\n```python\n{task.get("solution", "")}\n```')
        parts.append(f'hint (подсказки Сократа):\n{task.get("hint", "")}')
        parts.append(f'tests:\n```python\n{task.get("tests", "")}\n```')
        parts.append('')

    parts.append('## 4. РУБЕЖНЫЙ ТЕСТ ЮНИТА')
    siblings = bundle.get('sibling_skills', [])
    if siblings:
        parts.append('Другие навыки этого юнита (покрываются тем же рубежным тестом):')
        for sib in siblings:
            nt = sib.get('notes_titles', [])
            nt_str = f' [конспекты: {"; ".join(nt)}]' if nt else ''
            parts.append(f'- {sib["id"]}: {sib["title"]}{nt_str}')
        parts.append('')
    utest = bundle['unit_test']
    if not utest:
        parts.append('[Рубежный тест отсутствует]')
    else:
        parts.append(f'Тест юнита {bundle["unit_id"]}: {utest.get("title", "")}')
        for idx, q_item in enumerate(utest.get('questions', []), 1):
            opts = q_item.get('options', [])
            corr = q_item.get('correct')
            expl = q_item.get('explain') or q_item.get('hint') or ''
            parts.append(f'- Вопрос #{idx}: {_html_to_readable_markdown(q_item.get("q", ""))}')
            for opt_i, opt in enumerate(opts):
                mark = ' [ВЕРНЫЙ]' if opt_i == corr else ''
                parts.append(f'  {opt_i}. {opt}{mark}')
            parts.append(f'  Объяснение: {expl}')

    return '\n'.join(parts)


def _inline_json_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Разворачивает $defs/$ref и удаляет title для максимальной совместимости с Gemini response_format."""
    defs = copy.deepcopy(schema.get('$defs', {}))

    def _resolve(node: Any) -> Any:
        if isinstance(node, list):
            return [_resolve(item) for item in node]
        if not isinstance(node, dict):
            return node
        if '$ref' in node:
            ref_name = node['$ref'].split('/')[-1]
            target = copy.deepcopy(defs.get(ref_name, {}))
            # Сохраняем description, если оно было рядом с $ref
            if 'description' in node and 'description' not in target:
                target['description'] = node['description']
            return _resolve(target)

        out: dict[str, Any] = {}
        for k, v in node.items():
            if k in ('$defs', 'title'):
                continue
            out[k] = _resolve(v)
        return out

    return _resolve(schema)


def run_level3_gemini(bundle: dict[str, Any], api_key: str, model_name: str) -> dict[str, Any]:
    """Уровень 3: Смысловой и педагогический аудит через Google GenAI Interactions API."""
    from google import genai

    client = genai.Client(api_key=api_key)
    payload = format_bundle_for_llm(bundle)
    response_schema = _inline_json_schema(SkillQualityEvaluation.model_json_schema())

    last_err: Exception | None = None
    for attempt in range(1, 4):
        try:
            interaction = client.interactions.create(
                model=model_name,
                system_instruction=L3_SYSTEM_PROMPT,
                input=payload,
                store=False,
                response_format={
                    'type': 'text',
                    'mime_type': 'application/json',
                    'schema': response_schema,
                },
                generation_config={'temperature': 0.2},
            )
            raw_text = interaction.output_text
            if not raw_text:
                raise RuntimeError('Модель вернула пустой output_text')
            parsed = SkillQualityEvaluation.model_validate_json(raw_text)
            return {
                'model': model_name,
                'scores': parsed.scores.model_dump(),
                'issues': [iss.model_dump() for iss in parsed.issues],
                'summary': parsed.summary,
                'usage': interaction.usage.model_dump() if getattr(interaction, 'usage', None) else None,
            }
        except Exception as exc:
            last_err = exc
            if attempt < 3:
                time.sleep(2 * attempt)

    raise RuntimeError(f'Ошибка обращения к Gemini API для навыка {bundle["skill_id"]}: {last_err}') from last_err


def compute_verdict(l1: dict[str, Any], l2: dict[str, Any] | None, l3: dict[str, Any] | None) -> str:
    """Определяет итоговый статус навыка на основе результатов L1, L2 и L3."""
    if not l1['passed']:
        return 'NEEDS_FIX'
    if l2 is not None and not l2['passed']:
        return 'NEEDS_FIX'
    if l3 is not None:
        scores = l3['scores'].values()
        has_critical = any(iss['severity'] == 'critical' for iss in l3.get('issues', []))
        if min(scores) < 4 or has_critical:
            return 'NEEDS_FIX'
        return 'PASS'
    return 'L1_L2_PASS_NO_LLM'


def load_ledger() -> dict[str, Any]:
    """Загружает реестр качества data/quality_ledger.json."""
    if LEDGER_PATH.is_file():
        return json.loads(LEDGER_PATH.read_text(encoding='utf-8'))
    return {'_meta': {'rubric_version': RUBRIC_VERSION}, 'skills': {}}


def save_ledger(ledger: dict[str, Any]) -> None:
    """Сохраняет реестр качества в data/quality_ledger.json."""
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    ledger['_meta'] = {
        'rubric_version': RUBRIC_VERSION,
        'updated_at': dt.datetime.now().isoformat(timespec='seconds'),
        'skills_count': len(ledger.get('skills', {})),
    }
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding='utf-8')


def write_markdown_report(entries: list[dict[str, Any]]) -> None:
    """Формирует человекочитаемый отчёт data/quality_report.md по результатам прогона."""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        '# Паспорт качества учебных материалов (Content Quality Gate)',
        '',
        f'Обновлено: `{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}` | Версия рубрики: `{RUBRIC_VERSION}`',
        '',
        '| Навык | Эшелон | Статус | L1 (RF/W) | L2 (Err/W) | L3 (N/CL/C/P/T) | Критич. |',
        '| :--- | :---: | :--- | :---: | :---: | :---: | :---: |',
    ]

    for e in entries:
        l1 = e['l1']
        l2 = e.get('l2')
        l3 = e.get('l3')
        l1_str = f'{len(l1["red_flags"])} / {len(l1["warnings"])}'
        l2_str = f'{len(l2["errors"])} / {len(l2["warnings"])}' if l2 else '—'
        if l3:
            sc = l3['scores']
            l3_str = (
                f'{sc["notes_depth"]}/{sc["closed_loop"]}/'
                f'{sc["cards_quality"]}/{sc["practice_quality"]}/{sc["unit_test_quality"]}'
            )
            crit_cnt = sum(1 for i in l3.get('issues', []) if i['severity'] == 'critical')
        else:
            l3_str = 'не запускался'
            crit_cnt = 0

        lines.append(
            f'| `{e["skill_id"]}` {e["title"][:42]} | Э{e["tier"]} | **{e["verdict"]}** | '
            f'{l1_str} | {l2_str} | {l3_str} | {crit_cnt} |'
        )

    lines.append('')
    lines.append('## Детализация замечаний')
    lines.append('')

    for e in entries:
        lines.append(f'### Навык `{e["skill_id"]}` — {e["title"]} (`{e["verdict"]}`)')
        l1 = e['l1']
        l2 = e.get('l2')
        l3 = e.get('l3')

        if l1['red_flags']:
            lines.append('- **L1 Red Flags:**')
            for msg in l1['red_flags']:
                lines.append(f'  - `{msg}`')
        if l1['warnings']:
            lines.append('- **L1 Предупреждения:**')
            for msg in l1['warnings']:
                lines.append(f'  - {msg}')
        if l2 and l2['errors']:
            lines.append('- **L2 Ошибки исполнения:**')
            for msg in l2['errors']:
                lines.append(f'  - `{msg}`')
        if l2 and l2['warnings']:
            lines.append('- **L2 Замечания статического анализа:**')
            for msg in l2['warnings']:
                lines.append(f'  - {msg}')
        if l3:
            lines.append(f'- **L3 Резюме ({l3["model"]}):** {l3["summary"]}')
            if l3.get('issues'):
                lines.append('- **L3 Замечания:**')
                for iss in l3['issues']:
                    lines.append(
                        f'  - **[{iss["severity"].upper()} | {iss["area"]}] {iss["target"]}**: '
                        f'{iss["problem"]} -> *Исправление:* {iss["fix"]}'
                    )
        lines.append('')

    REPORT_PATH.write_text('\n'.join(lines), encoding='utf-8')


def print_console_summary(entries: list[dict[str, Any]], l3_skipped_reason: str | None) -> None:
    """Печатает компактную сводку в терминал."""
    print('=' * 78)
    print(f'CONTENT QUALITY GATE (Рубрика v{RUBRIC_VERSION}) | Навыков проверено: {len(entries)}')
    print('=' * 78)

    for e in entries:
        l1 = e['l1']
        l2 = e.get('l2')
        l3 = e.get('l3')
        cache_mark = ' [КЭШ]' if e.get('_from_cache') else ''
        print(f'\n[{e["verdict"]}] {e["skill_id"]} (Э{e["tier"]}): {e["title"]}{cache_mark}')
        print(
            f'  L1 Гигиена: Red Flags={len(l1["red_flags"])}, Предупреждения={len(l1["warnings"])}'
        )
        if l2 is not None:
            print(
                f'  L2 Исполняемость: задач={l2["tasks_checked"]}, сниппетов={l2["snippets_checked"]} | '
                f'Ошибки={len(l2["errors"])}, Предупреждения={len(l2["warnings"])}'
            )
        if l3 is not None:
            sc = l3['scores']
            print(
                f'  L3 Смысл ({l3["model"]}): конспект={sc["notes_depth"]}/5, контур={sc["closed_loop"]}/5, '
                f'карточки={sc["cards_quality"]}/5, практика={sc["practice_quality"]}/5, тест={sc["unit_test_quality"]}/5 | '
                f'Дефекты={len(l3.get("issues", []))}'
            )

        for msg in l1['red_flags']:
            print(f'    [L1 RED] {msg}')
        for msg in (l2['errors'] if l2 else []):
            print(f'    [L2 ERR] {msg}')
        for msg in (l2['warnings'] if l2 else []):
            print(f'    [L2 WARN] {msg}')
        if l3:
            for iss in l3.get('issues', []):
                print(f'    [L3 {iss["severity"].upper()}] {iss["target"]}: {iss["problem"]}')

    print('\n' + '-' * 78)
    pass_cnt = sum(1 for e in entries if e['verdict'] == 'PASS')
    fix_cnt = sum(1 for e in entries if e['verdict'] == 'NEEDS_FIX')
    part_cnt = sum(1 for e in entries if e['verdict'] == 'L1_L2_PASS_NO_LLM')
    print(f'ИТОГО: PASS={pass_cnt} | L1+L2 OK (без L3)={part_cnt} | NEEDS_FIX={fix_cnt}')
    print(f'Реестр: {LEDGER_PATH}')
    print(f'Отчёт:  {REPORT_PATH}')

    if l3_skipped_reason:
        print(f'\n[INFO] Смысловой аудит L3 пропущен: {l3_skipped_reason}')
        print('Рекомендуемый запуск (без API-ключей, через встроенный воркфлоу агентов):')
        print('  Передайте scripts/quality_gate_workflow.py в инструмент run_workflow.')
        print('Альтернативный режим через Gemini API:')
        print('  PowerShell: $env:GEMINI_API_KEY="ваш_ключ"; python scripts/quality_gate.py --gemini-api --skills ...')


def _export_l3_queue(
    queue_path: Path,
    bundles: list[dict[str, Any]],
    ledger: dict[str, Any],
    max_level: int,
    force: bool,
) -> int:
    """Выполняет L1/L2, обновляет реестр и сохраняет очередь навыков для L3-агентов."""
    ledger_skills = ledger.setdefault('skills', {})
    queue_items: list[dict[str, Any]] = []

    for bundle in bundles:
        sid = bundle['skill_id']
        bundle_hash = compute_bundle_hash(bundle)
        cached = ledger_skills.get(sid)
        cache_valid = (
            not force
            and cached is not None
            and cached.get('content_hash') == bundle_hash
            and cached.get('rubric_version') == RUBRIC_VERSION
        )

        if cache_valid:
            l1_res = cached['l1']
            l2_res = cached.get('l2')
            l3_res = cached.get('l3')
            if max_level >= 2 and l2_res is None:
                l2_res = run_level2(bundle)
        else:
            l1_res = run_level1(bundle)
            l2_res = run_level2(bundle) if max_level >= 2 else None
            l3_res = None

        verdict = compute_verdict(l1_res, l2_res, l3_res)
        ledger_skills[sid] = {
            'skill_id': sid,
            'unit_id': bundle['unit_id'],
            'tier': bundle['tier'],
            'track': bundle['track'],
            'title': bundle['title'],
            'content_hash': bundle_hash,
            'rubric_version': RUBRIC_VERSION,
            'updated_at': dt.datetime.now().isoformat(timespec='seconds'),
            'verdict': verdict,
            'l1': l1_res,
            'l2': l2_res,
            'l3': l3_res,
        }

        if force or not cache_valid or l3_res is None:
            queue_items.append({
                'skill_id': sid,
                'title': bundle['title'],
                'tier': bundle['tier'],
                'content_hash': bundle_hash,
                'payload': format_bundle_for_llm(bundle),
            })

    save_ledger(ledger)
    queue_data = {
        'rubric_version': RUBRIC_VERSION,
        'schema': get_l3_json_schema(),
        'system_prompt': L3_SYSTEM_PROMPT,
        'items': queue_items,
    }
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    queue_path.write_text(json.dumps(queue_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Экспортирована очередь L3: {len(queue_items)} из {len(bundles)} навыков -> {queue_path}')
    return 0


def _import_l3_results(
    results_path: Path,
    bundles: list[dict[str, Any]],
    ledger: dict[str, Any],
    strict: bool,
) -> int:
    """Импортирует L3-оценки от агентского воркфлоу, пересчитывает вердикты и обновляет отчёт."""
    if not results_path.is_file():
        print(f'Файл результатов L3 не найден: {results_path}')
        return 1

    raw_data = json.loads(results_path.read_text(encoding='utf-8'))
    results_map: dict[str, Any] = raw_data.get('results', {})
    ledger_skills = ledger.setdefault('skills', {})
    processed_entries: list[dict[str, Any]] = []

    for bundle in bundles:
        sid = bundle['skill_id']
        entry = ledger_skills.get(sid)
        if entry is None:
            l1_res = run_level1(bundle)
            l2_res = run_level2(bundle)
            entry = {
                'skill_id': sid,
                'unit_id': bundle['unit_id'],
                'tier': bundle['tier'],
                'track': bundle['track'],
                'title': bundle['title'],
                'content_hash': compute_bundle_hash(bundle),
                'rubric_version': RUBRIC_VERSION,
                'updated_at': dt.datetime.now().isoformat(timespec='seconds'),
                'verdict': 'L1_L2_PASS_NO_LLM',
                'l1': l1_res,
                'l2': l2_res,
                'l3': None,
            }

        if sid in results_map:
            raw_eval = results_map[sid]
            clean_eval = validate_l3_evaluation(raw_eval)
            entry['l3'] = {
                'model': raw_eval.get('model', 'antigravity-workflow'),
                'scores': clean_eval['scores'],
                'issues': clean_eval['issues'],
                'summary': clean_eval['summary'],
                'usage': None,
            }
            entry['updated_at'] = dt.datetime.now().isoformat(timespec='seconds')

        entry['verdict'] = compute_verdict(entry['l1'], entry.get('l2'), entry.get('l3'))
        ledger_skills[sid] = entry
        display_entry = dict(entry)
        display_entry['_from_cache'] = sid not in results_map
        processed_entries.append(display_entry)

    save_ledger(ledger)
    write_markdown_report(processed_entries)
    print_console_summary(processed_entries, None)

    if strict and any(e['verdict'] == 'NEEDS_FIX' for e in processed_entries):
        return 1
    return 0


def main() -> int:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(
        description='Единая трёхуровневая система проверки качества учебных материалов (L1 + L2 + L3)',
    )
    parser.add_argument(
        '--tier',
        choices=['1', '2', '3', '4', 'all'],
        default='1',
        help='Фильтр по эшелону (по умолчанию: 1)',
    )
    parser.add_argument(
        '--skills',
        help='Список ID навыков через запятую (например: 1.1.1,1.5.3,2.2.1)',
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Ограничить число проверяемых навыков (удобно для пилотного запуска)',
    )
    parser.add_argument(
        '--levels',
        choices=['1', '2', '3'],
        default='3',
        help='Максимальный уровень проверки: 1 (L1), 2 (L1+L2), 3 (L1+L2+L3, по умолчанию)',
    )
    parser.add_argument(
        '--no-llm',
        action='store_true',
        help='Выполнить только детерминированные проверки L1 + L2 без L3',
    )
    parser.add_argument(
        '--gemini-api',
        action='store_true',
        help='Явно использовать внешний Gemini API (требуется GEMINI_API_KEY) для уровня L3',
    )
    parser.add_argument(
        '--export-l3-queue',
        dest='export_l3_queue',
        help='Выполнить L1/L2 и сохранить JSON-очередь для воркфлоу run_workflow',
    )
    parser.add_argument(
        '--import-l3-results',
        dest='import_l3_results',
        help='Импортировать JSON с оценками L3 от воркфлоу и обновить отчёт',
    )
    parser.add_argument(
        '--model',
        default=DEFAULT_MODEL,
        help=f'Модель Gemini API для режима --gemini-api (по умолчанию: {DEFAULT_MODEL})',
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Игнорировать кэш SHA-256 хэшей и перепроверить заново',
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Возвращать код выхода 1, если хотя бы один навык получил статус NEEDS_FIX',
    )
    args = parser.parse_args()

    if args.export_l3_queue and args.import_l3_results:
        print('Нельзя одновременно указывать --export-l3-queue и --import-l3-results.')
        return 1

    max_level = 2 if args.no_llm else int(args.levels)
    skill_set = (
        {s.strip() for s in args.skills.split(',') if s.strip()}
        if args.skills
        else None
    )

    bundles = collect_skill_bundles(args.tier, skill_set, args.limit)
    if not bundles:
        print('Не найдено ни одного навыка по заданным фильтрам.')
        return 1

    ledger = load_ledger()

    if args.export_l3_queue:
        return _export_l3_queue(Path(args.export_l3_queue), bundles, ledger, max_level, args.force)

    if args.import_l3_results:
        return _import_l3_results(Path(args.import_l3_results), bundles, ledger, args.strict)

    api_key: str | None = None
    l3_skipped_reason: str | None = None
    run_l3 = max_level >= 3
    if run_l3:
        api_key = load_gemini_api_key()
        if not api_key:
            run_l3 = False
            if args.gemini_api:
                print('Ошибка: указан --gemini-api, но GEMINI_API_KEY не найден в окружении и .env.')
                return 1
            l3_skipped_reason = 'внешний GEMINI_API_KEY не задан (для L3 без ключа используйте run_workflow)'
    ledger_skills = ledger.setdefault('skills', {})
    processed_entries: list[dict[str, Any]] = []

    for bundle in bundles:
        sid = bundle['skill_id']
        bundle_hash = compute_bundle_hash(bundle)
        cached = ledger_skills.get(sid)
        cache_valid = (
            not args.force
            and cached is not None
            and cached.get('content_hash') == bundle_hash
            and cached.get('rubric_version') == RUBRIC_VERSION
        )

        used_cache = False
        if cache_valid:
            l1_res = cached['l1']
            l2_res = cached.get('l2')
            l3_res = cached.get('l3')
            if max_level >= 2 and l2_res is None:
                l2_res = run_level2(bundle)
            else:
                used_cache = True
            if run_l3 and (l3_res is None or l3_res.get('model') != args.model):
                l3_res = run_level3_gemini(bundle, api_key, args.model)
                used_cache = False
        else:
            l1_res = run_level1(bundle)
            l2_res = run_level2(bundle) if max_level >= 2 else None
            l3_res = run_level3_gemini(bundle, api_key, args.model) if run_l3 else None

        verdict = compute_verdict(l1_res, l2_res, l3_res)
        entry = {
            'skill_id': sid,
            'unit_id': bundle['unit_id'],
            'tier': bundle['tier'],
            'track': bundle['track'],
            'title': bundle['title'],
            'content_hash': bundle_hash,
            'rubric_version': RUBRIC_VERSION,
            'updated_at': dt.datetime.now().isoformat(timespec='seconds'),
            'verdict': verdict,
            'l1': l1_res,
            'l2': l2_res,
            'l3': l3_res,
        }
        ledger_skills[sid] = entry

        display_entry = dict(entry)
        display_entry['_from_cache'] = used_cache
        processed_entries.append(display_entry)

    save_ledger(ledger)
    write_markdown_report(processed_entries)
    print_console_summary(processed_entries, l3_skipped_reason)

    if args.strict and any(e['verdict'] == 'NEEDS_FIX' for e in processed_entries):
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
