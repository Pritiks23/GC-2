import os

MODEL = "gpt-4o-mini"

STEPS = 6

# THIS is your controlled scaling lever
BASE_CONTEXT = 800  # tokens (simulated size unit)

CONTEXT_GROWTH = 1200  # per step increase

MAX_OUTPUT_TOKENS = 80

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
