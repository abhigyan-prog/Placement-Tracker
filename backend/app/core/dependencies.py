from app.database import SessionLocal

from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import decode_access_token
from app.models.user import User

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = UUID(payload["sub"])

    except (InvalidTokenError, ValueError):
        raise credentials_exception

    stmt = select(User).where(User.id == user_id)
    user = db.scalar(stmt)

    if user is None:
        raise credentials_exception

    return user




