from typing import List, Optional
from pydantic import Field

from backend.app.schemas.common import CompatBaseModel


class TaskRunRequest(CompatBaseModel):
    """
    DTO запроса на запуск и валидацию решения задачи в Zen IDE.
    """
    task_id: int = Field(..., ge=1, le=500, description='ID практической задачи (1..401)')
    code: str = Field(..., description='Исходный Python-код обучающегося')


class TaskRunResponse(CompatBaseModel):
    """
    DTO результата проверки решения на сервере.
    """
    ok: bool = Field(default=True, description='Статус обработки запроса')
    task_id: int = Field(..., description='ID проверенной задачи')
    status: str = Field(..., description='Статус проверки: pass | fail | error')
    output: str = Field(default='', description='Вывод stdout/stderr и отчёт раннера')
    error_message: Optional[str] = Field(default=None, description='Человеческое описание непройденной проверки')
    error_line: Optional[int] = Field(default=None, description='Номер строки в коде обучающегося')
    xp_awarded: int = Field(default=0, description='Начисленный опыт (+15 XP при первом решении)')
    streak_days: int = Field(default=0, description='Текущий стрик дней')
    socratic_hint: Optional[str] = Field(default=None, description='Контекстная наводка Сократа без готового кода')


class TaskHintResponse(CompatBaseModel):
    """
    DTO выдачи наводки Сократа по задаче.
    """
    ok: bool = Field(default=True, description='Успешность запроса')
    task_id: int = Field(..., description='ID задачи')
    total_hints: int = Field(..., description='Всего доступных ступеней наводок')
    hint_level: int = Field(..., description='Текущая раскрытая ступень')
    hints: List[str] = Field(default_factory=list, description='Список раскрытых наводок')


class TaskDraftPayload(CompatBaseModel):
    """
    DTO сохранения черновика решения.
    """
    task_id: int = Field(..., description='ID задачи')
    draft_code: str = Field(..., description='Текущий рабочий черновик кода в редакторе')


class TaskDraftResponse(CompatBaseModel):
    """
    DTO подтверждения сохранения черновика.
    """
    ok: bool = Field(default=True, description='Статус сохранения')
    task_id: int = Field(..., description='ID задачи')
    saved_at: str = Field(..., description='ISO-время сохранения черновика')
