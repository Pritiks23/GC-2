import json
import os

RESULTS_PATH = "results/results.json"


def save_run(data):
    os.makedirs("results", exist_ok=True)

    with open(RESULTS_PATH, "w") as f:
        json.dump(data, f, indent=2)
