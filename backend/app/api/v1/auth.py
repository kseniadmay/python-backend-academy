from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel

from backend.app.core.config import read_json_file, settings
from backend.app.core.security import (
    clear_session_cookie,
    get_authenticated_admin,
    require_admin,
    set_session_cookie,
    verify_admin_credentials,
)

auth_router = APIRouter(prefix='/auth', tags=['Auth'])
private_router = APIRouter(prefix='/private', tags=['Private Profile'])


class LoginRequest(BaseModel):
    username: str
    password: str


@auth_router.post('/login')
def login(payload: LoginRequest, request: Request, response: Response) -> dict:
    response.headers['Cache-Control'] = 'no-store'
    if not verify_admin_credentials(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'Cache-Control': 'no-store'},
        )
    set_session_cookie(response, request, payload.username)
    return {'authenticated': True, 'username': payload.username}


@auth_router.post('/logout')
def logout(request: Request, response: Response) -> dict:
    response.headers['Cache-Control'] = 'no-store'
    clear_session_cookie(response, request)
    return {'authenticated': False}


@auth_router.get('/me')
def auth_me(request: Request, response: Response) -> dict:
    response.headers['Cache-Control'] = 'no-store'
    username = get_authenticated_admin(request)
    return {
        'authenticated': bool(username),
        'site_lock_enabled': bool(settings.SITE_LOCK_ENABLED),
        'has_private_profile': settings.private_profile_file.is_file(),
    }


@private_router.get('/profile')
def get_private_profile(
    response: Response,
    _admin: str = Depends(require_admin),
) -> dict:
    response.headers['Cache-Control'] = 'no-store'
    data = read_json_file(settings.private_profile_file, default={})
    return data if isinstance(data, dict) else {}
