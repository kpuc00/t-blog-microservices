from typing import List, Optional
from pydantic import BaseModel


class Blog(BaseModel):
    name: str
    description: str
    collaboratorsId: List[int]


class BlogInDB(Blog):
    authorId: int


class BlogOut(Blog):
    id: int
    authorId: int


class BlogUpdate(Blog):
    name: Optional[str] = None
    description: Optional[str] = None
    collaboratorsId: Optional[List[int]] = None
