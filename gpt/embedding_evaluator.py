# app/gpt/embedding_evaluator.py
from typing import List
from math import sqrt

from openai import OpenAI
from core.config import settings


# OpenAI 클라이언트 (Chat이 아니라 Embedding용으로도 사용)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

EMBEDDING_MODEL = "text-embedding-3-small"


def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    두 벡터 사이의 코사인 유사도 계산 (numpy 없이 순수 파이썬)
    """
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0

    dot = 0.0
    norm1 = 0.0
    norm2 = 0.0

    for a, b in zip(vec1, vec2):
        dot += a * b
        norm1 += a * a
        norm2 += b * b

    denom = sqrt(norm1) * sqrt(norm2)
    if denom == 0:
        return 0.0

    return dot / denom


def _get_embedding(text: str) -> List[float]:
    """
    단일 문자열에 대한 임베딩 벡터를 반환.
    """
    # OpenAI 1.x 스타일
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return resp.data[0].embedding


def evaluate_with_embedding(correct_answer: str, user_answer: str):
    """
    정답(모범답안)과 사용자 답변을 임베딩 후 코사인 유사도로 비교.
    반환: (similarity, is_correct)
    """
    if not correct_answer or not user_answer:
        return 0.0, False

    emb_correct = _get_embedding(correct_answer)
    emb_user = _get_embedding(user_answer)

    sim = _cosine_similarity(emb_correct, emb_user)  # -1 ~ 1 사이

    # 보통 임베딩 유사도는 0.0 ~ 1.0 근처에서 나오므로 그대로 사용
    similarity = sim

    # ✅ 임계값(threshold)은 나중에 조절 가능
    #   - 0.80 이상: 정답
    #   - 0.65~0.80: 애매하지만 일단 정답 처리할지 고민
    #   - 0.65 미만: 오답
    is_correct = similarity >= 0.65

    return similarity, is_correct
