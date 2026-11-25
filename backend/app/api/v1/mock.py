from typing import Optional
from fastapi import APIRouter, Query

from backend.app.schemas.mock import (
    MockEvaluationRequest,
    MockEvaluationResponse,
    MockSessionResponse,
)
from backend.app.services.mock_service import mock_service

router = APIRouter(prefix='/mock', tags=['Mock Technical Interview Simulator'])


@router.get(
    '/session',
    response_model=MockSessionResponse,
    summary='Старт или получение сессии технического собеседования',
    description='Инициализирует раунд Live-Coding интервью с таймингом (30 мин), задачей из пула эшелона и 4 уровнями сократических наводок.'
)
def get_mock_session(
    echelon: int = Query(1, ge=1, le=4, description='Эшелон собеседования'),
    task_id: Optional[int] = Query(None, description='Опциональный конкретный ID задачи')
) -> MockSessionResponse:
    """
    Старт сессии собеседования.
    """
    return mock_service.create_session(echelon_id=echelon, task_id=task_id)


@router.post(
    '/evaluate',
    response_model=MockEvaluationResponse,
    summary='Сдача решения на проверку техлиду',
    description='Проверяет код кандидата, оценивает независимость решения (число подсказок), присваивает грейд (Junior+) и начисляет +40 XP.'
)
def evaluate_mock_task(payload: MockEvaluationRequest) -> MockEvaluationResponse:
    """
    Оценка кода кандидата техлидом.
    """
    return mock_service.evaluate_candidate(payload)
