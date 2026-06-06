from dotenv import load_dotenv
load_dotenv()

import json
from agent.loop import run_agent
from metrics.analysis import extract_metrics
from metrics.recorder import save_results

from providers.openai_provider import OpenAIProvider
from providers.general_compute_provider import GeneralComputeProvider


def run_experiment(provider, name):
    print(f"\n🚀 Running {name}...\n")

    results = run_agent(provider)
    metrics = extract_metrics(results)

    output = {
        "raw": results,
        "metrics": metrics
    }

    path = f"results/{name}.json"
    save_results_to_path(output, path)

    return metrics


def save_results_to_path(data, path):
    import os
    os.makedirs("results", exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def main():

    openai_metrics = run_experiment(OpenAIProvider(), "openai")
    gc_metrics = run_experiment(GeneralComputeProvider(), "general_compute")

    print("\n✅ DONE BOTH EXPERIMENTS")

    print("OpenAI:", openai_metrics["total_latency"])
    print("GC:", gc_metrics["total_latency"])


if __name__ == "__main__":
    main()
