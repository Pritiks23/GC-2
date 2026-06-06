from dotenv import load_dotenv
load_dotenv()

from providers.openai_provider import call_openai
from benchmarks.context_scaling import run_context_scaling
from metrics.recorder import save_run
from metrics.amplification import compute_amplification, compute_context_amplification
from config import CONTEXT_SIZES


class OpenAIWrapper:
    def generate(self, messages, max_tokens):
        return call_openai(messages, max_tokens=max_tokens)


def main():
    provider = OpenAIWrapper()

    print("\n🚀 Running TrajectoryBench...\n")

    # ---------------------------
    # 1. Context scaling test
    # ---------------------------
    context_results = run_context_scaling(provider, CONTEXT_SIZES)

    # ---------------------------
    # 2. Agent-style trajectory (lightweight simulation)
    # ---------------------------
    messages = [{"role": "user", "content": "Debug a distributed training failure step by step."}]

    step_results = []

    for i in range(5):
        out = provider.generate(messages, max_tokens=80)

        step_results.append(out)

        messages.append({"role": "assistant", "content": out["text"]})
        messages.append({"role": "user", "content": "continue"})

    # ---------------------------
    # Metrics
    # ---------------------------
    step_times = [r["latency"] for r in step_results]
    prompt_tokens = [r["prompt_tokens"] for r in step_results]

    result = {
        "context_scaling": context_results,
        "trajectory": step_results,
        "trajectory_amplification": compute_amplification(step_times),
        "context_amplification": compute_context_amplification(prompt_tokens),
        "total_latency": sum(step_times)
    }

    save_run(result)

    print("\n✅ DONE")
    print("Trajectory amplification:", result["trajectory_amplification"])
    print("Context amplification:", result["context_amplification"])
    print("Total latency:", result["total_latency"])


if __name__ == "__main__":
    main()
