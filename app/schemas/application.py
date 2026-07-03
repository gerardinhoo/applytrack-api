from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    company: str
    position: str
    status: str = "Applied"