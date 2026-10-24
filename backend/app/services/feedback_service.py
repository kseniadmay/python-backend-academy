import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

from backend.app.core.config import settings
from backend.app.schemas.feedback import BugReportCreate

logger = logging.getLogger('academy.feedback')


class FeedbackService:
    def __init__(self) -> None:
        settings.DATA_DIR.mkdir(parents=True, exist_ok=True)

    def get_all_reports(self) -> List[Dict[str, Any]]:
        file_path = settings.feedback_queue_file
        if not file_path.exists():
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception as e:
            logger.error('Ошибка чтения очереди отзывов %s: %s', file_path, e)
            return []

    def add_report(self, report: BugReportCreate) -> int:
        reports = self.get_all_reports()
        now_utc = datetime.now(timezone.utc)

        report_dict = report.model_dump()
        if not report_dict.get('timestamp'):
            report_dict['timestamp'] = now_utc.isoformat()
        if not report_dict.get('createdAt'):
            report_dict['createdAt'] = datetime.now().strftime('%d.%m.%Y, %H:%M:%S')

        reports.append(report_dict)

        file_path = settings.feedback_queue_file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)

        logger.info('Новое замечание добавлено (всего в очереди: %d)', len(reports))
        return len(reports)


feedback_service = FeedbackService()
