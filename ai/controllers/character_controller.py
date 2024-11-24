from fastapi import APIRouter, HTTPException, Depends
from typing import List
from config import get_settings
from services.database import DatabaseService

router = APIRouter()

@router.get("/novels/{novel_id}/characters")
async def get_novel_characters(
    novel_id: str,
    settings = Depends(get_settings)
):
    """소설의 캐릭터 목록 조회"""
    try:
        db = DatabaseService()
        characters = db.get_characters_by_novel(novel_id)
        
        if not characters:
            raise HTTPException(
                status_code=404,
                detail="No characters found for this novel"
            )
            
        return characters
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get characters: {str(e)}"
        )