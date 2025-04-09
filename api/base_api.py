import logging
from typing import TypeVar

import allure
from playwright.sync_api import APIResponse
from pydantic import BaseModel, ValidationError

from core.http_client import HTTPClient

T = TypeVar("T", bound=BaseModel)


class BaseAPI:
    """
    Base class for all client specific APIs (AuthClient, UserClient, etc.).

    Provides a generic HTTP client instance and a method for handling responses.
    """

    def __init__(self, http_client: HTTPClient) -> None:
        """
        Initializes the underlying API client.

        Args:
            http_client: HTTPClient instance to execute requests.
        """
        self.http: HTTPClient = http_client

        self.logger = logging.getLogger(self.__class__.__name__)

    def _handle_response(
        self,
        response: APIResponse,
        expected_status: int,
        response_model: type[T] | None = None,
    ) -> T | APIResponse:
        """
        A generic method to handle the API response.

        Checks the status code and, if a model is specified, validates the response body against it.

        Args:
            response: APIResponse object received from HTTPClient.
            expected_status: Expected HTTP status code.
            response_model: Optional Pydantic model class for validating the response body.

        Returns:
            An instance of response_model if the validation was successful.
            Raw APIResponse object if response_model is not specified or validation is not required.

        Raises:
            AssertionError: If the actual status of the code does not match the expected_status,
                           or if it failed to parse JSON,
                           or if the Pydantic model validation failed.
        """
        self.logger.debug(
            "Handling response: Status=%s, Expected=%s, URL=%s",
            response.status,
            expected_status,
            response.url,
        )

        allure.attach(
            name=f"Status response code: {response.status} (Expected: {expected_status})",
            body=str(response.status),
            attachment_type=allure.attachment_type.TEXT,
        )

        assert response.status == expected_status, (
            f"The status was pending {expected_status}, but received {response.status}. "
            f"URL: {response.url}\nBody of the answer:\n{response.text()}"
        )

        if response_model and response.status == expected_status:
            try:
                body_json = response.json()
                parsed_model: BaseModel = response_model.model_validate(body_json)
                self.logger.debug(
                    "Response body validated successfully against %s", response_model.__name__
                )

                allure.attach(
                    name=f"Body of the answer (failed by {response_model.__name__})",
                    body=parsed_model.model_dump_json(indent=2),
                    attachment_type=allure.attachment_type.JSON,
                )
            except ValidationError as e:
                self.logger.exception("Pydantic validation failed for %s", response_model.__name__)

                allure.attach(
                    name="Pydantic validation error",
                    body=f"Model: {response_model.__name__}\nErrors: {e!s}\n"
                    f"Body of the answer:\n{response.text()}",
                    attachment_type=allure.attachment_type.TEXT,
                )
                raise AssertionError(
                    f"Model response validation error {response_model.__name__}: {e}.\n"
                    f"Body: {response.text()}"
                ) from e
            except Exception as e:
                self.logger.exception("Failed to parse response JSON or validate model: %s")

                allure.attach(
                    name="Response parsing/validation error",
                    body=f"Failed to parse JSON or failed to validate the model: {e}.\n"
                    f"Body of the answer:\n{response.text()}",
                    attachment_type=allure.attachment_type.TEXT,
                )
                raise AssertionError(
                    f"Failed to parse or failed to validate the response: {e}.\n"
                    f"Body: {response.text()}"
                ) from e
            else:
                return parsed_model
        else:
            self.logger.debug(
                "No response model provided or status mismatch, returning raw response."
            )
            return response
