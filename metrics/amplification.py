def compute_amplification(step_times):
    if not step_times:
        return 0

    return sum(step_times) / step_times[0]


def compute_context_amplification(prompt_tokens):
    if not prompt_tokens:
        return 0

    return prompt_tokens[-1] / prompt_tokens[0]
