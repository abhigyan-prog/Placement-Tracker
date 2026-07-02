from uuid import UUID
from fastapi import HTTPException,status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyUpdate


def create_company(company_data: CompanyCreate,db: Session, current_user: User) -> Company:
    company = Company(**company_data.model_dump(),created_by=current_user.id)

    db.add(company)
    db.commit()
    db.refresh(company)

    return company


def get_companies(db: Session, current_user: User) -> list[Company]:
    stmt = select(Company).where(Company.created_by == current_user.id)

    companies = db.scalars(stmt).all()

    return companies

def get_company_by_id(company_id: UUID,db: Session,current_user: User) -> Company:
    stmt = select(Company).where(Company.id == company_id)
    company = db.scalar(stmt)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    if company.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this company",
        )

    return company

def update_company(company_id:UUID,company_data:CompanyUpdate,db:Session,current_user:User) -> Company:
    stmt = select(Company).where(Company.id == company_id)
    company = db.scalar(stmt)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    if company.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this company",
        )
    update_data = company_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)
    return company

def delete_company(company_id:UUID,db:Session,current_user:User) -> None:
    stmt = select(Company).where(Company.id == company_id)
    company = db.scalar(stmt)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    if company.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this company",
        )
    db.delete(company)
    db.commit()

