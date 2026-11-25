from fastapi import APIRouter
from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.sync import router as sync_router
from backend.app.api.v1.feedback import router as feedback_router
from backend.app.api.v1.content import router as content_router
from backend.app.api.v1.srs import router as srs_router
from backend.app.api.v1.navigation import router as navigation_router
from backend.app.api.v1.practice import router as practice_router
from backend.app.api.v1.path import router as path_router
from backend.app.api.v1.notes import router as notes_router
from backend.app.api.v1.mock import router as mock_router

api_v1_router = APIRouter(prefix='/api/v1')

api_v1_router.include_router(health_router)
api_v1_router.include_router(sync_router)
api_v1_router.include_router(feedback_router)
api_v1_router.include_router(content_router)
api_v1_router.include_router(srs_router)
api_v1_router.include_router(navigation_router)
api_v1_router.include_router(practice_router)
api_v1_router.include_router(path_router)
api_v1_router.include_router(notes_router)
api_v1_router.include_router(mock_router)
