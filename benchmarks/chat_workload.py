def run_chat(provider):
    """
    Decode-heavy workload:
    short prompt → longer output
    """

    messages = [
        {
            "role": "user",
            "content": "Explain distributed systems in simple terms."
        }
    ]

    return provider.generate(messages, max_tokens=300)
