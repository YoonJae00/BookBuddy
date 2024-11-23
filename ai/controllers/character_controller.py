from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from models.character import Character, CharacterCreate
from services.character_analyzer import CharacterAnalyzer
from config import get_settings
from firebase_admin import firestore

router = APIRouter()
db = firestore.client()

@router.get("/characters/", response_model=List[Character])
async def get_characters(
    novel_id: Optional[str] = None,
    settings = Depends(get_settings)
):
    """캐릭터 목록 조회"""
    try:
        query = db.collection('characters')
        if novel_id:
            query = query.where('novel_id', '==', novel_id)
        
        characters = query.get()
        return [Character.from_dict(doc.to_dict()) for doc in characters]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/characters/{character_id}", response_model=Character)
async def get_character(character_id: str):
    """특정 캐릭터 정보 조회"""
    try:
        doc = db.collection('characters').document(character_id).get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Character not found")
        return Character.from_dict(doc.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/characters/{character_id}/development")
async def get_character_development(character_id: str):
    """캐릭터 발전 과정 조회"""
    try:
        doc = db.collection('characters').document(character_id).get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Character not found")
        return doc.to_dict()['development_history']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))