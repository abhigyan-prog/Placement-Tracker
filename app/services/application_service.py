from uuid import UUID

from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from app.models.application import Application
from app.models.company import Company
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationFilter, ApplicationStatusUpdate, ApplicationUpdate, PaginatedApplicationResponse


def create_application(application: ApplicationCreate,db: Session,current_user: User) -> Application:

    company = db.scalar(select(Company).where(Company.id == application.company_id))

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

    new_application = Application(**application.model_dump(),user_id=current_user.id,)

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application

def get_applications(db:Session,current_user:User,filters:ApplicationFilter)->PaginatedApplicationResponse:
    stmt=select(Application).where(Application.user_id==current_user.id)
    if filters.status:
        stmt=stmt.where(Application.status==filters.status)
    if filters.company_name:
        stmt = (
            stmt.join(Company)
            .where(Company.name.ilike(f"%{filters.company_name}%"))
        )
    if filters.role:
        stmt=stmt.where(Application.role.ilike(f"%{filters.role}%"))
    if filters.from_date:
        stmt=stmt.where(Application.application_date>=filters.from_date)
    if filters.to_date:
        stmt=stmt.where(
            Application.application_date<=filters.to_date
        )
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.scalar(count_stmt)
    offset = (filters.page - 1) * filters.limit
    stmt = stmt.offset(offset).limit(filters.limit)
    applications=db.scalars(stmt).all()
    return {
        "total": total,
        "page": filters.page,
        "limit": filters.limit,
        "items": applications,
    }
    

def get_application_by_id(application_id:UUID,db:Session,current_user:User)->Application:
    application=db.scalar(select(Application).where(Application.id==application_id))
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    if application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this application"
        )
    return application

def update_application(application_id: UUID,update_data: ApplicationUpdate,db: Session,current_user: User) -> Application:

    application = db.scalar(select(Application).where(Application.id == application_id))

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    if application.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this application",
        )

    if update_data.company_id is not None:
        company = db.scalar(select(Company).where(Company.id == update_data.company_id))

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

    updated_data = update_data.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application

def update_application_status(application_id: UUID, updated_status:ApplicationStatusUpdate,db:Session,current_user:User) ->Application:
    application=db.scalar(select(Application).where(Application.id == application_id))
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    if application.user_id!=current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this application",
        )
    application.status=updated_status.status
    db.commit()
    db.refresh(application)
    return application

def delete_application(application_id : UUID, db : Session, current_user : User) -> None:
    application=db.scalar(select(Application).where(Application.id == application_id))
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    if application.user_id!=current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this application",
        )
    db.delete(application)
    db.commit()

