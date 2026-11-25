import hmac
from typing import Optional
from fastapi import Header, HTTPException, status
from backend.app.core.config import settings


def verify_sync_token(authorization_header: Optional[str]) -> bool:
    """
    Проверяет Bearer token синхронизации в защищенном от timing attacks режиме.
    Если SYNC_TOKEN не задан в конфигурации, доступ открыт для локальной разработки.
    """
    if not settings.SYNC_TOKEN:
        return True

    if not authorization_header:
        return False

    prefix = 'Bearer '
    supplied = (
        authorization_header[len(prefix):]
        if authorization_header.startswith(prefix)
        else authorization_header
    )
    return hmac.compare_digest(supplied.strip(), settings.SYNC_TOKEN)


def require_sync_auth(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Единая FastAPI-зависимость авторизации для защищенных эндпоинтов синхронизации.
    """
    if not verify_sync_token(authorization):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized: invalid sync token'
        )
    return authorization
