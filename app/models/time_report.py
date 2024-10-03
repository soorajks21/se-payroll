from sqlalchemy import Column, Integer, String, Float, Date
from app.db.base import Base

class TimeReport(Base):
    __tablename__ = "time_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, unique=True, index=True)
    date = Column(Date, nullable=False)
    hours_worked = Column(Float, nullable=False)
    employee_id = Column(String, index=True, nullable=False)
    job_group = Column(String, nullable=False)