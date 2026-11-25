import json
import logging
import os
import secrets
import time
from pathlib import Path
from typing import Any, Optional

_DEFAULT_ROOT_DIR = Path(__file__).resolve().parents[3]
_EPHEMERAL_SESSION_SECRET = secrets.token_urlsafe(32)


def read_json_file(
    file_path: Path,
    default: Any = None,
    logger: Optional[logging.Logger] = None
) -> Any:
    """
    Безопасно читает и десериализует JSON-файл.
    При отсутствии файла или ошибке чтения возвращает default.
    """
    if not file_path.exists():
        return default
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        if logger:
            logger.error('Ошибка чтения JSON-файла %s: %s', file_path, e)
        return default


def atomic_write_json_file(file_path: Path, data: Any) -> None:
    """
    Атомарно сериализует данные в JSON-файл через временный файл и rename,
    гарантируя целостность данных при конкурентной записи или внезапном сбое.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temp_file = file_path.with_suffix(f'.{os.getpid()}.{int(time.time() * 1000)}.tmp')
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    temp_file.replace(file_path)


try:
    from pydantic import AliasChoices, Field, model_validator
    from pydantic_settings import BaseSettings, SettingsConfigDict

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(
            env_file='.env',
            env_file_encoding='utf-8',
            extra='ignore'
        )

        # Server Ports & Host
        PORT: int = Field(default=8080, validation_alias=AliasChoices('PORT', 'PBA_PORT'))
        HOST: str = '127.0.0.1'

        # Security & Storage
        SYNC_TOKEN: str = ''
        DATABASE_URL: str = ''
        SYNC_DEVICE_TTL_MS: int = 60 * 1000
        # Локальный dev-раннер кода на базе exec(); в публичном окружении рекомендуется false
        ALLOW_CODE_RUNNER: bool = True

        # Site-wide lock & personal profile
        SITE_LOCK_ENABLED: bool = False
        ADMIN_USERNAME: str = ''
        ADMIN_PASSWORD: str = ''
        SESSION_SECRET: str = ''
        SESSION_TTL_DAYS: int = 30
        PRIVATE_PROFILE_PATH: str = 'data/private/personal_profile.json'

        # Paths (derived from single _DEFAULT_ROOT_DIR)
        ROOT_DIR: Path = _DEFAULT_ROOT_DIR
        DATA_DIR: Path = _DEFAULT_ROOT_DIR / 'data'
        CLOUDFLARED_PATH: Path = _DEFAULT_ROOT_DIR / 'scripts' / 'cloudflared.exe'

        @model_validator(mode='after')
        def _ensure_session_secret(self) -> 'Settings':
            if not self.SESSION_SECRET:
                self.SESSION_SECRET = _EPHEMERAL_SESSION_SECRET
            return self

        @property
        def progress_sync_file(self) -> Path:
            return self.DATA_DIR / 'progress_sync.json'

        @property
        def feedback_queue_file(self) -> Path:
            return self.DATA_DIR / 'user_feedback_queue.json'

        @property
        def private_profile_file(self) -> Path:
            p = Path(self.PRIVATE_PROFILE_PATH)
            return p if p.is_absolute() else (self.ROOT_DIR / p)

except ImportError:
    from pydantic import BaseModel

    class Settings(BaseModel):
        PORT: int = int(os.getenv('PORT') or os.getenv('PBA_PORT') or '8080')
        HOST: str = os.getenv('HOST', '127.0.0.1')
        SYNC_TOKEN: str = os.getenv('SYNC_TOKEN', '')
        DATABASE_URL: str = os.getenv('DATABASE_URL', '')
        SYNC_DEVICE_TTL_MS: int = int(os.getenv('SYNC_DEVICE_TTL_MS', str(60 * 1000)))
        ALLOW_CODE_RUNNER: bool = os.getenv('ALLOW_CODE_RUNNER', 'true').strip().lower() in ('1', 'true', 'yes', 'on')
        SITE_LOCK_ENABLED: bool = os.getenv('SITE_LOCK_ENABLED', 'false').strip().lower() in ('1', 'true', 'yes', 'on')
        ADMIN_USERNAME: str = os.getenv('ADMIN_USERNAME', '')
        ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD', '')
        SESSION_SECRET: str = os.getenv('SESSION_SECRET') or _EPHEMERAL_SESSION_SECRET
        SESSION_TTL_DAYS: int = int(os.getenv('SESSION_TTL_DAYS', '30'))
        PRIVATE_PROFILE_PATH: str = os.getenv('PRIVATE_PROFILE_PATH', 'data/private/personal_profile.json')
        ROOT_DIR: Path = _DEFAULT_ROOT_DIR
        DATA_DIR: Path = Path(os.getenv('PBA_DATA_DIR', str(_DEFAULT_ROOT_DIR / 'data')))
        CLOUDFLARED_PATH: Path = _DEFAULT_ROOT_DIR / 'scripts' / 'cloudflared.exe'

        @property
        def progress_sync_file(self) -> Path:
            return self.DATA_DIR / 'progress_sync.json'

        @property
        def feedback_queue_file(self) -> Path:
            return self.DATA_DIR / 'user_feedback_queue.json'

        @property
        def private_profile_file(self) -> Path:
            p = Path(self.PRIVATE_PROFILE_PATH)
            return p if p.is_absolute() else (self.ROOT_DIR / p)


settings = Settings()
