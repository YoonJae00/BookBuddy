from typing import Optional, Any, Dict
import redis
import json
from datetime import timedelta

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
    
    async def get_character(self, character_id: str) -> Optional[Dict]:
        """캐릭터 정보 캐시에서 조회"""
        cached = self.redis_client.get(f"character:{character_id}")
        return json.loads(cached) if cached else None
    
    async def set_character(
        self,
        character_id: str,
        character_data: Dict,
        expire_in: int = 3600
    ):
        """캐릭터 정보 캐시에 저장"""
        self.redis_client.setex(
            f"character:{character_id}",
            timedelta(seconds=expire_in),
            json.dumps(character_data)
        )
    
    async def get_chat_history(
        self,
        character_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """대화 기록 캐시에서 조회"""
        cached = self.redis_client.lrange(
            f"chat_history:{character_id}",
            0,
            limit - 1
        )
        return [json.loads(msg) for msg in cached]
    
    async def add_chat_message(
        self,
        character_id: str,
        message: Dict
    ):
        """대화 기록 캐시에 추가"""
        self.redis_client.lpush(
            f"chat_history:{character_id}",
            json.dumps(message)
        )
        # 최대 50개 메시지만 유지
        self.redis_client.ltrim(f"chat_history:{character_id}", 0, 49)