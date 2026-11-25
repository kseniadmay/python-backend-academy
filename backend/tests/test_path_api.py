import unittest
from fastapi.testclient import TestClient

from backend.app.main import app


class TestPathApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_path_overview_endpoint(self) -> None:
        """Проверка общего обзора тропы по всем 4 эшелонам."""
        res = self.client.get('/api/v1/path/overview')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(len(data['echelons']), 4)
        self.assertGreater(data['total_units'], 30)
        self.assertIn('active_echelon_id', data)

    def test_echelon_1_structure(self) -> None:
        """Проверка структуры Эшелона 1: главы, узлы и ворота."""
        res = self.client.get('/api/v1/path/echelon/1')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['echelon_id'], 1)
        self.assertEqual(len(data['chapters']), 3)

        nodes = data.get('nodes', [])
        self.assertEqual(len(nodes), 14)

        # Проверка наличия активного узла
        active_nodes = [n for n in nodes if n['status'] == 'active']
        self.assertEqual(len(active_nodes), 1)

        # Проверка рубежных ворот глав
        gates = [n for n in nodes if n['is_gate']]
        self.assertGreaterEqual(len(gates), 3)

    def test_echelon_invalid_id(self) -> None:
        """Проверка отклонения невалидного номера эшелона."""
        res = self.client.get('/api/v1/path/echelon/99')
        self.assertEqual(res.status_code, 422)


if __name__ == '__main__':
    unittest.main()
