import random

def generate_fake_context(size):
    return "context " * size


def run_context_scaling(provider, context_sizes):
    results = []

    for size in context_sizes:
        context = generate_fake_context(size)

        messages = [
            {
                "role": "user",
                "content": f"""
SYSTEM CONTEXT:
{context}

Task: extract key issues in 3 bullet points.
"""
            }
        ]

        out = provider.generate(messages, max_tokens=120)

        results.append({
            "context_size": size,
            **out
        })

    return results
