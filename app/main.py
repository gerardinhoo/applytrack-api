from fastapi import FastAPI


app = FastAPI(
  title="ApplyTrack API",
  description="A FastAPI project for tracking job applications.",
  version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "ApplyTrack API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}