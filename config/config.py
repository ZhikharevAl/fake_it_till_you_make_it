import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path: Path = Path(__file__).parent.parent / ".env"

load_dotenv(dotenv_path=dotenv_path)

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
API_PREFIX = "/api"
TIMEOUT = int(os.getenv("API_TIMEOUT", "10000"))

TEST_USER_LOGIN = os.getenv("TEST_USER_LOGIN")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
INVALID_USER_PASSWORD = os.getenv("INVALID_USER_PASSWORD", "invalidPass123")


if not TEST_USER_LOGIN or not TEST_USER_PASSWORD:
    MESSAGE = "The TEST_USER_LOGIN and TEST_USER_PASSWORD environment variables must be set."
    raise ValueError(MESSAGE)
