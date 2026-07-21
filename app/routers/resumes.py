from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session


from app.core.dependencies import get_current_user, get_db
from app.schemas.resume import ResumeResponse, ResumeUpdate
from app.services.resume_service import activate_resume, delete_resume, get_resume_by_id, get_resumes, resume_upload, update_resume

router = APIRouter(
    prefix= "/resumes",
    tags= ['Resume']
)

@router.post("/", response_model=ResumeResponse , status_code=status.HTTP_201_CREATED)
async def upload(
    version_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return await resume_upload(file,version_name,db,current_user)

@router.get("/",response_model=list[ResumeResponse])
def get(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_resumes(db,current_user)

@router.get("/{id}",response_model=ResumeResponse)
def get_by_id(
    id : UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_resume_by_id(id,db,current_user)

@router.patch("/{id}",response_model=ResumeResponse)
def update_name(
    id : UUID,
    resume_update:ResumeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return update_resume(id,resume_update,db,current_user)

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id : UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return delete_resume(id,db,current_user)

@router.patch("/{id}/activate",response_model=ResumeResponse)
def update_activestatus(
    id : UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return activate_resume(id,db,current_user)