from typing import Dict, List
from datetime import datetime
from pydantic import BaseModel

class Character(BaseModel):
    id: str
    novel_id: str
    full_name: str
    aliases: List[str]
    initial_description: str
    personality_traits: List[str]
    speech_patterns: List[str]
    relationships: Dict[str, str]
    created_at: datetime

class Event(BaseModel):
    id: str
    novel_id: str
    summary: str
    characters_involved: List[str]
    location: str
    importance: int
    emotions: List[str]
    consequences: List[str]
    chapter_number: int
    timestamp: datetime