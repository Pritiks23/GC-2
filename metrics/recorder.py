import os
import json

def save_results(data):
    os.makedirs("results", exist_ok=True)

    with open("results/results.json", "w") as f:
        json.dump(data, f, indent=2)
