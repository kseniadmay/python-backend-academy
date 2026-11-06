from typing import List, Optional
from pydantic import Field

from backend.app.schemas.common import CompatBaseModel


class MockQuestionItem(CompatBaseModel):
    """
    Модель вопроса/задачи для раунда технического собеседования (Live-Coding).
    """
    id: int = Field(..., description='ID задачи в банке интервью')
    title: str = Field(..., description='Название темы / вопроса')
    tier: str = Field(default='Уровень 1', description='Уровень сложности')
    echelon: int = Field(default=1, ge=1, le=4, description='Эшелон программы')
    topic: str = Field(default='Python Core', description='Тематическая секция')
    desc: str = Field(..., description='Техническое задание / условие задачи')
    initial_code: str = Field(default='', description='Стартовая заготовка кода кандидата')
    socratic_levels: List[str] = Field(default_factory=list, description='4 уровня наводок Сократа без готового кода')


class MockSessionResponse(CompatBaseModel):
    """
    Сессия технического собеседования с таймингом и активным раундом.
    """
    ok: bool = Field(default=True, description='Статус ответа')
    session_id: str = Field(..., description='Уникальный ID сессии собеседования')
    echelon: int = Field(..., description='Номер выбранного эшелона')
    time_limit_sec: int = Field(default=1800, description='Лимит времени секции в секундах (30 мин)')
    question: MockQuestionItem = Field(..., description='Активный вопрос/задача раунда')
    total_curated_tasks: int = Field(default=0, description='Всего задач в пуле интервью')


class MockEvaluationRequest(CompatBaseModel):
    """
    DTO сдачи кода кандидата на проверку тимлиду.
    """
    session_id: str = Field(..., description='ID активной сессии')
    task_id: int = Field(..., description='ID проверяемой задачи')
    code: str = Field(..., description='Написанный кандидатом Python-код')
    hints_used: int = Field(default=0, ge=0, le=4, description='Сколько уровней подсказок использовал кандидат')


class MockEvaluationResponse(CompatBaseModel):
    """
    Результат проверки и вердикт техлида.
    """
    ok: bool = Field(default=True, description='Статус операции')
    status: str = Field(..., description='Статус прохождения раунда: pass | fail')
    verdict: str = Field(..., description='Вердикт техлида (например: «Strong Junior+ Pass», «Требуется доработка»)')
    output: str = Field(default='', description='Лог выполнения тестов')
    xp_awarded: int = Field(default=0, description='Начисленный опыт (+40 XP)')
    streak_days: int = Field(default=0, description='Текущий стрик дней')
    candidate_level: str = Field(default='Junior+', description='Оцененный грейд кандидата')
