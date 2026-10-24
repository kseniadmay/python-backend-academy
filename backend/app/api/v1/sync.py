from typing import Optional
from fastapi import APIRouter, Header, HTTPException, Response, status
from backend.app.core.security import verify_sync_token
from backend.app.schemas.progress import SyncPullResponse, SyncPushRequest, SyncPushResponse
from backend.app.services.sync_service import sync_service

router = APIRouter(prefix='/sync', tags=['Sync'])


@router.get('', response_model=SyncPullResponse)
def pull_progress(
    authorization: Optional[str] = Header(None)
) -> SyncPullResponse:
    """
    Получение актуального прогресса пользователя из хранилища.
    """
    if not verify_sync_token(authorization):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized: invalid sync token'
        )

    record = sync_service.read_sync_record()
    if not record:
        return SyncPullResponse(ok=True, updatedAt=0, device=None, bundle=None)

    return SyncPullResponse(
        ok=True,
        updatedAt=record.get('updatedAt', 0),
        device=record.get('device'),
        bundle=record.get('bundle')
    )


@router.post('', response_model=SyncPushResponse)
def push_progress(
    payload: SyncPushRequest,
    response: Response,
    authorization: Optional[str] = Header(None)
) -> SyncPushResponse:
    """
    Сохранение прогресса с устройства с защитой от потерянных обновлений.
    """
    if not verify_sync_token(authorization):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized: invalid sync token'
        )

    success, result_data, http_status = sync_service.process_push(payload)
    response.status_code = http_status

    if not success and http_status == 409:
        return SyncPushResponse(
            ok=False,
            conflict=True,
            updatedAt=result_data['updatedAt'],
            device=result_data['device'],
            bundle=result_data['bundle']
        )

    return SyncPushResponse(
        ok=True,
        updatedAt=result_data['updatedAt'],
        bundle=result_data['bundle']
    )
