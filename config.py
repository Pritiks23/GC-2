# -----------------------
# Experiment parameters
# -----------------------
import os
MODEL = "gpt-4o-mini"

STEPS = 6

BASE_CONTEXT = 800
CONTEXT_GROWTH = 1200

MAX_OUTPUT_TOKENS = 80


# -----------------------
# Provider configuration
# -----------------------
GENERAL_COMPUTE_API_KEY = os.getenv("GENERAL_COMPUTE_API_KEY")
GENERAL_COMPUTE_BASE_URL = "https://api.generalcompute.com"
GENERAL_COMPUTE_MODEL = "minimax-m2.7"