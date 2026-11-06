from typing import Any, Dict, List, Optional

from backend.app.schemas.navigation import NavGroup, NavItem, NavigationMetaResponse
from backend.app.services.srs_service import srs_service
from backend.app.services.sync_service import sync_service

# Канонический авторитарный реестр навигации платформы (DRY Single Source of Truth)
CANONICAL_NAV_ITEMS: List[Dict[str, Any]] = [
    {'route': '/', 'icon': 'home', 'label': 'Дашборд', 'short_label': 'Дашборд', 'mobile_tab': True, 'group': 'main'},
    {'route': '/path', 'icon': 'path', 'label': 'Путь к офферу', 'short_label': 'Путь', 'mobile_tab': True, 'group': 'main'},
    {'route': '/cards', 'icon': 'cards', 'label': 'Интервалка', 'short_label': 'Интервалка', 'mobile_tab': True, 'group': 'main', 'has_due_dot': True},
    {'route': '/practice', 'icon': 'code', 'label': 'Zen IDE', 'short_label': 'IDE', 'mobile_tab': True, 'group': 'main'},

    {'route': '/notes-review', 'icon': 'book', 'label': 'Конспекты', 'short_label': 'Конспекты', 'mobile_tab': False, 'group': 'trainer'},
    {'route': '/mock', 'icon': 'mock', 'label': 'Собеседование', 'short_label': 'Интервью', 'mobile_tab': False, 'group': 'trainer'},

    {'route': '/python', 'icon': 'python', 'label': 'Python Core', 'short_label': 'Python', 'mobile_tab': False, 'group': 'module'},
    {'route': '/web', 'icon': 'globe', 'label': 'Web и HTTP', 'short_label': 'Web', 'mobile_tab': False, 'group': 'module'},
    {'route': '/backend', 'icon': 'server', 'label': 'Backend', 'short_label': 'Backend', 'mobile_tab': False, 'group': 'module'},
    {'route': '/algorithms', 'icon': 'bolt', 'label': 'Алгоритмы', 'short_label': 'Алгоритмы', 'mobile_tab': False, 'group': 'module'},
    {'route': '/databases', 'icon': 'database', 'label': 'Базы данных', 'short_label': 'БД', 'mobile_tab': False, 'group': 'module'},
    {'route': '/architecture', 'icon': 'arch', 'label': 'Архитектура', 'short_label': 'Архит.', 'mobile_tab': False, 'group': 'module'},
    {'route': '/infra', 'icon': 'rocket', 'label': 'Инфраструктура', 'short_label': 'Инфра', 'mobile_tab': False, 'group': 'module'},

    {'route': '/docs', 'icon': 'book', 'label': 'Справочник', 'short_label': 'Справочник', 'mobile_tab': False, 'group': 'tool'},
    {'route': '/sandbox', 'icon': 'terminal', 'label': 'Песочница', 'short_label': 'Песочница', 'mobile_tab': False, 'group': 'tool'},
]

GROUP_TITLES: Dict[str, str] = {
    'main': 'Обучение и практика',
    'trainer': 'Собеседование и ретеншн',
    'module': 'Модули курса',
    'tool': 'База знаний и лаборатория',
}


class NavigationService:
    """
    Сервис управления навигационным деревом, метаданными и бейджами активности.
    """

    def get_navigation_meta(self) -> NavigationMetaResponse:
        # 1. Получение счетчиков интервального повторения на сегодня
        srs_stats = srs_service.get_stats()
        due_cards = srs_stats.due_today

        # 2. Получение сохраненного прогресса пользователя из sync_service
        sync_record = sync_service.read_sync_record()
        user_state = (sync_record.get('bundle', {}).get('academyState', {})) if sync_record else {}

        # 3. Расчет прогресса модулей (заглушка/расчет по пройденным урокам)
        mastered = user_state.get('mastered', [])
        mastered_count = len(mastered) if isinstance(mastered, list) else 0

        module_pct_map = {
            '/python': min(100, mastered_count * 10),
            '/web': 0,
            '/backend': 0,
            '/algorithms': 0,
            '/databases': 0,
            '/architecture': 0,
            '/infra': 0,
        }
        total_pct = min(100, round(mastered_count / 45 * 100))

        # 4. Формирование элементов с бейджами
        all_items: List[NavItem] = []
        for raw in CANONICAL_NAV_ITEMS:
            item = NavItem.model_validate(raw)
            if item.route == '/cards' and due_cards > 0:
                item.badge = str(due_cards)
            elif item.route == '/path':
                item.badge = f'Шаг {mastered_count + 1}'
            elif item.route in module_pct_map and module_pct_map[item.route] > 0:
                item.badge = f'{module_pct_map[item.route]}%'
            all_items.append(item)

        # 5. Разделение по группам для десктопного сайдбара
        desktop_groups: List[NavGroup] = []
        for grp_id, grp_title in GROUP_TITLES.items():
            grp_items = [it for it in all_items if it.group == grp_id]
            if grp_items:
                desktop_groups.append(NavGroup(id=grp_id, title=grp_title, items=grp_items))

        # 6. Мобильные табы (4 основных таба для зоны большого пальца)
        mobile_tabs = [it for it in all_items if it.mobile_tab]

        return NavigationMetaResponse(
            ok=True,
            desktop_groups=desktop_groups,
            mobile_tabs=mobile_tabs,
            drawer_items=all_items,
            due_cards_count=due_cards,
            due_notes_count=0,
            module_progress_pct=module_pct_map,
            total_progress_pct=total_pct,
        )


navigation_service = NavigationService()
