
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from ..schemas.user import Token, UserRegister,UserLogin,UserResponse, UserUpdate
from fastapi import APIRouter, Depends,status
from ..services.auth_service import login_user, register_user,update_user
from ..core.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post('/register',response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user:UserRegister,db: Session = Depends(get_db)):
    return register_user(user,db)

@router.post('/login',response_model=Token,status_code=status.HTTP_200_OK)
def login(user:UserLogin,db: Session = Depends(get_db)):
    return login_user(user,db)

@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user

@router.patch('/me' , response_model= UserResponse)
def update(update_data:UserUpdate,current_user=Depends(get_current_user),db: Session=Depends(get_db)):
    return update_user(update_data,current_user,db)