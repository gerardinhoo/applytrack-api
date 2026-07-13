from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.config import ENABLE_TEST_ENDPOINTS

from app.database import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreate

router = APIRouter()

applications = []



@router.get("/applications")
def get_applications(db: Session = Depends(get_db)):
    return db.query(Application).all()

# Create application
@router.post("/applications", status_code=201)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
):
    db_application = Application(
        company=application.company,
        position=application.position,
        status=application.status,
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application 

    
@router.get("/applications/{application_id}")
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application


@router.put("/applications/{application_id}")
def update_application(
    application_id: int,
    updated_application: ApplicationCreate,
    db: Session = Depends(get_db),
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    application.company = updated_application.company
    application.position = updated_application.position
    application.status = updated_application.status

    db.commit()
    db.refresh(application)

    return application


@router.delete("/applications/{application_id}", status_code=204)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    db.delete(application)
    db.commit()

    return None


@router.get("/test-error", tags=["Testing"])
def test_error():
    """
    Intentionally returns HTTP 500 to validate monitoring dashboards.
    Disabled by default.
    """

    if not ENABLE_TEST_ENDPOINTS:
        raise HTTPException(status_code=404, detail="Endpoint not available.")

    raise HTTPException(
        status_code=500,
        detail="Intentional test error for monitoring."
    )
    