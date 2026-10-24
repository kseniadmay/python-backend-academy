from typing import Any, Optional, Dict
from pydantic import BaseModel, Field


class ProgressBundle(BaseModel):
    academyState: Dict[str, Any] = Field(..., description='Основное состояние профиля академии (XP, стрик, уроки, карточки)')
    ideStatus: Optional[Dict[str, Any]] = Field(default_factory=dict, description='Статусы решенных задач в IDE')
    ideDrafts: Optional[Dict[str, Any]] = Field(default_factory=dict, description='Черновики незавершенного кода в IDE')


class SyncPullResponse(BaseModel):
    ok: bool = True
    updatedAt: int = Field(default=0, description='Unix timestamp последнего обновления в миллисекундах')
    device: Optional[str] = Field(default=None, description='Имя устройства, выполнившего последнее сохранение')
    bundle: Optional[ProgressBundle] = Field(default=None, description='Пакет данных прогресса')


class SyncPushRequest(BaseModel):
    bundle: ProgressBundle = Field(..., description='Пакет синхронизации прогресса')
    baseUpdatedAt: Optional[int] = Field(default=0, description='Timestamp версии, от которой отталкивался клиент')
    device: Optional[str] = Field(default='unknown', description='Идентификатор или имя устройства клиента')
    clientId: Optional[str] = Field(default=None, description='Уникальный ID клиентской инсталляции')


class SyncPushResponse(BaseModel):
    ok: bool = True
    updatedAt: int
    bundle: ProgressBundle
    conflict: Optional[bool] = None
    device: Optional[str] = None
