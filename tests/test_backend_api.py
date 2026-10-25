"""
Интеграционный запуск модульных тестов FastAPI бэкенда.
Позволяет запускать тесты стандартной командой из корня репозитория:
    python -m unittest
    python -m unittest discover tests
"""
import unittest
from backend.tests.test_api import TestBackendApi

__all__ = ['TestBackendApi']

if __name__ == '__main__':
    unittest.main()
