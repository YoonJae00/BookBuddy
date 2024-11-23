from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

class NovelTextSplitter:
    def __init__(self, chunk_size: int = 2000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", ",", " "]
        )
    
    def split_text(self, text: str) -> List[str]:
        """텍스트를 청크로 분할"""
        return self.splitter.split_text(text)
    
    def split_by_chapters(self, text: str) -> List[str]:
        """챕터 단위로 분할"""
        # 챕터 구분자는 소설 형식에 따라 조정 필요
        chapter_markers = [
            "Chapter", "제", "장", "CHAPTER",
            # 추가 구분자...
        ]
        
        chapters = []
        current_chapter = ""
        
        for line in text.split('\n'):
            if any(marker in line for marker in chapter_markers):
                if current_chapter:
                    chapters.append(current_chapter.strip())
                current_chapter = line + '\n'
            else:
                current_chapter += line + '\n'
        
        if current_chapter:
            chapters.append(current_chapter.strip())
        
        return chapters