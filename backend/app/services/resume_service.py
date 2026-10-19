import logging
import os
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from httpx import HTTPError
from sqlalchemy import select
from sqlalchemy.orm import Session
from storage3.utils import StorageException

from app.core.storage import supabase, SUPABASE_BUCKET
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeUpdate


MAX_FILE_SIZE = 5 * 1024 * 1024
SIGNED_URL_EXPIRES_IN = 300
logger = logging.getLogger(__name__)


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

    resume = Resume(
        user_id=current_user.id,
        version_name=version_name,
        file_path="pending",
        is_active=False,
    )

    storage_path = None
    uploaded_to_storage = False

    try:
        db.add(resume)
        db.flush()

        storage_path = f"{current_user.id}/{resume.id}.pdf"

        supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=storage_path,
            file=content,
            file_options={
                "content-type": "application/pdf",
                "upsert": "false",
            },
        )
        uploaded_to_storage = True

        resume.file_path = storage_path

        db.commit()
        db.refresh(resume)

        return resume

    except Exception:
        db.rollback()

        if uploaded_to_storage and storage_path is not None:
            try:
                supabase.storage.from_(SUPABASE_BUCKET).remove(
                    [storage_path]
                )
            except Exception:
                pass

        raise


def get_resumes(
    db: Session,
    current_user: User,
) -> list[Resume]:
    stmt = (
        select(Resume)
        .where(Resume.user_id == current_user.id)
        .order_by(Resume.uploaded_at.desc())
    )

    return db.scalars(stmt).all()


def get_resume_by_id(
    resume_id: UUID,
    db: Session,
    current_user: User,
) -> Resume:
    resume = db.scalar(
        select(Resume).where(Resume.id == resume_id)
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

    return resume


def get_resume_access_url(
    resume_id: UUID,
    db: Session,
    current_user: User,
    *,
    download: bool = False,
) -> dict[str, str | int]:
    resume = get_resume_by_id(resume_id, db, current_user)
    options = {"download": True} if download else None

    try:
        signed_url = supabase.storage.from_(SUPABASE_BUCKET).create_signed_url(
            resume.file_path,
            SIGNED_URL_EXPIRES_IN,
            options,
        )
    except (StorageException, HTTPError) as error:
        logger.exception("Could not create signed URL for resume %s", resume_id)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not access the stored resume. Please try again.",
        ) from error

    url = signed_url.get("signedURL") or signed_url.get("signedUrl")
    if not url:
        logger.error("Supabase returned no signed URL for resume %s", resume_id)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not access the stored resume. Please try again.",
        )

    return {"url": url, "expires_in": SIGNED_URL_EXPIRES_IN}


def delete_resume(
    resume_id: UUID,
    db: Session,
    current_user: User,
) -> None:
    resume = db.scalar(
        select(Resume).where(Resume.id == resume_id)
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
        supabase.storage.from_(SUPABASE_BUCKET).remove(
            [resume.file_path]
        )

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
        select(Resume).where(Resume.id == resume_id)
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
        select(Resume).where(Resume.id == resume_id)
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
        select(Resume).where(
            Resume.user_id == current_user.id
        )
    ).all()

    for user_resume in user_resumes:
        user_resume.is_active = False

    resume.is_active = True

    db.commit()
    db.refresh(resume)

    return resume