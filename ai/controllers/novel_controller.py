from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from services.novel_processor import NovelProcessor
from config import get_settings
from models.novel import NovelCreate
from utils.errors import NovelProcessingError, handle_processing_error
from services.database import DatabaseService

router = APIRouter()

@router.post("/novels/")
async def create_novel(
    novel: NovelCreate,
    settings = Depends(get_settings)
):
    """소설 텍스트 처리"""
    try:
        processor = NovelProcessor(settings)
        result = await processor.process_novel(
            title=novel.title,
            content=novel.content,
            author=novel.author
        )
        return result
    except NovelProcessingError as e:
        raise handle_processing_error(e)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@router.get("/novels/search")
async def search_novels(
    title: str,
    settings = Depends(get_settings)
):
    """소설 제목으로 검색"""
    db = DatabaseService()
    novels = db.search_novels_by_title(title)
    return novels

@router.get("/novels")
async def get_all_novels(
    settings = Depends(get_settings)
):
    """소설 전체 목록 조회"""
    db = DatabaseService()
    novels = db.get_all_novels()
    return novels