import json
import matplotlib.pyplot as plt


def load(path):
    with open(path, "r") as f:
        return json.load(f)


def main():

    openai = load("results/openai.json")["metrics"]["step_latency"]
    gc = load("results/general_compute.json")["metrics"]["step_latency"]

    plt.plot(openai, marker="o", label="OpenAI")
    plt.plot(gc, marker="o", label="General Compute")

    plt.title("Agent Trajectory Latency Comparison")
    plt.xlabel("Step")
    plt.ylabel("Latency (s)")
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main()
