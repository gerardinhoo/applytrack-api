from fastapi import FastAPI
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


@app.get("/")
def root():
    return {"message": "ApplyTrack API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}