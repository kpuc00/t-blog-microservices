from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class CommentIn(BaseModel):
    content: str
    userId: int
    # created: datetime = datetime.now()
    articleId: int


class CommentOut(CommentIn):
    id: int


class CommentUpdate(CommentIn):
    content: Optional[str] = None
    # modified: Optional[datetime] = None
