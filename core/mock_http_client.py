from typing import Any
from unittest.mock import Mock

from playwright.sync_api import APIRequestContext

from core.http_client import HTTPClient


class MockHTTPClient(HTTPClient):
    """
    Мок HTTP клиент для тестирования API.

    Используется для перехвата и обработки HTTP запросов и ответов.
    """

    def __init__(self) -> None:
        """Инициализирует HTTP клиент c фиктивным контекстом."""
        mock_api_context = Mock(spec=APIRequestContext)
        mock_api_context.get = lambda *a, **kw: self._mock_request(*a, method="GET", **kw)
        mock_api_context.post = lambda *a, **kw: self._mock_request(*a, method="POST", **kw)
        mock_api_context.put = lambda *a, **kw: self._mock_request(*a, method="PUT", **kw)
        mock_api_context.delete = lambda *a, **kw: self._mock_request(*a, method="DELETE", **kw)
        mock_api_context.patch = lambda *a, **kw: self._mock_request(*a, method="PATCH", **kw)

        super().__init__(api_context=mock_api_context)
        self.mocks = {}

    def _mock_request(
        self, *args: tuple[Any, ...], method: str = "GET", **kwargs: dict[str, Any]
    ) -> Mock:
        """Перехватывает запросы и возвращает мок-ответ."""
        endpoint = args[0] if args else kwargs.get("endpoint", "")
        key = f"{method.lower()}:{endpoint}"

        if key in self.mocks:
            return self.mocks[key]
        if f"{method.lower()}:*" in self.mocks:
            return self.mocks[f"{method.lower()}:*"]
        msg = "No mock setup for request: %s"
        raise RuntimeError(msg, key)

    def set_mock_response(self, method: str, endpoint: str, response: Mock) -> None:
        """Настраивает мок под конкретный метод и эндпоинт."""
        self.mocks[f"{method.lower()}:{endpoint}"] = response

    def clear_mocks(self) -> None:
        """Очищает все установленные моки."""
        self.mocks.clear()
