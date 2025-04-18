import logging
import re

from playwright.sync_api import Request, Route

from tests.mocks import mock_data

logger = logging.getLogger(__name__)

AUTH_URL = re.compile(r".*/api/auth")


def general_route_handler(route: Route, request: Request) -> None:
    """
    Основной обработчик маршрутов для мок-тестов.

    Определяет, какой ответ вернуть в зависимости от URL и метода.
    """
    url = request.url
    method = request.method
    logger.debug("Перехвачен мок-запрос: %s %s", method, url)

    if AUTH_URL.search(url) and method == "POST":
        payload = request.post_data_json
        if (
            payload
            and payload.get("login") == "test@test.com"
            and payload.get("password") == "password"
        ):
            logger.info("Мокируем успешный ответ для POST /api/auth")
            route.fulfill(status=200, json=mock_data.MOCK_AUTH_SUCCESS)
        else:
            logger.info("Мокируем ответ 400 для POST /api/auth")
            route.fulfill(status=400, json=mock_data.MOCK_AUTH_FAILURE_400)
        return
