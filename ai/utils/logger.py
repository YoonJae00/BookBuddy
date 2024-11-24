import logging
from datetime import datetime

class NovelLogger:
    def __init__(self):
        self.logger = logging.getLogger('novel_processor')
        self.logger.setLevel(logging.INFO)
        
        # 파일 핸들러 설정
        fh = logging.FileHandler('novel_processor.log')
        fh.setLevel(logging.INFO)
        
        # 포맷터 설정
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        # 핸들러 추가
        if not self.logger.handlers:
            self.logger.addHandler(fh)
    
    def log_error(self, message: str, details: dict = None):
        if details:
            self.logger.error(f"Error: {message}, details: {details}")
        else:
            self.logger.error(f"Error: {message}")
    
    def log_processing_start(self, message: str):
        self.logger.info(f"Started processing novel: {message}")
    
    def log_character_found(self, name: str, details: dict):
        self.logger.info(f"Found character: {name}, details: {details}")
    
    def log_event_extracted(self, event: str, chapter: int):
        self.logger.info(f"Extracted event from chapter {chapter}: {event}")