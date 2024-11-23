from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from typing import List, Dict, Optional

class VectorStore:
    def __init__(self, settings=None):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY if settings else None
        )
        self.db = Chroma(
            embedding_function=self.embeddings,
            persist_directory="./chroma_db"
        )
    
    async def add_event(self, event: Dict):
        """이벤트를 벡터 저장소에 추가"""
        metadata = {
            'event_id': event['id'],
            'chapter_number': event['chapter_number'],
            'characters': event['characters_involved'],
            'importance': event['importance']
        }
        
        self.db.add_texts(
            texts=[event['summary']],
            metadatas=[metadata]
        )
    
    async def search_similar(
        self,
        query: str,
        filter_dict: Optional[Dict] = None,
        k: int = 5
    ) -> List[Dict]:
        """유사한 이벤트 검색"""
        documents = self.db.similarity_search_with_score(
            query,
            k=k,
            filter=filter_dict
        )
        
        return [{
            'content': doc.page_content,
            'metadata': doc.metadata,
            'score': score
        } for doc, score in documents]
    
    def persist(self):
        """벡터 저장소 영구 저장"""
        self.db.persist()