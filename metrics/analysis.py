def compute_cumulative(latencies):
    out = []
    total = 0

    for t in latencies:
        total += t
        out.append(total)

    return out


def extract_metrics(results):
    latencies = [r["latency"] for r in results]
    prompt_tokens = [r["prompt_tokens"] for r in results]

    return {
        "step_latency": latencies,
        "cumulative_latency": compute_cumulative(latencies),
        "prompt_tokens": prompt_tokens,
        "total_latency": sum(latencies)
    }
