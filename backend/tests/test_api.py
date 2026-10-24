import unittest
from fastapi.testclient import TestClient

from backend.app.main import app


class TestBackendApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_healthz_endpoint(self) -> None:
        res = self.client.get('/healthz')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {'ok': True})

    def test_api_v1_health_endpoint(self) -> None:
        res = self.client.get('/api/v1/health')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {'ok': True})

    def test_api_ping_endpoint(self) -> None:
        res = self.client.get('/api/ping')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get('status'), 'ok')
        self.assertIn('time', data)

    def test_sync_push_and_pull_lifecycle(self) -> None:
        # 1. Pull initial state
        res = self.client.get('/api/sync')
        self.assertEqual(res.status_code, 200)
        initial_data = res.json()
        self.assertTrue(initial_data['ok'])
        base_time = initial_data.get('updatedAt', 0)

        # 2. Push state with baseUpdatedAt from previous pull
        payload = {
            'bundle': {
                'academyState': {'xp': 150, 'streak': 3},
                'ideStatus': {'task_1': 'passed'},
                'ideDrafts': {}
            },
            'baseUpdatedAt': base_time,
            'device': 'unittest-device',
            'clientId': 'unittest-client-01'
        }
        push_res = self.client.post('/api/sync', json=payload)
        self.assertEqual(push_res.status_code, 200)
        push_data = push_res.json()
        self.assertTrue(push_data['ok'])
        self.assertEqual(push_data['bundle']['academyState']['xp'], 150)

        # 3. Pull again and verify persistence
        pull_res = self.client.get('/api/sync')
        self.assertEqual(pull_res.status_code, 200)
        pulled = pull_res.json()
        self.assertEqual(pulled['bundle']['academyState']['xp'], 150)
        self.assertEqual(pulled['device'], 'unittest-device')

    def test_sync_conflict_lost_update_guard(self) -> None:
        # Устройство А пушит прогресс
        pull_res = self.client.get('/api/sync')
        base_time = pull_res.json().get('updatedAt', 0)

        self.client.post('/api/sync', json={
            'bundle': {'academyState': {'xp': 200}, 'ideStatus': {}, 'ideDrafts': {}},
            'baseUpdatedAt': base_time,
            'device': 'device-A',
            'clientId': 'client-A'
        })

        # Устройство Б пытается запушить со старым baseUpdatedAt (0)
        conflict_res = self.client.post('/api/sync', json={
            'bundle': {'academyState': {'xp': 100}, 'ideStatus': {}, 'ideDrafts': {}},
            'baseUpdatedAt': 0,
            'device': 'device-B',
            'clientId': 'client-B'
        })
        self.assertEqual(conflict_res.status_code, 409)
        self.assertTrue(conflict_res.json().get('conflict'))

    def test_feedback_submission(self) -> None:
        report = {
            'context': 'test-runner',
            'message': 'Проверка отправки отзыва через FastAPI'
        }
        res = self.client.post('/api/bug-report', json=report)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertGreaterEqual(data['count'], 1)

    def test_content_summary(self) -> None:
        res = self.client.get('/api/v1/content/summary')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['modulesCount'], 7)
        self.assertEqual(data['tasksCount'], 401)
        self.assertEqual(data['notesCount'], 238)

    def test_content_modules(self) -> None:
        res = self.client.get('/api/v1/content/modules')
        self.assertEqual(res.status_code, 200)
        modules = res.json()
        self.assertEqual(len(modules), 7)
        self.assertEqual(modules[0]['id'], '01')
        self.assertEqual(modules[0]['title'], 'Python Core')

    def test_content_get_note(self) -> None:
        res = self.client.get('/api/v1/content/notes/К-001')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['note']['id'], 'К-001')
        self.assertGreater(len(data['note']['steps']), 0)

    def test_content_get_deck(self) -> None:
        res = self.client.get('/api/v1/content/cards/Ф-001')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['deck']['id'], 'Ф-001')
        self.assertGreater(len(data['deck']['cards']), 0)

    def test_content_tasks_and_filter(self) -> None:
        res = self.client.get('/api/v1/content/tasks?level=1')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertGreater(data['count'], 0)
        for t in data['tasks']:
            self.assertEqual(t['level'], 1)

    def test_content_get_single_task(self) -> None:
        res = self.client.get('/api/v1/content/tasks/1')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['task']['id'], 1)
        self.assertGreater(len(data['task']['solution']), 0)

    def test_content_search(self) -> None:
        res = self.client.get('/api/v1/content/search?q=dict')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertGreater(data['count'], 0)

    def test_spa_root_serve(self) -> None:
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('text/html', res.headers.get('content-type', ''))

    def test_modular_frontend_serving(self) -> None:
        # 1. HTML Shell
        html_res = self.client.get('/frontend/index.html')
        self.assertEqual(html_res.status_code, 200)
        self.assertIn('text/html', html_res.headers.get('content-type', ''))
        self.assertIn('Python Backend Academy', html_res.text)

        # 2. Modular CSS
        css_res = self.client.get('/frontend/css/main.css')
        self.assertEqual(css_res.status_code, 200)
        self.assertIn('text/css', css_res.headers.get('content-type', ''))

        # 3. Modular JS
        js_res = self.client.get('/frontend/js/api.js')
        self.assertEqual(js_res.status_code, 200)
        self.assertIn('javascript', js_res.headers.get('content-type', ''))


if __name__ == '__main__':
    unittest.main()
