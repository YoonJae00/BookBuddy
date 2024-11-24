from firebase_admin import firestore
from typing import Dict, List
import uuid
from datetime import datetime
from utils.logger import NovelLogger
from google.cloud.firestore_v1.base_query import FieldFilter
from fastapi import HTTPException

class DatabaseService:
    def __init__(self):
        self.db = firestore.client()
        self.logger = NovelLogger()
    
    def save_novel(self, novel_id: str, title: str, content: str, author: str) -> None:
        """소설 정보 저장 (동기식)"""
        try:
            self.db.collection('novels').document(novel_id).set({
                'id': novel_id,
                'title': title,
                'content': content,
                'author': author,
                'created_at': firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            raise Exception(f"Failed to save novel: {str(e)}")
    
    def get_character(self, character_id: str) -> Dict:
        """캐릭터 ID로 캐릭터 정보 조회"""
        try:
            character = self.db.collection('characters').document(character_id).get()
            if character.exists:
                return {**character.to_dict(), 'id': character.id}
            return None
        except Exception as e:
            raise Exception(f"Failed to get character: {str(e)}")
    
    def get_character_events(self, character_name: str, novel_id: str) -> List[Dict]:
        """캐릭터 관련 이벤트 조회"""
        try:
            events = self.db.collection('events')\
                .where(filter=FieldFilter('novel_id', '==', novel_id))\
                .where(filter=FieldFilter('characters_involved', 'array_contains', character_name))\
                .get()
            return [event.to_dict() for event in events]
        except Exception as e:
            print(f"Failed to get character events: {str(e)}")
            return []
    
    def search_novels_by_title(self, title: str) -> List[Dict]:
        """소설 제목으로 검색 (동기식)"""
        try:
            # 대소문자 구분 없이 부분 일치 검색
            novels = self.db.collection('novels')\
                .where('title', '>=', title)\
                .where('title', '<=', title + '\uf8ff')\
                .get()
            
            if not novels:
                return []
            
            return [
                {
                    **novel.to_dict(),
                    'id': novel.id
                } 
                for novel in novels
            ]
        except Exception as e:
            print(f"Failed to search novels: {str(e)}")
            return []
    
    def get_characters_by_novel(self, novel_id: str) -> List[Dict]:
        """소설의 캐릭터 목록 조회 (동기식)"""
        try:
            characters = self.db.collection('characters')\
                .where('novel_id', '==', novel_id)\
                .get()
            return [character.to_dict() for character in characters]
        except Exception as e:
            raise Exception(f"Failed to get characters: {str(e)}")
    
    def check_duplicate_character(self, character_data: Dict) -> bool:
        """캐릭터 중복 체크"""
        try:
            existing_chars = self.db.collection('characters')\
                .where('full_name', '==', character_data['full_name'])\
                .where('novel_id', '==', character_data['novel_id'])\
                .get()
            
            return len(list(existing_chars)) > 0
        except Exception as e:
            print(f"Failed to check duplicate character: {str(e)}")
            return False
    
    def save_character(self, character_data: Dict) -> None:
        """캐릭터 정보 저장"""
        try:
            character_id = character_data.get('id')
            if not character_id:
                raise Exception("Character ID is required")
            
            self.db.collection('characters')\
                .document(character_id)\
                .set(character_data)
                
        except Exception as e:
            raise Exception(f"Failed to save character: {str(e)}")
    
    def save_event(self, event_data: Dict) -> None:
        """이벤트 정보 저장"""
        try:
            self.db.collection('events').document(event_data['id']).set(event_data)
        except Exception as e:
            raise Exception(f"Failed to save event: {str(e)}")
    
    def get_character_by_name_and_novel(self, character_name: str, novel_id: str) -> Dict:
        """캐릭터 이름과 소설 ID로 캐릭터 정보 조회"""
        try:
            characters = self.db.collection('characters')\
                .where('novel_id', '==', novel_id)\
                .where('full_name', '==', character_name)\
                .get()
            docs = list(characters)
            return docs[0].to_dict() if docs else None
        except Exception as e:
            raise Exception(f"Failed to get character: {str(e)}")
    
    def update_character(self, character_name: str, novel_id: str, updated_info: Dict) -> None:
        """캐릭터 정보 업데이트"""
        try:
            characters = self.db.collection('characters')\
                .where('novel_id', '==', novel_id)\
                .where('full_name', '==', character_name)\
                .get()
            docs = list(characters)
            if docs:
                self.db.collection('characters').document(docs[0].id).update(updated_info)
        except Exception as e:
            raise Exception(f"Failed to update character: {str(e)}")
    
    def get_all_novels(self) -> List[Dict]:
        """소설 전체 목록 조회 (동기식)"""
        try:
            novels = self.db.collection('novels')\
                .order_by('created_at', direction=firestore.Query.DESCENDING)\
                .get()
            
            return [
                {
                    **novel.to_dict(),
                    'id': novel.id
                } 
                for novel in novels
            ]
        except Exception as e:
            print(f"Failed to get all novels: {str(e)}")
            return []
    
    def save_chat_history(self, character_id: str, user_id: str, message: Dict) -> None:
        """대화 기록 저장"""
        try:
            self.db.collection('chat_history').add({
                'character_id': character_id,
                'user_id': user_id,
                'content': message['content'],
                'role': message['role'],
                'timestamp': firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            print(f"Failed to save chat history: {str(e)}")
    
    def get_chat_history(self, character_id: str, user_id: str, limit: int = 10) -> List[Dict]:
        """대화 기록 조회"""
        try:
            history = self.db.collection('chat_history')\
                .where('character_id', '==', character_id)\
                .where('user_id', '==', user_id)\
                .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                .limit(limit)\
                .get()
            
            return [msg.to_dict() for msg in history][::-1]
        except Exception as e:
            print(f"Chat error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))