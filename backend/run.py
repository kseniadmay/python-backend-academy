import uvicorn
from backend.app.core.config import settings


def main() -> None:
    uvicorn.run(
        'backend.app.main:app',
        host=settings.HOST,
        port=settings.PORT,
        reload=False
    )


if __name__ == '__main__':
    main()
