import json
from config import STEPS, BASE_CONTEXT, CONTEXT_GROWTH, MAX_OUTPUT_TOKENS
from agent.prompts import SYSTEM_PROMPT


def build_context(step, previous_actions):
    """
    Controlled context growth (this is your experimental variable)
    """

    context_size = BASE_CONTEXT + step * CONTEXT_GROWTH

    fake_context = "system_memory " * context_size

    observation_trace = "\n".join(previous_actions)

    return f"""
SYSTEM CONTEXT:
{fake_context}

AGENT HISTORY:
{observation_trace}

TASK:
Debug a distributed training failure step by step.
"""


def run_agent(provider):
    messages = []
    history = []
    results = []

    for step in range(STEPS):

        prompt = build_context(step, history)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]

        out = provider(messages, MAX_OUTPUT_TOKENS)

        results.append(out)

        # agent “action memory”
        history.append(out["text"])

    return results
