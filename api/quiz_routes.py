# app/api/v1/quiz_routes.py
from fastapi import APIRouter, HTTPException

from schemas.quiz import (
    QuizRequest,
    QuizResponse,
    QuizItem,
    QuizEvaluationRequest,
    QuizEvaluationResponse,
)
from gpt.quiz_generator import generate_multiple_quizzes_and_answers
from gpt.embedding_evaluator import evaluate_with_embedding

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


@router.post("/evaluate-embedding", response_model=QuizEvaluationResponse)
def evaluate_quiz_with_embedding(req: QuizEvaluationRequest):
    """
    GPT 임베딩(text-embedding-3-small)을 이용해 정답과 사용자 답변의
    의미 유사도를 계산하고, 일정 기준 이상이면 정답으로 처리.
    """
    similarity, is_correct = evaluate_with_embedding(
        correct_answer=req.correct_answer,
        user_answer=req.user_answer,
    )

    # 간단한 피드백 문구
    if is_correct:
        if similarity > 0.75:
            feedback = "정답이에요! 아주 잘 맞췄어요 🎉"
        else:
            feedback = "정답이에요!😊"
    else:
        feedback = "아쉬워요, 이번에는 조금 달라요. 정답을 한 번 더 읽어볼까요? 🧐"

    return QuizEvaluationResponse(
        is_correct=is_correct,
        similarity=similarity,
        feedback=feedback,
    )