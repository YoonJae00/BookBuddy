from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.chat import ChatMessage
from services.chatbot import CharacterChatbot
from services.database import DatabaseService
from config import get_settings

router = APIRouter()

@router.post("/chat/{character_id}")
async def chat_with_character(
    character_id: str,
    message: ChatMessage,
    settings = Depends(get_settings)
):
    """캐릭터와 채팅"""
    try:
        # DB에서 캐릭터 정보 조회
        db = DatabaseService()
        character = await db.get_character(character_id)
        if not character:
            raise HTTPException(status_code=404, detail="Character not found")
        
        # 캐릭터 관련 이벤트 조회
        events = await db.get_character_events(character['full_name'], character['novel_id'])
        
        # 챗봇 초기화
        chatbot = CharacterChatbot(
            character_data=character,
            events=events,
            settings=settings
        )
        
        # 응답 생성
        response = await chatbot.get_response(message.content)
        
        return {
            "character_name": character['full_name'],
            "response": response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))