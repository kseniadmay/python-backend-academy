import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from backend.app.api.legacy_compat import legacy_router
from backend.app.api.v1.router import api_v1_router
from backend.app.core.config import settings
from backend.app.core.network import get_local_ip


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    local_ip = get_local_ip()
    port = settings.PORT
    print('========================================================')
    print('       🐍 Python Backend Academy — FastAPI Core')
    print('========================================================')
    print(f'📁 Рабочая директория: {settings.ROOT_DIR}')
    print(f'💻 Локальный адрес на ПК: http://127.0.0.1:{port}/#/ (Swagger: http://127.0.0.1:{port}/docs)')
    print(f'📱 Локальный адрес (Wi-Fi): http://{local_ip}:{port}/#/')
    print('========================================================')
    yield


app = FastAPI(
    title='Python Backend Academy API',
    description='Высокопроизводительное ядро платформы подготовки Junior+ Python Backend разработчиков',
    version='1.0.0',
    lifespan=lifespan
)

# Настройка CORS для бесшовного доступа с мобильных устройств и PWA
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

NO_STORE_HEADERS = {
    'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0',
    'Pragma': 'no-cache',
    'Expires': '0',
    'Surrogate-Control': 'no-store',
}


@app.middleware('http')
async def add_no_store_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Surrogate-Control'] = 'no-store'
    return response


# Подключение API роутеров
app.include_router(legacy_router)
app.include_router(api_v1_router)


# Раздача статики и SPA fallback
@app.get('/{full_path:path}')
async def serve_spa_or_static(full_path: str, request: Request) -> Response:
    root_dir = settings.ROOT_DIR

    # Очистка пути от параметров и относительных обходов
    clean_path = full_path.strip().lstrip('/')
    if not clean_path or clean_path in ('index.html', 'academy.html'):
        return FileResponse(
            root_dir / 'academy.html',
            media_type='text/html; charset=utf-8',
            headers=NO_STORE_HEADERS
        )

    target_file = root_dir / clean_path

    # Защита от Path Traversal
    try:
        resolved_file = target_file.resolve()
        if not str(resolved_file).startswith(str(root_dir.resolve())):
            return FileResponse(root_dir / 'academy.html', media_type='text/html; charset=utf-8', headers=NO_STORE_HEADERS)
    except Exception:
        return FileResponse(root_dir / 'academy.html', media_type='text/html; charset=utf-8', headers=NO_STORE_HEADERS)

    if resolved_file.is_file():
        # Специфические MIME-типы для PWA и ассетов
        media_type = None
        suffix = resolved_file.suffix.lower()
        if suffix == '.js':
            media_type = 'application/javascript; charset=utf-8'
        elif suffix == '.css':
            media_type = 'text/css; charset=utf-8'
        elif suffix == '.json':
            media_type = 'application/json; charset=utf-8'
        elif suffix == '.svg':
            media_type = 'image/svg+xml'
        elif suffix == '.html':
            media_type = 'text/html; charset=utf-8'

        return FileResponse(
            resolved_file,
            media_type=media_type,
            headers=NO_STORE_HEADERS
        )

    # SPA Fallback для роутов
    return FileResponse(
        root_dir / 'academy.html',
        media_type='text/html; charset=utf-8',
        headers=NO_STORE_HEADERS
    )
