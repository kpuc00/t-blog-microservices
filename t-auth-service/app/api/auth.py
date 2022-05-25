import os
from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api import auth_handler
from app.api import db_manager
from app.api.models import User, UserInDB, Token


ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get('AUTH_ACCESS_TOKEN_EXPIRE_MINUTES'))


auth = APIRouter()


@auth.post('/register', status_code=201)
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
    return


@auth.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
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
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(auth_handler.get_current_active_user)):
    return current_user


@auth.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(auth_handler.get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
