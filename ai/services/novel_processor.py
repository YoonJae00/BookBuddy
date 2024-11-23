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
    
    async def process_novel(self, content: str) -> Dict:
        """소설 전체 처리"""
        try:
            self.logger.log_processing_start("Novel Processing")
            
            # 1. 초기 캐릭터 식별
            characters = await self._identify_characters(content)
            if not characters:
                raise NovelProcessingError("No characters found in the novel")
            
            for char in characters:
                self.name_resolver.add_character(char['full_name'], char['aliases'])
                self.logger.log_character_found(char['full_name'], char)
            
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
                        self.logger.log_event_extracted(event['summary'], i)
                    all_events.extend(events)
                    await self._update_character_info(normalized_chunk)
                except Exception as e:
                    self.logger.log_error(f"Error processing chunk {i}", {"error": str(e)})
                    continue
            
            if not all_events:
                self.logger.log_error("No events extracted from the novel")
            
            result = {
                "characters": characters,
                "events": all_events
            }
            
            # DB에 저장
            novel_id = str(uuid.uuid4())
            db = DatabaseService()
            await db.save_novel_analysis(novel_id, result)
            
            return {
                "novel_id": novel_id,
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
    
    async def _identify_characters(self, content: str) -> List[Dict]:
        """초기 캐릭터 식별"""
        character_prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            다음 소설 텍스트에서 등장하는 캐릭터들을 찾아서 JSON 형식으로 반환하세요.
            
            예시 형식:
            [
                {
                    "full_name": "청년",
                    "aliases": ["그", "그는"],
                    "initial_description": "갑옷을 입은 청년"
                }
            ]
            
            텍스트:
            {text}
            """
        )
        
        try:
            # 텍스트 분할 (더 작은 청크로)
            chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
            all_characters = {}
            
            for chunk in chunks[:2]:  # 처음 2개 청크만 처리
                try:
                    chain = character_prompt | self.llm
                    response = await chain.ainvoke({"text": chunk})
                    
                    # JSON 파싱
                    try:
                        chars = json.loads(response.content.strip())
                        if isinstance(chars, list):
                            for char in chars:
                                if char.get('full_name'):
                                    name = char['full_name']
                                    if name not in all_characters:
                                        all_characters[name] = {
                                            "full_name": name,
                                            "aliases": char.get('aliases', []),
                                            "initial_description": char.get('initial_description', '')
                                        }
                    except json.JSONDecodeError:
                        self.logger.log_error(f"JSON parsing error for chunk", {"response": response.content})
                        continue
                        
                except Exception as e:
                    self.logger.log_error(f"Error processing chunk", {"error": str(e)})
                    continue
            
            characters = list(all_characters.values())
            
            # 최소한 하나의 캐릭터는 있어야 함
            if not characters:
                # 기본 캐릭터 생성
                default_character = {
                    "full_name": "주인공",
                    "aliases": ["그", "그는"],
                    "initial_description": "소설의 주인공"
                }
                characters = [default_character]
                self.logger.log_error("No characters found, using default character")
            
            return characters
            
        except Exception as e:
            self.logger.log_error("Character identification failed", {"error": str(e)})
            # 기본 캐릭터로 진행
            return [{
                "full_name": "주인공",
                "aliases": ["그", "그는"],
                "initial_description": "소설의 주인공"
            }]
    
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