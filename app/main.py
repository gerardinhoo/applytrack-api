from fastapi import Depends, FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers import applications

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
    """Lightweight liveness check. Does not verify database connectivity."""
    return {"status": "healthy"}


@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    """Readiness check. Verifies the database is reachable."""
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")

    return {"status": "ready"}
