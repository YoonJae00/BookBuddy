import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from controllers import novel_controller, character_controller, chat_controller
from dotenv import load_dotenv

load_dotenv()

from langchain_teddynote import logging

# 프로젝트 이름을 입력합니다.
logging.langsmith("novel-character-chatbot")

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 기본 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Novel Character Chatbot API",
        version="1.0.0",
        description="API for processing novels and chatting with characters",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 라우터 등록
app.include_router(novel_controller.router, prefix="/api/v1")
app.include_router(character_controller.router, prefix="/api/v1")
app.include_router(chat_controller.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Novel Chatbot API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)