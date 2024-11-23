from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Dict, List
from datetime import datetime

class EventAnalyzer:
    def __init__(self, name_resolver):
        self.llm = ChatOpenAI(temperature=0)
        self.name_resolver = name_resolver
    
    async def extract_events(
        self, 
        chunk: str,
        chapter_number: int
    ) -> List[Dict]:
        """청크에서 주요 사건 추출"""
        prompt = PromptTemplate(
            input_variables=["chunk"],
            template="""
            다음 텍스트에서 주요 사건들을 추출하세요.
            각 사건에 대해 다음 정보를 JSON 형식으로 반환하세요:
            {
                "summary": "사건 요약",
                "characters_involved": ["관련된 캐릭터들"],
                "location": "발생 장소",
                "importance": "중요도 (1-5)",
                "emotions": ["주요 감정들"],
                "consequences": ["사건의 결과나 영향"]
            }
            
            텍스트:
            {chunk}
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = await chain.arun(chunk=chunk)
        
        events = self._parse_events_response(response)
        for event in events:
            event['chapter_number'] = chapter_number
            event['timestamp'] = datetime.now()
            # 캐릭터 이름 정규화
            event['characters_involved'] = [
                self.name_resolver.resolve_name(name)
                for name in event['characters_involved']
            ]
        
        return events