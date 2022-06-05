from fastapi import HTTPException
from typing import List
from fastapi import Header, APIRouter

from app.api.models import UserIn, UserOut, UserUpdate
from app.api import db_manager

users = APIRouter()


@users.post('/', status_code=201)
async def create_user(payload: UserIn):
    userId = await db_manager.add_user(payload)
    response = {
        'id': userId,
        **payload.dict()
    }

    return response


@users.get('/{id}', response_model=UserOut)
async def get_user(id: int):
    user = await db_manager.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
