import json
import logging
from enum import Enum
from typing import Protocol
from unittest.mock import Mock

from api.endpoints import APIEndpoints
from tests.mocks import mock_data

logger = logging.getLogger(__name__)


class MockHTTPClientProtocol(Protocol):
    """Интерфейс для мок-HTTP клиента."""

    def set_mock_response(self, method: str, endpoint: str, response: Mock) -> None:
        """Настраивает мок-ответ для заданного метода и эндпоинта."""

    def clear_mocks(self) -> None:
        """Очищает все настроенные моки."""


class MockFactory:
    """Фабрика для удобной настройки моков в MockHTTPClient."""

    def __init__(self, mock_http_client: MockHTTPClientProtocol) -> None:
        """Инициализирует MockFactory."""
        self.mock_http_client: MockHTTPClientProtocol = mock_http_client
        self.auth = self.Auth(self)
        self.user = self.User(self)
        self.request = self.user.Request(self)
        logger.debug("MockFactory инициализирована.")

    def _create_mock_response(
        self,
        status: int,
        json_data: dict | list | None = None,
        text_data: str | None = None,
        is_ok: bool | None = None,
    ) -> Mock:
        """Создает объект Mock, имитирующий APIResponse."""
        mock_response = Mock()
        mock_response.status = status
        mock_response.ok = is_ok if is_ok is not None else (200 <= status < 300)
        if json_data is not None:
            mock_response.json.return_value = json_data
            try:
                mock_response.text.return_value = json.dumps(json_data, ensure_ascii=False)
            except TypeError:
                mock_response.text.return_value = str(json_data)
        elif text_data is not None:
            mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
            mock_response.text.return_value = text_data
        else:
            mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
            mock_response.text.return_value = ""
        return mock_response

    def setup_mock(
        self,
        method: str,
        endpoint: APIEndpoints | str,
        status: int,
        json_data: dict | list | None = None,
        text_data: str | None = None,
        is_ok: bool | None = None,
    ) -> None:
        """Настраивает мок-ответ для заданного метода и эндпоинта."""
        endpoint_str = endpoint.value if isinstance(endpoint, Enum) else str(endpoint)

        mock_response = self._create_mock_response(status, json_data, text_data, is_ok)
        self.mock_http_client.set_mock_response(method, endpoint_str, mock_response)

    def clear_all_mocks(self) -> None:
        """Очищает все моки, настроенные через эту фабрику."""
        self.mock_http_client.clear_mocks()

    class Auth:
        """Класс для настройки моков, связанных c аутентификацией."""

        def __init__(self, outer: "MockFactory") -> None:
            """Инициализирует Auth."""
            self.outer = outer

        def success(self) -> None:
            """Настраивает мок для успешной аутентификации."""
            self.outer.setup_mock(
                "POST", APIEndpoints.AUTH, 200, json_data=mock_data.MOCK_AUTH_SUCCESS
            )

        def invalid_credentials(self) -> None:
            """Настраивает мок для невалидных учетных данных."""
            self.outer.setup_mock(
                "POST",
                APIEndpoints.AUTH,
                400,
                json_data=mock_data.MOCK_AUTH_FAILURE_400_CREDENTIALS,
            )

        def bad_request(self) -> None:
            """Настраивает мок для некорректного запроса."""
            self.outer.setup_mock(
                "POST",
                APIEndpoints.AUTH,
                400,
                json_data=mock_data.MOCK_AUTH_FAILURE_400_BAD_REQUEST,
            )

        def server_error(self) -> None:
            """Настраивает мок для ошибки сервера."""
            self.outer.setup_mock(
                "POST", APIEndpoints.AUTH, 500, json_data=mock_data.MOCK_SERVER_ERROR_500
            )

    class User:
        """Класс для настройки моков, связанных c пользователем."""

        def __init__(self, outer: "MockFactory") -> None:
            """Инициализирует User."""
            self.outer = outer

        def get_info_success(self) -> None:
            """Настраивает мок для успешного получения информации o пользователе."""
            self.outer.setup_mock("GET", APIEndpoints.USER, 200, json_data=mock_data.MOCK_USER_DATA)

        def get_info_unauthorized(self) -> None:
            """Настраивает мок для неавторизованного доступа к информации o пользователе."""
            self.outer.setup_mock(
                "GET", APIEndpoints.USER, 401, json_data=mock_data.MOCK_UNAUTHORIZED_401
            )

        def remove_favourite_success(self, request_id: str) -> None:
            """Настраивает мок для успешного удаления запроса из избранного."""
            endpoint = APIEndpoints.USER_FAVOURITES_DETAIL.format(requestId=request_id)
            self.outer.setup_mock(
                "DELETE", endpoint, 200, text_data=mock_data.MOCK_FAVOURITES_DELETE_SUCCESS_TEXT
            )

        def remove_favourite_bad_request(self, request_id: str) -> None:
            """Настраивает мок для ошибки 400 при удалении запроса из избранного."""
            endpoint = APIEndpoints.USER_FAVOURITES_DETAIL.format(requestId=request_id)
            self.outer.setup_mock(
                "DELETE", endpoint, 400, json_data=mock_data.MOCK_FAVOURITES_ERROR_400
            )

        def remove_favourite_unauthorized(self, request_id: str) -> None:
            """Настраивает мок для неавторизованного доступа при удалении запроса из избранного."""
            endpoint = APIEndpoints.USER_FAVOURITES_DETAIL.format(requestId=request_id)
            self.outer.setup_mock(
                "DELETE", endpoint, 401, json_data=mock_data.MOCK_UNAUTHORIZED_401
            )

        def get_favourites_success_list(self) -> None:
            """Настраивает мок для успешного получения списка избранных запросов."""
            self.outer.setup_mock(
                "GET", APIEndpoints.USER_FAVOURITES, 200, json_data=mock_data.MOCK_FAVOURITES_LIST
            )

        def get_favourites_unauthorized(self) -> None:
            """Настраивает мок для неавторизованного доступа к избранным запросам."""
            self.outer.setup_mock(
                "GET", APIEndpoints.USER_FAVOURITES, 401, json_data=mock_data.MOCK_UNAUTHORIZED_401
            )

        def add_favourite_success(self) -> None:
            """Настраивает мок для успешного добавления запроса в избранное."""
            self.outer.setup_mock(
                "POST",
                APIEndpoints.USER_FAVOURITES,
                200,
                text_data=mock_data.MOCK_FAVOURITES_ADD_SUCCESS_TEXT,
            )

        def add_favourite_unauthorized(self) -> None:
            """Настраивает мок для неавторизованного доступа при добавлении запроса в избранное."""
            self.outer.setup_mock(
                "POST", APIEndpoints.USER_FAVOURITES, 401, json_data=mock_data.MOCK_UNAUTHORIZED_401
            )

        class Request:
            """Класс для настройки моков, связанных c запросами помощи."""

            def __init__(self, outer: "MockFactory") -> None:
                """Инициализирует Request."""
                self.outer = outer

            def get_all_success(self, *, empty: bool = False) -> None:
                """Настраивает мок для успешного получения списка всех запросов."""
                data = [] if empty else mock_data.MOCK_REQUESTS_LIST
                self.outer.setup_mock("GET", APIEndpoints.REQUESTS, 200, json_data=data)

            def get_all_server_error(self) -> None:
                """Настраивает мок для ошибки сервера при получении списка запросов."""
                self.outer.setup_mock(
                    "GET", APIEndpoints.REQUESTS, 500, json_data=mock_data.MOCK_SERVER_ERROR_500
                )

            def get_details_success(self, request_id: str) -> None:
                """Настраивает мок для успешного получения деталей запроса помощи."""
                endpoint = APIEndpoints.REQUEST_DETAIL.format(id=request_id)
                data = (
                    mock_data.MOCK_HELP_REQUEST_DATA
                    if request_id == mock_data.MOCK_HELP_REQUEST_DATA["id"]
                    else {}
                )
                self.outer.setup_mock("GET", endpoint, 200, json_data=data)

            def get_details_not_found(self, request_id: str) -> None:
                """Настраивает мок для ошибки 404 при получении деталей запроса помощи."""
                endpoint = APIEndpoints.REQUEST_DETAIL.format(id=request_id)
                self.outer.setup_mock("GET", endpoint, 404, json_data=mock_data.MOCK_NOT_FOUND_404)

            def contribute_success(self, request_id: str) -> None:
                """Настраивает мок для успешного внесения вклада в запрос помощи."""
                endpoint = APIEndpoints.REQUEST_CONTRIBUTION.format(id=request_id)
                self.outer.setup_mock(
                    "POST", endpoint, 200, text_data=mock_data.MOCK_CONTRIBUTION_SUCCESS_TEXT
                )

            def contribute_not_found(self, request_id: str) -> None:
                """Настраивает мок для ошибки 404 при внесении вклада в запрос помощи."""
                endpoint = APIEndpoints.REQUEST_CONTRIBUTION.format(id=request_id)
                self.outer.setup_mock("POST", endpoint, 404, json_data=mock_data.MOCK_NOT_FOUND_404)
