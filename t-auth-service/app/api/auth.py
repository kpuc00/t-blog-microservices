import os
from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.api import auth_handler
from app.api import db_manager
from app.api.models import User, UserInDB


ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get('AUTH_ACCESS_TOKEN_EXPIRE_MINUTES'))


auth = APIRouter()


@auth.post("/register", status_code=201)
async def register_user(payload: UserInDB):
    username = payload.username
    password = payload.password
    full_name = payload.full_name
    email = payload.email
    disabled = payload.disabled
    exist = await db_manager.get_user(username)
    if exist:
        raise HTTPException(status_code=400, detail="Username is taken.")
    hashed_password = auth_handler.get_password_hash(password)
    user = {
        "username": username,
        "password": hashed_password,
        "full_name": full_name,
        "email": email,
        "disabled": disabled
    }
    await db_manager.add_user(user)
    return {"message": "User registered successfully."}


@auth.post("/login")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_handler.authenticate_user(
        form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_handler.create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token",
                        value=f"Bearer {access_token}", httponly=True)
    return {"message": "User logged in successfully."}


@auth.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(auth_handler.get_current_active_user)):
    return current_user


@auth.get("/moderator")
async def test_moderator_permission(current_user: User = Depends(auth_handler.try_moderator_scope)):
    return {"message": f"User {current_user.username} is moderator"}


@auth.get("/admin")
async def test_admin_permission(current_user: User = Depends(auth_handler.try_admin_scope)):
    return {"message": f"User {current_user.username} is administrator"}
