import logging
from typing import Any
from unittest.mock import Mock

from playwright.sync_api import APIRequestContext, APIResponse

from core.http_client import HTTPClient

logger = logging.getLogger(__name__)


class MockHTTPClient(HTTPClient):
    """
    Мок HTTP клиент для тестирования API. Перехватывает вызовы методов.

    и возвращает заранее настроенные ответы вместо реальных запросов.
    """

    def __init__(self) -> None:
        """Инициализирует HTTP клиент c фиктивным контекстом и хранилищем моков."""
        mock_api_context = Mock(spec=APIRequestContext)
        super().__init__(api_context=mock_api_context)
        self.mocks: dict[str, Mock] = {}
        logger.info("MockHTTPClient ID %s инициализирован. Mocks: %s", id(self), self.mocks)

    def _get_mock_key(self, method: str, endpoint: str) -> str:
        """Формирует ключ для словаря моков, гарантируя строку."""
        endpoint_str = str(endpoint)
        key = f"{method.upper()}:{endpoint_str}"
        logger.debug("Генерация ключа мока: '%s'", key)
        return key

    def _mock_request(self, endpoint: str, method: str = "GET") -> Mock:
        """Основная логика перехвата. Ищет мок и возвращает ego или вызывает ошибку."""
        key = self._get_mock_key(method, endpoint)
        logger.info(
            "MockHTTPClient ID %s ищет мок для ключа: '%s'. Текущие моки: %s",
            id(self),
            key,
            list(self.mocks.keys()),
        )

        if key in self.mocks:
            logger.info("Найден и возвращен мок для: %s", key)
            return self.mocks[key]

        msg = f"Мок не настроен для запроса: {method.upper()} {endpoint}"
        logger.error(msg)
        raise RuntimeError(msg)

    def get(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,  # noqa: ARG002
        params: dict[str, Any] | None = None,  # noqa: ARG002
        **kwargs: dict,
    ) -> APIResponse:
        """Перехватывает GET запросы и возвращает мок-ответ."""
        return self._mock_request(endpoint, method="GET", **kwargs)

    def post(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,  # noqa: ARG002
        data: dict[str, Any] | str | bytes | None = None,  # noqa: ARG002
        json: dict[str, Any] | None = None,  # noqa: ARG002
        **kwargs: dict,
    ) -> APIResponse:
        """Перехватывает POST запросы и возвращает мок-ответ."""
        return self._mock_request(endpoint, method="POST", **kwargs)

    def put(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,  # noqa: ARG002
        data: dict[str, Any] | str | bytes | None = None,  # noqa: ARG002
        json: dict[str, Any] | None = None,  # noqa: ARG002
        **kwargs: dict,
    ) -> APIResponse:
        """Перехватывает PUT запросы и возвращает мок-ответ."""
        return self._mock_request(endpoint, method="PUT", **kwargs)

    def delete(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,  # noqa: ARG002
        params: dict[str, Any] | None = None,  # noqa: ARG002
        **kwargs: dict,
    ) -> APIResponse:
        """Перехватывает DELETE запросы и возвращает мок-ответ."""
        return self._mock_request(endpoint, method="DELETE", **kwargs)

    def patch(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,  # noqa: ARG002
        data: dict[str, Any] | str | bytes | None = None,  # noqa: ARG002
        json: dict[str, Any] | None = None,  # noqa: ARG002
        **kwargs: dict,
    ) -> APIResponse:
        """Перехватывает PATCH запросы и возвращает мок-ответ."""
        return self._mock_request(endpoint, method="PATCH", **kwargs)

    def set_mock_response(self, method: str, endpoint: str, response: Mock) -> None:
        """Настраивает мок-ответ."""
        key = self._get_mock_key(method, str(endpoint))
        self.mocks[key] = response
        logger.info(
            "MockHTTPClient ID %s установил мок для: '%s' (Статус: %s). Текущие моки: %s",
            id(self),
            key,
            response.status,
            list(self.mocks.keys()),
        )

    def clear_mocks(self) -> None:
        """Очищает все установленные моки."""
        logger.info(
            "MockHTTPClient ID %s очищает моки. Было: %s", id(self), list(self.mocks.keys())
        )
        self.mocks.clear()
