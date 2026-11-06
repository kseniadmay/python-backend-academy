import unittest
import uuid
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas.srs import SrsRating


class TestSrsApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_get_due_cards_basic(self) -> None:
        """Проверка выдачи очереди карточек на повторение."""
        res = self.client.get('/api/v1/srs/due?limit=10')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertIn('due_count', data)
        self.assertIn('cards', data)
        self.assertGreater(data['due_count'], 0)
        card = data['cards'][0]
        self.assertIn('card_id', card)
        self.assertIn('question', card)
        self.assertIn('answer', card)

    def test_get_due_cards_with_echelon_filter(self) -> None:
        """Проверка фильтрации карточек по номеру эшелона."""
        res = self.client.get('/api/v1/srs/due?echelon=1&limit=5')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        for card in data['cards']:
            self.assertEqual(card['echelon'], 1)

    def test_rate_card_validation_error(self) -> None:
        """Проверка отклонения некорректных оценок (валидация Pydantic)."""
        invalid_payload = {
            'card_id': 'Ф-001#0',
            'deck_id': 'Ф-001',
            'rating': 99  # Недопустимый рейтинг
        }
        res = self.client.post('/api/v1/srs/rate', json=invalid_payload)
        self.assertEqual(res.status_code, 422)

    def test_rate_card_again_resets_stability(self) -> None:
        """Оценка 1 («Не вспомнил»): сброс стабильности и интервала в 0."""
        unique_cid = f'test_card_again_{uuid.uuid4().hex[:8]}'
        payload = {
            'card_id': unique_cid,
            'deck_id': 'Ф-001',
            'rating': SrsRating.AGAIN,
            'duration_ms': 2500
        }
        res = self.client.post('/api/v1/srs/rate', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertEqual(data['rating'], 1)
        self.assertEqual(data['rating_label'], 'Не вспомнил')
        self.assertEqual(data['interval_days'], 0)
        self.assertEqual(data['xp_awarded'], 5)

        # Проверка через эндпоинт состояния карточки
        card_res = self.client.get(f'/api/v1/srs/card/{unique_cid}')
        self.assertEqual(card_res.status_code, 200)
        card_data = card_res.json()
        self.assertEqual(card_data['lapses'], 1)

    def test_rate_card_fsrs_progression(self) -> None:
        """Проверка роста интервалов при повторении: Hard -> Good -> Easy."""
        unique_cid = f'test_fsrs_growth_{uuid.uuid4().hex[:8]}'
        deck_id = 'Ф-001'

        # 1. Первый показ — оценка «Вспомнил» (Good)
        res1 = self.client.post('/api/v1/srs/rate', json={
            'card_id': unique_cid,
            'deck_id': deck_id,
            'rating': SrsRating.GOOD
        })
        self.assertEqual(res1.status_code, 200)
        d1 = res1.json()
        self.assertEqual(d1['rating_label'], 'Вспомнил')
        self.assertGreaterEqual(d1['interval_days'], 1)
        self.assertEqual(d1['xp_awarded'], 12)

        # 2. Второй показ — оценка «На автомате» (Easy)
        res2 = self.client.post('/api/v1/srs/rate', json={
            'card_id': unique_cid,
            'deck_id': deck_id,
            'rating': SrsRating.EASY
        })
        self.assertEqual(res2.status_code, 200)
        d2 = res2.json()
        self.assertEqual(d2['rating_label'], 'На автомате')
        self.assertGreater(d2['new_stability'], d1['new_stability'])
        self.assertGreater(d2['interval_days'], d1['interval_days'])
        self.assertEqual(d2['xp_awarded'], 15)

    def test_srs_stats_endpoint(self) -> None:
        """Проверка получения агрегированных метрик SRS."""
        res = self.client.get('/api/v1/srs/stats')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['ok'])
        self.assertIn('total_cards_tracked', data)
        self.assertIn('retention_rate_pct', data)
        self.assertIn('xp_total', data)
        self.assertIn('streak_days', data)


if __name__ == '__main__':
    unittest.main()
