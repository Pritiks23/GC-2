import time
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL
from providers.base import LLMProvider

client = OpenAI(api_key=OPENAI_API_KEY)


class OpenAIProvider(LLMProvider):

    def call(self, messages, max_tokens):
        start = time.time()

        resp = client.chat.completions.create(
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
