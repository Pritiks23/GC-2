# import json
# import matplotlib.pyplot as plt


# def load(path):
#     with open(path, "r") as f:
#         return json.load(f)


# def main():

#     openai = load("results/openai.json")["metrics"]["step_latency"]
#     gc = load("results/general_compute.json")["metrics"]["step_latency"]

#     plt.plot(openai, marker="o", label="OpenAI")
#     plt.plot(gc, marker="o", label="General Compute")

#     plt.title("Agent Trajectory Latency Comparison")
#     plt.xlabel("Step")
#     plt.ylabel("Latency (s)")
#     plt.legend()

#     plt.show()


# if __name__ == "__main__":
#     main()
import json
import numpy as np
import matplotlib.pyplot as plt


def load(path):
    with open(path, "r") as f:
        return json.load(f)


def main():

    openai = load("results/openai.json")["metrics"]["step_latency"]
    gc = load("results/general_compute.json")["metrics"]["step_latency"]

    steps = np.arange(1, len(openai) + 1)

    # Derived metrics
    openai_cum = np.cumsum(openai)
    gc_cum = np.cumsum(gc)

    openai_growth = np.array(openai) / openai[0]
    gc_growth = np.array(gc) / gc[0]

    delta = np.array(openai) - np.array(gc)

    # Summary stats
    openai_total = np.sum(openai)
    gc_total = np.sum(gc)

    openai_avg = np.mean(openai)
    gc_avg = np.mean(gc)

    # Figure
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    fig.suptitle(
        "Trajectory-Level Latency Dynamics\nGPT-4o-mini vs MiniMax M2",
        fontsize=16,
        fontweight="bold"
    )

    # --------------------------------------------------
    # 1. Per-Step Latency
    # --------------------------------------------------
    axs[0, 0].plot(
        steps,
        openai,
        marker="o",
        linewidth=2,
        label="GPT-4o-mini"
    )

    axs[0, 0].plot(
        steps,
        gc,
        marker="o",
        linewidth=2,
        label="MiniMax M2"
    )

    axs[0, 0].set_title("Per-Step Latency")
    axs[0, 0].set_xlabel("Trajectory Step")
    axs[0, 0].set_ylabel("Latency (s)")
    axs[0, 0].grid(alpha=0.3)
    axs[0, 0].legend()

    # --------------------------------------------------
    # 2. Cumulative Latency
    # --------------------------------------------------
    axs[0, 1].plot(
        steps,
        openai_cum,
        marker="o",
        linewidth=2,
        label="GPT-4o-mini"
    )

    axs[0, 1].plot(
        steps,
        gc_cum,
        marker="o",
        linewidth=2,
        label="MiniMax M2"
    )

    axs[0, 1].set_title("Cumulative Execution Time")
    axs[0, 1].set_xlabel("Trajectory Step")
    axs[0, 1].set_ylabel("Total Time (s)")
    axs[0, 1].grid(alpha=0.3)
    axs[0, 1].legend()

    # --------------------------------------------------
    # 3. Latency Amplification
    # --------------------------------------------------
    axs[1, 0].plot(
        steps,
        openai_growth,
        marker="o",
        linewidth=2,
        label="GPT-4o-mini"
    )

    axs[1, 0].plot(
        steps,
        gc_growth,
        marker="o",
        linewidth=2,
        label="MiniMax M2"
    )

    axs[1, 0].axhline(
        1.0,
        linestyle="--",
        alpha=0.5
    )

    axs[1, 0].set_title("Latency Amplification")
    axs[1, 0].set_xlabel("Trajectory Step")
    axs[1, 0].set_ylabel("Relative to Step 1")
    axs[1, 0].grid(alpha=0.3)
    axs[1, 0].legend()

    # --------------------------------------------------
    # 4. Provider Difference
    # --------------------------------------------------
    axs[1, 1].plot(
        steps,
        delta,
        marker="o",
        linewidth=2
    )

    axs[1, 1].axhline(
        0,
        linestyle="--",
        alpha=0.5
    )

    axs[1, 1].set_title("Latency Difference")
    axs[1, 1].set_xlabel("Trajectory Step")
    axs[1, 1].set_ylabel("OpenAI − General Compute (s)")
    axs[1, 1].grid(alpha=0.3)

    # Text summary box
    summary = (
        f"OpenAI Total: {openai_total:.2f}s\n"
        f"GC Total: {gc_total:.2f}s\n\n"
        f"OpenAI Avg: {openai_avg:.2f}s\n"
        f"GC Avg: {gc_avg:.2f}s\n\n"
        f"Speedup: {openai_total/gc_total:.2f}x"
    )

    fig.text(
        0.83,
        0.15,
        summary,
        fontsize=10,
        bbox=dict(boxstyle="round", alpha=0.15)
    )

    plt.tight_layout(rect=[0, 0, 0.95, 0.95])

    plt.savefig(
        "trajectory_latency_comparison.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


if __name__ == "__main__":
    main()