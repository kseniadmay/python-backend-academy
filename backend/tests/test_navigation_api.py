import unittest
from fastapi.testclient import TestClient

from backend.app.main import app


class TestNavigationApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_navigation_meta_structure(self) -> None:
        """Проверка структуры навигационного контракта."""
        res = self.client.get('/api/v1/navigation/meta')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])

        # 1. Десктопные группы
        desktop_groups = data.get('desktop_groups', [])
        self.assertGreaterEqual(len(desktop_groups), 3)
        group_ids = [g['id'] for g in desktop_groups]
        self.assertIn('main', group_ids)
        self.assertIn('trainer', group_ids)
        self.assertIn('module', group_ids)

        # 2. Мобильные табы (ровно 4 таба)
        mobile_tabs = data.get('mobile_tabs', [])
        self.assertEqual(len(mobile_tabs), 4)
        tab_routes = [t['route'] for t in mobile_tabs]
        self.assertEqual(tab_routes, ['/', '/path', '/cards', '/practice'])

        # 3. Полный список ссылок для шторки (drawer)
        drawer_items = data.get('drawer_items', [])
        self.assertEqual(len(drawer_items), 15)

        # 4. Проверка полей карточки и счетчиков
        self.assertIn('due_cards_count', data)
        self.assertIn('module_progress_pct', data)
        self.assertIn('/python', data['module_progress_pct'])


if __name__ == '__main__':
    unittest.main()
