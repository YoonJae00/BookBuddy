import logging
from datetime import datetime
from typing import Dict, Any
import traceback

class NovelLogger:
    def __init__(self):
        self.logger = logging.getLogger("novel_processor")
        self.logger.setLevel(logging.INFO)
        
        # 파일 핸들러 설정
        fh = logging.FileHandler("novel_processor.log")
        fh.setLevel(logging.INFO)
        
        # 포맷터 설정
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        
        self.logger.addHandler(fh)
    
    def log_processing_start(self, novel_title: str):
        self.logger.info(f"Started processing novel: {novel_title}")
    
    def log_character_found(self, character_name: str, details: Dict[str, Any]):
        self.logger.info(
            f"Found character: {character_name}, details: {details}"
        )
    
    def log_event_extracted(self, event_summary: str, chapter: int):
        self.logger.info(
            f"Extracted event from chapter {chapter}: {event_summary}"
        )
    
    def log_error(self, error_message: str, details: Dict[str, Any] = None):
        error_details = details or {}
        if isinstance(details, Exception):
            error_details = {
                "error_type": type(details).__name__,
                "error_message": str(details),
                "traceback": traceback.format_exc()
            }
        self.logger.error(
            f"Error: {error_message}",
            extra={"details": error_details}
        )