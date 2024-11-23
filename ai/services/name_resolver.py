from typing import List, Dict
import re

class NameResolver:
    def __init__(self):
        self.character_aliases = {}  # {full_name: set(aliases)}
        self.alias_to_full = {}     # {alias: full_name}
    
    def add_character(self, full_name: str, aliases: List[str]) -> None:
        """캐릭터와 별칭 추가"""
        # 기존 별칭 세트 가져오기 또는 새로 생성
        existing_aliases = self.character_aliases.get(full_name, set())
        
        # 새 별칭 추가
        for alias in aliases:
            existing_aliases.add(alias)
            self.alias_to_full[alias.lower()] = full_name
        
        # full_name도 별칭으로 추가
        existing_aliases.add(full_name)
        self.alias_to_full[full_name.lower()] = full_name
        
        # 업데이트된 별칭 세트 저장
        self.character_aliases[full_name] = existing_aliases
    
    def resolve_name(self, name: str) -> str:
        """별칭을 전체 이름으로 변환"""
        return self.alias_to_full.get(name.lower(), name)
    
    def get_all_characters(self) -> List[str]:
        """등록된 모든 캐릭터의 전체 이름 반환"""
        return list(self.character_aliases.keys())