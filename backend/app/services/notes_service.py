import datetime
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.app.core.config import atomic_write_json_file, read_json_file, settings
from backend.app.schemas.notes import (
    NoteDetail,
    NoteDueItem,
    NoteDueResponse,
    NoteProgressRequest,
    NoteProgressResponse,
    NoteStep,
)
from backend.app.services.content_service import content_service
from backend.app.services.srs_service import srs_service
from backend.app.services.sync_service import sync_service

logger = logging.getLogger('academy.notes')

NOTE_SRS_SCHEDULE: List[int] = [1, 3, 7, 21, 30]


def _today_iso() -> str:
    return datetime.date.today().isoformat()


class NotesService:
    """
    Сервис управления атомарными конспектами, прогрессом чтения и интервальным повторением.
    """

    def __init__(self) -> None:
        self.progress_file = settings.DATA_DIR / 'user' / 'notes_progress.json'
        self._cache: Optional[Dict[str, Any]] = None

    def _ensure_dir(self) -> None:
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)

    def _get_data(self) -> Dict[str, Any]:
        if self._cache is None:
            self._ensure_dir()
            data = read_json_file(self.progress_file, default={}, logger=logger)
            self._cache = data if isinstance(data, dict) else {}
        return self._cache

    def _save_data(self) -> None:
        if self._cache is not None:
            self._ensure_dir()
            atomic_write_json_file(self.progress_file, self._cache)

    def get_note_detail(self, note_id: str) -> Optional[NoteDetail]:
        raw_note = content_service.get_note(note_id)
        if not raw_note:
            return None

        # Определение связанной колоды (К-001 -> Ф-001)
        related_deck = note_id.replace('К-', 'Ф-') if 'К-' in note_id else None
        all_decks = content_service.get_cards()
        if related_deck and related_deck not in all_decks:
            related_deck = None

        data = self._get_data()
        note_entry = data.get(note_id, {})
        saved_step = int(note_entry.get('saved_step', 0))
        is_read = bool(note_entry.get('is_read', False))

        raw_steps = raw_note.get('steps', [])
        steps: List[NoteStep] = []
        for idx, s in enumerate(raw_steps):
            steps.append(
                NoteStep(
                    step_index=idx,
                    title=s.get('title') or f'Шаг {idx + 1}',
                    html=s.get('html') or s.get('text') or '',
                    is_final=(idx == len(raw_steps) - 1),
                )
            )

        return NoteDetail(
            id=note_id,
            title=raw_note.get('title', note_id),
            total_steps=len(steps),
            related_deck_id=related_deck,
            current_saved_step=saved_step,
            is_read=is_read,
            steps=steps,
        )

    def save_progress(self, payload: NoteProgressRequest) -> NoteProgressResponse:
        note_id = payload.note_id
        step_index = payload.step_index
        is_completed = payload.is_completed

        data = self._get_data()
        entry = data.get(note_id, {
            'saved_step': 0,
            'is_read': False,
            'srs_step': 0,
            'due_date': None,
            'last_read_date': None,
        })

        entry['saved_step'] = step_index
        was_read = entry.get('is_read', False)

        xp_awarded = 0
        next_review_date = None

        if is_completed:
            entry['is_read'] = True
            today_date = datetime.date.today()
            today_str = today_date.isoformat()
            entry['last_read_date'] = today_str

            # Расписание Note SRS (1, 3, 7, 21, 30 дн.)
            current_srs_step = int(entry.get('srs_step', 0))
            interval_idx = min(len(NOTE_SRS_SCHEDULE) - 1, current_srs_step)
            interval_days = NOTE_SRS_SCHEDULE[interval_idx]
            next_date = today_date + datetime.timedelta(days=interval_days)
            next_review_date = next_date.isoformat()
            entry['due_date'] = next_review_date
            entry['srs_step'] = current_srs_step + 1

            if not was_read:
                xp_awarded = 10
                # Фиксация в sync_service
                sync_record = sync_service.read_sync_record()
                user_state = (sync_record.get('bundle', {}).get('academyState', {})) if sync_record else {}
                read_notes = user_state.get('readNotes', [])
                if note_id not in read_notes:
                    read_notes.append(note_id)
                    user_state['readNotes'] = read_notes
                    user_state['xp'] = int(user_state.get('xp', 0)) + 10

                    sync_service.write_sync_record({
                        'updatedAt': int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000),
                        'device': 'fastapi-reader',
                        'clientId': 'server-reader-engine',
                        'bundle': {
                            'academyState': user_state,
                            'ideStatus': {},
                            'ideDrafts': {}
                        }
                    })

        data[note_id] = entry
        self._save_data()

        return NoteProgressResponse(
            ok=True,
            note_id=note_id,
            saved_step=step_index,
            is_read=entry.get('is_read', False),
            next_review_date=next_review_date,
            xp_awarded=xp_awarded,
        )

    def get_due_notes(self) -> NoteDueResponse:
        data = self._get_data()
        today_str = _today_iso()
        all_notes = content_service.get_notes()

        due_items: List[NoteDueItem] = []
        for nid, entry in data.items():
            due_date = entry.get('due_date')
            if due_date and due_date <= today_str:
                note_title = all_notes.get(nid, {}).get('title', nid)
                srs_step = int(entry.get('srs_step', 1)) - 1
                srs_step = max(0, min(len(NOTE_SRS_SCHEDULE) - 1, srs_step))
                interval = NOTE_SRS_SCHEDULE[srs_step]

                due_items.append(
                    NoteDueItem(
                        note_id=nid,
                        title=note_title,
                        step=srs_step,
                        interval_days=interval,
                        due_date=due_date,
                    )
                )

        return NoteDueResponse(
            ok=True,
            due_count=len(due_items),
            notes=due_items,
        )


notes_service = NotesService()
