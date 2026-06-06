import json
import matplotlib.pyplot as plt


def load():
    with open("results/results.json", "r") as f:
        return json.load(f)


def plot_step_latency(data):
    y = data["metrics"]["step_latency"]

    plt.plot(range(len(y)), y, marker="o")
    plt.title("Agent Step Latency")
    plt.xlabel("Step")
    plt.ylabel("Latency (s)")
    plt.show()


def plot_cumulative_latency(data):
    y = data["metrics"]["cumulative_latency"]

    plt.plot(range(len(y)), y, marker="o")
    plt.title("Cumulative Agent Latency (Trajectory Cost)")
    plt.xlabel("Step")
    plt.ylabel("Total Latency (s)")
    plt.show()


def plot_prompt_growth(data):
    y = data["metrics"]["prompt_tokens"]

    plt.plot(range(len(y)), y, marker="o")
    plt.title("Context Growth (Prompt Tokens)")
    plt.xlabel("Step")
    plt.ylabel("Tokens")
    plt.show()


if __name__ == "__main__":
    data = load()

    plot_step_latency(data)
    plot_cumulative_latency(data)
    plot_prompt_growth(data)
