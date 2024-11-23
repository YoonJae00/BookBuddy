from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class CharacterBase(BaseModel):
    full_name: str
    aliases: List[str] = []
    initial_description: str = ""
    personality_traits: List[str] = []
    speech_patterns: List[str] = []
    relationships: Dict[str, str] = {}

class CharacterCreate(CharacterBase):
    novel_id: str

class Character(CharacterBase):
    id: str
    novel_id: str
    created_at: datetime = datetime.now()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data) 