import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Optional

_DEFAULT_ROOT_DIR = Path(__file__).resolve().parents[3]


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
    from pydantic_settings import BaseSettings, SettingsConfigDict

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(
            env_file='.env',
            env_file_encoding='utf-8',
            extra='ignore'
        )

        # Server Ports & Host
        PORT: int = 8080
        HOST: str = '0.0.0.0'

        # Security & Storage
        SYNC_TOKEN: str = ''
        DATABASE_URL: str = ''
        SYNC_DEVICE_TTL_MS: int = 60 * 1000

        # Paths (derived from single _DEFAULT_ROOT_DIR)
        ROOT_DIR: Path = _DEFAULT_ROOT_DIR
        DATA_DIR: Path = _DEFAULT_ROOT_DIR / 'data'
        CLOUDFLARED_PATH: Path = _DEFAULT_ROOT_DIR / 'scripts' / 'cloudflared.exe'

        @property
        def progress_sync_file(self) -> Path:
            return self.DATA_DIR / 'progress_sync.json'

        @property
        def feedback_queue_file(self) -> Path:
            return self.DATA_DIR / 'user_feedback_queue.json'

except ImportError:
    from pydantic import BaseModel

    class Settings(BaseModel):
        PORT: int = int(os.getenv('PORT', '8080'))
        HOST: str = os.getenv('HOST', '0.0.0.0')
        SYNC_TOKEN: str = os.getenv('SYNC_TOKEN', '')
        DATABASE_URL: str = os.getenv('DATABASE_URL', '')
        SYNC_DEVICE_TTL_MS: int = int(os.getenv('SYNC_DEVICE_TTL_MS', str(60 * 1000)))
        ROOT_DIR: Path = _DEFAULT_ROOT_DIR
        DATA_DIR: Path = Path(os.getenv('PBA_DATA_DIR', str(_DEFAULT_ROOT_DIR / 'data')))
        CLOUDFLARED_PATH: Path = _DEFAULT_ROOT_DIR / 'scripts' / 'cloudflared.exe'

        @property
        def progress_sync_file(self) -> Path:
            return self.DATA_DIR / 'progress_sync.json'

        @property
        def feedback_queue_file(self) -> Path:
            return self.DATA_DIR / 'user_feedback_queue.json'


settings = Settings()
