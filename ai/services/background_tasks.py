from celery import Celery
from typing import Dict, List
import asyncio
from services.novel_processor import NovelProcessor
from services.database import DatabaseService
from utils.logger import NovelLogger

celery_app = Celery('novel_processor', broker='redis://localhost:6379/1')

@celery_app.task
def process_novel_background(novel_data: Dict):
    """소설 처리 백그라운드 작업"""
    try:
        # 비동기 함수를 동기적으로 실행
        loop = asyncio.get_event_loop()
        processor = NovelProcessor()
        result = loop.run_until_complete(
            processor.process_novel(novel_data['content'])
        )
        
        # 처리 결과 저장
        db = DatabaseService()
        loop.run_until_complete(
            db.update_novel_status(
                novel_data['id'],
                'completed',
                result
            )
        )
        
    except Exception as e:
        # 에러 처리
        logger = NovelLogger()
        logger.log_error(
            "Novel processing failed",
            {"novel_id": novel_data['id'], "error": str(e)}
        )
        
        db = DatabaseService()
        loop.run_until_complete(
            db.update_novel_status(
                novel_data['id'],
                'error',
                {"error": str(e)}
            )
        )