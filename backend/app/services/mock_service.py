import uuid
from typing import Any, Dict, List, Optional

from backend.app.schemas.mock import (
    MockEvaluationRequest,
    MockEvaluationResponse,
    MockQuestionItem,
    MockSessionResponse,
)
from backend.app.schemas.practice import TaskRunRequest
from backend.app.services.code_runner_service import code_runner_service
from backend.app.services.content_service import content_service
from backend.app.services.srs_service import srs_service

# Курируемый пул задач для Live-Coding интервью
CURATED_INTERVIEW_TASK_IDS: List[int] = [1, 2, 10, 15, 24, 35, 42, 50, 64, 75]


def _build_socratic_levels(task: Dict[str, Any]) -> List[str]:
    raw_hint = task.get('hint') or ''
    steps = [p.strip() for p in raw_hint.split('Шаг ') if p.strip()] if 'Шаг ' in raw_hint else [raw_hint]

    levels = [
        f'Уровень 0 (Zero Hint): Проверьте граничные условия и типы данных для задачи «{task.get("title", "")}».',
        f'Уровень 1 (Conceptual): Концептуальная ментальная модель: {steps[0] if steps else "постройте пайплайн преобразования"}.',
        f'Уровень 2 (Structural): Декомпозиция: {steps[1] if len(steps) > 1 else "выделите целевую функцию и сигнатуру"}.',
        f'Уровень 3 (Tactical): Контракт и возврат: {steps[2] if len(steps) > 2 else "проверьте возвращаемое значение assert"}.',
    ]
    return levels


class MockService:
    """
    Сервис симуляции технических интервью Junior+ Python Backend Developer.
    """

    def create_session(self, echelon_id: int = 1, task_id: Optional[int] = None) -> MockSessionResponse:
        session_id = f'mock_{uuid.uuid4().hex[:12]}'

        # Подбор задачи
        target_id = task_id or CURATED_INTERVIEW_TASK_IDS[0]
        task = content_service.get_task(target_id)
        if not task:
            task = content_service.get_task(1) or {
                'id': 1,
                'title': 'Техническое задание',
                'desc': 'Реализуйте целевую функцию',
                'initialCode': 'def solution():\n    pass\n',
                'level': 1,
                'tier': 'Уровень 1',
                'topic': 'Python Core',
            }

        socratic_levels = _build_socratic_levels(task)

        question = MockQuestionItem(
            id=task['id'],
            title=task.get('title', 'Задача'),
            tier=task.get('tier') or f'Уровень {task.get("level", 1)}',
            echelon=echelon_id,
            topic=task.get('topic', 'Python Core'),
            desc=task.get('desc', ''),
            initial_code=task.get('initialCode') or '',
            socratic_levels=socratic_levels,
        )

        return MockSessionResponse(
            ok=True,
            session_id=session_id,
            echelon=echelon_id,
            time_limit_sec=1800,
            question=question,
            total_curated_tasks=len(CURATED_INTERVIEW_TASK_IDS),
        )

    def evaluate_candidate(self, payload: MockEvaluationRequest) -> MockEvaluationResponse:
        # Запуск кода через единый раннер практики (DRY)
        run_res = code_runner_service.run_task(
            TaskRunRequest(task_id=payload.task_id, code=payload.code)
        )

        stats = srs_service._get_stats_data()
        streak = int(stats.get('streak_days', 1))

        if run_res.status == 'pass':
            hints = payload.hints_used
            if hints == 0:
                verdict = '✓ Live-Coding успешно пройден без подсказок (Zero-Hint Mastery)!'
                grade = 'Strong Junior+'
            elif hints <= 2:
                verdict = f'✓ Live-Coding сдан успешно (использовано наводок: {hints}). Отличный ход рассуждений!'
                grade = 'Junior+'
            else:
                verdict = f'✓ Решение принято (использовано подсказок: {hints}). Рекомендуется закрепить тему.'
                grade = 'Junior'

            xp = 40
            # Начисление XP за собеседование
            stats['xp_total'] = int(stats.get('xp_total', 0)) + xp
            srs_service._save_stats_data()

            return MockEvaluationResponse(
                ok=True,
                status='pass',
                verdict=verdict,
                output=run_res.output,
                xp_awarded=xp,
                streak_days=streak,
                candidate_level=grade,
            )
        else:
            return MockEvaluationResponse(
                ok=True,
                status='fail',
                verdict=f'✗ Решение не принято: {run_res.error_message or "тесты не пройдены"}. Воспользуйтесь сократической наводкой.',
                output=run_res.output,
                xp_awarded=0,
                streak_days=streak,
                candidate_level='Требуется подготовка',
            )


mock_service = MockService()
