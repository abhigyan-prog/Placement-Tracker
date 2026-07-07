from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.note import NoteType


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    application_id: UUID | None = None
    company_id: UUID | None = None
    note_type: NoteType = NoteType.GENERAL


class NoteUpdate(BaseModel):
    model_config=ConfigDict(extra='forbid')

    title: str | None = None
    content: str | None = None
    note_type: NoteType | None = None
    application_id: UUID | None = None
    company_id: UUID | None = None


class NoteResponse(NoteBase):
    id: UUID
    user_id: UUID
    application_id: UUID | None
    company_id: UUID | None
    note_type: NoteType
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)