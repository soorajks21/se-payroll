from fastapi import FastAPI
from app.api import uploads, reports

app = FastAPI()

app.include_router(uploads.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")

@app.on_event("startup")
def startup_event():
    from app.db.session import engine, Base
    Base.metadata.create_all(bind=engine)