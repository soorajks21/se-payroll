from pydantic import BaseModel
from datetime import date

class TimeReportBase(BaseModel):
    date: date
    hours_worked: float
    employee_id: str
    job_group: str

class TimeReportCreate(TimeReportBase):
    report_id: int