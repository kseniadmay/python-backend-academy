from typing import Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class BugReportCreate(BaseModel):
    context: Optional[str] = Field(default='general', description='Контекст или экран возникновения замечания')
    message: Optional[str] = Field(default='', description='Текст замечания или отзыва')
    userAgent: Optional[str] = Field(default=None, description='User-Agent браузера устройства')
    timestamp: Optional[str] = Field(default=None, description='ISO 8601 временная метка')
    createdAt: Optional[str] = Field(default=None, description='Человекочитаемая дата и время создания')
    meta: Optional[dict[str, Any]] = Field(default=None, description='Дополнительные технические метаданные')


class BugReportResponse(BaseModel):
    ok: bool = True
    count: int
    id: int


class BugReportListResponse(BaseModel):
    ok: bool = True
    count: int
    reports: List[dict[str, Any]]
