from fastapi import APIRouter, HTTPException
from app.schemas.application import ApplicationCreate

router = APIRouter()

applications = []

@router.get("/applications")
def get_applications():
    return applications

@router.post("/applications", status_code=201)
def create_application(application: ApplicationCreate):
    new_application = application.model_dump()
    new_application["id"] = len(applications)

    applications.append(new_application)
    return new_application 

@router.get("/applications/count")
def get_application_count():
    return {
        "count": len(applications)
    }
    
@router.get("/applications/{application_id}")
def get_application(application_id: int):
    
    if application_id >= len(applications):
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )
    return applications[application_id]


@router.put("/applications/{application_id}")
def update_application(application_id: int, updated_application: ApplicationCreate):
       if application_id >= len(applications):
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )
       
       application_data = updated_application.model_dump()
       application_data["id"] = application_id

       applications[application_id] = application_data

       return application_data


@router.delete("/applications/{application_id}", status_code=204)
def delete_application(application_id: int):
    if application_id >= len(applications):
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    applications.pop(application_id)

    return None
    