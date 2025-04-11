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
from api.user.client import UserClient
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
    """Предоставляет экземпляр Playwright для всего сеанса тестирования."""
    logger.info("\n[Fixture] Playwright's launch...")
    with sync_playwright() as p:
        yield p
    logger.info("[Fixture] Playwright's stop...")


@pytest.fixture(scope="session", name="api_request_context")
def api_request_context_fixture(playwright_instance: Playwright) -> Generator[APIRequestContext]:
    """Создает и предоставляет APIRequestContext для всей сессии."""
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
    """Предоставляет экземпляр базового HTTP-клиента для всей сессии."""
    logger.info("\n[Fixture] Creation HTTPClient...")
    return HTTPClient(api_context=api_request_context)


@pytest.fixture(scope="session", name="auth_client")
def auth_client_fixture(http_client: HTTPClient) -> AuthClient:
    """Предоставляет экземпляр клиента API авторизации на всю сессию."""
    logger.info("\n[Fixture] Creation AuthClient...")
    return AuthClient(http_client)


@pytest.fixture(scope="session", name="user_client")
def user_client_fixture(http_client: HTTPClient) -> UserClient:
    """Предоставляет неаутентифицированный экземпляр клиента API пользователя."""
    logger.info("\n[Fixture] Создание UserClient...")
    return UserClient(http_client)


@pytest.fixture(scope="session", name="auth_token")
def auth_token_fixture(auth_client: AuthClient) -> str | None:
    """
    Выполняет вход тестового пользователя один раз за сессию и возвращает токен.

    Если входные данные не работают, прерывает все тесты, зависящие от этого приспособления..
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


@pytest.fixture
def authenticated_api_request_context(
    playwright_instance: Playwright, auth_token: str
) -> Generator[APIRequestContext]:
    """Создает APIRequestContext c добавленным заголовком Authorization: Bearer."""
    logger.info(
        "\n[Fixture] Создание авторизованного APIRequestContext (токен: %s...)...", auth_token[:5]
    )
    headers = {"Authorization": f"Bearer {auth_token}"}
    context = playwright_instance.request.new_context(
        base_url=BASE_URL, extra_http_headers=headers, ignore_https_errors=True
    )
    yield context
    logger.info("[Fixture] Уничтожение авторизованного APIRequestContext...")
    context.dispose()


@pytest.fixture
def authenticated_http_client(api_request_context_with_auth: APIRequestContext) -> HTTPClient:
    """Создает HTTPClient, использующий авторизованный контекст."""
    return HTTPClient(api_context=api_request_context_with_auth)


@pytest.fixture
def authenticated_user_client(http_client: HTTPClient) -> UserClient:
    """Предоставляет аутентифицированный экземпляр клиента API пользователя."""
    return UserClient(http_client)
