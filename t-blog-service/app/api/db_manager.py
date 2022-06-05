from app.api.models import BlogIn, BlogOut, BlogUpdate
from app.api.db import blogs, database


async def add_blog(payload: BlogIn):
    query = blogs.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_blogs():
    query = blogs.select()
    return await database.fetch_all(query=query)


async def get_blog(id):
    query = blogs.select(blogs.c.id == id)
    return await database.fetch_one(query=query)


async def delete_blog(id: int):
    query = blogs.delete().where(blogs.c.id == id)
    return await database.execute(query=query)


async def update_blog(id: int, payload: BlogIn):
    query = (
        blogs
        .update()
        .where(blogs.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)
