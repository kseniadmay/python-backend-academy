import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from backend.app.core.config import settings
from backend.app.schemas.progress import ProgressBundle, SyncPushRequest

logger = logging.getLogger('academy.sync')


class SyncService:
    def __init__(self) -> None:
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        settings.DATA_DIR.mkdir(parents=True, exist_ok=True)

    def read_sync_record(self) -> Optional[Dict[str, Any]]:
        """
        Считывает текущее сохраненное состояние прогресса из хранилища.
        """
        sync_file = settings.progress_sync_file
        if not sync_file.exists():
            return None

        try:
            with open(sync_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'bundle' in data:
                    return data
        except Exception as e:
            logger.error('Ошибка чтения sync_file %s: %s', sync_file, e)

        return None

    def write_sync_record(self, record: Dict[str, Any]) -> None:
        """
        Атомарно записывает состояние прогресса через временный файл и rename,
        предотвращая повреждение файла при внезапном сбое процесса.
        """
        self._ensure_storage_dir()
        sync_file = settings.progress_sync_file
        temp_file = sync_file.with_suffix(f'.{os.getpid()}.{int(time.time() * 1000)}.tmp')

        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)

        temp_file.replace(sync_file)

    def process_push(self, payload: SyncPushRequest) -> Tuple[bool, Dict[str, Any], int]:
        """
        Обрабатывает пуш прогресса с устройства с защитой от потерянных обновлений
        и серверным слиянием монотонно возрастающего прогресса.
        Возвращает: (is_success, response_data, http_status_code)
        """
        bundle = payload.bundle.model_dump()
        client_id = str(payload.clientId or payload.device or 'unknown')
        base_updated_at = payload.baseUpdatedAt or 0

        stored = self.read_sync_record()
        now_ms = int(time.time() * 1000)

        if stored:
            stored_client_id = str(stored.get('clientId') or stored.get('device') or '')
            stored_updated_at = int(stored.get('updatedAt', 0))

            # Lost-update guard: если другое устройство успело запушить более свежий бандл
            is_stale = (
                stored_client_id
                and stored_client_id != client_id
                and stored_updated_at > (base_updated_at + settings.SYNC_DEVICE_TTL_MS)
            )

            if is_stale:
                logger.warning(
                    'Конфликт устройств (%s vs %s) — требуется повторное слияние',
                    payload.device,
                    stored.get('device')
                )
                return False, {
                    'ok': False,
                    'conflict': True,
                    'updatedAt': stored_updated_at,
                    'device': stored.get('device'),
                    'bundle': stored.get('bundle')
                }, 409

        # Безопасное объединение прогресса, чтобы не затереть решения с разных устройств
        next_bundle = bundle
        if stored and stored.get('bundle'):
            stored_bundle = stored['bundle']
            next_bundle = {
                'academyState': {**(stored_bundle.get('academyState') or {}), **(bundle.get('academyState') or {})},
                'ideStatus': {**(stored_bundle.get('ideStatus') or {}), **(bundle.get('ideStatus') or {})},
                'ideDrafts': {**(stored_bundle.get('ideDrafts') or {}), **(bundle.get('ideDrafts') or {})}
            }

        new_record = {
            'updatedAt': now_ms,
            'device': str(payload.device or 'unknown'),
            'clientId': client_id,
            'bundle': next_bundle
        }

        self.write_sync_record(new_record)
        logger.info('Прогресс успешно сохранен (устройство: %s, timestamp: %s)', payload.device, now_ms)

        return True, {
            'ok': True,
            'updatedAt': now_ms,
            'bundle': next_bundle
        }, 200


sync_service = SyncService()
