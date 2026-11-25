#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sync_etalons.py

Единый модуль синхронизации и проверки побайтовой идентичности
канонического эталона standards/standards.html и рабочего файла academy.html (DRY).
"""

import hashlib
import os
import shutil
from pathlib import Path
from typing import Optional, Tuple

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent


def get_file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()[:10]


def sync_canonical_etalons(root_dir: Optional[Path] = None) -> Tuple[bool, str, int]:
    """
    Копирует канонический эталон standards/standards.html в academy.html
    и проверяет 100% побайтовое совпадение по SHA-256.
    Возвращает: (is_identical, short_sha256, size_bytes)
    """
    base = root_dir or _ROOT
    academy_html = base / 'academy.html'
    standards_path = base / 'standards' / 'standards.html'

    if not standards_path.is_file():
        raise FileNotFoundError(f'Canonical standard not found: {standards_path}')

    shutil.copy2(standards_path, academy_html)
    hash_main = get_file_hash(academy_html)
    hash_standards = get_file_hash(standards_path)
    size_bytes = os.path.getsize(academy_html)
    return (hash_main == hash_standards), hash_main, size_bytes


if __name__ == '__main__':
    ok, digest, size = sync_canonical_etalons()
    if not ok:
        raise RuntimeError('SHA-256 mismatch after syncing standards.html -> academy.html')
    print(f'Copied {_ROOT / "standards" / "standards.html"} -> {_ROOT / "academy.html"} ({size} bytes, SHA-256: {digest})')
