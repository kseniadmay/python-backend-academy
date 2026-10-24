import time
from typing import Any, Dict, Optional
from fastapi import APIRouter, Header, HTTPException, Response, status
from backend.app.core.security import verify_sync_token
from backend.app.schemas.feedback import BugReportCreate
from backend.app.schemas.progress import SyncPushRequest
from backend.app.services.feedback_service import feedback_service
from backend.app.services.sync_service import sync_service

legacy_router = APIRouter(tags=['Legacy Compatibility'])


@legacy_router.get('/healthz')
def legacy_healthz() -> Dict[str, Any]:
    return {'ok': True}


@legacy_router.get('/api/ping')
def legacy_ping() -> Dict[str, Any]:
    return {'status': 'ok', 'time': int(time.time() * 1000)}


@legacy_router.get('/api/bug-report')
def legacy_get_bug_reports() -> Dict[str, Any]:
    reports = feedback_service.get_all_reports()
    return {'ok': True, 'count': len(reports), 'reports': reports}


@legacy_router.post('/api/bug-report')
def legacy_post_bug_report(report: BugReportCreate) -> Dict[str, Any]:
    count = feedback_service.add_report(report)
    return {'ok': True, 'count': count, 'id': count}


@legacy_router.get('/api/sync')
def legacy_get_sync(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    if not verify_sync_token(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

    record = sync_service.read_sync_record()
    if not record:
        return {'ok': True, 'updatedAt': 0, 'device': None, 'bundle': None}

    return {
        'ok': True,
        'updatedAt': record.get('updatedAt', 0),
        'device': record.get('device'),
        'bundle': record.get('bundle')
    }


@legacy_router.post('/api/sync')
def legacy_post_sync(
    payload: SyncPushRequest,
    response: Response,
    authorization: Optional[str] = Header(None)
) -> Dict[str, Any]:
    if not verify_sync_token(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

    success, result_data, http_status = sync_service.process_push(payload)
    response.status_code = http_status

    if not success and http_status == 409:
        return {
            'ok': False,
            'conflict': True,
            'updatedAt': result_data['updatedAt'],
            'device': result_data['device'],
            'bundle': result_data['bundle']
        }

    return {
        'ok': True,
        'updatedAt': result_data['updatedAt'],
        'bundle': result_data['bundle']
    }
