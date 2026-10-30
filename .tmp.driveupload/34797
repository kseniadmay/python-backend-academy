import time
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Response
from backend.app.api.v1.feedback import list_reports, submit_report
from backend.app.api.v1.health import get_health
from backend.app.api.v1.sync import pull_progress, push_progress
from backend.app.core.security import require_sync_auth
from backend.app.schemas.common import HealthResponse
from backend.app.schemas.feedback import BugReportCreate, BugReportListResponse, BugReportResponse
from backend.app.schemas.progress import SyncPullResponse, SyncPushRequest, SyncPushResponse

legacy_router = APIRouter(tags=['Legacy Compatibility'])


@legacy_router.get('/healthz', response_model=HealthResponse)
def legacy_healthz() -> HealthResponse:
    return get_health()


@legacy_router.get('/api/ping')
def legacy_ping() -> Dict[str, Any]:
    return {'status': 'ok', 'time': int(time.time() * 1000)}


@legacy_router.get('/api/bug-report', response_model=BugReportListResponse)
def legacy_get_bug_reports() -> BugReportListResponse:
    return list_reports()


@legacy_router.post('/api/bug-report', response_model=BugReportResponse)
def legacy_post_bug_report(report: BugReportCreate) -> BugReportResponse:
    return submit_report(report)


@legacy_router.get('/api/sync', response_model=SyncPullResponse)
def legacy_get_sync(
    _auth: Optional[str] = Depends(require_sync_auth)
) -> SyncPullResponse:
    return pull_progress(_auth=_auth)


@legacy_router.post('/api/sync', response_model=SyncPushResponse)
def legacy_post_sync(
    payload: SyncPushRequest,
    response: Response,
    _auth: Optional[str] = Depends(require_sync_auth)
) -> SyncPushResponse:
    return push_progress(payload=payload, response=response, _auth=_auth)
