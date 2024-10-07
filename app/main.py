from fastapi import FastAPI
from app.api import uploads, reports
from contextlib import asynccontextmanager
from app.db.session import engine, Base
import logging

app = FastAPI()

app.include_router(uploads.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully.")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
    yield
    # Add any shutdown tasks here if needed

app.router.lifespan_context = lifespan