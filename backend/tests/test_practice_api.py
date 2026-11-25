import unittest
from fastapi.testclient import TestClient

from backend.app.main import app


class TestPracticeApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_run_task_success(self) -> None:
        """Успешное решение задачи 1: корректный SQL-запрос."""
        valid_solution = """
sql = '''
SELECT u.username, o.id AS order_id, o.total_amount, o.status
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';
'''
"""
        res = self.client.post('/api/v1/practice/run', json={
            'task_id': 1,
            'code': valid_solution
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['status'], 'pass')
        self.assertIsNone(data['error_message'])
        self.assertGreaterEqual(data['xp_awarded'], 0)

    def test_run_task_syntax_error(self) -> None:
        """Передача кода с синтаксической ошибкой."""
        broken_code = "def invalid_syntax(: pass"
        res = self.client.post('/api/v1/practice/run', json={
            'task_id': 1,
            'code': broken_code
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['status'], 'fail')
        self.assertIn('Синтаксическая ошибка', data['error_message'])
        self.assertIsNotNone(data['error_line'])
        self.assertIsNotNone(data['socratic_hint'])

    def test_run_task_assertion_failure(self) -> None:
        """Код синтаксически верный, но не удовлетворяет условию задачи."""
        incomplete_code = "sql = 'SELECT 1;'"  # Отсутствуют нужные поля username, order_id
        res = self.client.post('/api/v1/practice/run', json={
            'task_id': 1,
            'code': incomplete_code
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['status'], 'fail')
        self.assertIn('username', data['error_message'])
        self.assertIsNotNone(data['socratic_hint'])

    def test_task_socratic_hints(self) -> None:
        """Получение наводок Сократа без готового кода."""
        res = self.client.get('/api/v1/practice/hint/1?level=2')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['task_id'], 1)
        self.assertGreaterEqual(data['total_hints'], 1)
        self.assertGreaterEqual(len(data['hints']), 1)

    def test_task_draft_lifecycle(self) -> None:
        """Сохранение и последующее чтение черновика решения."""
        draft_text = "def solution():\n    return 42\n"
        save_res = self.client.post('/api/v1/practice/draft', json={
            'task_id': 99,
            'draft_code': draft_text
        })
        self.assertEqual(save_res.status_code, 200)
        save_data = save_res.json()
        self.assertTrue(save_data['ok'])

        # Чтение сохраненного черновика
        get_res = self.client.get('/api/v1/practice/draft/99')
        self.assertEqual(get_res.status_code, 200)
        get_data = get_res.json()
        self.assertTrue(get_data['ok'])
        self.assertEqual(get_data['draft'], draft_text)


if __name__ == '__main__':
    unittest.main()
