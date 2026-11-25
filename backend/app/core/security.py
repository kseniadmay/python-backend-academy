import base64
import hashlib
import hmac
import json
import time
from typing import Optional
from fastapi import Header, HTTPException, Request, Response, status
from backend.app.core.config import settings

SESSION_COOKIE_NAME = 'pba_session'


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


def verify_admin_credentials(username: str, password: str) -> bool:
    """
    Проверяет логин и пароль администратора через hmac.compare_digest.
    При пустых ADMIN_USERNAME или ADMIN_PASSWORD доступ всегда запрещён.
    """
    expected_user = settings.ADMIN_USERNAME
    expected_pass = settings.ADMIN_PASSWORD
    if not expected_user or not expected_pass:
        return False

    user_ok = hmac.compare_digest(username.encode('utf-8'), expected_user.encode('utf-8'))
    pass_ok = hmac.compare_digest(password.encode('utf-8'), expected_pass.encode('utf-8'))
    return user_ok and pass_ok


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode('ascii')


def _b64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode('ascii'))


def _sign_payload(payload_b64: str) -> str:
    secret = settings.SESSION_SECRET.encode('utf-8')
    digest = hmac.new(secret, payload_b64.encode('ascii'), hashlib.sha256).digest()
    return _b64url_encode(digest)


def create_session_token(username: str, ttl_days: Optional[int] = None) -> str:
    """
    Создаёт подписанный HMAC-SHA256 токен сессии с временем жизни.
    """
    days = ttl_days if ttl_days is not None else settings.SESSION_TTL_DAYS
    exp = int(time.time()) + max(1, days) * 86400
    payload = json.dumps({'u': username, 'exp': exp}, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    payload_b64 = _b64url_encode(payload)
    sig_b64 = _sign_payload(payload_b64)
    return f'{payload_b64}.{sig_b64}'


def verify_session_token(token: Optional[str]) -> Optional[str]:
    """
    Проверяет подпись HMAC-SHA256, срок действия и имя пользователя в токене сессии.
    Возвращает username при успехе или None.
    """
    if not token or '.' not in token:
        return None
    parts = token.split('.')
    if len(parts) != 2:
        return None
    payload_b64, sig_b64 = parts
    expected_sig = _sign_payload(payload_b64)
    if not hmac.compare_digest(sig_b64.encode('ascii'), expected_sig.encode('ascii')):
        return None

    try:
        payload = json.loads(_b64url_decode(payload_b64).decode('utf-8'))
    except Exception:
        return None

    if not isinstance(payload, dict):
        return None
    username = payload.get('u')
    exp = payload.get('exp')
    if not isinstance(username, str) or not username or not isinstance(exp, (int, float)):
        return None
    if exp <= time.time():
        return None
    if settings.ADMIN_USERNAME and not hmac.compare_digest(
        username.encode('utf-8'),
        settings.ADMIN_USERNAME.encode('utf-8')
    ):
        return None
    return username


def is_https_request(request: Request) -> bool:
    forwarded_proto = request.headers.get('x-forwarded-proto', '').split(',')[0].strip().lower()
    return request.url.scheme == 'https' or forwarded_proto == 'https'


def set_session_cookie(response: Response, request: Request, username: str) -> None:
    token = create_session_token(username)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite='lax',
        max_age=settings.SESSION_TTL_DAYS * 86400,
        secure=is_https_request(request),
        path='/',
    )


def clear_session_cookie(response: Response, request: Request) -> None:
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=True,
        samesite='lax',
        secure=is_https_request(request),
        path='/',
    )


def get_authenticated_admin(request: Request) -> Optional[str]:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    return verify_session_token(token)


def require_admin(request: Request) -> str:
    """
    FastAPI-зависимость: пропускает только запросы с валидной сессионной cookie.
    """
    username = get_authenticated_admin(request)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    return username
