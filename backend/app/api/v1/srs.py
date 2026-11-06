from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.schemas.srs import (
    SrsCardRecord,
    SrsDueResponse,
    SrsRateRequest,
    SrsRateResponse,
    SrsStatsResponse,
)
from backend.app.services.srs_service import srs_service

router = APIRouter(prefix='/srs', tags=['Spaced Repetition System (FSRS)'])


@router.get(
    '/due',
    response_model=SrsDueResponse,
    summary='Очередь карточек для повторения на сегодня',
    description='Возвращает карточки, запланированные к повторению алгоритмом FSRS, с возможностью фильтрации по эшелону или теме.'
)
def get_due_cards(
    echelon: Optional[int] = Query(None, ge=1, le=4, description='Фильтр по номеру эшелона 1..4'),
    deck_id: Optional[str] = Query(None, description='ID конкретной колоды (например, Ф-001)'),
    limit: int = Query(50, ge=1, le=200, description='Максимальное число карточек в порции')
) -> SrsDueResponse:
    """
    Выдача очереди карточек для сессии интервального повторения.
    """
    return srs_service.get_due_cards(
        echelon_filter=echelon,
        deck_filter=deck_id,
        limit=limit
    )


@router.post(
    '/rate',
    response_model=SrsRateResponse,
    summary='Фиксация субъективной оценки карточки',
    description='Принимает оценку 1..4 («Не вспомнил», «Со скрипом», «Вспомнил», «На автомате»), пересчитывает стабильность FSRS и начисляет XP.'
)
def rate_card(payload: SrsRateRequest) -> SrsRateResponse:
    """
    Фиксация когнитивно скользкой оценки карточки и расчёт следующего шага интервала.
    """
    try:
        return srs_service.rate_card(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка обработки оценки карточки: {exc}'
        )


@router.get(
    '/stats',
    response_model=SrsStatsResponse,
    summary='Сводная статистика удержания знаний',
    description='Возвращает метрики ретеншна, число повторённых карточек, среднюю сложность колод, стрик и накопленный опыт XP.'
)
def get_srs_stats() -> SrsStatsResponse:
    """
    Получение статистики прогресса SRS.
    """
    return srs_service.get_stats()


@router.get(
    '/card/{card_id:path}',
    response_model=SrsCardRecord,
    summary='Текущее состояние карточки в модели памяти FSRS'
)
def get_card_state(card_id: str) -> SrsCardRecord:
    """
    Получение детального состояния карточки (стабильность S, сложность D, интервал, reps, lapses).
    """
    record = srs_service.get_card_state(card_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Карточка {card_id} ещё не изучалась в FSRS'
        )
    return record
