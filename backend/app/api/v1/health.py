import time
from fastapi import APIRouter
from backend.app.schemas.common import HealthResponse

router = APIRouter(prefix='/health', tags=['Health'])


@router.get('', response_model=HealthResponse)
def get_health() -> HealthResponse:
    """
    Проверка жизнеспособности сервиса.
    """
    return HealthResponse(ok=True)
