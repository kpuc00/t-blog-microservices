from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from app.api.models import Blog, BlogOut, BlogUpdate, BlogInDB
from app.api import db_manager
from app.api.service import is_user_present
from app.api.utils import OAuth2PasswordBearerWithCookie
from app.api.rabbitmq.rpc_client import RpcClient
import os

blogs = APIRouter()

USER_SERVICE_HOST_URL = 'http://localhost:8002/api/users/'
url = os.environ.get('USER_SERVICE_HOST_URL') or USER_SERVICE_HOST_URL

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl=f'{url}login')


@blogs.get('/', response_model=List[BlogOut])
async def index(token: str = Depends(oauth2_scheme)):
    return await db_manager.get_all_blogs()


@blogs.get('/{id}', response_model=BlogOut,)
async def get_blog(id: int, token: str = Depends(oauth2_scheme)):
    blog = await db_manager.get_blog(id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@blogs.post('/', status_code=201, response_model=BlogOut)
async def create_blog(payload: Blog, token: str = Depends(oauth2_scheme)):
    rpc = await RpcClient().connect()
    authorId = await rpc.call(token)

    for collaboratorId in payload.collaboratorsId:
        if not is_user_present(collaboratorId, token):
            raise HTTPException(
                status_code=404, detail=f"Collaborator with id:{collaboratorId} does not exist!")
    blog = BlogInDB.parse_obj({"name": payload.name, "description": payload.description,
                               "collaboratorsId": payload.collaboratorsId, "authorId": authorId})
    blogId = await db_manager.add_blog(blog)
    response = {
        'id': blogId,
        **blog.dict()
    }
    return response


@blogs.put('/{id}')
async def update_blog(id: int, payload: BlogUpdate,  token: str = Depends(oauth2_scheme)):
    blog = await db_manager.get_blog(id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    update_data = payload.dict(exclude_unset=True)

    if "collaboratorsId" in update_data:
        for collaboratorId in payload.collaboratorsId:
            if not is_user_present(collaboratorId, token):
                raise HTTPException(
                    status_code=404, detail=f"User with id:{collaboratorId} does not exist!")

    blog_in_db = Blog(**blog)

    updated_blog = blog_in_db.copy(update=update_data)

    return await db_manager.update_blog(id, updated_blog)


@blogs.delete('/{id}', status_code=204)
async def delete_blog(id: int, token: str = Depends(oauth2_scheme)):
    blog = await db_manager.get_blog(id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return await db_manager.delete_blog(id)
