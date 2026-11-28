import logging
import re
import time
from typing import Any, Dict, List, Optional, Tuple

from backend.app.core.config import atomic_write_json_file, read_json_file, settings
from backend.app.schemas.progress import SyncPushRequest

logger = logging.getLogger('academy.sync')
_BUG_JUNK_RE = re.compile(r'[\ufffd\x00-\x08\x0b\x0c\x0e-\x1f]+')
_CTRL_JUNK_RE = re.compile(r'[\ufffd\x00-\x1f]+')
_DIGITS_RE = re.compile(r'\d+')
_PAIR_NUM_RE = re.compile(r'(\d+):(\d+)')
_CHUNK_KEY_RE = re.compile(r'^skill:.*?(\d+):(\d+):(\d+)$')

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
            rev_a = str(entry_a.get('lastReview') or entry_a.get('lastReviewed') or '')
            rev_b = str(entry_b.get('lastReview') or entry_b.get('lastReviewed') or '')
            if rev_b != rev_a:
                pick_b = rev_b > rev_a
            else:
                ts_a = int(entry_a.get('reviewedAt') or entry_a.get('lastSignalAt') or 0)
                ts_b = int(entry_b.get('reviewedAt') or entry_b.get('lastSignalAt') or 0)
                if ts_a != ts_b:
                    pick_b = ts_b > ts_a
                else:
                    prog_a = int(entry_a.get(progress_key) or 0)
                    prog_b = int(entry_b.get(progress_key) or 0)
                    pick_b = prog_b >= prog_a
            merged[k] = dict(entry_b if pick_b else entry_a)
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

    if isinstance(a.get('taskSrs'), dict) or isinstance(b.get('taskSrs'), dict):
        merged['taskSrs'] = _merge_srs_entries(a.get('taskSrs'), b.get('taskSrs'), 'reps')

    if 'practiceDailyLimit' in a or 'practiceDailyLimit' in b:
        b_newer = int(b.get('updatedAt') or 0) >= int(a.get('updatedAt') or 0)
        if b_newer and 'practiceDailyLimit' in b:
            merged['practiceDailyLimit'] = b['practiceDailyLimit']
        elif 'practiceDailyLimit' in a:
            merged['practiceDailyLimit'] = a['practiceDailyLimit']
        elif 'practiceDailyLimit' in b:
            merged['practiceDailyLimit'] = b['practiceDailyLimit']

    if isinstance(a.get('cardSrs'), dict) or isinstance(b.get('cardSrs'), dict):
        merged['cardSrs'] = _merge_srs_entries(a.get('cardSrs'), b.get('cardSrs'), 'reps')
        if not isinstance(merged.get('cardRatings'), dict):
            merged['cardRatings'] = {}
        for ck, srs_item in merged['cardSrs'].items():
            if isinstance(srs_item, dict) and isinstance(srs_item.get('lastGrade'), (int, float)) and srs_item['lastGrade'] > 0:
                merged['cardRatings'][ck] = int(srs_item['lastGrade'])

    for bool_key in ('completedNoteSteps', 'unlockedChunks'):
        if isinstance(a.get(bool_key), dict) or isinstance(b.get(bool_key), dict):
            map_a = a.get(bool_key) if isinstance(a.get(bool_key), dict) else {}
            map_b = b.get(bool_key) if isinstance(b.get(bool_key), dict) else {}
            merged_bool: Dict[str, bool] = {}
            for src in (map_a, map_b):
                for bk, bv in src.items():
                    merged_bool[bk] = bool(merged_bool.get(bk) or bv)
            merged[bool_key] = merged_bool

    if isinstance(a.get('readingPositions'), dict) or isinstance(b.get('readingPositions'), dict):
        pos_a = a.get('readingPositions') if isinstance(a.get('readingPositions'), dict) else {}
        pos_b = b.get('readingPositions') if isinstance(b.get('readingPositions'), dict) else {}
        merged['readingPositions'] = {**pos_a, **pos_b}

    return sanitize_academy_state(merged)


def _sanitize_academy_key(k: Any, prefix: str = '') -> str:
    """Нормализует ключи конспектов и колод (К-NNN / Ф-NNN), очищая битые UTF-8 префиксы."""
    if not isinstance(k, str):
        return ''
    m = _DIGITS_RE.search(k)
    if m:
        return f'{prefix}{m.group(0).zfill(3)}'
    return _CTRL_JUNK_RE.sub('', k).strip()


def _sanitize_card_key(k: Any) -> str:
    """Нормализует ключи карточек к виду Ф-NNN:idx."""
    if not isinstance(k, str):
        return str(k)
    m = _PAIR_NUM_RE.search(k)
    if m:
        return f'Ф-{m.group(1).zfill(3)}:{m.group(2)}'
    return _CTRL_JUNK_RE.sub('', k).strip()


def _sanitize_bug_reports(items: Any) -> List[Dict[str, Any]]:
    """Очищает список замечаний от битой кодировки, обрезает текст и убирает дубли."""
    if not isinstance(items, list):
        return []
    cleaned: List[Dict[str, Any]] = []
    seen = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        raw_text = _BUG_JUNK_RE.sub('', str(item.get('text') or '')).strip()[:2000]
        if not raw_text:
            continue
        raw_ctx = _BUG_JUNK_RE.sub('', str(item.get('context') or '')).strip()[:500]
        dedup_key = f"{item.get('timestamp') or ''}|{raw_ctx}|{raw_text}"
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        cleaned.append({**item, 'text': raw_text, 'context': raw_ctx})
    return cleaned


def sanitize_academy_state(s: Any) -> Any:
    """Нормализует и дедуплицирует ключи прогресса с битой кодировкой U+FFFD без потери данных."""
    if not isinstance(s, dict):
        return s

    if isinstance(s.get('readNotes'), list):
        clean_rn: List[str] = []
        seen_rn = set()
        for item in s['readNotes']:
            cx = _sanitize_academy_key(item, 'К-')
            if cx and cx not in seen_rn:
                seen_rn.add(cx)
                clean_rn.append(cx)
        s['readNotes'] = clean_rn

    if isinstance(s.get('reviewedDecks'), list):
        clean_rd: List[str] = []
        seen_rd = set()
        for item in s['reviewedDecks']:
            cd = _sanitize_academy_key(item, 'Ф-')
            if cd and cd not in seen_rd:
                seen_rd.add(cd)
                clean_rd.append(cd)
        s['reviewedDecks'] = clean_rd

    if isinstance(s.get('noteSrs'), dict):
        clean_notes: Dict[str, Any] = {}
        for k, v in s['noteSrs'].items():
            ck = _sanitize_academy_key(k, 'К-')
            if not ck or not isinstance(v, dict):
                continue
            cur = clean_notes.get(ck)
            if cur is None:
                clean_notes[ck] = dict(v)
            else:
                v_rank = (int(v.get('step') or 0), int(v.get('interval') or 0), str(v.get('lastReview') or ''))
                c_rank = (int(cur.get('step') or 0), int(cur.get('interval') or 0), str(cur.get('lastReview') or ''))
                if v_rank > c_rank:
                    clean_notes[ck] = dict(v)
        s['noteSrs'] = clean_notes

    if isinstance(s.get('cardSrs'), dict):
        clean_cards: Dict[str, Any] = {}
        for k, v in s['cardSrs'].items():
            ck = _sanitize_card_key(k)
            if not ck or not isinstance(v, dict):
                continue
            cur = clean_cards.get(ck)
            if cur is None:
                clean_cards[ck] = dict(v)
            else:
                v_rank = (
                    str(v.get('lastReview') or ''),
                    int(v.get('reviewedAt') or v.get('lastSignalAt') or 0),
                    int(v.get('reps') or 0),
                    int(v.get('interval') or 0),
                )
                c_rank = (
                    str(cur.get('lastReview') or ''),
                    int(cur.get('reviewedAt') or cur.get('lastSignalAt') or 0),
                    int(cur.get('reps') or 0),
                    int(cur.get('interval') or 0),
                )
                if v_rank > c_rank:
                    clean_cards[ck] = dict(v)
        s['cardSrs'] = clean_cards

    if isinstance(s.get('cardRatings'), dict):
        clean_ratings: Dict[str, Any] = {}
        for k, v in s['cardRatings'].items():
            ck = _sanitize_card_key(k)
            if not ck:
                continue
            try:
                num = float(v or 0)
            except (TypeError, ValueError):
                num = 0
            cur_val = float(clean_ratings.get(ck) or 0)
            best = max(cur_val, num)
            clean_ratings[ck] = int(best) if best.is_integer() else best
        s['cardRatings'] = clean_ratings

    if isinstance(s.get('completedNoteSteps'), dict):
        clean_steps: Dict[str, bool] = {}
        for k, v in s['completedNoteSteps'].items():
            ks = str(k)
            m = _PAIR_NUM_RE.search(ks)
            if m:
                ck = f'К-{m.group(1).zfill(3)}:{m.group(2)}'
            elif _CTRL_JUNK_RE.search(ks):
                continue
            else:
                ck = ks
            clean_steps[ck] = bool(clean_steps.get(ck) or v)
        s['completedNoteSteps'] = clean_steps

    if isinstance(s.get('unlockedChunks'), dict):
        clean_chunks: Dict[str, bool] = {}
        for k, v in s['unlockedChunks'].items():
            ks = str(k)
            m = _CHUNK_KEY_RE.match(ks)
            if m:
                ck = f'skill:К-{m.group(1).zfill(3)}:{m.group(2)}:{m.group(3)}'
            elif _CTRL_JUNK_RE.search(ks):
                continue
            else:
                ck = ks
            clean_chunks[ck] = bool(clean_chunks.get(ck) or v)
        s['unlockedChunks'] = clean_chunks

    if isinstance(s.get('readingPositions'), dict):
        for pos in s['readingPositions'].values():
            if not isinstance(pos, dict):
                continue
            if pos.get('kId'):
                pos['kId'] = _sanitize_academy_key(pos['kId'], 'К-')
            if pos.get('fId'):
                pos['fId'] = _sanitize_academy_key(pos['fId'], 'Ф-')
            if pos.get('deckId'):
                pos['deckId'] = _sanitize_academy_key(pos['deckId'], 'Ф-')
            if isinstance(pos.get('deckPositions'), dict):
                clean_dp: Dict[str, Any] = {}
                for dp_k, dp_v in pos['deckPositions'].items():
                    cdp_k = _sanitize_academy_key(dp_k, 'Ф-')
                    if not cdp_k:
                        continue
                    if cdp_k not in clean_dp or (
                        isinstance(dp_v, dict)
                        and int(dp_v.get('sessionLearned') or 0) > int((clean_dp[cdp_k] or {}).get('sessionLearned') or 0)
                    ):
                        clean_dp[cdp_k] = dp_v
                pos['deckPositions'] = clean_dp

    if isinstance(s.get('cardsHubPos'), dict):
        chp = s['cardsHubPos']
        if chp.get('deckId'):
            chp['deckId'] = _sanitize_academy_key(chp['deckId'], 'Ф-')
        if isinstance(chp.get('dueQueue'), list):
            clean_dq: List[Dict[str, Any]] = []
            seen_dq = set()
            for item in chp['dueQueue']:
                if not isinstance(item, dict):
                    continue
                did = _sanitize_academy_key(item.get('deckId'), 'Ф-')
                cidx = int(item.get('cardIdx') or 0)
                ckey = f'{did}:{cidx}'
                if ckey not in seen_dq:
                    seen_dq.add(ckey)
                    clean_dq.append({**item, 'deckId': did, 'cardIdx': cidx})
            chp['dueQueue'] = clean_dq

    if isinstance(s.get('bugReports'), list):
        s['bugReports'] = _sanitize_bug_reports(s['bugReports'])

    if isinstance(s.get('taskSrs'), dict):
        clean_tasks: Dict[str, Any] = {}
        for k, v in s['taskSrs'].items():
            if not isinstance(v, dict):
                continue
            try:
                tid_int = int(str(k).strip())
            except (TypeError, ValueError):
                continue
            if tid_int <= 0:
                continue
            tk = str(tid_int)
            try:
                interval_val = max(0.0, float(v.get('interval') or 0))
            except (TypeError, ValueError):
                interval_val = 0.0
            try:
                ease_val = max(1.3, float(v.get('ease') or 2.5))
            except (TypeError, ValueError):
                ease_val = 2.5
            try:
                reps_val = max(0, int(v.get('reps') or 0))
            except (TypeError, ValueError):
                reps_val = 0
            try:
                lapses_val = max(0, int(v.get('lapses') or 0))
            except (TypeError, ValueError):
                lapses_val = 0
            clean_entry: Dict[str, Any] = {
                'interval': int(interval_val) if interval_val.is_integer() else round(interval_val, 2),
                'ease': round(ease_val, 2),
                'reps': reps_val,
                'lapses': lapses_val,
                'due': _CTRL_JUNK_RE.sub('', str(v.get('due') or '')).strip()[:32],
                'lastReviewed': _CTRL_JUNK_RE.sub('', str(v.get('lastReviewed') or '')).strip()[:32],
                'lastOutcome': _CTRL_JUNK_RE.sub('', str(v.get('lastOutcome') or '')).strip()[:16],
                'neededHelp': bool(v.get('neededHelp', False)),
                'skillId': _CTRL_JUNK_RE.sub('', str(v.get('skillId') or '')).strip()[:32],
            }
            cur = clean_tasks.get(tk)
            if cur is None:
                clean_tasks[tk] = clean_entry
            else:
                v_rank = (clean_entry['lastReviewed'], clean_entry['reps'], clean_entry['interval'])
                c_rank = (cur['lastReviewed'], cur['reps'], cur['interval'])
                if v_rank > c_rank:
                    clean_tasks[tk] = clean_entry
        s['taskSrs'] = clean_tasks

    if 'practiceDailyLimit' in s:
        try:
            lim = int(s['practiceDailyLimit'])
        except (TypeError, ValueError):
            lim = 0
        s['practiceDailyLimit'] = lim if lim in (0, 3, 5, 10) else 0

    return s


class SyncService:
    def __init__(self) -> None:
        settings.DATA_DIR.mkdir(parents=True, exist_ok=True)

    def read_sync_record(self) -> Optional[Dict[str, Any]]:
        """
        Считывает текущее сохраненное состояние прогресса из хранилища.
        """
        data = read_json_file(settings.progress_sync_file, default=None, logger=logger)
        if isinstance(data, dict) and 'bundle' in data:
            bundle = data.get('bundle')
            if isinstance(bundle, dict) and isinstance(bundle.get('academyState'), dict):
                bundle['academyState'] = sanitize_academy_state(bundle['academyState'])
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
        elif isinstance(next_bundle.get('academyState'), dict):
            next_bundle['academyState'] = sanitize_academy_state(next_bundle['academyState'])

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
