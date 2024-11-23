from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from utils.vector_store import VectorStore

class CharacterChatbot:
    def __init__(self, character_data: Dict, events: List[Dict], settings):
        self.character = character_data
        self.events = events
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-4-1106-preview",
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    async def get_response(self, user_input: str) -> str:
        # 관련 이벤트 검색
        relevant_events = await self.vector_store.search_similar(
            user_input,
            filter_dict={"characters": self.character["full_name"]}
        )
        
        # 응답 생성
        prompt = PromptTemplate(
            input_variables=["character", "events", "user_input"],
            template="""
            당신은 다음 특성을 가진 캐릭터입니다:
            이름: {character[full_name]}
            성격: {character[personality_traits]}
            말투: {character[speech_patterns]}
            
            관련된 사건들:
            {events}
            
            이 캐릭터의 성격과 경험을 바탕으로 대화하세요.
            
            사용자: {user_input}
            캐릭터:
            """
        )
        
        response = await self.llm.agenerate([
            prompt.format(
                character=self.character,
                events=relevant_events,
                user_input=user_input
            )
        ])
        
        return response.generations[0][0].text