import os

MODEL = "gpt-4o-mini"

# Keep this SMALL for budget safety
STEPS = 5

CONTEXT_SIZES = [500, 1000, 2000, 4000]

OUTPUT_MAX_TOKENS = 80

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
