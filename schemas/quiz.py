# app/schemas/quiz.py
from typing import List
from pydantic import BaseModel, conint


class QuizRequest(BaseModel):
    stories: List[str]
    captions: List[str]
    n_quizzes: conint(ge=1, le=20) = 3


class QuizItem(BaseModel):
    quiz: str
    answer: str


class QuizResponse(BaseModel):
    items: List[QuizItem]


class QuizEvaluationRequest(BaseModel):
    quiz: str           # 문제(문맥용, 임베딩에는 안 써도 됨, 원하면 써도 됨)
    correct_answer: str # 모범 답안
    user_answer: str    # 아이가 쓴 답


# 🔹 정답 채점 응답
class QuizEvaluationResponse(BaseModel):
    is_correct: bool
    similarity: float   # 0.0 ~ 1.0 사이 유사도
    feedback: str       # 아이에게 보여줄 간단한 설명
