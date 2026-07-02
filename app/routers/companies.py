from uuid import UUID

from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services.company_service import create_company, delete_company, get_companies, get_company_by_id, update_company


router= APIRouter(
    prefix="/companies",
    tags=['Companies']
)

@router.post("/",response_model=CompanyResponse,status_code=status.HTTP_201_CREATED)
def create(company_data:CompanyCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return create_company(company_data,db,current_user)

@router.get('/',response_model=list[CompanyResponse])
def get_all_companies(db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    return get_companies(db,current_user)

@router.get("/{company_id}",response_model=CompanyResponse)
def get_company(company_id:UUID,db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    return get_company_by_id(company_id,db,current_user)

@router.patch("/{company_id}",response_model=CompanyResponse)
def update(company_id:UUID,update_data:CompanyUpdate,db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    return update_company(company_id,update_data,db,current_user)

@router.delete("/{company_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(company_id:UUID,db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    return delete_company(company_id,db,current_user)