from datetime import date,datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.models.application import ApplicationStatus

class ApplicationBase(BaseModel):
    role:str
    application_date:date
    company_id:UUID

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationResponse(ApplicationBase):
    id:UUID
    status:ApplicationStatus
    resume_id:UUID|None
    created_at:datetime
    updated_at:datetime

    model_config=ConfigDict(from_attributes=True)

class ApplicationUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: str | None = None
    application_date: date | None = None
    company_id: UUID | None = None

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
