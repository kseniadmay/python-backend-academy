from typing import Dict, List, Optional
from pydantic import Field

from backend.app.schemas.common import CompatBaseModel


class NavItem(CompatBaseModel):
    """
    Элемент навигации приложения (Single Source of Truth для ПК и мобилки).
    """
    route: str = Field(..., description='Маршрут SPA (например, /path, /cards)')
    label: str = Field(..., description='Полное наименование для десктопа и шторки')
    short_label: str = Field(..., description='Краткое наименование для мобильного таббара')
    icon: str = Field(..., description='Имя SVG-иконки (home, path, cards, code, book, etc.)')
    group: str = Field(..., description='Категория: main | trainer | module | tool')
    mobile_tab: bool = Field(default=False, description='Отображать ли в нижнем плавающем таббаре смартфона')
    has_due_dot: bool = Field(default=False, description='Показывать ли бейдж наличия задач к повторению')
    badge: Optional[str] = Field(default=None, description='Текстовый бейдж (например, процент, счетчик)')


class NavGroup(CompatBaseModel):
    """
    Группа элементов меню.
    """
    id: str = Field(..., description='Идентификатор группы')
    title: str = Field(..., description='Заголовок группы в меню')
    items: List[NavItem] = Field(default_factory=list, description='Список ссылок в группе')


class NavigationMetaResponse(CompatBaseModel):
    """
    Полная модель навигации и состояния бейджей платформы.
    """
    ok: bool = Field(default=True, description='Статус ответа')
    desktop_groups: List[NavGroup] = Field(default_factory=list, description='Группы для десктопного сайдбара')
    mobile_tabs: List[NavItem] = Field(default_factory=list, description='Элементы плавающего мобильного таббара (4-5 пунктов)')
    drawer_items: List[NavItem] = Field(default_factory=list, description='Полный реестр ссылок для мобильной шторки')
    due_cards_count: int = Field(default=0, description='Число карточек SRS, готовых к повторению сегодня')
    due_notes_count: int = Field(default=0, description='Число конспектов, ожидающих повторения')
    module_progress_pct: Dict[str, int] = Field(default_factory=dict, description='Прогресс изучения по модулям курса в %')
    total_progress_pct: int = Field(default=0, description='Общий суммарный прогресс курса в %')
