from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, Response

from backend.app.api.legacy_compat import legacy_router
from backend.app.api.v1.router import api_v1_router
from backend.app.core.config import settings
from backend.app.core.network import get_local_ip
from backend.app.core.security import get_authenticated_admin


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

# Настройка CORS для доступа PWA и мобильного клиента (без credentials при wildcard origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
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

ALLOWED_STATIC_FILES = frozenset({
    'manifest.json',
    'sw.js',
    'icon.svg',
    'favicon.ico',
})
ALLOWED_STATIC_DIRS = frozenset({'frontend'})
BLOCKED_INTERNAL_DIRS = frozenset({
    'backend',
    'data',
    'scripts',
    'docs',
    'deploy',
    'tests',
    'knowledge_base',
    'standards',
    'exports',
    'output',
    'screenshots_output',
})


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
            }
        )
    except Exception:
        return FileResponse(file_path, media_type=media_type)

def _serve_spa_entry(root_dir: Path, request: Request) -> Response:
    return _serve_file_with_etag(root_dir / 'academy.html', 'text/html; charset=utf-8', request)


SITE_LOCK_ALLOWLIST = frozenset({
    '/login',
    '/api/v1/auth/login',
    '/api/v1/auth/me',
    '/api/v1/health',
    '/robots.txt',
    '/favicon.ico',
    '/manifest.json',
})

LOGIN_PAGE_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>Вход — Python Backend Academy</title>
  <style>
    :root { color-scheme: dark; }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100dvh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: radial-gradient(circle at 20% 20%, rgba(16, 185, 129, 0.14), transparent 45%), #07090e;
      color: #f8fafc;
    }
    .card {
      width: 100%;
      max-width: 390px;
      padding: 28px 24px;
      border-radius: 20px;
      background: rgba(15, 23, 42, 0.72);
      border: 1px solid rgba(255, 255, 255, 0.12);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15), 0 20px 44px rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(18px);
    }
    h1 {
      margin: 0 0 8px;
      font-size: 1.35rem;
      font-weight: 800;
    }
    p {
      margin: 0 0 22px;
      color: #94a3b8;
      font-size: 0.92rem;
      line-height: 1.45;
    }
    label {
      display: block;
      margin-bottom: 6px;
      font-size: 0.85rem;
      color: #cbd5e1;
      font-weight: 600;
    }
    input {
      width: 100%;
      min-height: 48px;
      padding: 12px 14px;
      margin-bottom: 16px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.16);
      background: rgba(7, 9, 14, 0.75);
      color: #f8fafc;
      font-size: 16px;
      outline: none;
    }
    input:focus {
      border-color: #10b981;
      box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
    }
    button {
      width: 100%;
      min-height: 50px;
      border: 0;
      border-radius: 14px;
      background: linear-gradient(135deg, #10b981, #059669);
      color: #03150e;
      font-size: 1rem;
      font-weight: 800;
      cursor: pointer;
    }
    button:disabled { opacity: 0.65; cursor: wait; }
    .err {
      min-height: 20px;
      margin-top: 12px;
      color: #fb7185;
      font-size: 0.88rem;
      text-align: center;
    }
  </style>
</head>
<body>
  <main class="card">
    <h1>Python Backend Academy</h1>
    <p>Введите логин и пароль для доступа к персональному тренажёру.</p>
    <form id="login-form" method="post" action="/api/v1/auth/login">
      <label for="username">Логин</label>
      <input id="username" name="username" type="text" autocomplete="username" autocapitalize="none" required>
      <label for="password">Пароль</label>
      <input id="password" name="password" type="password" autocomplete="current-password" required>
      <button id="submit-btn" type="submit">Войти</button>
      <div id="err-msg" class="err" role="alert"></div>
    </form>
  </main>
  <script>
    const form = document.getElementById('login-form');
    const btn = document.getElementById('submit-btn');
    const err = document.getElementById('err-msg');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      err.textContent = '';
      btn.disabled = true;
      try {
        const res = await fetch('/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'same-origin',
          body: JSON.stringify({
            username: form.username.value.trim(),
            password: form.password.value
          })
        });
        if (res.ok) {
          window.location.replace('/');
          return;
        }
        err.textContent = 'Неверный логин или пароль';
      } catch (_) {
        err.textContent = 'Ошибка соединения с сервером';
      } finally {
        btn.disabled = false;
      }
    });
  </script>
</body>
</html>
"""


def _apply_security_headers(response: Response, path: str) -> Response:
    if path.startswith('/api/') or path.startswith('/healthz') or path == '/login':
        for key, val in NO_STORE_HEADERS.items():
            response.headers[key] = val
    if settings.SITE_LOCK_ENABLED:
        response.headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
    return response


@app.middleware('http')
async def site_lock_and_headers_middleware(request: Request, call_next):
    path = request.url.path
    if settings.SITE_LOCK_ENABLED and path not in SITE_LOCK_ALLOWLIST:
        if not get_authenticated_admin(request):
            if path.startswith('/api/'):
                resp = JSONResponse({'detail': 'Unauthorized'}, status_code=401)
            else:
                resp = RedirectResponse(url='/login', status_code=302)
            for key, val in NO_STORE_HEADERS.items():
                resp.headers[key] = val
            resp.headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
            return resp

    response = await call_next(request)
    return _apply_security_headers(response, path)


@app.get('/robots.txt', include_in_schema=False)
def robots_txt() -> PlainTextResponse:
    if settings.SITE_LOCK_ENABLED:
        body = 'User-agent: *\nDisallow: /\n'
    else:
        body = 'User-agent: *\nAllow: /\n'
    return PlainTextResponse(body, media_type='text/plain; charset=utf-8')


@app.get('/login', include_in_schema=False)
def login_page() -> HTMLResponse:
    return HTMLResponse(LOGIN_PAGE_HTML, headers=dict(NO_STORE_HEADERS))


# Подключение API роутеров
app.include_router(legacy_router)
app.include_router(api_v1_router)


# Раздача статики строго по allowlist и SPA fallback
@app.get('/{full_path:path}')
async def serve_spa_or_static(full_path: str, request: Request) -> Response:
    root_dir = settings.ROOT_DIR
    clean_path = full_path.strip().lstrip('/')

    if not clean_path or clean_path in ('index.html', 'academy.html'):
        return _serve_spa_entry(root_dir, request)

    rel_path = Path(clean_path)
    parts = rel_path.parts

    # Блокируем абсолютные пути, обход директорий (..) и любые dotfiles/dotdirs (.env, .git/...)
    if (
        not parts
        or rel_path.is_absolute()
        or any(part in ('..', '') or part.startswith('.') for part in parts)
    ):
        raise HTTPException(status_code=404, detail='Not Found')

    is_allowed_root_file = len(parts) == 1 and parts[0] in ALLOWED_STATIC_FILES
    is_allowed_dir_file = len(parts) >= 2 and parts[0] in ALLOWED_STATIC_DIRS

    if is_allowed_root_file or is_allowed_dir_file:
        try:
            resolved_root = root_dir.resolve()
            resolved_file = (root_dir / rel_path).resolve()
            if not resolved_file.is_relative_to(resolved_root):
                raise HTTPException(status_code=404, detail='Not Found')
            if is_allowed_dir_file:
                allowed_dir_root = (root_dir / parts[0]).resolve()
                if not resolved_file.is_relative_to(allowed_dir_root):
                    raise HTTPException(status_code=404, detail='Not Found')
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=404, detail='Not Found')

        if resolved_file.is_file():
            media_type = STATIC_MEDIA_TYPES.get(resolved_file.suffix.lower()) or 'application/octet-stream'
            return _serve_file_with_etag(resolved_file, media_type, request)
        raise HTTPException(status_code=404, detail='Not Found')

    # Любые запросы к внутренним каталогам или файлам с расширением вне allowlist запрещены
    if parts[0] in BLOCKED_INTERNAL_DIRS or rel_path.suffix != '':
        raise HTTPException(status_code=404, detail='Not Found')

    return _serve_spa_entry(root_dir, request)
