import unittest
import uuid
from fastapi.testclient import TestClient

from backend.app.main import app


class TestNotesApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_get_note_detail(self) -> None:
        """Получение детального конспекта К-001 со всеми микро-шагами."""
        res = self.client.get('/api/v1/notes/К-001')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['id'], 'К-001')
        self.assertIn('Структуры данных', data['title'])
        self.assertGreater(data['total_steps'], 3)
        self.assertEqual(data['related_deck_id'], 'Ф-001')
        self.assertEqual(len(data['steps']), data['total_steps'])

        # Проверка флага is_final на последнем шаге
        last_step = data['steps'][-1]
        self.assertTrue(last_step['is_final'])

    def test_save_note_step_progress(self) -> None:
        """Сохранение промежуточного шага чтения конспекта."""
        res = self.client.post('/api/v1/notes/progress', json={
            'note_id': 'К-001',
            'step_index': 3,
            'is_completed': False
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['saved_step'], 3)

        # Проверка через повторный GET
        get_res = self.client.get('/api/v1/notes/К-001')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()['current_saved_step'], 3)

    def test_save_note_completion_and_srs_schedule(self) -> None:
        """Полное прочтение конспекта планирует дату повторения и начисляет +10 XP."""
        unique_note_id = f'test_note_{uuid.uuid4().hex[:8]}'
        res = self.client.post('/api/v1/notes/progress', json={
            'note_id': unique_note_id,
            'step_index': 5,
            'is_completed': True
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertTrue(data['is_read'])
        self.assertIsNotNone(data['next_review_date'])
        self.assertEqual(data['xp_awarded'], 10)

    def test_get_due_notes_endpoint(self) -> None:
        """Проверка получения конспектов, готовых к повторению."""
        res = self.client.get('/api/v1/notes/due')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertIn('due_count', data)
        self.assertIn('notes', data)


if __name__ == '__main__':
    unittest.main()
