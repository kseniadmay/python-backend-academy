from fastapi import APIRouter
from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.sync import router as sync_router
from backend.app.api.v1.feedback import router as feedback_router
from backend.app.api.v1.content import router as content_router

api_v1_router = APIRouter(prefix='/api/v1')

api_v1_router.include_router(health_router)
api_v1_router.include_router(sync_router)
api_v1_router.include_router(feedback_router)
api_v1_router.include_router(content_router)
