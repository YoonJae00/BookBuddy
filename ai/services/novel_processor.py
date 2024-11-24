from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Dict, List
from services.name_resolver import NameResolver
from utils.vector_store import VectorStore
import json
from datetime import datetime
from services.character_analyzer import CharacterAnalyzer
from utils.text_splitter import NovelTextSplitter
from utils.logger import NovelLogger
from utils.errors import NovelProcessingError
from services.database import DatabaseService
import uuid
import re

class NovelProcessor:
    def __init__(self, settings):
        self.settings = settings
        self.name_resolver = NameResolver()
        self.logger = NovelLogger()
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4o-mini",
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vector_store = VectorStore(settings)
        self.text_splitter = NovelTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
    
    async def process_novel(self, title: str, content: str, author: str) -> Dict:
        """소설 전체 처리"""
        try:
            self.logger.log_processing_start("Novel Processing")
            
            # 소설 ID 생성
            novel_id = str(uuid.uuid4())
            
            # DB에 소설 정보 저장 (동기식)
            db = DatabaseService()
            db.save_novel(novel_id, title, content, author) # 굳이 저장을 해야할까??
            
            # 1. 초기 캐릭터 식별
            characters = await self._identify_characters(content, novel_id)
            if not characters:
                raise NovelProcessingError("No characters found in the novel")
            
            for char in characters:
                self.name_resolver.add_character(char['full_name'], char['aliases'])
                self.logger.log_character_found(char['full_name'], char)
                
                # 캐릭터 정보 저장 (동기식)
                db.save_character({
                    'id': str(uuid.uuid4()),
                    'novel_id': novel_id,
                    **char
                })
            
            # 2. 텍스트 분할
            chunks = self.text_splitter.split_text(content)
            if not chunks:
                raise NovelProcessingError("Failed to split text into chunks")
            
            # 3. 각 청크 처리
            all_events = []
            for i, chunk in enumerate(chunks):
                try:
                    normalized_chunk = self._normalize_names(chunk)
                    events = await self._extract_events(normalized_chunk, i)
                    for event in events:
                        # 이벤트 저장 (동기식)
                        event['id'] = str(uuid.uuid4())
                        event['novel_id'] = novel_id
                        db.save_event(event)
                        self.logger.log_event_extracted(event['summary'], i)
                    all_events.extend(events)
                except Exception as e:
                    self.logger.log_error(f"Error processing chunk {i}", {"error": str(e)})
                    continue
            
            if not all_events:
                self.logger.log_error("No events extracted from the novel")
            
            result = {
                "characters": characters,
                "events": all_events
            }
            
            return {
                "novel_id": novel_id,
                "title": title,
                "author": author,
                **result
            }
            
        except Exception as e:
            self.logger.log_error("Novel processing failed", {"error": str(e)})
            raise NovelProcessingError("Failed to process novel", {"error": str(e)})
    
    def _normalize_names(self, text: str) -> str:
        """텍스트 내의 모든 캐릭터 이름을 정규화"""
        words = text.split()
        normalized_words = []
        
        for word in words:
            # 이름이면 전체 이름으로 변환
            full_name = self.name_resolver.resolve_name(word)
            normalized_words.append(full_name)
        
        return ' '.join(normalized_words)
    
    async def _identify_characters(self, content: str, novel_id: str) -> List[Dict]:
        try:
            # 1. 먼저 기본적인 캐릭터 추출
            initial_characters = await self._extract_characters_from_events(content)
            if not initial_characters:
                self.logger.log_error("No initial characters found")
                return []
            
            # 2. 각 캐릭터에 대해 상세 분석
            enriched_characters = []
            chunks = [content[i:i+3000] for i in range(0, len(content), 2500)]
            
            for char in initial_characters:
                char_info = await self._analyze_single_character(char["full_name"], chunks[:5])
                if char_info:
                    enriched_characters.append(char_info)
            
            if not enriched_characters:
                self.logger.log_error("No enriched characters found")
                return [{
                    "full_name": "주인공",
                    "aliases": ["그", "그는"],
                    "initial_description": "소설의 주인공",
                    "personality": {"traits": ["미상"], "values": ["미상"], 
                                  "motivations": ["미상"], "fears": ["미상"]},
                    "background": {"origin": "미상", "occupation": "미상", "skills": []},
                    "story_role": "주인공",
                    "relationships": []
                }]
            
            return enriched_characters
            
        except Exception as e:
            self.logger.log_error(f"Failed to identify characters: {str(e)}")
            raise NovelProcessingError(f"Failed to identify characters: {str(e)}")
    
    async def _extract_characters_from_events(self, content: str) -> List[Dict]:
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            다음 텍스트에서 실제 등장인물만을 찾아 JSON 형식으로 반환하세요.
            대명사나 일반 명사가 아닌 실제 캐릭터만 추출하세요.

            예시:
            - "그", "그녀", "나", "너" 같은 대명사는 제외
            - "사람들", "누군가" 같은 불특정 명사는 제외
            - "청년", "소녀" 같은 일반 명사는 구체적인 캐릭터를 지칭할 때만 포함

            반드시 다음 형식으로 반환해주세요:
            {{
                "characters": [
                    {{
                        "full_name": "캐릭터의 실제 이름",
                        "aliases": ["다른 호칭이나 별명"],
                        "initial_description": "캐릭터 설명",
                        "role": "역할 (예: 주인공, 적대자 등)"
                    }}
                ]
            }}
            
            텍스트:
            {text}
            """
        )
        
        try:
            chunks = [content[i:i+3000] for i in range(0, len(content), 2500)]
            all_characters = {}
            
            for chunk in chunks[:5]:
                chain = prompt | self.llm
                response = await chain.ainvoke({"text": chunk})
                
                try:
                    content = response.content.strip()
                    if '```json' in content:
                        content = content.split('```json')[1].split('```')[0]
                    
                    result = json.loads(content)
                    if "characters" in result:
                        for char in result["characters"]:
                            name = char["full_name"]
                            if name not in all_characters:
                                all_characters[name] = char
                            else:
                                # 기존 정보와 병합
                                self._merge_character_info(all_characters[name], char)
                
                except json.JSONDecodeError:
                    self.logger.log_error(f"Failed to parse characters from chunk")
                    continue
            
            return list(all_characters.values())
            
        except Exception as e:
            self.logger.log_error(f"Error extracting characters: {str(e)}")
            return []
    
    def _merge_character_info(self, existing: Dict, new: Dict) -> None:
        """캐릭터 정보 스마트 병합"""
        # 병합 로직 비활성화
        return new  # 새로운 데이터만 반환
    
    def _try_partial_parsing(self, content: str, all_characters: Dict) -> None:
        """부분적 파싱 시도"""
        # 파싱 실패 시 부분적으로 파싱 시도
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            current_obj = line
            
            try:
                # 전체 객체를 파싱 시도
                data = json.loads(current_obj)
                
                # 중첩된 객체 처리
                if isinstance(data, dict):
                    if 'full_name' in data:  # 단일 캐릭터
                        all_characters[data['full_name']] = data
                    else:  # 여러 캐릭터가 포함된 객체
                        for char_data in data.values():
                            if isinstance(char_data, dict) and 'full_name' in char_data:
                                char_data.setdefault('aliases', [])
                                char_data.setdefault('initial_description', '')
                                all_characters[char_data['full_name']] = char_data
                current_obj = ""
            except json.JSONDecodeError:
                continue
    
    def _parse_character_response(self, response: str) -> List[Dict]:
        """LLM 응답을 파싱하여 캐릭터 정보로 변환"""
        try:
            # 응답 문자열을 여러 JSON 객체로 분리
            json_objects = []
            current_obj = ""
            for line in response.split('\n'):
                line = line.strip()
                if not line:
                    continue
                current_obj += line
                
                try:
                    # 전체 객체를 파싱 시도
                    data = json.loads(current_obj)
                    
                    # 중첩된 객체 처리
                    if isinstance(data, dict):
                        if 'full_name' in data:  # 단일 캐릭터
                            json_objects.append(data)
                        else:  # 여러 캐릭터가 포함된 객체
                            for char_data in data.values():
                                if isinstance(char_data, dict) and 'full_name' in char_data:
                                    char_data.setdefault('aliases', [])
                                    char_data.setdefault('initial_description', '')
                                    json_objects.append(char_data)
                    current_obj = ""
                except json.JSONDecodeError:
                    continue
            
            return json_objects
        except Exception as e:
            print(f"Error processing response: {str(e)}")
            print(f"Response: {response}")
            return []
    
    async def _extract_events(self, chunk: str, chapter_number: int) -> List[Dict]:
        """청크에서 이벤트 추출"""
        prompt = PromptTemplate(
            input_variables=["chunk"],
            template="""
            다음 텍스트에서 주요 사건들을 추출하세요.
            각 사건에 대해 다음 정보를 JSON 형식으로 반환하세요:
            {{
                "summary": "사건 요약",
                "characters_involved": ["관련된 캐릭터들"],
                "location": "발생 장소",
                "importance": "중요도 (1-5)",
                "emotions": ["주요 감정들"],
                "consequences": ["사건의 결과나 영향"]
            }}
            
            텍스트:
            {chunk}
            
            JSON 형식으로만 응답하세요. 마크다운이나 다른 포맷을 사용하지 마세요.
            """
        )
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"chunk": chunk})
        
        try:
            # 마크다운 포맷 제거
            content = response.content
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            
            events = json.loads(content.strip())
            if not isinstance(events, list):
                events = [events]
            
            for event in events:
                event['chapter_number'] = chapter_number
                event['timestamp'] = datetime.now()
            
            return events
        except json.JSONDecodeError as e:
            print(f"Failed to parse events response: {response.content}")
            print(f"JSON Error: {str(e)}")
            return []
    
    async def _update_character_info(self, chunk: str) -> None:
        """청크에서 캐릭터 정보 업데이트"""
        # 현재 등록된 모든 캐릭터에 대해 분석
        for character_name in self.name_resolver.get_all_characters():
            try:
                # 캐릭터 분석기 생성
                analyzer = CharacterAnalyzer(self.name_resolver)
                
                # 캐릭터 정보 분석
                analysis = await analyzer.analyze_character_in_chunk(
                    chunk=chunk,
                    character_name=character_name,
                    chapter_number=0  # 필요한 경우 chapter_number 전달
                )
                
                # TODO: 분석 결과를 데이터베이스에 저장
                # 현재는 로깅만 수행
                print(f"Updated info for {character_name}: {analysis}")
                
            except Exception as e:
                print(f"Error updating character info for {character_name}: {str(e)}")
                continue
    
    async def _analyze_single_character(self, character_name: str, chunks: List[str]) -> Dict:
        """단일 캐릭터 상세 분석"""
        try:
            prompt = PromptTemplate(
                input_variables=["text", "character_name"],
                template="""
                다음 텍스트에서 '{character_name}'에 대한 정보를 상세히 분석하여 JSON 형식으로 반환하세요:
                
                {{
                    "full_name": "{character_name}",
                    "aliases": ["다른 호칭이나 별명"],
                    "initial_description": "캐릭터 설명",
                    "personality": {{
                        "traits": ["성격 특성들"],
                        "values": ["가치관들"],
                        "motivations": ["동기들"],
                        "fears": ["두려움들"]
                    }},
                    "background": {{
                        "origin": "출신 배경",
                        "occupation": "직업",
                        "skills": ["보유 기술들"]
                    }},
                    "story_role": "스토리에서의 역할",
                    "relationships": []
                }}
                
                텍스트:
                {text}
                """
            )
            
            combined_info = None
            for chunk in chunks:
                chain = prompt | self.llm
                response = await chain.ainvoke({
                    "text": chunk,
                    "character_name": character_name
                })
                
                try:
                    content = response.content.strip()
                    if '```json' in content:
                        content = content.split('```json')[1].split('```')[0]
                    
                    char_info = json.loads(content)
                    if not combined_info:
                        combined_info = char_info
                    else:
                        self._merge_character_info(combined_info, char_info)
                    
                except json.JSONDecodeError:
                    self.logger.log_error(f"Failed to parse character info for {character_name}")
                    continue
                
            return combined_info
            
        except Exception as e:
            self.logger.log_error(f"Error analyzing character {character_name}: {str(e)}")
            return None