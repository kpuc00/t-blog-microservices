from app.api.models import UserInDB
from app.api.db import users, database


async def add_user(payload: UserInDB):
    query = users.insert().values(payload)

    return await database.execute(query=query)


async def get_user(username: str):
    query = users.select(users.c.username == username)
    return await database.fetch_one(query=query)


async def update_user(id: int, payload: UserInDB):
    query = (
        users
        .update()
        .where(users.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)


async def delete_user(id: int):
    query = users.delete().where(users.c.id == id)
    return await database.execute(query=query)

# async def get_all_users():
#     query = users.select()
#     return await database.fetch_all(query=query)
