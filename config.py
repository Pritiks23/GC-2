import os

MODEL = "gpt-4o-mini"

STEPS = 6

# THIS is your controlled scaling lever
BASE_CONTEXT = 800  # tokens (simulated size unit)

CONTEXT_GROWTH = 1200  # per step increase

MAX_OUTPUT_TOKENS = 80

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GENERAL_COMPUTE_API_KEY = os.getenv("GENERAL_COMPUTE_API_KEY")
GENERAL_COMPUTE_BASE_URL = "https://api.generalcompute.com"
GENERAL_COMPUTE_MODEL = "minimax-m2.7"
