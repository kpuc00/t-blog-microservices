from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ArticleIn(BaseModel):
    title: str
    content: str
    authorId: int
    # created: datetime = datetime.now()
    blogId: int


class ArticleOut(ArticleIn):
    id: int


class ArticleUpdate(ArticleIn):
    title: Optional[str] = None
    content: Optional[str] = None
    # modified: Optional[datetime] = None
