# app/api/v1/quiz_routes.py
from fastapi import APIRouter, HTTPException

from schemas.quiz import QuizRequest, QuizResponse, QuizItem
from gpt.quiz_generator import generate_multiple_quizzes_and_answers

router = APIRouter(prefix="/quizzes", tags=["Quiz"])


@router.post("/generation", response_model=QuizResponse)
def create_quizzes(req: QuizRequest):
    if not req.stories and not req.captions:
        raise HTTPException(400, "stories 또는 captions 중 하나는 있어야 합니다.")

    quizzes, answers = generate_multiple_quizzes_and_answers(
        req.stories,
        req.captions,
        req.n_quizzes
    )

    items = [
        QuizItem(quiz=q, answer=a)
        for q, a in zip(quizzes, answers)
    ]

    return QuizResponse(items=items)
