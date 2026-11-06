import unittest
from fastapi.testclient import TestClient

from backend.app.main import app


class TestMockApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_get_mock_session(self) -> None:
        """Проверка старта сессии собеседования."""
        res = self.client.get('/api/v1/mock/session?echelon=1')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertIn('session_id', data)
        self.assertEqual(data['time_limit_sec'], 1800)
        q = data['question']
        self.assertIn('title', q)
        self.assertIn('desc', q)
        self.assertEqual(len(q['socratic_levels']), 4)

    def test_evaluate_mock_success_zero_hint(self) -> None:
        """Сдача верного решения без подсказок (Zero-Hint Mastery)."""
        session_res = self.client.get('/api/v1/mock/session?task_id=1')
        session_id = session_res.json()['session_id']

        valid_solution = """
sql = '''
SELECT u.username, o.id AS order_id, o.total_amount, o.status
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';
'''
"""
        eval_res = self.client.post('/api/v1/mock/evaluate', json={
            'session_id': session_id,
            'task_id': 1,
            'code': valid_solution,
            'hints_used': 0
        })
        self.assertEqual(eval_res.status_code, 200)
        data = eval_res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['status'], 'pass')
        self.assertEqual(data['candidate_level'], 'Strong Junior+')
        self.assertEqual(data['xp_awarded'], 40)
        self.assertIn('Zero-Hint', data['verdict'])

    def test_evaluate_mock_failure(self) -> None:
        """Сдача некорректного кода на собеседовании."""
        session_res = self.client.get('/api/v1/mock/session?task_id=1')
        session_id = session_res.json()['session_id']

        eval_res = self.client.post('/api/v1/mock/evaluate', json={
            'session_id': session_id,
            'task_id': 1,
            'code': "sql = 'SELECT 1;'",
            'hints_used': 1
        })
        self.assertEqual(eval_res.status_code, 200)
        data = eval_res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['status'], 'fail')
        self.assertEqual(data['xp_awarded'], 0)


if __name__ == '__main__':
    unittest.main()
