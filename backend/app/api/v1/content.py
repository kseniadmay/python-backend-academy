from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.services.content_service import content_service

router = APIRouter(prefix='/content', tags=['Content'])


@router.get('/summary')
def get_content_summary() -> Dict[str, Any]:
    """
    Возвращает сводные метрики программы обучения:
    число модулей, конспектов, карточек и практических задач.
    """
    manifest = content_service.get_manifest()
    return {
        'ok': True,
        'modulesCount': len(manifest.get('modules', [])),
        'notesCount': manifest.get('totalNotes', 0),
        'cardsCount': manifest.get('totalDecks', 0),
        'flashcardsCount': manifest.get('totalFlashcards', 0),
        'tasksCount': manifest.get('totalTasks', 0),
        'version': manifest.get('version', '1.0.0')
    }


@router.get('/modules')
def list_modules() -> List[Dict[str, Any]]:
    """
    Возвращает список 7 ключевых модулей программы обучения.
    """
    manifest = content_service.get_manifest()
    return manifest.get('modules', [])


@router.get('/notes/{note_id}')
def get_note(note_id: str) -> Dict[str, Any]:
    """
    Получение атомарного конспекта с микро-шагами по ID (например, К-001).
    """
    note = content_service.get_note(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Конспект с ID {note_id} не найден'
        )
    return {'ok': True, 'note': note}


@router.get('/cards/{deck_id}')
def get_deck(deck_id: str) -> Dict[str, Any]:
    """
    Получение колоды карточек интервального повторения по ID (например, Ф-001).
    """
    deck = content_service.get_deck(deck_id)
    if not deck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Колода с ID {deck_id} не найдена'
        )
    return {'ok': True, 'deck': deck}


@router.get('/tasks')
def list_tasks(
    level: Optional[int] = Query(None, ge=1, le=7, description='Уровень сложности 1..7'),
    topic: Optional[str] = Query(None, description='Тематика задачи')
) -> Dict[str, Any]:
    """
    Список практических задач IDE с возможностью фильтрации по уровню и теме.
    """
    tasks = content_service.get_tasks(level=level, topic=topic)
    return {'ok': True, 'count': len(tasks), 'tasks': tasks}


@router.get('/tasks/{task_id}')
def get_task(task_id: int) -> Dict[str, Any]:
    """
    Получение конкретной задачи с формулировкой, тестами и начальным кодом.
    """
    task = content_service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Задача с ID {task_id} не найдена'
        )
    return {'ok': True, 'task': task}


@router.get('/search')
def search_content(
    q: str = Query(..., min_length=2, description='Поисковый запрос')
) -> Dict[str, Any]:
    """
    Быстрый полнотекстовый поиск по конспектам и практическим задачам.
    """
    results = content_service.search(q)
    return {'ok': True, 'query': q, 'count': len(results), 'results': results}
