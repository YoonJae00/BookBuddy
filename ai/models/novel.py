from pydantic import BaseModel
from typing import Optional

class NovelBase(BaseModel):
    title: str
    content: str
    author: Optional[str] = None

class NovelCreate(NovelBase):
    pass

class Novel(NovelBase):
    id: str