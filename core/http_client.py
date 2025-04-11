import logging
from typing import Any

from playwright.sync_api import APIRequestContext, APIResponse

from config.config import TIMEOUT
from utils.allure_utils import AllureUtils


class HTTPClient:
    """
    Low-level HTTP client.

    Uses the Playwright APIRequestContext to make requests to the API.
    """

    def __init__(self, api_context: APIRequestContext) -> None:
        """
        Initializes HTTPClient with the provided APIRequestContext Playwright.

        Args:
            api_context: The APIRequestContext instance configured with the base URL, etc.
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
        Sends a GET request to the specified endpoint.

        Args:
            endpoint: Relative path to the endpoint (relative to the base_url of the context).
            headers: Optional dictionary of request headers.
            params: Optional dictionary of URL request parameters.

        Returns:
            APIResponse object by Playwright.
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
        data: dict[str, Any] | str | bytes | None = None,
        json: Any | None = None,  # noqa: ANN401
    ) -> APIResponse:
        """
        Sends a POST request to the specified endpoint.

        Preferably use either `data` or `json`, not oba immediately.

        Args:
            endpoint: Relative path to the endpoint.
            headers: Optional dictionary of request headers.
            data: Optional data to be sent (e.g. form data).
            json: Optional data to send in JSON format.

        Returns:
            APIResponse object by Playwright.
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
        data: dict[str, Any] | str | bytes | None = None,
        json: Any | None = None,  # noqa: ANN401
    ) -> APIResponse:
        """
        Sends a PUT request to the specified endpoint.

        Args:
            endpoint: Relative path to the endpoint.
            headers: Optional dictionary of request headers.
            data: Optional data to be sent (e.g. form data).
            json: Optional data to send in JSON format.

        Returns:
            APIResponse object by Playwright.
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
        Sends a DELETE request to the specified endpoint.

        Args:
            endpoint: Relative path to the endpoint.
            headers: Optional query header dictionary.
            params: Optional dictionary of URL request parameters.

        Returns:
            APIResponse object by Playwright.
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
        data: dict[str, Any] | str | bytes | None = None,
        json: Any | None = None,  # noqa: ANN401
    ) -> APIResponse:
        """
        Sends a PATCH request to the specified endpoint.

        Args:
            endpoint: Relative path to the endpoint.
            headers: Optional query header dictionary.
            data: Optional data to send (e.g. form data).
            json: Optional data to send in JSON format.

        Returns:
            APIResponse object by Playwright.
        """
        self.logger.info("Sending PATCH request to %s", endpoint)
        response: APIResponse = self.api_request_context.patch(
            endpoint, headers=headers, data=data or json, timeout=TIMEOUT
        )
        self.logger.info("Received response %s from %s", response.status, response.url)
        AllureUtils.attach_response(response)
        return response
