from uuid import UUID
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.application import Application
from app.models.company import Company
from app.models.note import Note,NoteType
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate


def create_note(note:NoteCreate,db:Session,current_user:User)->Note:
    if note.application_id is not None:
        application=db.scalar(select(Application).where(note.application_id==Application.id))
        if application is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application does not exist"
            )
        if application.user_id!=current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this application"
            )
    if note.company_id is not None:
        company=db.scalar(select(Company).where(note.company_id==Company.id))
        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company does not exist"
            )
        if company.created_by!=current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this company"
            )
    new_note=Note(**note.model_dump(),user_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def get_notes(note_type: NoteType | None,db: Session,current_user: User) -> list[Note]:
    query = select(Note).where(Note.user_id == current_user.id)

    if note_type is not None:
        query = query.where(Note.note_type == note_type)

    notes = db.scalars(query).all()

    return notes
def get_note_by_id(id:UUID,db:Session,current_user:User)->Note:
    note=db.scalar(select(Note).where(id==Note.id))
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note does not exist"
            )
    if note.user_id != current_user.id:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this note"
            )
    return note

def update_note(id: UUID,update_data: NoteUpdate,db: Session,current_user: User) -> Note:
    note = db.scalar(select(Note).where(Note.id == id))

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note does not exist",
        )

    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this note",
        )

    updated_data = update_data.model_dump(exclude_unset=True)

    if "application_id" in updated_data and updated_data["application_id"] is not None:
        application = db.scalar(select(Application).where(Application.id == updated_data["application_id"]))

        if application is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application does not exist",
            )

        if application.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this application",
            )

    if "company_id" in updated_data and updated_data["company_id"] is not None:
        company = db.scalar(select(Company).where(Company.id == updated_data["company_id"]))

        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company does not exist",
            )

        if company.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this company",
            )

    for field, value in updated_data.items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)

    return note

def delete_note(id:UUID,db:Session,current_user:User)->None:
    note = db.scalar(select(Note).where(Note.id == id))

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note does not exist",
        )

    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this note",
        )
    db.delete(note)
    db.commit()

def get_notes_by_application(application_id: UUID,db: Session,current_user: User) -> list[Note]:
    application = db.scalar(select(Application).where(Application.id == application_id))

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application does not exist",
        )

    if application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this application",
        )

    notes = db.scalars(select(Note).where(Note.application_id == application_id,Note.user_id == current_user.id)).all()

    return notes