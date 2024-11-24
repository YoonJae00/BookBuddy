from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from services.database import DatabaseService
from typing import Dict, List

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
        
        character_info = {
            'full_name': self.character.get('full_name', '알 수 없음'),
            'personality': self.character.get('personality', '알 수 없음'),
            'background': self.character.get('background', '알 수 없음'),
            'speech_style': self.character.get('speech_style', '일반적인 말투')
        }
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            당신은 다음 특성을 가진 캐릭터입니다:
            이름: {name}
            성격: {personality}
            배경: {background}
            말투: {speech_style}
            
            관련된 사건들:
            {events}
            
            이 캐릭터의 성격과 경험을 바탕으로 대화하세요.
            """),
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
                "name": character_info['full_name'],
                "personality": character_info['personality'],
                "background": character_info['background'],
                "speech_style": character_info['speech_style'],
                "events": events_text,
                "input": user_input
            },
            {"session_id": f"{self.character['id']}_{self.user_id}"}
        )
        
        # 대화 기록 저장
        self.db.save_chat_history(
            character_id=self.character['id'],
            user_id=self.user_id,
            message={
                'content': user_input,
                'role': 'user'
            }
        )
        self.db.save_chat_history(
            character_id=self.character['id'],
            user_id=self.user_id,
            message={
                'content': response.content,
                'role': 'assistant'
            }
        )
        
        return response.content