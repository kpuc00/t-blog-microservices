from app.api.models import CommentIn, CommentOut, CommentUpdate
from app.api.db import comments, database


async def add_comment(payload: CommentIn):
    query = comments.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_articles():
    query = comments.select()
    return await database.fetch_all(query=query)


async def get_comment(id):
    query = comments.select(comments.c.id == id)
    return await database.fetch_one(query=query)


async def update_comment(id: int, payload: CommentIn):
    query = (
        comments
        .update()
        .where(comments.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)


async def delete_comment(id: int):
    query = comments.delete().where(comments.c.id == id)
    return await database.execute(query=query)
