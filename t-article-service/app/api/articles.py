from fastapi import HTTPException
from typing import List
from fastapi import Header, APIRouter

from app.api.models import ArticleIn, ArticleOut, ArticleUpdate
from app.api import db_manager
from app.api.service import is_user_present, is_blog_present

articles = APIRouter()


@articles.get('/', response_model=List[ArticleOut])
async def index():
    return await db_manager.get_all_articles()


@articles.get('/{id}', response_model=ArticleOut)
async def get_article(id: int):
    article = await db_manager.get_article(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@articles.post('/', status_code=201)
async def create_article(payload: ArticleIn):
    authorId = payload.authorId
    blogId = payload.blogId

    if not is_user_present(authorId):
        raise HTTPException(
            status_code=404, detail=f"Author with id:{authorId} not found!")
    if not is_blog_present(blogId):
        raise HTTPException(
            status_code=404, detail=f"Blog with id:{blogId} not found!")

    articleId = await db_manager.add_article(payload)
    response = {
        'id': articleId,
        **payload.dict()
    }

    return response


@articles.put('/{id}')
async def update_article(id: int, payload: ArticleUpdate):
    article = await db_manager.get_article(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    update_data = payload.dict(exclude_unset=True)

    article_in_db = ArticleIn(**article)

    updated_article = article_in_db.copy(update=update_data)

    return await db_manager.update_article(id, updated_article)


@articles.delete('/{id}')
async def delete_article(id: int):
    article = await db_manager.get_article(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return await db_manager.delete_article(id)
