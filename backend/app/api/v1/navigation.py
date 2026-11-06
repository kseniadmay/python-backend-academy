from fastapi import APIRouter

from backend.app.schemas.navigation import NavigationMetaResponse
from backend.app.services.navigation_service import navigation_service

router = APIRouter(prefix='/navigation', tags=['Navigation & App Shell'])


@router.get(
    '/meta',
    response_model=NavigationMetaResponse,
    summary='Метаданные навигации платформы',
    description='Единый источник истины (Single Source of Truth) для сборки десктопного сайдбара, мобильного таббара и шторки меню с бейджами активности.'
)
def get_navigation_meta() -> NavigationMetaResponse:
    """
    Возвращает структуру маршрутов, иконки, группы и динамические бейджи прогресса.
    """
    return navigation_service.get_navigation_meta()
