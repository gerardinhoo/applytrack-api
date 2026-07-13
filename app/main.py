from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.routers import applications
from app.database import engine, Base
from app.models import application


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ApplyTrack API",
    description="A FastAPI project for tracking job applications.",
    version="1.0.0",
)

app.include_router(applications.router)

Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
    include_in_schema=False,
)

@app.get("/")
def root():
    return {"message": "ApplyTrack API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}



