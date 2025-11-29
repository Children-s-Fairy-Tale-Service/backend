# app/gpt/quiz_generator.py
from gpt.client import gpt_client


def gpt(conversations):
    return gpt_client.chat(conversations)


def llm_function(system_prompt: str, user_prompt: str, gpt_callable):
    conversations = [{"role": "system", "content": system_prompt}]
    exemplars = user_prompt.split("\n\n\n") if user_prompt else [""]

    for ex in exemplars:
        conversations.append({"role": "user", "content": ex})

    return gpt_callable(conversations)


def generate_multiple_quizzes_and_answers(stories, captions, n_quizzes):
    story_block = "\n".join(stories)
    caption_block = "\n".join(f"- {c}" for c in captions if str(c).strip())

    prompt = (
        f"다음 '동화 줄거리'와 '장면 캡션'을 모두 참고하여, "
        f"6~12세 어린이가 재미있게 맞힐 수 있는 서로 다른 퀴즈 {n_quizzes}개를 만들어 주세요.\n\n"
        "먼저, 동화 줄거리와 장면 캡션을 읽고 다음을 파악하세요:\n"
        "- 주요 등장인물과 그들의 행동\n"
        "- 중요한 사건이나 전환점\n"
        "- 등장인물의 감정이나 의도\n"
        "- 이야기의 교훈이나 메시지\n\n"
        "그 후, 이러한 내용을 바탕으로 어린이가 재미있게 풀 수 있는 퀴즈를 만드세요.\n"
        "퀴즈의 유형은 다음 예시처럼 다양하게 섞어 주세요 (단, 중복되지 않게):\n"
        "- 인물 퀴즈 (누가 ~했나요?)\n"
        "- 사건 퀴즈 (어떤 일이 일어났나요?)\n"
        "- 장소 퀴즈 (어디에서 일어났나요?)\n"
        "- 감정 퀴즈 (이때 주인공은 어떤 기분이었나요?)\n"
        "- 교훈 퀴즈 (이 이야기에서 배울 점은 무엇인가요?)\n"
        "- 관찰 퀴즈 (그림이나 캡션 속에서 무엇이 보이나요?)\n\n"
        "좋은 퀴즈의 기준:\n"
        "- 줄거리나 장면과 직접적으로 관련되어야 함\n"
        "- 어린이의 상상력을 자극하면서도 정답이 명확해야 함\n"
        "- 단어 선택은 쉽고 자연스러워야 함\n"
        "- 너무 긴 문장은 피하고, 질문은 한 문장으로 제한할 것\n\n"
        "📘 출력 형식:\n"
        "퀴즈 1: [퀴즈 내용]\n"
        "정답 1: [정답 내용]\n\n"
        "퀴즈 2: [퀴즈 내용]\n"
        "정답 2: [정답 내용]\n\n"
        f"(이 형식을 퀴즈 {n_quizzes}개 모두 반복)\n\n"
        f"[동화 줄거리]\n{story_block}\n\n"
        f"[장면 캡션]\n{caption_block}\n"
    )

    output = llm_function(prompt, "", gpt)

    quizzes = []
    answers = []

    lines = output.splitlines()
    current_quiz = ""
    current_answer = ""

    for line in lines:
        line = line.strip()
        if line.startswith("퀴즈"):
            if current_quiz and current_answer:
                quizzes.append(current_quiz)
                answers.append(current_answer)
            current_quiz = line.split(":", 1)[1].strip()
            current_answer = ""
        elif line.startswith("정답"):
            current_answer = line.split(":", 1)[1].strip()

    if current_quiz and current_answer:
        quizzes.append(current_quiz)
        answers.append(current_answer)

    while len(quizzes) < n_quizzes:
        quizzes.append("퀴즈 생성 실패")
        answers.append("정답 생성 실패")

    return quizzes[:n_quizzes], answers[:n_quizzes]
