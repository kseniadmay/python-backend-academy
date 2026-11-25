from typing import List, Optional
from pydantic import Field

from backend.app.schemas.common import CompatBaseModel


class NoteStep(CompatBaseModel):
    """
    Атомарный микро-шаг теории конспекта (1 шаг = 1 экран = 15-45 сек чтения).
    """
    step_index: int = Field(..., ge=0, description='Индекс шага (0..N)')
    title: str = Field(..., description='Предметный заголовок ментальной модели шага')
    html: str = Field(..., description='HTML-содержимое конспекта со сниппетами и формулами')
    is_final: bool = Field(default=False, description='Является ли шаг финальным с CTA «Закрепить в карточках»')


class NoteDetail(CompatBaseModel):
    """
    Полная модель атомарного конспекта.
    """
    id: str = Field(..., description='ID конспекта (например, К-001)')
    title: str = Field(..., description='Название темы конспекта')
    total_steps: int = Field(..., description='Общее количество микро-шагов')
    related_deck_id: Optional[str] = Field(default=None, description='ID связанной колоды флеш-карточек (например, Ф-001)')
    current_saved_step: int = Field(default=0, description='Сохраненная позиция чтения (Zero-Progress-Loss)')
    is_read: bool = Field(default=False, description='Был ли конспект уже прочитан')
    steps: List[NoteStep] = Field(default_factory=list, description='Список микро-шагов')


class NoteProgressRequest(CompatBaseModel):
    """
    DTO фиксации прогресса чтения конспекта.
    """
    note_id: str = Field(..., description='ID конспекта (например, К-001)')
    step_index: int = Field(..., ge=0, description='Текущий микро-шаг, до которого дошел пользователь')
    is_completed: bool = Field(default=False, description='Флаг полного прочтения всех шагов')


class NoteProgressResponse(CompatBaseModel):
    """
    DTO ответа сохранения прогресса конспекта.
    """
    ok: bool = Field(default=True, description='Статус операции')
    note_id: str = Field(..., description='ID конспекта')
    saved_step: int = Field(..., description='Сохраненный микро-шаг')
    is_read: bool = Field(..., description='Статус полного прочтения')
    next_review_date: Optional[str] = Field(default=None, description='Дата следующего интервального повторения YYYY-MM-DD')
    xp_awarded: int = Field(default=0, description='Начисленный опыт (+10 XP при первом прочтении)')


class NoteDueItem(CompatBaseModel):
    """
    Конспект, готовый к интервальному повторению сегодня.
    """
    note_id: str = Field(..., description='ID конспекта')
    title: str = Field(..., description='Название темы')
    step: int = Field(..., description='Текущая ступень интервала (0..4)')
    interval_days: int = Field(..., description='Текущий интервал в днях (1, 3, 7, 21, 30)')
    due_date: str = Field(..., description='Дата повторения YYYY-MM-DD')


class NoteDueResponse(CompatBaseModel):
    """
    Очередь конспектов для повторения на сегодня.
    """
    ok: bool = Field(default=True, description='Статус запроса')
    due_count: int = Field(..., description='Количество конспектов к повторению на сегодня')
    notes: List[NoteDueItem] = Field(default_factory=list, description='Список конспектов')
