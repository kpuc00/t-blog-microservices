from typing import List, Optional
from pydantic import BaseModel


class UserIn(BaseModel):
    name: str
    email: str


class UserOut(UserIn):
    id: int


class UserUpdate(UserIn):
    name: Optional[str] = None
    email: Optional[str] = None
