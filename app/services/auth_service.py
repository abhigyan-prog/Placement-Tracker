from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import  create_access_token,hash_password, verify_password
from app.models.user import User
from app.schemas.user import Token, UserLogin, UserRegister, UserUpdate


def register_user(new_user: UserRegister, db: Session) -> User:
    existing_email = db.scalar(
        select(User).where(User.email == new_user.email)
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    existing_username = db.scalar(
        select(User).where(User.username == new_user.username)
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken.",
        )

    user_data = new_user.model_dump()

    user_data["hashed_password"] = hash_password(
        user_data.pop("password")
    )

    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(login_data: UserLogin, db: Session) -> Token:
    user = db.scalar(
        select(User).where(User.email == login_data.email)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not verify_password(
        login_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )
def update_user(update_data: UserUpdate,current_user:User,db:Session) -> User:
    existing_username=db.scalar(select(User).where(User.username==update_data.username))
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken.",
        )
    updated_data = update_data.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user
    