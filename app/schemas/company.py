from datetime import datetime
from uuid import UUID

from pydantic import BaseModel,ConfigDict

class CompanyBase(BaseModel):
    name:str
    website:str|None=None
    industry:str|None=None

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id:UUID
    created_at:datetime
    created_by:UUID

    model_config = ConfigDict(from_attributes=True)

class CompanyUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name:str|None=None
    website:str|None=None
    industry:str|None=None

class CompanySummary(BaseModel):
    id:UUID
    name:str

    model_config = ConfigDict(from_attributes=True)