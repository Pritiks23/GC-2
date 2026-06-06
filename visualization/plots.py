import matplotlib.pyplot as plt


def plot_latency(results):
    steps = list(range(len(results)))
    latencies = [r["latency"] for r in results]

    plt.plot(steps, latencies)
    plt.title("Step Latency")
    plt.xlabel("Step")
    plt.ylabel("Latency (s)")
    plt.show()


def plot_context_scaling(results):
    x = [r["context_size"] for r in results]
    y = [r["latency"] for r in results]

    plt.plot(x, y)
    plt.title("Context Size vs Latency")
    plt.xlabel("Context Tokens (scaled)")
    plt.ylabel("Latency (s)")
    plt.show()
