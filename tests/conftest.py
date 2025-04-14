import logging
from collections.abc import Generator

import pytest
from playwright.sync_api import (
    APIRequestContext,
    APIResponse,
    Playwright,
    sync_playwright,
)
from playwright.sync_api import (
    Error as PlaywrightError,
)

from api.auth.client import AuthClient
from api.auth.models import AuthPayload, AuthSuccessResponse
from api.user.client import UserClient
from config.config import BASE_URL, TEST_USER_LOGIN, TEST_USER_PASSWORD
from core.http_client import HTTPClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s [%(filename)s:%(lineno)s]",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", name="playwright_instance")
def playwright_instance_fixture() -> Generator[Playwright]:
    """Предоставляет экземпляр Playwright на всю сессию тестов."""
    logger.info("Запуск Playwright...")
    with sync_playwright() as p:
        yield p
    logger.info("Остановка Playwright...")


@pytest.fixture(scope="session", name="api_request_context")
def api_request_context_fixture(
    playwright_instance: Playwright,
) -> Generator[APIRequestContext]:
    """Создает и предоставляет APIRequestContext на всю сессию."""
    logger.info("Создание APIRequestContext для BASE_URL: %s...", BASE_URL)
    context = playwright_instance.request.new_context(base_url=BASE_URL, ignore_https_errors=True)
    yield context
    logger.info("Уничтожение APIRequestContext...")
    context.dispose()


@pytest.fixture(scope="session", name="http_client")
def http_client_fixture(api_request_context: APIRequestContext) -> HTTPClient:
    """Предоставляет экземпляр базового HTTP клиента на всю сессию."""
    logger.info("Создание HTTPClient...")
    return HTTPClient(api_context=api_request_context)


@pytest.fixture(scope="session", name="auth_client")
def auth_client_fixture(http_client: HTTPClient) -> AuthClient:
    """Предоставляет неаутентифицированный экземпляр клиента API авторизации."""
    logger.info("Создание AuthClient...")
    return AuthClient(http_client)


@pytest.fixture(scope="session", name="user_client")
def user_client_fixture(http_client: HTTPClient) -> UserClient:
    """Предоставляет неаутентифицированный экземпляр клиента API пользователя."""
    logger.info("Создание UserClient...")
    return UserClient(http_client)


@pytest.fixture(scope="session", name="auth_token")
def auth_token_fixture(auth_client: AuthClient) -> str | None:
    """
    Выполняет вход тестового пользователя один раз за сессию и возвращает токен.

    Если вход не удался, прерывает выполнение тестов.
    """
    logger.info(
        "Попытка логина для получения сессионного токена (пользователь: %s)...",
        TEST_USER_LOGIN,
    )
    if not TEST_USER_LOGIN or not TEST_USER_PASSWORD:
        pytest.fail("Учетные данные тестового пользователя не настроены.", pytrace=False)

    payload = AuthPayload(login=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
    try:

        @pytest.mark.xfail(
            reason="API нестабильно возвращает 500 вместо 200", raises=AssertionError, strict=False
        )
        def attempt_login() -> AuthSuccessResponse | APIResponse:
            return auth_client.login(payload, expected_status=200)

        response: AuthSuccessResponse | APIResponse = attempt_login()

        if isinstance(response, AuthSuccessResponse) and response.token:
            logger.info("Сессионный логин успешен.")
            return response.token
        raw_response_text = (
            response.text() if isinstance(response, APIResponse) else "Ответ не является текстом"
        )
        pytest.fail(
            f"Ошибка сессионного логина: Неожиданный тип ответа {type(response)} или пустой токен. "
            f"Тело ответа: {raw_response_text}",
            pytrace=False,
        )

    except (PlaywrightError, AssertionError) as e:
        pytest.fail(
            f"КРИТИЧЕСКАЯ ОШИБКА: He удалось выполнить сессионный логин для пользователя "
            f"{TEST_USER_LOGIN}. Ошибка: {e}",
            pytrace=False,
        )
        return None
    except Exception as e:  # noqa: BLE001
        pytest.fail(f"НЕПРЕДВИДЕННАЯ ОШИБКА при сессионном логине: {e}", pytrace=False)
        return None


@pytest.fixture
def authenticated_api_req_context(
    playwright_instance: Playwright, auth_token: str
) -> Generator[APIRequestContext]:
    """Создает APIRequestContext  добавленным заголовком Authorization: Bearer."""
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
def authenticated_http_client(authenticated_api_req_context: APIRequestContext) -> HTTPClient:
    """Создает HTTPClient, использующий авторизованный контекст."""
    return HTTPClient(api_context=authenticated_api_req_context)


@pytest.fixture
def authenticated_user_client(authenticated_http_client: HTTPClient) -> UserClient:
    """Предоставляет аутентифицированный экземпляр клиента API пользователя."""
    return UserClient(authenticated_http_client)
