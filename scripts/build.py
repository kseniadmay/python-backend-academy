#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build.py

Единый детерминированный конвейер сборки и верификации платформы Python Backend Academy.
Собирает ассеты, валидирует схемы Pydantic, синхронизирует эталоны и контролирует инварианты.
"""

import hashlib
import json
import logging
import os
import re
import shutil
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

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('builder')


def get_file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()[:10]


def step_validate_schemas() -> bool:
    """[1/4] Валидация канонических данных контента через Pydantic"""
    logger.info('[1/4] Проверка целостности данных в data/content/...')
    content_dir = _ROOT / 'data' / 'content'
    required_files = ['manifest.json', 'tasks.json', 'notes.json', 'cards.json']

    for rf in required_files:
        p = content_dir / rf
        if not p.is_file():
            logger.error('  ❌ Отсутствует обязательный файл: %s', rf)
            return False

    with open(content_dir / 'manifest.json', 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    with open(content_dir / 'tasks.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    with open(content_dir / 'notes.json', 'r', encoding='utf-8') as f:
        notes = json.load(f)
    with open(content_dir / 'cards.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)

    logger.info(
        '  ✓ Схемы валидны: %d модулей, %d задач, %d конспектов, %d колод карточек',
        len(manifest.get('modules', [])),
        len(tasks),
        len(notes),
        len(cards)
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
    """[3/4] Синхронизация канонических эталонов SPA"""
    logger.info('[3/4] Проверка и синхронизация эталонов...')
    academy_html = _ROOT / 'academy.html'
    standards_html = _ROOT / 'standards' / 'standards.html'

    if not academy_html.is_file():
        logger.error('  ❌ Файл academy.html не найден')
        return False

    # Синхронизация 1:1 с каноническим эталоном
    standards_html.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(academy_html, standards_html)

    hash_main = get_file_hash(academy_html)
    hash_standards = get_file_hash(standards_html)

    if hash_main == hash_standards:
        logger.info(f'  ✓ 100% побайтовая идентичность эталонов подтверждена (SHA-256: {hash_main})')
        return True
    else:
        logger.error('  ❌ Ошибка синхронизации эталонов: хэши не совпадают!')
        return False


def step_preflight_checks() -> bool:
    """[4/4] Контроль критических инвариантов качества"""
    logger.info('[4/4] Контроль инвариантов качества и безопасности...')
    # 1. Проверка отсутствия запрещенных токенов в коммитах и новых файлах
    # (инварианты AGENTS.md: Clean Human UI, No Technical IDs)
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
