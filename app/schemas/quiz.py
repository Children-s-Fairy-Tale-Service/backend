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
