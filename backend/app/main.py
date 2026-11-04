from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, Response

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
app.add_middleware(GZipMiddleware, minimum_size=1024)

NO_STORE_HEADERS = {
    'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0',
    'Pragma': 'no-cache',
    'Expires': '0',
    'Surrogate-Control': 'no-store',
}

STATIC_MEDIA_TYPES = {
    '.js': 'application/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.html': 'text/html; charset=utf-8',
}


def _serve_file_with_etag(file_path: Path, media_type: str, request: Request) -> Response:
    try:
        st = file_path.stat()
        etag = f'W/"{st.st_size:x}-{int(st.st_mtime):x}"'
        if request.headers.get('if-none-match') == etag:
            return Response(status_code=304, headers={'ETag': etag, 'Cache-Control': 'no-cache, must-revalidate'})
        return FileResponse(
            file_path,
            media_type=media_type,
            headers={
                'ETag': etag,
                'Cache-Control': 'no-cache, must-revalidate',
                'Access-Control-Allow-Origin': '*'
            }
        )
    except Exception:
        return FileResponse(file_path, media_type=media_type)

def _serve_spa_entry(root_dir: Path, request: Request) -> Response:
    return _serve_file_with_etag(root_dir / 'academy.html', 'text/html; charset=utf-8', request)


@app.middleware('http')
async def add_no_store_headers(request: Request, call_next):
    response = await call_next(request)
    path = request.url.path
    if path.startswith('/api/') or path.startswith('/healthz'):
        for key, val in NO_STORE_HEADERS.items():
            response.headers[key] = val
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
        return _serve_spa_entry(root_dir, request)

    target_file = root_dir / clean_path

    # Защита от Path Traversal
    try:
        resolved_file = target_file.resolve()
        if not str(resolved_file).startswith(str(root_dir.resolve())):
            return _serve_spa_entry(root_dir, request)
    except Exception:
        return _serve_spa_entry(root_dir, request)

    if resolved_file.is_file():
        media_type = STATIC_MEDIA_TYPES.get(resolved_file.suffix.lower()) or 'application/octet-stream'
        return _serve_file_with_etag(resolved_file, media_type, request)

    return _serve_spa_entry(root_dir, request)
