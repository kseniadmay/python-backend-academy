"""
Интеграционный запуск модульных тестов FastAPI бэкенда.
Позволяет запускать тесты стандартной командой из корня репозитория:
    python -m unittest
    python -m unittest discover tests
"""
import os
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from backend.tests.test_api import TestBackendApi

__all__ = ['TestBackendApi']

if __name__ == '__main__':
    unittest.main()

