from datetime import datetime, timedelta
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from food_link.config.settings import Settings
from food_link.controller.database import get_session
from food_link.middleware.error_hadler import credentials_exception
from food_link.models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
pwd_context = PasswordHash.recommended()
settings = Settings()

T_Session = Annotated[Session, Depends(get_session)]


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = data.copy()
    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user(session: T_Session, token: str = Depends(oauth2_scheme)):
    try:
        paylod = decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email = paylod.get('sub')
        if not email:
            raise credentials_exception()

    except PyJWTError:
        raise credentials_exception()

    user = session.scalar(select(User).where(User.email == email))

    if not user:
        raise credentials_exception()

    return user
