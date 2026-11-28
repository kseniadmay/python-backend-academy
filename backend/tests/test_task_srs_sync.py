import unittest

from backend.app.services.sync_service import merge_academy_states, sanitize_academy_state


class TestTaskSrsSync(unittest.TestCase):
    def test_sanitize_task_srs_and_daily_limit(self) -> None:
        raw = {
            'practiceDailyLimit': '5',
            'taskSrs': {
                ' 20 ': {
                    'interval': 7,
                    'ease': 2.6,
                    'reps': 2,
                    'lapses': 0,
                    'due': '2026-12-05',
                    'lastReviewed': '2026-11-28',
                    'lastOutcome': 'easy',
                    'neededHelp': False,
                    'skillId': '1.1.1',
                },
                'bad_key': {'interval': 1},
                '-5': {'interval': 1},
            },
        }
        cleaned = sanitize_academy_state(raw)
        self.assertEqual(cleaned['practiceDailyLimit'], 5)
        self.assertEqual(list(cleaned['taskSrs'].keys()), ['20'])
        self.assertEqual(cleaned['taskSrs']['20']['lastOutcome'], 'easy')
        self.assertFalse(cleaned['taskSrs']['20']['neededHelp'])

        invalid_lim = sanitize_academy_state({'practiceDailyLimit': 99})
        self.assertEqual(invalid_lim['practiceDailyLimit'], 0)

    def test_merge_task_srs_prefers_fresher_review_and_higher_reps(self) -> None:
        stored = {
            'updatedAt': 1000,
            'practiceDailyLimit': 3,
            'taskSrs': {
                '20': {
                    'interval': 3,
                    'ease': 2.5,
                    'reps': 1,
                    'lapses': 0,
                    'due': '2026-12-01',
                    'lastReviewed': '2026-11-28',
                    'lastOutcome': 'good',
                    'neededHelp': False,
                    'skillId': '1.1.1',
                },
                '1': {
                    'interval': 1,
                    'ease': 2.3,
                    'reps': 1,
                    'lapses': 1,
                    'due': '2026-11-28',
                    'lastReviewed': '2026-11-27',
                    'lastOutcome': 'again',
                    'neededHelp': True,
                    'skillId': '5.1.1',
                },
            },
        }
        incoming = {
            'updatedAt': 2000,
            'practiceDailyLimit': 10,
            'taskSrs': {
                '20': {
                    'interval': 1,
                    'ease': 2.3,
                    'reps': 0,
                    'lapses': 1,
                    'due': '2026-11-27',
                    'lastReviewed': '2026-11-26',
                    'lastOutcome': 'again',
                    'neededHelp': True,
                    'skillId': '1.1.1',
                },
                '1': {
                    'interval': 3,
                    'ease': 2.5,
                    'reps': 2,
                    'lapses': 0,
                    'due': '2026-12-01',
                    'lastReviewed': '2026-11-28',
                    'lastOutcome': 'good',
                    'neededHelp': False,
                    'skillId': '5.1.1',
                },
            },
        }
        merged = merge_academy_states(stored, incoming)
        self.assertEqual(merged['practiceDailyLimit'], 10)
        self.assertEqual(merged['taskSrs']['20']['lastReviewed'], '2026-11-28')
        self.assertEqual(merged['taskSrs']['20']['lastOutcome'], 'good')
        self.assertEqual(merged['taskSrs']['1']['lastReviewed'], '2026-11-28')
        self.assertEqual(merged['taskSrs']['1']['reps'], 2)
