from fastapi import APIRouter, HTTPException, Path as PathParam, status

from backend.app.schemas.path import EchelonProgression, PathOverviewResponse
from backend.app.services.path_service import path_service

router = APIRouter(prefix='/path', tags=['Learning Trail & Progression'])


@router.get(
    '/overview',
    response_model=PathOverviewResponse,
    summary='Общий обзор Тропы обучения по всем 4 эшелонам',
    description='Возвращает агрегированный прогресс по всем эшелонам, общее число уроков и текущий активный эшелон.'
)
def get_path_overview() -> PathOverviewResponse:
    """
    Получение сводки прогрессии Тропы обучения.
    """
    return path_service.get_overview()


@router.get(
    '/echelon/{echelon_id}',
    response_model=EchelonProgression,
    summary='Детальное дерево узлов тропы для выбранного эшелона (1..4)',
    description='Возвращает структуру глав, узлов змейки, статусы (active, mastered, locked) и рубежные ворота глав.'
)
def get_echelon_path(
    echelon_id: int = PathParam(..., ge=1, le=4, description='Номер эшелона (1..4)')
) -> EchelonProgression:
    """
    Выдача узлов интерактивной змейки выбранного эшелона.
    """
    return path_service.get_echelon_progression(echelon_id)
