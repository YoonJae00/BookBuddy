from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from services.novel_processor import NovelProcessor
from config import get_settings
from models.novel import NovelCreate
from utils.errors import NovelProcessingError, handle_processing_error

router = APIRouter()

@router.post("/novels/")
async def create_novel(
    novel: NovelCreate,
    settings = Depends(get_settings)
):
    """소설 텍스트 처리"""
    try:
        processor = NovelProcessor(settings)
        result = await processor.process_novel(novel.content)
        return result
    except NovelProcessingError as e:
        raise handle_processing_error(e)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )