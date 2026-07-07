from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.note import NoteType
from app.schemas.note import (
    NoteCreate,
    NoteResponse,
    NoteUpdate,
)
from app.services import note_service

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return note_service.create_note(note, db, current_user)


@router.get("/", response_model=list[NoteResponse])
def get_all(
    note_type: NoteType | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return note_service.get_notes(note_type, db, current_user)


@router.get("/{note_id}", response_model=NoteResponse)
def get(
    note_id:UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return note_service.get_note_by_id(note_id, db, current_user)


@router.patch("/{note_id}", response_model=NoteResponse)
def update(
    note_id:UUID,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return note_service.update_note(note_id, note_data, db, current_user)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    note_id:UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return note_service.delete_note(note_id, db, current_user)