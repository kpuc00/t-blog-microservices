import os
from fastapi import Depends, HTTPException, Security, status
from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.api.models import User, TokenData
from app.api import db_manager
from app.api.utils import OAuth2PasswordBearerWithCookie
from fastapi.security import SecurityScopes
from pydantic import ValidationError

SECRET_KEY = os.environ.get('AUTH_SECRET_KEY')
ALGORITHM = os.environ.get('AUTH_TOKEN_ALGORITHM')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl="login",
    # scopes={"moderator": "Can moderate other user's comments on articles",
    #         "admin": "Can review reports and remove articles"}
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await db_manager.get_user_by_username(username)
    if user.disabled:
        raise HTTPException(
            status_code=400, detail="This account is disabled!")
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(  # security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme)):
    # if security_scopes.scopes:
    #     authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    # else:
    authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await db_manager.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    # for scope in security_scopes.scopes:
    #     if scope not in token_data.scopes:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Not enough permissions",
    #             headers={"WWW-Authenticate": authenticate_value},
    #         )
    return user


async def get_current_active_user(current_user: User = Security(get_current_user)):
    if current_user.disabled:
        return None
    else:
        return current_user


# async def try_moderator_scope(current_user: User = Security(get_current_user, scopes=["moderator"])):
#     return current_user


# async def try_admin_scope(current_user: User = Security(get_current_user, scopes=["admin"])):
#     return current_user
