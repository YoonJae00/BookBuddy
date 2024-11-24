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
    settings = Depends(get_settings),
    user_id: str = "anonymous"
):
    """캐릭터와 채팅"""
    try:
        db = DatabaseService()
        character = db.get_character(character_id)
        if not character:
            raise HTTPException(status_code=404, detail="Character not found")
        
        events = db.get_character_events(character['full_name'], character['novel_id'])
        
        chatbot = CharacterChatbot(
            character_data=character,
            events=events,
            settings=settings,
            user_id=user_id
        )
        
        response = await chatbot.get_response(message.content)
        
        return {
            "character_name": character['full_name'],
            "response": response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history/{character_id}")
async def get_chat_history(
    character_id: str,
    user_id: str = "anonymous"
):
    db = DatabaseService()
    history = db.get_chat_history(character_id=character_id, user_id=user_id)
    return history