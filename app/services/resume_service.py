import os
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeUpdate


MAX_FILE_SIZE = 5 * 1024 * 1024
UPLOAD_DIR = "uploads"


async def resume_upload(
    file: UploadFile,
    version_name: str,
    db: Session,
    current_user: User,
) -> Resume:

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size should not exceed 5 MB.",
        )

    upload_dir = os.path.join(
        UPLOAD_DIR,
        str(current_user.id),
    )

    os.makedirs(upload_dir, exist_ok=True)

    resume = Resume(
        user_id=current_user.id,
        version_name=version_name,
        file_path="pending",
        is_active=False,
    )

    try:
        db.add(resume)
        db.flush()

        filename = f"{resume.id}.pdf"

        file_path = os.path.join(
            upload_dir,
            filename,
        )

        with open(file_path, "wb") as f:
            f.write(content)

        resume.file_path = file_path

        db.commit()
        db.refresh(resume)

        return resume

    except Exception:
        db.rollback()

        if "file_path" in locals() and os.path.exists(file_path):
            os.remove(file_path)

        raise

def get_resumes(
     db:Session,
     current_user:User   
) -> list[Resume]:
    stmt = (
        select(Resume)
        .where(Resume.user_id==current_user.id)
        .order_by(Resume.uploaded_at.desc())
    )
    resumes=db.scalars(stmt).all()
    return resumes

def get_resume_by_id(
        resume_id:UUID,
        db:Session,
        current_user:User
) -> Resume:
    resume = db.scalar(
        select(Resume)
        .where(Resume.id==resume_id)
    )
    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorised to access this resume"
        )
    
    return resume

def delete_resume(
    resume_id: UUID,
    db: Session,
    current_user: User,
) -> None:

    resume = db.scalar(
        select(Resume)
        .where(Resume.id == resume_id)
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this resume.",
        )

    try:
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)

        db.delete(resume)
        db.commit()

    except Exception:
        db.rollback()
        raise

def update_resume(
    resume_id: UUID,
    resume_update: ResumeUpdate,
    db: Session,
    current_user: User,
) -> Resume:

    resume = db.scalar(
        select(Resume)
        .where(Resume.id == resume_id)
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this resume.",
        )

    update_data = resume_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(resume, key, value)

    db.commit()
    db.refresh(resume)

    return resume

def activate_resume(
    resume_id: UUID,
    db: Session,
    current_user: User,
) -> Resume:

    resume = db.scalar(
        select(Resume)
        .where(Resume.id == resume_id)
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resume.",
        )

    if resume.is_active:
        return resume

    user_resumes = db.scalars(
        select(Resume)
        .where(Resume.user_id == current_user.id)
    ).all()

    for user_resume in user_resumes:
        user_resume.is_active = False

    resume.is_active = True

    db.commit()
    db.refresh(resume)

    return resume