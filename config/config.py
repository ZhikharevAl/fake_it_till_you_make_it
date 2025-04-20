import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import EmailStr

dotenv_path: Path = Path(__file__).parent.parent / ".env"

load_dotenv(dotenv_path=dotenv_path)

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
API_PREFIX = "/api"
TIMEOUT = int(os.getenv("API_TIMEOUT", "10000"))

login: EmailStr | None = os.getenv("TEST_USER_LOGIN")

if login is not None:
    TEST_USER_LOGIN: EmailStr = login
else:
    MESSAGE = "The TEST_USER_LOGIN environment variable must be set."
    raise ValueError(MESSAGE)

password: str | None = os.getenv("TEST_USER_PASSWORD")

if password is not None:
    TEST_USER_PASSWORD: str = password
else:
    MESSAGE = "The TEST_USER_PASSWORD environment variable must be set."
    raise ValueError(MESSAGE)

INVALID_USER_PASSWORD = os.getenv("INVALID_USER_PASSWORD", "invalidPass123")
