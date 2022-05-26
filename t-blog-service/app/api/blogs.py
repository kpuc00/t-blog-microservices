from fastapi import HTTPException
from typing import List
from fastapi import Header, APIRouter, Depends
from fastapi.security import SecurityScopes
from app.api.models import BlogIn, BlogOut, BlogUpdate
from app.api import db_manager
from app.api.service import is_user_present
from app.api.utils import OAuth2PasswordBearerWithCookie
import httpx

blogs = APIRouter()

oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl="http://localhost/api/auth/login")


@blogs.get('/', response_model=List[BlogOut])
async def index(authorization: str = Depends(oauth2_scheme)):
    print(authorization)
    headers = {"Authorization": f"Bearer {authorization}"}
    result = httpx.get(
        "http://t-auth-service:8000/api/auth/users/me", headers=headers)
    print(result)
    return await db_manager.get_all_blogs()


@blogs.get('/{id}', response_model=BlogOut)
async def get_blog(id: int):
    blog = await db_manager.get_blog(id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@blogs.post('/', status_code=201)
async def create_blog(payload: BlogIn):
    authorId = payload.authorId
    collaboratorsId = payload.collaboratorsId

    if not is_user_present(authorId):
        raise HTTPException(
            status_code=404, detail=f"Author with id:{authorId} not found")
    for collaboratorId in collaboratorsId:
        if not is_user_present(collaboratorId):
            raise HTTPException(
                status_code=404, detail=f"Collaborator with id:{collaboratorId} not found")

    blogId = await db_manager.add_blog(payload)
    response = {
        'id': blogId,
        **payload.dict()
    }

    return response


@blogs.put('/{id}')
async def update_blog(id: int, payload: BlogUpdate):
    blog = await db_manager.get_blog(id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    update_data = payload.dict(exclude_unset=True)

    if "collaboratorsId" in update_data:
        for collaboratorId in payload.collaboratorsId:
            if not is_user_present(collaboratorId):
                raise HTTPException(
                    status_code=404, detail=f"User with id:{collaboratorId} not found")

    blog_in_db = BlogIn(**blog)

    updated_blog = blog_in_db.copy(update=update_data)

    return await db_manager.update_blog(id, updated_blog)


@blogs.delete('/{id}')
async def delete_blog(id: int):
    blog = await db_manager.get_blog(id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return await db_manager.delete_blog(id)
