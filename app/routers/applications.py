
from uuid import UUID
from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationStatusUpdate, ApplicationUpdate
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

@router.get("/{id}",response_model=ApplicationResponse)
def get(id:UUID,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return get_application_by_id(id,db,current_user)

@router.patch("/{id}",response_model=ApplicationResponse)
def update(id:UUID,application_data:ApplicationUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return update_application(id,application_data,db,current_user)

@router.patch("/{id}/status",response_model=ApplicationResponse)
def update_status(id:UUID,updated_status:ApplicationStatusUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return update_application_status(id,updated_status,db,current_user)

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id:UUID,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return delete_application(id,db,current_user)
