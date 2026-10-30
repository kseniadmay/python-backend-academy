import logging
import time
from typing import Any, Dict, List, Optional, Tuple

from backend.app.core.config import atomic_write_json_file, read_json_file, settings
from backend.app.schemas.progress import SyncPushRequest

logger = logging.getLogger('academy.sync')

_UNION_LIST_KEYS = (
    'mastered',
    'completedLessons',
    'completedTasks',
    'readNotes',
    'reviewedDecks',
    'passedUnitTests',
    'passedBosses',
    'diagnosticGaps',
)

_MAX_NUMERIC_MAP_KEYS = (
    'skillMastery',
    'dailyXpByDate',
    'cardRatings',
)


def _unique_union_list(base_list: Any, incoming_list: Any) -> List[Any]:
    out: List[Any] = []
    seen = set()
    for src in (base_list, incoming_list):
        if isinstance(src, list):
            for item in src:
                marker = repr(item)
                if marker not in seen:
                    seen.add(marker)
                    out.append(item)
    return out


def _merge_srs_entries(base_map: Any, incoming_map: Any, progress_key: str) -> Dict[str, Any]:
    a = base_map if isinstance(base_map, dict) else {}
    b = incoming_map if isinstance(incoming_map, dict) else {}
    merged: Dict[str, Any] = {}
    all_keys = list(dict.fromkeys(list(a.keys()) + list(b.keys())))
    for k in all_keys:
        entry_a = a.get(k)
        entry_b = b.get(k)
        if isinstance(entry_a, dict) and isinstance(entry_b, dict):
            rev_a = str(entry_a.get('lastReview') or '')
            rev_b = str(entry_b.get('lastReview') or '')
            prog_a = int(entry_a.get(progress_key) or 0)
            prog_b = int(entry_b.get(progress_key) or 0)
            pick_b = (rev_b >= rev_a) or (prog_b > prog_a)
            merged[k] = {**entry_a, **(entry_b if pick_b else entry_a)}
        elif isinstance(entry_b, dict):
            merged[k] = dict(entry_b)
        elif isinstance(entry_a, dict):
            merged[k] = dict(entry_a)
        elif k in b:
            merged[k] = entry_b
        else:
            merged[k] = entry_a
    return merged


def merge_academy_states(stored_state: Optional[Dict[str, Any]], incoming_state: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Глубокое монотонное слияние состояния прогресса:
    - сохраняет верхнеуровневые поля incoming поверх stored;
    - объединяет списки пройденных конспектов, колод, уроков и задач без дублей;
    - глубоко сливает расписания интервального повторения cardSrs и noteSrs (1/3/7/21/30),
      а также оценки карточек cardRatings и прогресс чтения readingPositions.
    """
    a = stored_state if isinstance(stored_state, dict) else {}
    b = incoming_state if isinstance(incoming_state, dict) else {}
    merged: Dict[str, Any] = {**a, **b}

    for key in _UNION_LIST_KEYS:
        if key in a or key in b:
            merged[key] = _unique_union_list(a.get(key), b.get(key))

    for key in _MAX_NUMERIC_MAP_KEYS:
        if isinstance(a.get(key), dict) or isinstance(b.get(key), dict):
            map_a = a.get(key) if isinstance(a.get(key), dict) else {}
            map_b = b.get(key) if isinstance(b.get(key), dict) else {}
            combined: Dict[str, Any] = {**map_a, **map_b}
            for sub_key in set(map_a.keys()).intersection(map_b.keys()):
                try:
                    combined[sub_key] = max(float(map_a[sub_key] or 0), float(map_b[sub_key] or 0))
                    if float(combined[sub_key]).is_integer():
                        combined[sub_key] = int(combined[sub_key])
                except (TypeError, ValueError):
                    combined[sub_key] = map_b[sub_key]
            merged[key] = combined

    if isinstance(a.get('noteSrs'), dict) or isinstance(b.get('noteSrs'), dict):
        merged['noteSrs'] = _merge_srs_entries(a.get('noteSrs'), b.get('noteSrs'), 'step')

    if isinstance(a.get('cardSrs'), dict) or isinstance(b.get('cardSrs'), dict):
        merged['cardSrs'] = _merge_srs_entries(a.get('cardSrs'), b.get('cardSrs'), 'reps')

    if isinstance(a.get('readingPositions'), dict) or isinstance(b.get('readingPositions'), dict):
        pos_a = a.get('readingPositions') if isinstance(a.get('readingPositions'), dict) else {}
        pos_b = b.get('readingPositions') if isinstance(b.get('readingPositions'), dict) else {}
        merged['readingPositions'] = {**pos_a, **pos_b}

    return merged


class SyncService:
    def __init__(self) -> None:
        settings.DATA_DIR.mkdir(parents=True, exist_ok=True)

    def read_sync_record(self) -> Optional[Dict[str, Any]]:
        """
        Считывает текущее сохраненное состояние прогресса из хранилища.
        """
        data = read_json_file(settings.progress_sync_file, default=None, logger=logger)
        if isinstance(data, dict) and 'bundle' in data:
            return data
        return None

    def write_sync_record(self, record: Dict[str, Any]) -> None:
        """
        Атомарно записывает состояние прогресса через единый слой хранения.
        """
        atomic_write_json_file(settings.progress_sync_file, record)

    def process_push(self, payload: SyncPushRequest) -> Tuple[bool, Dict[str, Any], int]:
        """
        Обрабатывает пуш прогресса с устройства с защитой от потерянных обновлений
        и серверным слиянием монотонно возрастающего прогресса.
        Возвращает: (is_success, response_data, http_status_code)
        """
        bundle = payload.bundle.model_dump()
        client_id = str(payload.clientId or payload.device or 'unknown')
        base_updated_at = payload.baseUpdatedAt or 0

        stored = self.read_sync_record()
        now_ms = int(time.time() * 1000)

        if stored:
            stored_client_id = str(stored.get('clientId') or stored.get('device') or '')
            stored_updated_at = int(stored.get('updatedAt', 0))

            # Lost-update guard: если другое устройство успело запушить более свежий бандл
            is_stale = (
                stored_client_id
                and stored_client_id != client_id
                and stored_updated_at > (base_updated_at + settings.SYNC_DEVICE_TTL_MS)
            )

            if is_stale:
                logger.warning(
                    'Конфликт устройств (%s vs %s) — требуется повторное слияние',
                    payload.device,
                    stored.get('device')
                )
                return False, {
                    'ok': False,
                    'conflict': True,
                    'updatedAt': stored_updated_at,
                    'device': stored.get('device'),
                    'bundle': stored.get('bundle')
                }, 409

        # Безопасное глубокое объединение прогресса (включая cardSrs, noteSrs, readNotes, reviewedDecks)
        next_bundle = bundle
        if stored and stored.get('bundle'):
            stored_bundle = stored['bundle']
            next_bundle = {
                'academyState': merge_academy_states(
                    stored_bundle.get('academyState'),
                    bundle.get('academyState')
                ),
                'ideStatus': {**(stored_bundle.get('ideStatus') or {}), **(bundle.get('ideStatus') or {})},
                'ideDrafts': {**(stored_bundle.get('ideDrafts') or {}), **(bundle.get('ideDrafts') or {})}
            }

        new_record = {
            'updatedAt': now_ms,
            'device': str(payload.device or 'unknown'),
            'clientId': client_id,
            'bundle': next_bundle
        }

        self.write_sync_record(new_record)
        logger.info('Прогресс успешно сохранен (устройство: %s, timestamp: %s)', payload.device, now_ms)

        return True, {
            'ok': True,
            'updatedAt': now_ms,
            'bundle': next_bundle
        }, 200


sync_service = SyncService()
