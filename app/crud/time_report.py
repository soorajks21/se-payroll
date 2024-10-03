from sqlalchemy.orm import Session
from app.models.time_report import TimeReport
from app.schemas.time_report import TimeReportCreate
from app.crud.base import CRUDBase

class CRUDTimeReport(CRUDBase[TimeReport]):
    def get_by_report_id(self, db: Session, report_id: int):
        return db.query(TimeReport).filter(TimeReport.report_id == report_id).first()

time_report = CRUDTimeReport(TimeReport)