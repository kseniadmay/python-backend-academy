from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.schemas.practice import (
    TaskDraftPayload,
    TaskDraftResponse,
    TaskHintResponse,
    TaskRunRequest,
    TaskRunResponse,
)
from backend.app.services.code_runner_service import code_runner_service

router = APIRouter(prefix='/practice', tags=['Zen IDE & Code Execution'])


@router.post(
    '/run',
    response_model=TaskRunResponse,
    summary='Исполнение и тестирование Python-решения задачи',
    description='Запускает код обучающегося в изолированном контексте, проверяет через набор проверочных условий задачи, начисляет +15 XP и стрик при успехе.'
)
def run_task_code(payload: TaskRunRequest) -> TaskRunResponse:
    """
    Запуск решения практической задачи с возвратом статуса (pass/fail), stdout и ошибок.
    """
    return code_runner_service.run_task(payload)


@router.get(
    '/hint/{task_id}',
    response_model=TaskHintResponse,
    summary='Получение ступенчатых наводок Сократа без готового кода',
    description='Возвращает дидактические наводки уровня 1..N, направляющие мышление разработчика к самостоятельному решению.'
)
def get_task_hints(
    task_id: int,
    level: int = Query(1, ge=1, le=10, description='Ступень наводки')
) -> TaskHintResponse:
    """
    Выдача сократических подсказок по задаче.
    """
    return code_runner_service.get_hints(task_id, requested_level=level)


@router.post(
    '/draft',
    response_model=TaskDraftResponse,
    summary='Сохранение черновика кода задачи'
)
def save_task_draft(payload: TaskDraftPayload) -> TaskDraftResponse:
    """
    Персистентное сохранение черновика решения в редакторе.
    """
    return code_runner_service.save_draft(payload)


@router.get(
    '/draft/{task_id}',
    summary='Загрузка последнего черновика кода'
)
def get_task_draft(task_id: int):
    """
    Получение ранее сохранённого черновика решения.
    """
    draft = code_runner_service.get_draft(task_id)
    return {'ok': True, 'task_id': task_id, 'draft': draft}
