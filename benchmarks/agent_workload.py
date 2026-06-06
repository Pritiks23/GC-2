from config import OUTPUT_MAX_TOKENS

BASE_SYSTEM = """
You are an agent.

Return ONLY JSON tool calls like:
{"tool": "...", "query": "..."}
"""


def run_agent(provider):
    """
    Prefill-heavy workload:
    large context → small structured output
    """

    state = BASE_SYSTEM + "\nTask: debug a distributed training failure"

    messages = [{"role": "user", "content": state}]

    result = []

    for i in range(5):
        out = provider.generate(messages, max_tokens=OUTPUT_MAX_TOKENS)

        result.append(out)

        messages.append({"role": "assistant", "content": out["text"]})
        messages.append({"role": "user", "content": "continue"})

    return result
