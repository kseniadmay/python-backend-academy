from typing import Any, Dict, List, Optional
from pydantic import Field
from backend.app.schemas.common import CompatBaseModel


class BugReportCreate(CompatBaseModel):
    context: Optional[str] = Field(default='general', description='Контекст или экран возникновения замечания')
    message: Optional[str] = Field(default='', description='Текст замечания или отзыва')
    userAgent: Optional[str] = Field(default=None, description='User-Agent браузера устройства')
    timestamp: Optional[str] = Field(default=None, description='ISO 8601 временная метка')
    createdAt: Optional[str] = Field(default=None, description='Человекочитаемая дата и время создания')
    meta: Optional[Dict[str, Any]] = Field(default=None, description='Дополнительные технические метаданные')


class BugReportResponse(CompatBaseModel):
    ok: bool = True
    count: int
    id: int


class BugReportListResponse(CompatBaseModel):
    ok: bool = True
    count: int
    reports: List[Dict[str, Any]]
