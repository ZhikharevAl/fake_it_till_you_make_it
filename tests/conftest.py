import logging
from collections.abc import Generator

import pytest
from playwright.sync_api import (
    APIRequestContext,
    Playwright,
    sync_playwright,
)
from playwright.sync_api import (
    Error as PlaywrightError,
)

from api.auth.client import AuthClient
from api.auth.models import AuthPayload, AuthSuccessResponse
from config.config import (
    BASE_URL,
    TEST_USER_LOGIN,
    TEST_USER_PASSWORD,
)
from core.http_client import HTTPClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", name="playwright_instance")
def playwright_instance_fixture() -> Generator[Playwright]:
    """Provides an instance of Playwright for the entire test session."""
    logger.info("\n[Fixture] Playwright's launch...")
    with sync_playwright() as p:
        yield p
    logger.info("[Fixture] Playwright's stop...")


@pytest.fixture(scope="session", name="api_request_context")
def api_request_context_fixture(playwright_instance: Playwright) -> Generator[APIRequestContext]:
    """Creates and provides an APIRequestContext for the entire session."""
    logger.info("\n[Fixture] Creating APIRequestContext for BASE_URL: %s...", BASE_URL)
    context = playwright_instance.request.new_context(
        base_url=BASE_URL,
        ignore_https_errors=True,
    )
    yield context
    logger.info("[Fixture] Destruction APIRequestContext...")
    context.dispose()


@pytest.fixture(scope="session", name="http_client")
def http_client_fixture(api_request_context: APIRequestContext) -> HTTPClient:
    """Provides an instance of the underlying HTTP client for the entire session."""
    logger.info("\n[Fixture] Creation HTTPClient...")
    return HTTPClient(api_context=api_request_context)


@pytest.fixture(scope="session", name="auth_client")
def auth_client_fixture(http_client: HTTPClient) -> AuthClient:
    """Provides an instance of the authorization API client for the entire session."""
    logger.info("\n[Fixture] Creation AuthClient...")
    return AuthClient(http_client)


@pytest.fixture(scope="session", name="auth_token")
def auth_token_fixture(auth_client: AuthClient) -> str | None:
    """
    Logs the test user in once per session and returns the token.

    If the input fails, aborts all tests that depend on this fixture.
    """
    logger.info(
        "\n[Fixture] Login attempt to obtain a session token (user: %s)...",
        TEST_USER_LOGIN,
    )
    if not TEST_USER_LOGIN or not TEST_USER_PASSWORD:
        pytest.fail(
            "Test user credentials (TEST_USER_LOGIN, TEST_USER_PASSWORD) are not configured.",
            pytrace=False,
        )

    payload = AuthPayload(login=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
    try:
        response = auth_client.login(payload, expected_status=200)
        if isinstance(response, AuthSuccessResponse) and response.token:
            logger.info("[Fixture] Session login successful.")
            return response.token
    except (PlaywrightError, AssertionError) as e:
        pytest.fail(
            f"[Fixture] CRITICAL ERROR: Failed to execute session login user {TEST_USER_LOGIN}. "
            f"Error: {e}",
            pytrace=False,
        )
