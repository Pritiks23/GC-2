from openai import OpenAI
import time
from config import OPENAI_API_KEY, MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def call_openai(messages, max_tokens=100):
    start = time.time()

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=max_tokens
    )

    latency = time.time() - start

    usage = response.usage

    return {
        "text": response.choices[0].message.content,
        "latency": latency,
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
    }
