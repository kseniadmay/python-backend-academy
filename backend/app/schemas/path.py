from typing import List, Optional
from pydantic import Field

from backend.app.schemas.common import CompatBaseModel


class ChapterMeta(CompatBaseModel):
    """
    Метаданные главы Тропы обучения.
    """
    num: int = Field(..., ge=1, le=7, description='Номер главы (1..7)')
    title: str = Field(..., description='Полное название главы')
    short_title: str = Field(..., description='Краткое название главы для рельсы навигации')
    track: str = Field(..., description='Идентификатор трека (python, web, backend, etc.)')
    unit_count: int = Field(default=0, description='Количество уроков в главе')


class PathUnitNode(CompatBaseModel):
    """
    Узел урока на интерактивной змейке Тропы обучения.
    """
    id: str = Field(..., description='Идентификатор урока')
    title: str = Field(..., description='Название темы урока')
    unit_num: int = Field(..., description='Порядковый номер урока на тропе эшелона')
    chapter_num: int = Field(..., description='Номер главы (1..7)')
    echelon: int = Field(..., ge=1, le=4, description='Номер эшелона (1..4)')
    status: str = Field(..., description='Статус узла: active | mastered | locked')
    is_gate: bool = Field(default=False, description='Является ли узел рубежными воротами главы')
    notes_count: int = Field(default=1, description='Число конспектов в теме')
    cards_count: int = Field(default=1, description='Число карточек для закрепления')
    tasks_count: int = Field(default=1, description='Число задач в IDE')


class EchelonProgression(CompatBaseModel):
    """
    Полное состояние и структура конкретного эшелона.
    """
    echelon_id: int = Field(..., ge=1, le=4, description='Номер эшелона (1..4)')
    title: str = Field(..., description='Название эшелона')
    subtitle: str = Field(..., description='Фокус программы эшелона')
    total_units: int = Field(..., description='Всего уроков в эшелоне')
    mastered_units: int = Field(..., description='Пройдено уроков')
    progress_pct: int = Field(..., description='Процент завершения эшелона')
    active_unit_id: Optional[str] = Field(default=None, description='ID текущего активного урока для CTA')
    chapters: List[ChapterMeta] = Field(default_factory=list, description='Главы эшелона')
    nodes: List[PathUnitNode] = Field(default_factory=list, description='Узлы тропы эшелона')


class PathOverviewResponse(CompatBaseModel):
    """
    Общий обзор Тропы обучения по всем 4 эшелонам.
    """
    ok: bool = Field(default=True, description='Статус успешности запроса')
    total_units: int = Field(..., description='Всего уроков в курсе')
    total_mastered: int = Field(..., description='Всего освоено уроков')
    overall_progress_pct: int = Field(..., description='Общий прогресс курса в %')
    active_echelon_id: int = Field(default=1, description='Текущий активный эшелон обучающегося')
    echelons: List[EchelonProgression] = Field(default_factory=list, description='Список всех 4 эшелонов')
