from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        payload=to_encode,
        key=settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    payload = jwt.decode(
        jwt=token,
        key=settings.secret_key,
        algorithms=[settings.algorithm],
    )

    if "sub" not in payload:
        raise InvalidTokenError("Token payload missing subject")

    return payload