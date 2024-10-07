# FILE: tests/test_uploads.py

import io
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app  # Ensure this import is correct
from app.crud import time_report
from app.schemas.time_report import TimeReportCreate
from app.utils.cache import redis_client

client = TestClient(app)

@pytest.fixture
def db_session():
    # Mock the database session
    session = Session()
    yield session
    session.close()

@pytest.fixture
def mock_time_report(monkeypatch):
    # Mock the time_report CRUD functions
    def mock_get_by_report_id(db, report_id):
        return None

    def mock_create(db, report):
        pass

    monkeypatch.setattr(time_report, "get_by_report_id", mock_get_by_report_id)
    monkeypatch.setattr(time_report, "create", mock_create)

@pytest.fixture
def mock_redis_client(monkeypatch):
    # Mock the redis_client delete function
    def mock_delete(key):
        pass

    monkeypatch.setattr(redis_client, "delete", mock_delete)

def test_upload_file_success(db_session, mock_time_report, mock_redis_client):
    file_content = """date,hours worked,employee id,job group
01/01/2023,8,1,A
02/01/2023,7,1,A
"""
    file = io.BytesIO(file_content.encode('utf-8'))
    file.name = "time-report-2023-1.csv"

    response = client.post("/upload/", files={"file": (file.name, file, "text/csv")})
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully"}

def test_upload_file_invalid_filename(db_session, mock_time_report, mock_redis_client):
    file_content = """date,hours worked,employee id,job group
01/01/2023,8,1,A
02/01/2023,7,1,A
"""
    file = io.BytesIO(file_content.encode('utf-8'))
    file.name = "invalid-filename.csv"

    response = client.post("/upload/", files={"file": (file.name, file, "text/csv")})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file name format"}

def test_upload_file_existing_report(db_session, mock_time_report, mock_redis_client, monkeypatch):
    file_content = """date,hours worked,employee id,job group
01/01/2023,8,1,A
02/01/2023,7,1,A
"""
    file = io.BytesIO(file_content.encode('utf-8'))
    file.name = "time-report-2023-1.csv"

    def mock_get_by_report_id(db, report_id):
        return TimeReportCreate(
            report_id=report_id,
            date=datetime.strptime("01/01/2023", '%d/%m/%Y').date(),
            hours_worked=8,
            employee_id="1",
            job_group="A"
        )

    monkeypatch.setattr(time_report, "get_by_report_id", mock_get_by_report_id)

    response = client.post("/upload/", files={"file": (file.name, file, "text/csv")})
    assert response.status_code == 400
    assert response.json() == {"detail": "Report with this ID already exists"}