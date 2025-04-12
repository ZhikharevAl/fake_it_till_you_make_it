from playwright.sync_api import APIResponse

from api.auth.models import AuthPayload, AuthSuccessResponse
from api.base_api import BaseAPI
from api.endpoints import APIEndpoints


class AuthClient(BaseAPI):
    """
    API client for interaction with authorization endpoint (/api/auth).

    Inherits from BaseAPI to use a generic HTTP client and handle responses.
    """

    def login(
        self,
        payload: AuthPayload,
        expected_status: int = 200,
    ) -> AuthSuccessResponse | APIResponse:
        """
        Executes a user authorization request (POST /api/auth).

        Args:
            payload (AuthPayload): Object with login data (login and password).
            expected_status (int): Expected HTTP response status (default 200).

        Returns:
            AuthSuccessResponse: Token object on successful authorization (status 200)
                and valid response.
            APIResponse: Raw Playwright response object with other status codes or if
                model validation fails.

        Raises:
            AssertionError: If the received status code does not match expected_status
                           or if AuthSuccessResponse model validation fails
                           (called from BaseAPI._handle_response).
        """
        endpoint = APIEndpoints.AUTH
        response: APIResponse = self.http.post(
            endpoint=endpoint.format(),
            json=payload.model_dump(),
        )

        if response.ok:
            return self._handle_response(
                response,
                expected_status,
                response_model=AuthSuccessResponse,
            )
        return self._handle_response(response, expected_status)
