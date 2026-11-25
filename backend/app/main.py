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
<html lang="ru" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="color-scheme" content="dark">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <title>Вход — Python Backend Academy</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&display=optional">
  <style>
    :root {
      color-scheme: dark;
      --paper: #0d1016;
      --surface: rgba(22, 27, 36, 0.76);
      --ink: #f8fafc;
      --ink-soft: #cbd5e1;
      --ink-muted: #94a3b8;
      --emerald: #10b981;
      --font-d: 'Onest', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    * { box-sizing: border-box; }
    html { -webkit-text-size-adjust: 100%; }
    body {
      margin: 0;
      min-height: 100dvh;
      position: relative;
      overflow-x: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      font-family: var(--font-d);
      background-color: var(--paper);
      background-image: radial-gradient(rgba(255, 255, 255, 0.055) 1.2px, transparent 1.2px);
      background-size: 24px 24px;
      background-attachment: fixed;
      color: var(--ink);
      -webkit-font-smoothing: antialiased;
    }
    .ambient-orb {
      position: fixed;
      border-radius: 50%;
      pointer-events: none;
      z-index: 0;
      transform: translate3d(0, 0, 0);
      will-change: transform, opacity;
    }
    .ambient-orb--burgundy {
      width: 440px;
      height: 440px;
      top: -70px;
      left: -70px;
      background: radial-gradient(circle, rgba(190, 18, 60, 0.32) 0%, rgba(136, 19, 55, 0.16) 60%, transparent 80%);
      filter: blur(75px);
      animation: celestialDriftBurgundy 16s ease-in-out infinite alternate;
    }
    .ambient-orb--emerald {
      width: 460px;
      height: 460px;
      bottom: -70px;
      right: -60px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.28) 0%, rgba(6, 78, 59, 0.14) 60%, transparent 80%);
      filter: blur(80px);
      animation: celestialDriftEmerald 18s ease-in-out infinite alternate;
    }
    @keyframes celestialDriftBurgundy {
      0% { transform: translate3d(0, 0, 0) scale(1); opacity: 0.75; }
      50% { transform: translate3d(48px, 58px, 0) scale(1.18); opacity: 1.0; }
      100% { transform: translate3d(22px, 95px, 0) scale(0.96); opacity: 0.75; }
    }
    @keyframes celestialDriftEmerald {
      0% { transform: translate3d(0, 0, 0) scale(1); opacity: 0.75; }
      50% { transform: translate3d(-52px, -48px, 0) scale(1.22); opacity: 1.0; }
      100% { transform: translate3d(-26px, -85px, 0) scale(0.92); opacity: 0.75; }
    }
    @media (max-width: 768px) {
      .ambient-orb--burgundy {
        width: 270px;
        height: 270px;
        top: -50px;
        left: -50px;
        filter: blur(58px);
      }
      .ambient-orb--emerald {
        width: 280px;
        height: 280px;
        bottom: -50px;
        right: -50px;
        filter: blur(62px);
      }
    }
    @media (prefers-reduced-motion: reduce) {
      .ambient-orb--burgundy,
      .ambient-orb--emerald {
        animation: none !important;
      }
    }
    .card {
      position: relative;
      z-index: 1;
      width: 100%;
      max-width: 372px;
      padding: 26px 26px 26px 30px;
      border-radius: 22px;
      background: var(--surface);
      border: 1px solid rgba(255, 255, 255, 0.11);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.16), 0 16px 40px -12px rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
    }
    .brand-head {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 22px;
    }
    .brand-icon {
      width: 40px;
      height: 40px;
      flex-shrink: 0;
      display: block;
      filter: drop-shadow(0 4px 12px rgba(16, 185, 129, 0.22));
    }
    .brand-title {
      margin: 0;
      font-size: 1.04rem;
      font-weight: 800;
      letter-spacing: -0.015em;
      line-height: 1.18;
      color: var(--ink);
    }
    .brand-sub {
      margin: 3px 0 0;
      font-size: 0.80rem;
      color: var(--ink-muted);
      line-height: 1.25;
    }
    .field-group {
      margin-bottom: 12px;
    }
    .field-group--last {
      margin-bottom: 18px;
    }
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    @keyframes beadBeacon {
      0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.50), 0 0 6px rgba(16, 185, 129, 0.75); }
      50% { box-shadow: 0 0 0 3.5px rgba(16, 185, 129, 0), 0 0 10px rgba(52, 211, 153, 0.90); }
    }
    .invite-bead {
      position: absolute;
      left: -14px;
      top: 50%;
      transform: translateY(-50%);
      width: 7px;
      height: 7px;
      border-radius: 999px;
      background: #ffffff;
      border: 1.5px solid #10b981;
      animation: beadBeacon 2.8s infinite ease-in-out;
      pointer-events: none;
      z-index: 2;
      transition: background 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .invite-bead.filled {
      background: radial-gradient(circle at 35% 35%, #a7f3d0, #10b981);
      border-color: #6ee7b7;
      animation: none;
      box-shadow: 0 0 8px rgba(16, 185, 129, 0.75);
    }
    .invite-bead.error {
      background: #fda4af;
      border-color: #f43f5e;
      animation: none;
      box-shadow: 0 0 10px rgba(244, 63, 94, 0.8);
    }
    .input-wrap {
      position: relative;
      display: flex;
      align-items: center;
    }
    input {
      width: 100%;
      min-height: 46px;
      padding: 11px 14px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.12);
      background: rgba(7, 9, 14, 0.72);
      color: var(--ink);
      font-family: inherit;
      font-size: 16px;
      outline: none;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    input::placeholder {
      color: var(--ink-muted);
      opacity: 0.85;
    }
    input.has-bead {
      padding-left: 14px;
    }
    input.has-eye {
      padding-right: 44px;
    }
    input:focus {
      border-color: rgba(16, 185, 129, 0.75);
      box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.18);
    }
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus {
      -webkit-text-fill-color: #f8fafc;
      -webkit-box-shadow: 0 0 0 1000px #090c12 inset;
      transition: background-color 5000s ease-in-out 0s;
    }
    .eye-btn {
      position: absolute;
      right: 6px;
      width: 36px;
      height: 36px;
      border: 0;
      border-radius: 10px;
      background: transparent;
      color: var(--ink-muted);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: color 0.18s ease, background 0.18s ease;
    }
    .eye-btn:hover {
      color: var(--ink);
      background: rgba(255, 255, 255, 0.06);
    }
    .dominant-btn {
      width: 100%;
      min-height: 46px;
      margin-top: 0;
      padding: 11px 16px;
      border-radius: 12px;
      background: linear-gradient(180deg, rgba(16, 185, 129, 0.26) 0%, rgba(6, 78, 59, 0.25) 100%);
      border: 1.5px solid rgba(52, 211, 153, 0.65);
      color: #ffffff;
      font-family: inherit;
      font-size: 0.96rem;
      font-weight: 700;
      letter-spacing: 0.01em;
      cursor: pointer;
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
      box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.20), 0 4px 20px -2px rgba(16, 185, 129, 0.35);
      transition: background 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1), transform 0.15s ease;
    }
    .dominant-btn:hover {
      background: linear-gradient(180deg, rgba(16, 185, 129, 0.36) 0%, rgba(6, 78, 59, 0.35) 100%);
      border-color: rgba(52, 211, 153, 0.95);
      box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.25), 0 6px 24px -2px rgba(16, 185, 129, 0.50);
    }
    .dominant-btn:active { transform: scale(0.985); }
    .dominant-btn:disabled { opacity: 0.65; cursor: wait; }
    .err {
      margin-top: 12px;
      color: #fb7185;
      font-size: 0.86rem;
      line-height: 1.35;
      text-align: center;
    }
    .err:empty {
      display: none;
    }
  </style>
</head>
<body>
  <div class="ambient-orb ambient-orb--burgundy" aria-hidden="true"></div>
  <div class="ambient-orb ambient-orb--emerald" aria-hidden="true"></div>
  <main class="card">
    <div class="brand-head">
      <svg class="brand-icon" viewBox="0 0 512 512" aria-hidden="true">
        <defs>
          <radialGradient id="bg-sq" cx="50%" cy="38%" r="68%">
            <stop offset="0%" stop-color="#171d29"/><stop offset="65%" stop-color="#0b0f17"/><stop offset="100%" stop-color="#05070b"/>
          </radialGradient>
          <linearGradient id="rim-sq" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="rgba(110,231,183,0.65)"/><stop offset="45%" stop-color="rgba(255,255,255,0.12)"/><stop offset="100%" stop-color="rgba(190,18,60,0.55)"/>
          </linearGradient>
          <linearGradient id="se" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#6ee7b7"/><stop offset="32%" stop-color="#059669"/><stop offset="72%" stop-color="#047857"/><stop offset="100%" stop-color="#022c22"/>
          </linearGradient>
          <linearGradient id="sb" x1="100%" y1="100%" x2="0%" y2="0%">
            <stop offset="0%" stop-color="#fda4af"/><stop offset="32%" stop-color="#be123c"/><stop offset="72%" stop-color="#881337"/><stop offset="100%" stop-color="#3b0714"/>
          </linearGradient>
        </defs>
        <rect width="512" height="512" rx="120" fill="url(#bg-sq)"/>
        <rect x="6" y="6" width="500" height="500" rx="114" fill="none" stroke="url(#rim-sq)" stroke-width="10"/>
        <g transform="translate(118.5,118.5) scale(2.5)">
          <path fill="url(#se)" d="M55.023-0.077c-25.971,0-26.25,10.081-26.25,12.156v12.594h26.75v3.781H18.148c-7.949,0-17.938,4.833-17.938,26.25c0,19.673,7.792,27.281,15.656,27.281h9.344V68.86c0-5.491,2.721-15.656,15.406-15.656h26.531c3.902,0,14.906-1.696,14.906-14.406V14.579C82.054,11.426,81.515-0.077,55.023-0.077z"/>
          <circle cx="40.27" cy="13.2" r="5.8" fill="#022c22"/>
          <path d="M 40.27,6 Q 40.27,13.2 47.47,13.2 Q 40.27,13.2 40.27,20.4 Q 40.27,13.2 33.07,13.2 Q 40.27,13.2 40.27,6 Z" fill="#ffffff"/>
          <path fill="url(#sb)" d="M55.397,109.923c25.959,0,26.282-10.271,26.282-12.156V85.173H54.897v-3.781h37.375c8.009,0,17.938-4.954,17.938-26.25c0-23.322-10.538-27.281-15.656-27.281h-9.344v13.125c0,5.491-2.631,15.656-15.406,15.656H43.272c-3.892,0-14.906,1.896-14.906,14.406v24.219C28.366,100.497,31.562,109.923,55.397,109.923z"/>
          <circle cx="70.15" cy="96.64" r="5.8" fill="#3b0714"/>
          <path d="M 70.15,89.44 Q 70.15,96.64 77.35,96.64 Q 70.15,96.64 70.15,103.84 Q 70.15,96.64 62.95,96.64 Q 70.15,96.64 70.15,89.44 Z" fill="#ffffff"/>
        </g>
      </svg>
      <div>
        <h1 class="brand-title">Python Backend Academy</h1>
        <p class="brand-sub">Вход в тренажёр</p>
      </div>
    </div>
    <form id="login-form" method="post" action="/api/v1/auth/login">
      <div class="field-group">
        <label for="username" class="sr-only">Логин</label>
        <div class="input-wrap">
          <span id="login-bead" class="invite-bead" aria-hidden="true"></span>
          <input id="username" name="username" type="text" class="has-bead" placeholder="Логин" autocomplete="username" autocapitalize="none" required>
        </div>
      </div>
      <div class="field-group field-group--last">
        <label for="password" class="sr-only">Пароль</label>
        <div class="input-wrap">
          <input id="password" name="password" type="password" class="has-eye" placeholder="Пароль" autocomplete="current-password" required>
          <button type="button" id="toggle-pass" class="eye-btn" aria-label="Показать пароль" title="Показать пароль">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
          </button>
        </div>
      </div>
      <button id="submit-btn" type="submit" class="dominant-btn">Войти</button>
      <div id="err-msg" class="err" role="alert"></div>
    </form>
  </main>
  <script>
    const form = document.getElementById('login-form');
    const userEl = document.getElementById('username');
    const passEl = document.getElementById('password');
    const eyeBtn = document.getElementById('toggle-pass');
    const bead = document.getElementById('login-bead');
    const btn = document.getElementById('submit-btn');
    const err = document.getElementById('err-msg');

    const syncBead = () => {
      bead.classList.remove('error');
      bead.classList.toggle('filled', userEl.value.trim().length > 0);
    };
    userEl.addEventListener('input', syncBead);
    userEl.addEventListener('change', syncBead);
    setTimeout(syncBead, 150);

    eyeBtn.addEventListener('click', () => {
      const show = passEl.type === 'password';
      passEl.type = show ? 'text' : 'password';
      eyeBtn.setAttribute('aria-label', show ? 'Скрыть пароль' : 'Показать пароль');
    });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      err.textContent = '';
      bead.classList.remove('error');
      btn.disabled = true;
      try {
        const res = await fetch('/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'same-origin',
          body: JSON.stringify({
            username: userEl.value.trim(),
            password: passEl.value
          })
        });
        if (res.ok) {
          window.location.replace('/');
          return;
        }
        bead.classList.add('error');
        err.textContent = 'Неверный логин или пароль';
      } catch (_) {
        bead.classList.add('error');
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
