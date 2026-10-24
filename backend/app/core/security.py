import hmac
from typing import Optional
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
    supplied = authorization_header[len(prefix):] if authorization_header.startswith(prefix) else authorization_header
    return hmac.compare_digest(supplied.strip(), settings.SYNC_TOKEN)
