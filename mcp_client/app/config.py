
import os
from dotenv import load_dotenv

load_dotenv()

CLAUDE_MODEL = os.getenv(
    "CLAUDE_MODEL",
    "claude-sonnet-4-20250514"
)

MAX_TOKENS = 1000
