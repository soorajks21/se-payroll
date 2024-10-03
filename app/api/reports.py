from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.report_service import ReportService
from app.schemas.report import PayrollReport
from app.utils.cache import cache_get, cache_set

router = APIRouter()

@router.get("/report/", response_model=PayrollReport)
def get_payroll_report(db: Session = Depends(get_db)):
    cache_key = "payroll_report"
    cached_report = cache_get(cache_key)
    
    if cached_report:
        return cached_report
    
    report_service = ReportService(db)
    payroll_report = report_service.generate_payroll_report()
    
    cache_set(cache_key, payroll_report.dict(), ttl=3600)
    
    return payroll_report