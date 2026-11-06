from enum import IntEnum
from typing import Dict, List, Optional
from pydantic import Field

from backend.app.schemas.common import CompatBaseModel


class SrsRating(IntEnum):
    """
    Когнитивно скользкая шкала субъективной оценки памяти (FSRS 1..4):
    1: AGAIN — «Не вспомнил» (сброс стабильности, повторный показ)
    2: HARD — «Со скрипом» (вспомнил с трудом, стабильность растет медленно)
    3: GOOD — «Вспомнил» (уверенное воспроизведение, оптимальный интервал)
    4: EASY — «На автомате» (мгновенный отклик, максимальный интервал)
    """
    AGAIN = 1
    HARD = 2
    GOOD = 3
    EASY = 4


RATING_METADATA: Dict[int, Dict[str, str]] = {
    SrsRating.AGAIN: {
        'label': 'Не вспомнил',
        'shortcut': '1',
        'color': '#fb7185',
        'desc': 'Сброс интервала, повтор в этой сессии'
    },
    SrsRating.HARD: {
        'label': 'Со скрипом',
        'shortcut': '2',
        'color': '#f59e0b',
        'desc': 'Тяжело далось, короткий шаг'
    },
    SrsRating.GOOD: {
        'label': 'Вспомнил',
        'shortcut': '3',
        'color': '#10b981',
        'desc': 'Хорошо усвоено, канонический шаг'
    },
    SrsRating.EASY: {
        'label': 'На автомате',
        'shortcut': '4',
        'color': '#38bdf8',
        'desc': 'Легко и моментально, длинный шаг'
    }
}


class SrsCardRecord(CompatBaseModel):
    """
    Хранимое состояние отдельной карточки в FSRS-модели памяти.
    """
    card_id: str = Field(..., description='Уникальный идентификатор карточки')
    deck_id: str = Field(..., description='ID колоды, к которой принадлежит карточка')
    stability: float = Field(default=0.0, description='Стабильность памяти S (в днях до падения R до 90%)')
    difficulty: float = Field(default=5.0, ge=1.0, le=10.0, description='Сложность материала D от 1.0 (легко) до 10.0 (сложно)')
    reps: int = Field(default=0, ge=0, description='Счетчик успешных воспроизведений')
    lapses: int = Field(default=0, ge=0, description='Счетчик забываний (оценка 1)')
    state: str = Field(default='new', description='Состояние: new | learning | review | relearning')
    due_date: str = Field(..., description='Дата следующего повторения в формате YYYY-MM-DD')
    interval_days: int = Field(default=0, ge=0, description='Текущий интервал в днях')
    last_reviewed: Optional[str] = Field(default=None, description='ISO-штамп времени последней оценки')


class SrsRateRequest(CompatBaseModel):
    """
    DTO запроса фиксации оценки от клиента (мобилка или десктоп).
    """
    card_id: str = Field(..., description='ID карточки')
    deck_id: str = Field(..., description='ID колоды карточки')
    rating: int = Field(
        ...,
        ge=1,
        le=4,
        description='Оценка 1..4 (1: Не вспомнил, 2: Со скрипом, 3: Вспомнил, 4: На автомате)'
    )
    duration_ms: Optional[int] = Field(
        default=None,
        ge=0,
        description='Время ответа карточки в миллисекундах'
    )


class SrsRateResponse(CompatBaseModel):
    """
    DTO ответа после расчета интервала и начисления наград на сервере.
    """
    ok: bool = Field(default=True, description='Статус операции')
    card_id: str = Field(..., description='ID карточки')
    rating: int = Field(..., description='Полученная оценка 1..4')
    rating_label: str = Field(..., description='Когнитивно гладкий лейбл оценки')
    new_stability: float = Field(..., description='Рассчитанная стабильность памяти S')
    new_difficulty: float = Field(..., description='Рассчитанная сложность карточки D')
    interval_days: int = Field(..., description='Интервал до следующего показа в днях')
    due_date: str = Field(..., description='Дата следующего повторения YYYY-MM-DD')
    xp_awarded: int = Field(..., description='Начисленный опыт XP (+5 .. +15 XP)')
    streak_days: int = Field(..., description='Текущий стрик дней')
    message: str = Field(default='Оценка сохранена', description='Сообщение для интерфейса')


class SrsDueCardItem(CompatBaseModel):
    """
    Карточка, ожидающая повторения на сегодня.
    """
    card_id: str = Field(..., description='ID карточки')
    deck_id: str = Field(..., description='ID колоды')
    deck_title: str = Field(default='', description='Название темы/колоды')
    question: str = Field(..., description='Вопрос карточки')
    answer: str = Field(..., description='Развернутый эталонный ответ')
    echelon: int = Field(default=1, ge=1, le=4, description='Эшелон программы (1..4)')
    topic: Optional[str] = Field(default=None, description='Раздел курса')
    stability: float = Field(default=0.0, description='Текущая стабильность')
    difficulty: float = Field(default=5.0, description='Текущая сложность')
    reps: int = Field(default=0, description='Число повторений')
    is_due: bool = Field(default=True, description='Требует ли повторения сегодня')


class SrsDueResponse(CompatBaseModel):
    """
    Очередь карточек для повторения на сегодня.
    """
    ok: bool = Field(default=True, description='Успешность запроса')
    due_count: int = Field(..., description='Количество карточек, готовых к повторению')
    echelon_counts: Dict[str, int] = Field(default_factory=dict, description='Распределение по 4 эшелонам')
    cards: List[SrsDueCardItem] = Field(default_factory=list, description='Список карточек к показу')


class SrsStatsResponse(CompatBaseModel):
    """
    Сводная статистика удержания знаний пользователя.
    """
    ok: bool = Field(default=True, description='Статус ответа')
    total_cards_tracked: int = Field(..., description='Всего изученных карточек в памяти')
    due_today: int = Field(..., description='Осталось повторить сегодня')
    reviewed_today: int = Field(..., description='Повторено за сегодня')
    retention_rate_pct: float = Field(..., description='Процент удержания памяти (% успешных припоминаний)')
    average_difficulty: float = Field(..., description='Средняя сложность колод')
    streak_days: int = Field(..., description='Текущий стрик дней')
    xp_total: int = Field(..., description='Общий накопленный опыт XP')
