import logging
from typing import Any

from playwright.sync_api import APIRequestContext, APIResponse

from config.config import TIMEOUT
from utils.allure_utils import AllureUtils


class HTTPClient:
    """
    Низкоуровневый HTTP клиент.

    Использует Playwright APIRequestContext для выполнения запросов к API.
    """

    def __init__(self, api_context: APIRequestContext) -> None:
        """
        Инициализирует HTTPClient c предоставленным APIRequestContext Playwright.

        Args:
            api_context: Экземпляр APIRequestContext, настроенный c базовым URL и т.д.
        """
        self.api_request_context: APIRequestContext = api_context
        self.logger = logging.getLogger(__name__)

    def get(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> APIResponse:
        """
        Отправляет GET запрос на указанный эндпоинт.

        Args:
            endpoint: Относительный путь к эндпоинту (относительно base_url контекста).
            headers: Опциональный словарь заголовков запроса.
            params: Опциональный словарь параметров URL запроса.

        Returns:
            Объект APIResponse от Playwright.
        """
        self.logger.info("Sending GET request to %s with params: %s", endpoint, params)
        response: APIResponse = self.api_request_context.get(
            endpoint, headers=headers, params=params, timeout=TIMEOUT
        )
        self.logger.info("Received response %s from %s", response.status, response.url)
        AllureUtils.attach_response(response)
        return response

    def post(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        data: Any | None = None,
        json: Any | None = None,
    ) -> APIResponse:
        """
        Отправляет POST запрос на указанный эндпоинт.

        Предпочтительно использовать либо `data`, либо `json`, не oba сразу.

        Args:
            endpoint: Относительный путь к эндпоинту.
            headers: Опциональный словарь заголовков запроса.
            data: Опциональные данные для отправки (например, form data).
            json: Опциональные данные для отправки в формате JSON.

        Returns:
            Объект APIResponse от Playwright.
        """
        self.logger.info("Sending POST request to %s", endpoint)
        response: APIResponse = self.api_request_context.post(
            endpoint,
            headers=headers,
            data=data or json,
            timeout=TIMEOUT,
        )
        self.logger.info("Received response %s from %s", response.status, response.url)
        AllureUtils.attach_response(response)
        return response

    def put(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        data: Any | None = None,
        json: Any | None = None,
    ) -> APIResponse:
        """
        Отправляет PUT запрос на указанный эндпоинт.

        Args:
            endpoint: Относительный путь к эндпоинту.
            headers: Опциональный словарь заголовков запроса.
            data: Опциональные данные для отправки (например, form data).
            json: Опциональные данные для отправки в формате JSON.

        Returns:
            Объект APIResponse от Playwright.
        """
        self.logger.info("Sending PUT request to %s", endpoint)
        response: APIResponse = self.api_request_context.put(
            endpoint,
            headers=headers,
            data=data or json,
            timeout=TIMEOUT,
        )
        self.logger.info("Received response %s from %s", response.status, response.url)
        AllureUtils.attach_response(response)
        return response

    def delete(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> APIResponse:
        """
        Отправляет DELETE запрос на указанный эндпоинт.

        Args:
            endpoint: Относительный путь к эндпоинту.
            headers: Опциональный словарь заголовков запроса.
            params: Опциональный словарь параметров URL запроса.

        Returns:
            Объект APIResponse от Playwright.
        """
        self.logger.info("Sending DELETE request to %s", endpoint)
        response: APIResponse = self.api_request_context.delete(
            endpoint, headers=headers, params=params, timeout=TIMEOUT
        )
        self.logger.info("Received response %s from %s", response.status, response.url)
        AllureUtils.attach_response(response)
        return response

    def patch(
        self,
        endpoint: str,
        headers: dict[str, Any] | None = None,
        data: Any | None = None,
        json: Any | None = None,
    ) -> APIResponse:
        """
        Отправляет PATCH запрос на указанный эндпоинт.

        Args:
            endpoint: Относительный путь к эндпоинту.
            headers: Опциональный словарь заголовков запроса.
            data: Опциональные данные для отправки (например, form data).
            json: Опциональные данные для отправки в формате JSON.

        Returns:
            Объект APIResponse от Playwright.
        """
        self.logger.info("Sending PATCH request to %s", endpoint)
        response: APIResponse = self.api_request_context.patch(
            endpoint, headers=headers, data=data or json, timeout=TIMEOUT
        )
        self.logger.info("Received response %s from %s", response.status, response.url)
        AllureUtils.attach_response(response)
        return response
