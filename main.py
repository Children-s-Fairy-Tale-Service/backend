from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.quiz_routes import router as quiz_router
app = FastAPI(
    title="FairyTale Service API",
    version="0.1.0",
)

origins = [
    "https://children-fairytale.vercel.app",
    "http://localhost:5173",  # React 기본 포트
    "http://127.0.0.1:5173",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, PUT, DELETE 전부 허용
    allow_headers=["*"],   # Authorization 포함 모든 헤더 허용
)

app.include_router(quiz_router)

# 헬스 체크용
@app.get("/")
def health_check():
    return {"status": "ok"}

