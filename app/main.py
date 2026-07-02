from fastapi import FastAPI, HTTPException

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
def create_application(application: dict):
    applications.append(application)
    return application 

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
