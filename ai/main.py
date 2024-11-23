import os
from typing import List, Dict
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# 환경 변수 설정
load_dotenv()

# Firebase 초기화
cred = credentials.Certificate("path/to/serviceAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class NovelProcessor:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0)
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        
    def extract_events_from_chapter(self, chapter_text: str, chapter_number: int) -> Dict:
        """각 챕터에서 주요 사건을 추출"""
        event_prompt = PromptTemplate(
            input_variables=["chapter_text"],
            template="""
            다음 챕터의 내용을 분석하여 주요 사건들을 추출하세요.
            형식:
            1. 사건 요약
            2. 관련 인물
            3. 발생 장소
            4. 시간적 배경
            5. 사건의 중요도 (1-5)
            
            챕터 내용:
            {chapter_text}
            """
        )
        
        event_chain = LLMChain(llm=self.llm, prompt=event_prompt)
        response = event_chain.run(chapter_text=chapter_text)
        
        # LLM 응답을 구조화된 형식으로 파싱
        # 실제 구현에서는 더 강건한 파싱 로직이 필요
        event_data = self._parse_event_response(response)
        event_data['chapter_number'] = chapter_number
        
        return event_data
    
    def extract_character_info(self, text: str) -> Dict:
        """캐릭터 정보 추출"""
        character_prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            다음 텍스트에서 등장인물의 정보를 추출하세요:
            1. 이름
            2. 성격 특성
            3. 특징적인 말투나 표현
            4. 다른 인물과의 관계
            5. 주요 행동 패턴
            
            텍스트:
            {text}
            """
        )
        
        character_chain = LLMChain(llm=self.llm, prompt=character_prompt)
        response = character_chain.run(text=text)
        
        return self._parse_character_response(response)
    
    def _parse_event_response(self, response: str) -> Dict:
        """LLM 응답을 구조화된 데이터로 변환"""
        # 실제 구현에서는 더 정교한 파싱 로직 필요
        return {
            'summary': response,
            'timestamp': datetime.now(),
            'processed': True
        }
    
    def _parse_character_response(self, response: str) -> Dict:
        """캐릭터 정보 응답을 구조화된 데이터로 변환"""
        # 실제 구현에서는 더 정교한 파싱 로직 필요
        return {
            'character_info': response,
            'timestamp': datetime.now()
        }

class NovelDatabase:
    def __init__(self):
        self.db = firestore.client()
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
    
    def store_event(self, event_data: Dict):
        """Firestore와 Chroma에 이벤트 저장"""
        # Firestore에 저장
        events_ref = self.db.collection('events')
        event_doc = events_ref.add(event_data)
        
        # Chroma에 저장
        if self.vectorstore is None:
            self.vectorstore = Chroma(
                embedding_function=self.embeddings,
                persist_directory="./chroma_db"
            )
        
        self.vectorstore.add_texts(
            texts=[event_data['summary']],
            metadatas=[{
                'chapter_number': event_data['chapter_number'],
                'event_id': event_doc[1].id
            }]
        )
    
    def store_character(self, character_data: Dict):
        """캐릭터 정보 저장"""
        characters_ref = self.db.collection('characters')
        characters_ref.add(character_data)

class NovelChatbot:
    def __init__(self, vectorstore):
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(temperature=0.7),
            retriever=vectorstore.as_retriever(),
            memory=self.memory
        )
        self.db = firestore.client()
    
    def answer_question(self, question: str) -> str:
        """사용자 질문에 답변"""
        # 질문 유형 분류
        if "캐릭터" in question or "인물" in question:
            return self._handle_character_question(question)
        elif "사건" in question or "어떤 일" in question:
            return self._handle_event_question(question)
        else:
            return self._handle_general_question(question)
    
    def _handle_character_question(self, question: str) -> str:
        """캐릭터 관련 질문 처리"""
        characters_ref = self.db.collection('characters')
        # 실제 구현에서는 더 정교한 검색 로직 필요
        characters = characters_ref.get()
        return self._format_character_response(characters)
    
    def _handle_event_question(self, question: str) -> str:
        """사건 관련 질문 처리"""
        response = self.qa_chain({"question": question})
        return response['answer']
    
    def _handle_general_question(self, question: str) -> str:
        """일반 질문 처리"""
        response = self.qa_chain({"question": question})
        return response['answer']

def main():
    # 소설 텍스트 로드
    with open('novel.txt', 'r', encoding='utf-8') as file:
        novel_text = file.read()
    
    # 텍스트를 챕터별로 분할 (실제 구현에서는 더 정교한 분할 로직 필요)
    chapters = novel_text.split('Chapter')
    
    # 프로세서 및 데이터베이스 초기화
    processor = NovelProcessor()
    novel_db = NovelDatabase()
    
    # 각 챕터 처리
    for i, chapter in enumerate(chapters[1:], 1):  # 첫 번째 요소 건너뛰기
        # 사건 추출 및 저장
        event_data = processor.extract_events_from_chapter(chapter, i)
        novel_db.store_event(event_data)
        
        # 캐릭터 정보 추출 및 저장
        character_data = processor.extract_character_info(chapter)
        novel_db.store_character(character_data)
    
    # 챗봇 초기화
    chatbot = NovelChatbot(novel_db.vectorstore)
    
    # 대화 예시
    while True:
        question = input("질문을 입력하세요 (종료하려면 'quit' 입력): ")
        if question.lower() == 'quit':
            break
        answer = chatbot.answer_question(question)
        print(f"답변: {answer}")

if __name__ == "__main__":
    main()