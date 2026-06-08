from dotenv import load_dotenv
load_dotenv()

from providers.openai_provider import OpenAIProvider
from agent.loop import run_agent
from metrics.recorder import save_results
from metrics.analysis import extract_metrics


def main():

    print("\n🚀 Running Trajectory-Level Agent Benchmark...\n")

    # ----------------------------------------
    # 1. Initialize provider (OpenAI / GC swap)
    # ----------------------------------------
    provider = OpenAIProvider()

    # ----------------------------------------
    # 2. Run full agent trajectory
    # ----------------------------------------
    results = run_agent(provider)

    # ----------------------------------------
    # 3. Extract metrics (latency, tokens, etc.)
    # ----------------------------------------
    metrics = extract_metrics(results)

    # ----------------------------------------
    # 4. Persist experiment output
    # ----------------------------------------
    output = {
        "raw": results,
        "metrics": metrics
    }

    save_results(output)

    # ----------------------------------------
    # 5. Summary logging
    # ----------------------------------------
    print("\n✅ DONE")
    print(f"Steps: {len(results)}")
    print("Total latency:", metrics["total_latency"])
    print("Avg step latency:", metrics["total_latency"] / len(metrics["step_latency"]))


if __name__ == "__main__":
    main()