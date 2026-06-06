import time
from openai import OpenAI
from config import GENERAL_COMPUTE_BASE_URL, GENERAL_COMPUTE_MODEL, GENERAL_COMPUTE_API_KEY
from providers.base import LLMProvider

client = OpenAI(
    base_url=GENERAL_COMPUTE_BASE_URL,
    api_key=GENERAL_COMPUTE_API_KEY
)


class GeneralComputeProvider(LLMProvider):

    def call(self, messages, max_tokens):
        start = time.time()

        resp = client.chat.completions.create(
            model=GENERAL_COMPUTE_MODEL,
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
