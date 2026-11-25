from typing import Any, Dict, List, Optional

from backend.app.schemas.path import (
    ChapterMeta,
    EchelonProgression,
    PathOverviewResponse,
    PathUnitNode,
)
from backend.app.services.content_service import content_service
from backend.app.services.sync_service import sync_service

ECHELONS_CONFIG = [
    {
        'id': 1,
        'title': 'Эшелон 1 · Скрининг и база',
        'subtitle': 'Синтаксис, структуры данных, базовый HTTP и подготовка к первичному скринингу',
        'chapters': [
            {'num': 1, 'title': 'Python Core: структуры, генераторы и ООП', 'short_title': 'Python Core', 'track': 'python', 'units': 5},
            {'num': 2, 'title': 'Web & HTTP: протоколы, заголовки, REST', 'short_title': 'Web & HTTP', 'track': 'web', 'units': 5},
            {'num': 3, 'title': 'Backend фундамент: роутинг и обработка данных', 'short_title': 'Backend', 'track': 'backend', 'units': 4},
        ],
    },
    {
        'id': 2,
        'title': 'Эшелон 2 · Тех-ядро и стек',
        'subtitle': 'FastAPI, асинхронность, PostgreSQL, транзакции и ORM',
        'chapters': [
            {'num': 4, 'title': 'Алгоритмическая сложность и базовые структуры', 'short_title': 'Алгоритмы', 'track': 'algorithms', 'units': 4},
            {'num': 5, 'title': 'Базы данных: индексы, ACID, миграции', 'short_title': 'Базы данных', 'track': 'databases', 'units': 5},
            {'num': 6, 'title': 'Паттерны архитектуры и чистый код', 'short_title': 'Архитектура', 'track': 'architecture', 'units': 5},
        ],
    },
    {
        'id': 3,
        'title': 'Эшелон 3 · Лайвкодинг и алгоритмы',
        'subtitle': 'Решение алгоритмических секций, оптимизация и concurrency',
        'chapters': [
            {'num': 4, 'title': 'Продвинутые структуры данных и графы', 'short_title': 'Алгоритмы Pro', 'track': 'algorithms', 'units': 4},
            {'num': 7, 'title': 'Инфраструктура: Docker, CI/CD, логирование', 'short_title': 'DevOps', 'track': 'infra', 'units': 4},
        ],
    },
    {
        'id': 4,
        'title': 'Эшелон 4 · Архитектура и оффер',
        'subtitle': 'Highload, микросервисы, шардирование и System Design финал',
        'chapters': [
            {'num': 6, 'title': 'System Design: распределённые очереди и кэш', 'short_title': 'System Design', 'track': 'architecture', 'units': 5},
            {'num': 7, 'title': 'Production Readiness и защита оффера', 'short_title': 'Оффер', 'track': 'infra', 'units': 4},
        ],
    },
]


class PathService:
    """
    Сервис расчёта и управления прогрессией интерактивной Тропы обучения.
    """

    def _get_mastered_unit_ids(self) -> List[str]:
        sync_record = sync_service.read_sync_record()
        user_state = (sync_record.get('bundle', {}).get('academyState', {})) if sync_record else {}
        mastered = user_state.get('mastered', [])
        return [str(m) for m in mastered] if isinstance(mastered, list) else []

    def get_echelon_progression(self, echelon_id: int) -> EchelonProgression:
        config = next((e for e in ECHELONS_CONFIG if e['id'] == echelon_id), ECHELONS_CONFIG[0])
        mastered_ids = self._get_mastered_unit_ids()

        chapters_meta: List[ChapterMeta] = []
        nodes: List[PathUnitNode] = []
        unit_counter = 1
        active_found = False
        active_unit_id: Optional[str] = None

        for ch in config['chapters']:
            ch_num = ch['num']
            u_count = ch['units']
            chapters_meta.append(
                ChapterMeta(
                    num=ch_num,
                    title=ch['title'],
                    short_title=ch['short_title'],
                    track=ch['track'],
                    unit_count=u_count,
                )
            )

            for u_idx in range(u_count):
                uid = f'unit_{echelon_id}_{ch_num}_{u_idx + 1}'
                is_mastered = uid in mastered_ids or (f'unit_{unit_counter}' in mastered_ids)

                if is_mastered:
                    status = 'mastered'
                elif not active_found:
                    status = 'active'
                    active_found = True
                    active_unit_id = uid
                else:
                    status = 'locked'

                is_gate = (u_idx == u_count - 1)  # Последний урок главы — рубежные ворота
                title = f'{ch["short_title"]} · Урок {u_idx + 1}'

                nodes.append(
                    PathUnitNode(
                        id=uid,
                        title=title,
                        unit_num=unit_counter,
                        chapter_num=ch_num,
                        echelon=echelon_id,
                        status=status,
                        is_gate=is_gate,
                        notes_count=1,
                        cards_count=5,
                        tasks_count=2,
                    )
                )
                unit_counter += 1

        total_units = len(nodes)
        mastered_count = sum(1 for n in nodes if n.status == 'mastered')
        pct = round(mastered_count / total_units * 100) if total_units > 0 else 0

        if not active_unit_id and nodes:
            active_unit_id = nodes[0].id

        return EchelonProgression(
            echelon_id=echelon_id,
            title=config['title'],
            subtitle=config['subtitle'],
            total_units=total_units,
            mastered_units=mastered_count,
            progress_pct=pct,
            active_unit_id=active_unit_id,
            chapters=chapters_meta,
            nodes=nodes,
        )

    def get_overview(self) -> PathOverviewResponse:
        echelons = [self.get_echelon_progression(e['id']) for e in ECHELONS_CONFIG]
        total_units = sum(e.total_units for e in echelons)
        total_mastered = sum(e.mastered_units for e in echelons)
        overall_pct = round(total_mastered / total_units * 100) if total_units > 0 else 0

        # Определение текущего активного эшелона (первый, в котором прогресс < 100%)
        active_ech = 1
        for e in echelons:
            if e.progress_pct < 100:
                active_ech = e.echelon_id
                break

        return PathOverviewResponse(
            ok=True,
            total_units=total_units,
            total_mastered=total_mastered,
            overall_progress_pct=overall_pct,
            active_echelon_id=active_ech,
            echelons=echelons,
        )


path_service = PathService()
