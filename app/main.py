from fastapi import FastAPI, HTTPException
from app.schemas.application import ApplicationCreate

app = FastAPI(
  title="ApplyTrack API",
  description="A FastAPI project for tracking job applications.",
  version="1.0.0"
)

applications = []

@app.get("/")
def root():
    return {"message": "ApplyTrack API is running"}

@app.get("/health")
def healthcheck():
    return {"status": "healthy"}

@app.get("/applications")
def get_applications():
    return applications

@app.post("/applications", status_code=201)
def create_application(application: ApplicationCreate):
    new_application = application.model_dump()
    new_application["id"] = len(applications)

    applications.append(application)
    return new_application 

@app.get("/applications/count")
def get_application_count():
    return {
        "count": len(applications)
    }
    
@app.get("/applications/{application_id}")
def get_application(application_id: int):
    
    if application_id >= len(applications):
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )
    return applications[application_id]


@app.put("/applications/{application_id}")
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


@app.delete("/applications/{application_id}", status_code=204)
def delete_application(application_id: int):
    if application_id >= len(applications):
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    applications.pop(application_id)

    return None