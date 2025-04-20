import logging
import re
from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, BrowserContext, Playwright

from api.auth.client import AuthClient
from config.config import BASE_URL
from core.http_client import HTTPClient
from tests.mocks.handlers import general_route_handler

logger = logging.getLogger(__name__)


@pytest.fixture
def mockable_browser_context(
    playwright_instance: Playwright,
) -> Generator[BrowserContext]:
    """Создает временный BrowserContext для настройки маршрутов."""
    browser = playwright_instance.chromium.launch()
    context = browser.new_context(base_url=BASE_URL, ignore_https_errors=True)
    logger.info("Создан временный BrowserContext для мокирования.")
    yield context
    logger.info("Уничтожение временного BrowserContext...")
    context.close()
    browser.close()


@pytest.fixture
def mocked_api_request_context(
    mockable_browser_context: BrowserContext,
) -> Generator[APIRequestContext]:
    """
    Создает APIRequestContext из BrowserContext и регистрирует.

    обработчик маршрутов для мокирования.
    """
    logger.info("Регистрация обработчика маршрутов на BrowserContext...")
    try:
        mockable_browser_context.route(re.compile(r".*/api/.*"), general_route_handler)
        logger.info("Обработчик маршрутов зарегистрирован.")
        api_context = mockable_browser_context.request
        yield api_context
    finally:
        logger.info("Удаление обработчиков маршрутов...")
        mockable_browser_context.unroute_all()


@pytest.fixture
def mocked_http_client(mocked_api_request_context: APIRequestContext) -> HTTPClient:
    """Создает HTTPClient, использующий мокированный APIRequestContext."""
    return HTTPClient(api_context=mocked_api_request_context)


@pytest.fixture
def mocked_auth_client(mocked_http_client: HTTPClient) -> AuthClient:
    """Предоставляет мокированный экземпляр клиента API авторизации."""
    return AuthClient(mocked_http_client)
