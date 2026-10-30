from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class CompatBaseModel(BaseModel):
    """
    Единая базовая модель Pydantic с прозрачной совместимостью API v1 и v2
    (предоставляет model_dump и model_validate в обоих окружениях).
    """

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        if hasattr(super(), 'model_dump'):
            return super().model_dump(*args, **kwargs)  # type: ignore[misc]
        return self.dict(*args, **kwargs)

    @classmethod
    def model_validate(cls, obj: Any, *args: Any, **kwargs: Any) -> Any:
        if hasattr(super(), 'model_validate'):
            return super().model_validate(obj, *args, **kwargs)  # type: ignore[misc]
        return cls.parse_obj(obj)


class HealthResponse(CompatBaseModel):
    ok: bool = Field(default=True, description='Статус здоровья сервиса')


class ErrorResponse(CompatBaseModel):
    ok: bool = Field(default=False, description='Флаг ошибки')
    error: str = Field(..., description='Сообщение об ошибке')
    detail: Optional[str] = Field(default=None, description='Подробная отладочная информация')
