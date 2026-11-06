from fastapi import APIRouter, HTTPException, status

from backend.app.schemas.notes import (
    NoteDetail,
    NoteDueResponse,
    NoteProgressRequest,
    NoteProgressResponse,
)
from backend.app.services.notes_service import notes_service

router = APIRouter(prefix='/notes', tags=['Atomic Notes & Reader'])


@router.get(
    '/due',
    response_model=NoteDueResponse,
    summary='Конспекты, готовые к повторению сегодня (SRS 1/3/7/21/30)',
    description='Возвращает список прочитанных ранее конспектов, для которых подошел очередной интервал повторения.'
)
def get_due_notes() -> NoteDueResponse:
    """
    Выдача очереди конспектов на повторение.
    """
    return notes_service.get_due_notes()


@router.get(
    '/{note_id}',
    response_model=NoteDetail,
    summary='Получение атомарного конспекта по ID (например, К-001)',
    description='Возвращает пошаговый конспект (микро-шаги), сохраненную позицию чтения и связанную колоду карточек.'
)
def get_note_detail(note_id: str) -> NoteDetail:
    """
    Выдача конспекта с микро-шагами для Ридера.
    """
    note = notes_service.get_note_detail(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Конспект с ID {note_id} не найден'
        )
    return note


@router.post(
    '/progress',
    response_model=NoteProgressResponse,
    summary='Сохранение позиции чтения и завершения конспекта',
    description='Фиксирует текущий микро-шаг (Zero-Progress-Loss), при завершении начисляет +10 XP и планирует дату повторения.'
)
def save_note_progress(payload: NoteProgressRequest) -> NoteProgressResponse:
    """
    Фиксация прогресса чтения конспекта.
    """
    return notes_service.save_progress(payload)
