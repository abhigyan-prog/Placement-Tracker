
from uuid import UUID
from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationStatusUpdate, ApplicationUpdate
from app.schemas.note import NoteResponse
from app.services import note_service
from app.services.application_service import create_application, delete_application, get_application_by_id, get_applications, update_application, update_application_status
router=APIRouter(
    prefix="/applications",
    tags=["Applications"]
)

@router.post('/',response_model=ApplicationResponse,status_code=status.HTTP_201_CREATED)
def create(application:ApplicationCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return create_application(application,db,current_user)

@router.get("/",response_model=list[ApplicationResponse])
def get_all(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return get_applications(db,current_user)

@router.get("/{application_id}",response_model=ApplicationResponse)
def get(application_id:UUID,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return get_application_by_id(application_id,db,current_user)

@router.patch("/{application_id}",response_model=ApplicationResponse)
def update(application_id:UUID,application_data:ApplicationUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return update_application(application_id,application_data,db,current_user)

@router.patch("/{application_id}/status",response_model=ApplicationResponse)
def update_status(application_id:UUID,updated_status:ApplicationStatusUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return update_application_status(application_id,updated_status,db,current_user)

@router.delete("/{application_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(application_id:UUID,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return delete_application(application_id,db,current_user)

@router.get("/{application_id}/notes", response_model=list[NoteResponse])
def get_notes_by_application(application_id: UUID,db: Session = Depends(get_db),current_user = Depends(get_current_user),):
    return note_service.get_notes_by_application(application_id,db,current_user)
