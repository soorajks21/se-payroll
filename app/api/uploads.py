import csv
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.crud import time_report
from app.schemas.time_report import TimeReportCreate
from app.db.session import get_db
from datetime import datetime
from app.utils.cache import redis_client

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        report_id = int(file.filename.split('-')[2].split('.')[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid file name format")

    if time_report.get_by_report_id(db, report_id):
        raise HTTPException(status_code=400, detail="Report with this ID already exists")

    reader = csv.DictReader(file.file)
    for row in reader:
        report = TimeReportCreate(
            report_id=report_id,
            date=datetime.strptime(row['date'], '%d/%m/%Y').date(),
            hours_worked=float(row['hours worked']),
            employee_id=row['employee id'],
            job_group=row['job group']
        )
        time_report.create(db, report)

    redis_client.delete("payroll_report")
    
    return {"message": "File uploaded successfully"}