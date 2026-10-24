from typing import Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    ok: bool = Field(default=True, description='Статус здоровья сервиса')


class ErrorResponse(BaseModel):
    ok: bool = Field(default=False, description='Флаг ошибки')
    error: str = Field(..., description='Сообщение об ошибке')
    detail: Optional[str] = Field(default=None, description='Подробная отладочная информация')
