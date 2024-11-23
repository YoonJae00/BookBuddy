from firebase_admin import firestore
from typing import Dict, List
import uuid
from datetime import datetime

class DatabaseService:
    def __init__(self):
        self.db = firestore.client()
    
    async def save_novel_analysis(self, novel_id: str, analysis_result: Dict):
        """분석 결과를 DB에 저장"""
        try:
            batch = self.db.batch()
            
            # 캐릭터 저장
            for character in analysis_result['characters']:
                char_id = str(uuid.uuid4())
                character['id'] = char_id
                character['novel_id'] = novel_id
                character['created_at'] = datetime.now()
                char_ref = self.db.collection('characters').document(char_id)
                batch.set(char_ref, character)
            
            # 이벤트 저장
            for event in analysis_result['events']:
                event_id = str(uuid.uuid4())
                event['id'] = event_id
                event['novel_id'] = novel_id
                event['updated_at'] = datetime.now()
                event_ref = self.db.collection('events').document(event_id)
                batch.set(event_ref, event)
            
            # 일괄 처리 실행
            batch.commit()
            return novel_id
        
        except Exception as e:
            raise NovelProcessingError(
                "Failed to save novel analysis",
                {"error": str(e)}
            )
    
    async def get_character(self, character_id: str) -> Dict:
        """캐릭터 정보 조회"""
        doc = await self.db.collection('characters').document(character_id).get()
        return doc.to_dict() if doc.exists else None
    
    async def get_character_events(self, character_name: str, novel_id: str) -> List[Dict]:
        """캐릭터 관련 이벤트 조회"""
        events = await self.db.collection('events')\
            .where('novel_id', '==', novel_id)\
            .where('characters_involved', 'array_contains', character_name)\
            .get()
        return [event.to_dict() for event in events]