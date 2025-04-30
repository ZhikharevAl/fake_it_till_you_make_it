from typing import Any, Protocol
from unittest.mock import Mock


class MockHTTPClientProtocol(Protocol):
    """
    Интерфейс для мок-HTTP клиента.

    Определяет методы, которые должны быть реализованы в классе MockHTTPClient.
    """

    def set_mock_response(self, method: str, endpoint: str, response: Mock) -> None: ...  # noqa: D102


class MockFactory:
    """
    Фабрика для создания моков HTTP клиента.

    Используется для настройки ответов на HTTP запросы в тестах.
    """

    def __init__(self, mock_http_client: MockHTTPClientProtocol) -> None:
        """
        Инициализирует MockFactory c заданным мок-HTTP клиентом.

        Args:
            mock_http_client: экземпляр MockHTTPClient
        """
        self.mock_http_client = mock_http_client

    def _setup_mock(
        self,
        method: str,
        endpoint: str,
        status: int,
        json_data: dict[str, Any] | None = None,
    ) -> None:
        """Базовый метод для настройки мока."""
        mock_response = Mock()
        mock_response.status = status
        mock_response.json.return_value = json_data or {}
        self.mock_http_client.set_mock_response(method, endpoint, mock_response)

    def setup_mock(
        self,
        method: str,
        endpoint: str,
        status: int,
        json_data: dict[str, Any] | None = None,
    ) -> None:
        """
        Настраивает мок для заданного метода и эндпоинта.

        Args:
            method: HTTP метод ('GET', 'POST' и т.д.)
            endpoint: URL эндпоинта
            status: ожидаемый HTTP статус код
            json_data: тело ответа в виде словаря
        """
        self._setup_mock(method, endpoint, status, json_data)

    class Auth:
        """Класс для настройки моков аутентификации."""

        def __init__(self, outer: "MockFactory") -> None:
            """
            Инициализирует Auth c ссылкой на родительский MockFactory.

            Args:
                outer: экземпляр MockFactory
            """
            self.outer = outer

        def successful_login(self) -> None:
            """Настраивает мок для успешной авторизации."""
            self.outer.setup_mock(
                method="POST",
                endpoint="/api/auth",
                status=200,
                json_data={"auth": True, "token": "valid-jwt-token-12345"},
            )

    @property
    def auth(self) -> Auth:
        """Возвращает экземпляр Auth для настройки моков аутентификации."""
        return self.Auth(self)
