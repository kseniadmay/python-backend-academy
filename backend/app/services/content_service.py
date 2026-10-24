import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.app.core.config import settings

logger = logging.getLogger('academy.content')


class ContentService:
    def __init__(self) -> None:
        self.content_dir = settings.DATA_DIR / 'content'
        self._manifest: Optional[Dict[str, Any]] = None
        self._notes: Optional[Dict[str, Any]] = None
        self._cards: Optional[Dict[str, Any]] = None
        self._tasks: Optional[List[Dict[str, Any]]] = None

    def _load_json(self, file_name: str) -> Any:
        path = self.content_dir / file_name
        if not path.exists():
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error('Ошибка загрузки %s: %s', path, e)
            return None

    def get_manifest(self) -> Dict[str, Any]:
        if self._manifest is None:
            data = self._load_json('manifest.json')
            self._manifest = data or {
                'version': '1.0.0',
                'totalTasks': 401,
                'totalNotes': 238,
                'totalDecks': 287,
                'modules': []
            }
        return self._manifest

    def get_notes(self) -> Dict[str, Any]:
        if self._notes is None:
            self._notes = self._load_json('notes.json') or {}
        return self._notes

    def get_note(self, note_id: str) -> Optional[Dict[str, Any]]:
        notes = self.get_notes()
        return notes.get(note_id)

    def get_cards(self) -> Dict[str, Any]:
        if self._cards is None:
            self._cards = self._load_json('cards.json') or {}
        return self._cards

    def get_deck(self, deck_id: str) -> Optional[Dict[str, Any]]:
        cards = self.get_cards()
        return cards.get(deck_id)

    def get_tasks(
        self,
        level: Optional[int] = None,
        topic: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        if self._tasks is None:
            self._tasks = self._load_json('tasks.json') or []

        results = self._tasks
        if level is not None:
            results = [t for t in results if t.get('level') == level]
        if topic:
            topic_lower = topic.lower()
            results = [t for t in results if topic_lower in t.get('topic', '').lower()]
        return results

    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        tasks = self.get_tasks()
        for t in tasks:
            if t.get('id') == task_id:
                return t
        return None

    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        q = query.strip().lower()
        if not q:
            return []

        results = []
        # Поиск по конспектам
        notes = self.get_notes()
        for cid, note in notes.items():
            if q in note.get('title', '').lower():
                results.append({
                    'type': 'note',
                    'id': cid,
                    'title': note.get('title'),
                    'snippet': f"Конспект {cid}"
                })
                if len(results) >= limit:
                    return results

        # Поиск по задачам
        tasks = self.get_tasks()
        for t in tasks:
            if q in t.get('title', '').lower() or q in t.get('desc', '').lower():
                results.append({
                    'type': 'task',
                    'id': t.get('id'),
                    'title': t.get('title'),
                    'snippet': f"Задача #{t.get('id')} ({t.get('tier')})"
                })
                if len(results) >= limit:
                    return results

        return results


content_service = ContentService()
