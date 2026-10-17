from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import get_dashboard_stats

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/",response_model=DashboardResponse)
def get(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return get_dashboard_stats(db,current_user)