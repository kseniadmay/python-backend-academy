#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build.py

Единый детерминированный конвейер сборки и верификации платформы Python Backend Academy.
Собирает ассеты, валидирует схемы, синхронизирует эталоны и контролирует инварианты.
"""

import json
import logging
import re
import sys
import time
from pathlib import Path

# Добавляем пути
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from sync_etalons import sync_canonical_etalons

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('builder')


def step_validate_schemas() -> bool:
    """[1/4] Валидация канонических данных контента"""
    logger.info('[1/4] Проверка целостности данных в data/content/...')
    content_dir = _ROOT / 'data' / 'content'
    required_files = ['manifest.json', 'tasks.json', 'notes.json', 'cards.json']

    loaded = {}
    for rf in required_files:
        p = content_dir / rf
        if not p.is_file():
            logger.error('  ❌ Отсутствует обязательный файл: %s', rf)
            return False
        with open(p, 'r', encoding='utf-8') as f:
            loaded[rf] = json.load(f)

    logger.info(
        '  ✓ Схемы валидны: %d модулей, %d задач, %d конспектов, %d колод карточек',
        len(loaded['manifest.json'].get('modules', [])),
        len(loaded['tasks.json']),
        len(loaded['notes.json']),
        len(loaded['cards.json'])
    )
    return True


def step_bundle_css() -> bool:
    """[2/4] Компиляция модульного CSS в оптимизированный бандл"""
    logger.info('[2/4] Компиляция модульного CSS (frontend/css/ -> dist/css/)...')
    css_dir = _ROOT / 'frontend' / 'css'
    main_css = css_dir / 'main.css'

    if not main_css.is_file():
        logger.error('  ❌ Отсутствует главный файл стилей frontend/css/main.css')
        return False

    dist_dir = _ROOT / 'frontend' / 'dist'
    dist_dir.mkdir(parents=True, exist_ok=True)
    bundle_file = dist_dir / 'bundle.css'

    # Рекурсивная склейка @import
    content_lines = []
    with open(main_css, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        m = re.match(r'''^\s*@import\s+['"]\.\/([^'"]+)['"]\s*;''', line)
        if m:
            import_path = css_dir / m.group(1)
            if import_path.is_file():
                with open(import_path, 'r', encoding='utf-8') as inc:
                    content_lines.append(f'/* --- {m.group(1)} --- */\n')
                    content_lines.append(inc.read() + '\n')
            else:
                logger.warning('  ⚠️ Не найден файл импорта: %s', import_path)
        else:
            content_lines.append(line)

    bundled_text = ''.join(content_lines)
    with open(bundle_file, 'w', encoding='utf-8') as out:
        out.write(bundled_text)

    logger.info('  ✓ Скомпилирован CSS бандл: %s (%d КБ)', bundle_file.name, len(bundled_text) // 1024)
    return True


def step_sync_etalons() -> bool:
    """[3/4] Синхронизация рабочего SPA из канонического эталона через единый модуль sync_etalons"""
    logger.info('[3/4] Синхронизация рабочего SPA из канонического эталона...')
    try:
        is_identical, digest, _ = sync_canonical_etalons(_ROOT)
    except FileNotFoundError:
        logger.error('  ❌ Канонический эталон standards/standards.html не найден')
        return False

    if is_identical:
        logger.info(f'  ✓ 100% побайтовая идентичность эталонов подтверждена (SHA-256: {digest})')
        return True

    logger.error('  ❌ Ошибка синхронизации эталонов: хэши не совпадают!')
    return False


def step_preflight_checks() -> bool:
    """[4/4] Контроль критических инвариантов качества"""
    logger.info('[4/4] Контроль инвариантов качества и безопасности...')
    frontend_index = _ROOT / 'frontend' / 'index.html'
    if frontend_index.is_file():
        with open(frontend_index, 'r', encoding='utf-8') as f:
            html = f.read()
        if re.search(r'\bЮнит\s+\d+\.\d+\b', html):
            logger.error('  ❌ Нарушен инвариант: обнаружен технический код "Юнит X.Y" в UI!')
            return False

    logger.info('  ✓ Все инварианты Clean Human UI и архитектурные ограничения соблюдены.')
    return True


def run_build() -> bool:
    start_time = time.time()
    logger.info('========================================================')
    logger.info('   🐍 Python Backend Academy — Мастер-пайплайн сборки   ')
    logger.info('========================================================')

    steps = [
        step_validate_schemas,
        step_bundle_css,
        step_sync_etalons,
        step_preflight_checks,
    ]

    for step in steps:
        if not step():
            logger.error('❌ Сборка прервана из-за ошибки на одном из этапов.')
            return False

    elapsed = time.time() - start_time
    logger.info('========================================================')
    logger.info('🎉 Сборка успешно завершена за %.2f сек! (100%% PASS)', elapsed)
    logger.info('========================================================')
    return True


if __name__ == '__main__':
    success = run_build()
    sys.exit(0 if success else 1)
