from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Dict, List
from datetime import datetime

class CharacterAnalyzer:
    def __init__(self, name_resolver):
        self.llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
        self.name_resolver = name_resolver
    
    async def analyze_character_in_chunk(
        self, 
        chunk: str, 
        character_name: str,
        chapter_number: int
    ) -> Dict:
        """청크에서 캐릭터 정보 분석"""
        prompt = PromptTemplate(
            input_variables=["chunk", "character_name"],
            template="""
            다음 텍스트에서 '{character_name}'의 정보를 분석하세요.
            JSON 형식으로 다음 정보를 추출하세요:
            {
                "personality_traits": ["발견된 새로운 성격 특성"],
                "speech_patterns": ["특징적인 말투나 표현"],
                "emotions": ["이 장면에서의 감정 상태"],
                "actions": ["주요 행동이나 결정"],
                "relationships": {
                    "character_name": "관계 설명"
                }
            }
            
            텍스트:
            {chunk}
            """
        )
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "chunk": chunk,
            "character_name": character_name
        })
        
        analysis = self._parse_analysis_response(response.content)
        analysis['chapter_number'] = chapter_number
        analysis['timestamp'] = datetime.now()
        
        return analysis
    
    def _parse_analysis_response(self, response: str) -> Dict:
        """LLM 응답을 파싱하여 구조화된 데이터로 변환"""
        try:
            content = response
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            return json.loads(content.strip())
        except json.JSONDecodeError:
            return {
                "personality_traits": [],
                "speech_patterns": [],
                "emotions": [],
                "actions": [],
                "relationships": {}
            }