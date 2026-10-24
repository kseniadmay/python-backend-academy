from fastapi import APIRouter
from backend.app.schemas.feedback import BugReportCreate, BugReportListResponse, BugReportResponse
from backend.app.services.feedback_service import feedback_service

router = APIRouter(prefix='/feedback', tags=['Feedback'])


@router.get('', response_model=BugReportListResponse)
def list_reports() -> BugReportListResponse:
    """
    Получение всех накопленных замечаний и отзывов.
    """
    reports = feedback_service.get_all_reports()
    return BugReportListResponse(ok=True, count=len(reports), reports=reports)


@router.post('', response_model=BugReportResponse)
def submit_report(report: BugReportCreate) -> BugReportResponse:
    """
    Отправка замечания или сообщения об ошибке из интерфейса.
    """
    count = feedback_service.add_report(report)
    return BugReportResponse(ok=True, count=count, id=count)
