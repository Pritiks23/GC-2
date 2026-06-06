from dotenv import load_dotenv
load_dotenv()

from providers.openai_provider import call_llm
from agent.loop import run_agent
from metrics.recorder import save_results
from metrics.analysis import extract_metrics


class ProviderWrapper:
    def __call__(self, messages, max_tokens):
        return call_llm(messages, max_tokens)


def main():
    provider = ProviderWrapper()

    print("\n🚀 Running Structured Agent Benchmark...\n")

    results = run_agent(provider)

    metrics = extract_metrics(results)

    output = {
        "raw": results,
        "metrics": metrics
    }

    save_results(output)

    print("\n✅ DONE")
    print("Total latency:", metrics["total_latency"])


if __name__ == "__main__":
    main()
