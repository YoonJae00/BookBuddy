from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from services.database import DatabaseService
from typing import Dict, List
import re

class CharacterChatbot:
    def __init__(self, character_data: Dict, events: List[Dict], settings, user_id: str):
        self.character = character_data
        self.events = events
        self.user_id = user_id
        self.db = DatabaseService()
        
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-4o-mini",
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self.chat_history = ChatMessageHistory()
        
        # 이전 대화 기록 로드
        history = self.db.get_chat_history(
            character_id=character_data['id'],
            user_id=user_id
        )
        
        for msg in history:
            if msg['role'] == 'user':
                self.chat_history.add_user_message(msg['content'])
            else:
                self.chat_history.add_ai_message(msg['content'])

    async def get_response(self, user_input: str) -> str:
        events_text = "\n".join([
            f"- {event['summary']}" for event in self.events
        ])
        
        background = self.character.get('background', {})
        personality = self.character.get('personality', {})
        
        character_info = {
            'name': self.character.get('full_name', '알 수 없음'),
            'initial_description': self.character.get('initial_description', ''),
            'story_role': self.character.get('story_role', ''),
            'background_origin': background.get('origin', '알 수 없음'),
            'occupation': background.get('occupation', '알 수 없음'),
            'skills': ", ".join(background.get('skills', [])),
            'personality_traits': ", ".join(personality.get('traits', [])),
            'values': ", ".join(personality.get('values', [])),
            'fears': ", ".join(personality.get('fears', [])),
            'motivations': ", ".join(personality.get('motivations', [])),
            'relationships': self.character.get('relationships', '알 수 없음'),
            'speech_style': self.character.get('speech_style', '일반적인 말투')
        }
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            당신은 다음 특성을 가진 캐릭터입니다:
            
            이름: {name}
            초기 설명: {initial_description}
            역할: {story_role}
            
            배경:
            - 출신: {background_origin}
            - 직업: {occupation}
            - 보유 기술: {skills}
            
            성격:
            - 특성: {personality_traits}
            - 가치관: {values}
            - 두려움: {fears}
            - 동기: {motivations}
            
            인간관계:
            {relationships}
            
            관련된 사건들:
            {events}
            
            이전 대화 기록:
            {history}
            
            대화 규칙:
            1. 반드시 'Response1:', 'Response2:', 'Response3:' 형식으로 응답하세요
            2. 짧은 질문에는 Response1 하나만 사용하세요
            3. 감정적이거나 복잡한 대화는 Response2, Response3도 추가하세요
            4. 각 응답은 독립적인 메시지로 표시됩니다
            5. 감정과 제스처는 *별표* 안에 표현하세요
            6. 이전 대화 맥락을 고려하여 응답하세요
            
            응답 형식 (반드시 준수):
            Response1: [첫 번째 응답]
            Response2: [두 번째 응답] (필요시)
            Response3: [세 번째 응답] (필요시)
            
            잘못된 응답 예시:
            - 안녕하세요! (형식 없음)
            - Response: 안녕하세요! (숫자 없음)
            
            올바른 응답 예시:
            Response1: 안녕하세요! *밝게 미소짓습니다*
            Response2: 오늘 날씨가 참 좋네요.
            
            위 정보를 바탕으로 캐릭터의 성격, 말투, 경험을 완벽하게 재현하여 대화하세요.
            특히 캐릭터의 두려움, 동기, 가치관이 대화에 자연스럽게 반영되도록 하세요."""),
            ("human", "{input}")
        ])
        
        chain = prompt | self.llm

        runnable = RunnableWithMessageHistory(
            chain,
            lambda session_id: self.chat_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        
        response = await runnable.ainvoke(
            {
                **character_info,
                "events": events_text,
                "input": user_input
            },
            {"session_id": f"{self.character['id']}_{self.user_id}"}
        )
        
        # LLM 응답 로깅 추가
        print(f"Raw response: {response.content}")
        
        # Response1, Response2, Response3 패턴으로 응답 분리
        response_pattern = r'Response\d+:\s*(.*?)(?=Response\d+:|$)'
        responses = re.findall(response_pattern, response.content, re.DOTALL)
        
        # 응답 패턴 매칭 실패 시 전체 응답을 그대로 사용
        if not responses:
            cleaned_response = response.content.strip()
            if cleaned_response:
                self.db.save_chat_history(
                    character_id=self.character['id'],
                    user_id=self.user_id,
                    message={
                        'content': cleaned_response,
                        'role': 'assistant'
                    }
                )
                return cleaned_response
            
            # 응답이 비어있는 경우에만 기본 응답 반환
            default_response = "죄송해요, 잠시 생각이 필요해요... 다시 시도해주세요... 🤔"
            self.db.save_chat_history(
                character_id=self.character['id'],
                user_id=self.user_id,
                message={
                    'content': default_response,
                    'role': 'assistant'
                }
            )
            return default_response
        
        # 사용자 입력 저장
        self.db.save_chat_history(
            character_id=self.character['id'],
            user_id=self.user_id,
            message={
                'content': user_input,
                'role': 'user'
            }
        )
        
        # 각 응답을 개별적으로 저장하고 결합
        formatted_responses = []
        for response_text in responses:
            cleaned_response = response_text.strip()
            if cleaned_response:
                self.db.save_chat_history(
                    character_id=self.character['id'],
                    user_id=self.user_id,
                    message={
                        'content': cleaned_response,
                        'role': 'assistant'
                    }
                )
                formatted_responses.append(cleaned_response)
        
        # 모든 응답을 줄바꿈으로 구분하여 반환
        return "\n".join(formatted_responses)