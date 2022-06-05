from app.api.models import ArticleIn, ArticleOut, ArticleUpdate
from app.api.db import articles, database


async def add_article(payload: ArticleIn):
    query = articles.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_all_articles():
    query = articles.select()
    return await database.fetch_all(query=query)


async def get_article(id):
    query = articles.select(articles.c.id == id)
    return await database.fetch_one(query=query)


async def delete_article(id: int):
    query = articles.delete().where(articles.c.id == id)
    return await database.execute(query=query)


async def update_article(id: int, payload: ArticleIn):
    query = (
        articles
        .update()
        .where(articles.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)
