from datetime import date,datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.models.application import ApplicationStatus
from app.schemas.company import  CompanySummary

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
    company:CompanySummary

    model_config=ConfigDict(from_attributes=True)

class ApplicationUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: str | None = None
    application_date: date | None = None
    company_id: UUID | None = None

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus

class ApplicationFilter(BaseModel):
    status: ApplicationStatus | None = None
    company_name: str | None = None
    role: str | None = None
    from_date: date | None = None
    to_date: date | None = None
    page: int = 1
    limit: int = 10

class PaginatedApplicationResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[ApplicationResponse]