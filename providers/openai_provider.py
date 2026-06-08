import time
import os
from openai import OpenAI
from providers.base import LLMProvider
from config import MODEL


class OpenAIProvider(LLMProvider):

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")

        self.client = OpenAI(api_key=api_key)

    def call(self, messages, max_tokens):
        start = time.time()

        resp = self.client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=max_tokens
        )

        latency = time.time() - start

        return {
            "text": resp.choices[0].message.content,
            "latency": latency,
            "prompt_tokens": resp.usage.prompt_tokens,
            "completion_tokens": resp.usage.completion_tokens,
        }