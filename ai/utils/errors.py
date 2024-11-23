from fastapi import HTTPException
from typing import Dict, Any

class NovelProcessingError(Exception):
    def __init__(self, message: str, details: Dict[str, Any] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class CharacterNotFoundError(Exception):
    def __init__(self, character_name: str):
        self.character_name = character_name
        super().__init__(f"Character not found: {character_name}")

def handle_processing_error(e: Exception) -> HTTPException:
    """에러 처리 헬퍼 함수"""
    if isinstance(e, NovelProcessingError):
        return HTTPException(
            status_code=500,
            detail={
                "message": e.message,
                "details": e.details
            }
        )
    elif isinstance(e, CharacterNotFoundError):
        return HTTPException(
            status_code=404,
            detail=str(e)
        )
    else:
        return HTTPException(
            status_code=500,
            detail="Internal server error"
        )