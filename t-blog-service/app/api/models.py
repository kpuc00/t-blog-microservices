from typing import List, Optional
from pydantic import BaseModel

class BlogIn(BaseModel):
    name: str
    description: str
    authorId: int
    collaboratorsId: List[int]

class BlogOut(BlogIn):
    id: int

class BlogUpdate(BlogIn):
    name: Optional[str] = None
    description: Optional[str] = None
    authorId: Optional[int] = None
    collaboratorsId: Optional[List[int]] = None