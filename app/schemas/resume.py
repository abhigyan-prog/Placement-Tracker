from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class ResumeResponse(BaseModel):
    id : UUID
    version_name : str
    file_path : str
    is_active : bool
    uploaded_at : datetime

    model_config = ConfigDict(from_attributes=True)

class ResumeUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    version_name: str | None = None