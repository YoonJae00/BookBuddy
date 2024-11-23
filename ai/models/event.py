from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

class Event(BaseModel):
    id: str
    novel_id: str
    chapter_number: int
    summary: str
    characters_involved: List[str]
    location: str
    importance: int
    timestamp: datetime
    vector_id: str