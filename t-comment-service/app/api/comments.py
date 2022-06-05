from fastapi import HTTPException
from typing import List
from fastapi import Header, APIRouter

from app.api.models import CommentIn, CommentOut, CommentUpdate
from app.api import db_manager
from app.api.service import is_user_present, is_article_present

comments = APIRouter()


@comments.get('/', response_model=List[CommentOut])
async def index():
    return await db_manager.get_all_articles()


@comments.get('/{id}', response_model=CommentOut)
async def get_comment(id: int):
    comment = await db_manager.get_comment(id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@comments.post('/', status_code=201)
async def create_comment(payload: CommentIn):
    userId = payload.userId
    articleId = payload.articleId

    if not is_user_present(userId):
        raise HTTPException(
            status_code=404, detail=f"User with id:{userId} not found")
    if not is_article_present(articleId):
        raise HTTPException(
            status_code=404, detail=f"Article with id:{articleId} not found")

    commentId = await db_manager.add_comment(payload)
    response = {
        'id': commentId,
        **payload.dict()
    }

    return response


@comments.put('/{id}')
async def update_comment(id: int, payload: CommentUpdate):
    comment = await db_manager.get_comment(id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    update_data = payload.dict(exclude_unset=True)

    comment_in_db = CommentIn(**comment)

    updated_comment = comment_in_db.copy(update=update_data)

    return await db_manager.update_comment(id, updated_comment)


@comments.delete('/{id}')
async def delete_comment(id: int):
    comment = await db_manager.get_comment(id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return await db_manager.delete_comment(id)
