import os
from pathlib import Path
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

    # Paths
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    DATA_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent / 'data'
    CLOUDFLARED_PATH: Path = Path(__file__).resolve().parent.parent.parent.parent / 'scripts' / 'cloudflared.exe'

    @property
    def progress_sync_file(self) -> Path:
        return self.DATA_DIR / 'progress_sync.json'

    @property
    def feedback_queue_file(self) -> Path:
        return self.DATA_DIR / 'user_feedback_queue.json'


settings = Settings()
