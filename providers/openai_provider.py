import time
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def call_llm(messages, max_tokens=80):
    start = time.time()

    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=max_tokens,
    )

    latency = time.time() - start

    usage = resp.usage

    return {
        "text": resp.choices[0].message.content,
        "latency": latency,
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens
    }
