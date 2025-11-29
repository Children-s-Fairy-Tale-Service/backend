from openai import OpenAI
from core.config import settings


class GPTClient:
    def __init__(self, api_key: str, model: str):
        if not api_key:
            raise RuntimeError("OpenAI API 키가 비어 있습니다. .env 파일을 확인해 주세요.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, messages, temperature: float = 0.7) -> str:
        """
        messages: [{"role": "system" | "user" | "assistant", "content": "..."}, ...]
        """
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip()


gpt_client = GPTClient(
    api_key=settings.OPENAI_API_KEY,
    model=settings.OPENAI_MODEL,
)