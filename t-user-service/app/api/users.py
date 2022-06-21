import os
from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.api import auth_handler
from app.api import db_manager
from app.api.models import UserInDB, UserOut

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get('AUTH_ACCESS_TOKEN_EXPIRE_MINUTES'))

users = APIRouter()


@users.post("/register", status_code=201)
async def register_user(payload: UserInDB):
    username = payload.username
    password = payload.password
    first_name = payload.first_name
    last_name = payload.last_name
    email = payload.email
    disabled = None
    if payload.disabled is None:
        disabled = False
    else:
        disabled = payload.disabled
    exist = await db_manager.get_user_by_username(username)
    if exist:
        raise HTTPException(status_code=400, detail="Username is taken!")
    hashed_password = auth_handler.get_password_hash(password)
    user = {
        "username": username,
        "password": hashed_password,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "disabled": disabled
    }
    await db_manager.add_user(user)
    return {"message": "User registered successfully."}


@users.post("/login", response_model=UserOut)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_handler.authenticate_user(
        form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_handler.create_access_token(
        data={
            "sub": user.username,
            # "scopes": form_data.scopes
        },
        expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token",
                        value=f"Bearer {access_token}", httponly=True)
    return user


@users.get("/logout")
async def logout_user(response: Response, token: str = Depends(auth_handler.oauth2_scheme)):
    response.set_cookie(key="access_token", value=None, httponly=True)
    return {"message": "You have been logged out!"}


@users.get("/me", response_model=UserOut)
async def get_own_user_data(current_user: UserOut = Depends(auth_handler.get_current_active_user)):
    if current_user is None:
        raise HTTPException(
            status_code=400, detail="This account is disabled!")
    else:
        return current_user


# @users.get("/moderator")
# async def test_moderator_permission(current_user: User = Depends(auth_handler.try_moderator_scope)):
#     return {"message": f"User {current_user.username} is moderator"}


# @users.get("/admin")
# async def test_admin_permission(current_user: User = Depends(auth_handler.try_admin_scope)):
#     return {"message": f"User {current_user.username} is administrator"}


@users.get('/{id}', response_description="User exists")
async def check_if_user_exists(id: int):
    user = await db_manager.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return
