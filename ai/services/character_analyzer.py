from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Dict, List
from datetime import datetime
import json
from copy import deepcopy

class CharacterAnalyzer:
    def __init__(self, name_resolver, db_service):
        self.llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
        self.name_resolver = name_resolver
        self.db = db_service
        
    async def analyze_character_in_chunk(
        self, 
        chunk: str, 
        character_name: str,
        novel_id: str,
        chapter_number: int
    ) -> Dict:
        """청크에서 캐릭터 정보 분석 (이전 정보 고려)"""
        # 기존 캐릭터 정보 조회
        existing_info = self.db.get_character_by_name_and_novel(character_name, novel_id)
        
        prompt = PromptTemplate(
            input_variables=["chunk", "character_name", "existing_info"],
            template="""
            이전에 파악된 캐릭터 정보:
            {existing_info}
            
            위 정보를 기반으로, 다음 텍스트에서 '{character_name}'의 추가적인 정보나 변화를 분석하세요.
            
            JSON 형식으로 다음 정보를 추출하세요:
            {
                "personality": {
                    "traits": ["성격 특성 (새로 발견되거나 변화된)"],
                    "values": ["가치관 (새로 발견되거나 변화된)"],
                    "motivations": ["동기 (새로 발견되거나 변화된)"],
                    "fears": ["두려움 (새로 발견되거나 변화된)"]
                },
                "relationships": {
                    "character_name": {
                        "type": "관계 유형",
                        "description": "관계 설명",
                        "changes": "관계 변화"
                    }
                },
                "development": {
                    "changes": ["성격/태도 변화"],
                    "events": ["변화를 일으킨 사건"]
                }
            }
            
            텍스트:
            {chunk}
            """
        )
        
        # 분석 실행
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "chunk": chunk,
            "character_name": character_name,
            "existing_info": json.dumps(existing_info, ensure_ascii=False) if existing_info else "{}"
        })
        
        # 새로운 정보와 기존 정보 병합
        new_analysis = self._parse_analysis_response(response.content)
        merged_info = self._merge_character_info(existing_info, new_analysis)
        
        # 업데이트된 정보 저장
        self.db.update_character(
            character_name=character_name,
            novel_id=novel_id,
            updated_info=merged_info
        )
        
        return merged_info

    def _merge_character_info(self, existing: Dict, new: Dict) -> Dict:
        """기존 정보와 새로운 정보를 병합"""
        if not existing:
            return new
            
        result = deepcopy(existing)
        
        # 성격 특성 병합
        if 'personality' in new:
            for key in ['traits', 'values', 'motivations', 'fears']:
                if key in new['personality']:
                    result['personality'][key] = list(set(
                        result['personality'].get(key, []) + new['personality'][key]
                    ))
        
        # 관계 정보 업데이트
        if 'relationships' in new:
            for char_name, rel_info in new['relationships'].items():
                if char_name in result['relationships']:
                    result['relationships'][char_name].update(rel_info)
                else:
                    result['relationships'][char_name] = rel_info
        
        # 발전 과정 추가
        if 'development' in new:
            if 'development' not in result:
                result['development'] = []
            result['development'].append({
                'changes': new['development']['changes'],
                'events': new['development']['events'],
                'chapter_number': new.get('chapter_number'),
                'timestamp': datetime.now()
            })
        
        return result

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