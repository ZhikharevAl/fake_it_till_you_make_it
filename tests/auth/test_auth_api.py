import logging

import pytest
from playwright.sync_api import APIResponse

from api.auth.client import AuthClient
from api.auth.models import AuthPayload, AuthSuccessResponse
from config.config import (
    INVALID_USER_PASSWORD,
    TEST_USER_LOGIN,
    TEST_USER_PASSWORD,
)

logger = logging.getLogger(__name__)


@pytest.mark.auth
class TestAuthenticationAPI:
    """Test suite for POST authorization endpoint /api/auth."""

    @pytest.mark.negative
    @pytest.mark.parametrize(
        ("login", "password", "expected_status", "description"),
        [
            pytest.param(
                TEST_USER_LOGIN,
                INVALID_USER_PASSWORD,
                400,
                "Correct login, wrong password",
                id="invalid_password",
            ),
            pytest.param(
                "nonexistent.user@example.com",
                TEST_USER_PASSWORD,
                400,
                "Incorrect login, correct password",
                id="invalid_login",
            ),
            pytest.param(
                "nonexistent.user@example.com",
                INVALID_USER_PASSWORD,
                400,
                "Wrong login, wrong password",
                marks=pytest.mark.xfail(
                    reason="API erratically returns 500 instead of 400", raises=AssertionError
                ),
                id="invalid_login_and_pass_xfail",
            ),
        ],
    )
    def test_login_failure_invalid_credentials(
        self,
        auth_client: AuthClient,
        login: str,
        password: str,
        expected_status: int,
        description: str,
    ) -> None:
        """
        Verify unsuccessful authorization with incorrect credentials.

        Expected result: status code 400 Bad Request.
        """
        logger.info("\nTest: %s", description)
        payload = AuthPayload(login=login, password=password)
        response = auth_client.login(payload=payload, expected_status=expected_status)
        assert isinstance(response, APIResponse), (
            f"APIResponse type was expected at status {expected_status}"
        )

    @pytest.mark.negative
    @pytest.mark.parametrize(
        ("payload_dict", "expected_status", "description"),
        [
            pytest.param(
                {"login": TEST_USER_LOGIN},
                400,
                "No password field",
                marks=pytest.mark.xfail(
                    reason="API erratically returns 500 instead of 400", raises=AssertionError
                ),
                id="missing_password_xfail",
            ),
            pytest.param(
                {"password": TEST_USER_PASSWORD},
                400,
                "No login field",
                id="missing_login_400",
            ),
            pytest.param({}, 400, "Empty request body", id="empty_payload_400"),
            pytest.param(
                {"login": "", "password": TEST_USER_PASSWORD},
                400,
                "Empty string in the login field",
                id="empty_login_str_400",
            ),
            pytest.param(
                {"login": TEST_USER_LOGIN, "password": ""},
                400,
                "Empty string in the password field",
                marks=pytest.mark.xfail(
                    reason="API erratically returns 500 instead of 400", raises=AssertionError
                ),
                id="empty_pass_str_xfail",
            ),
            pytest.param(
                {"login": "not email", "password": TEST_USER_PASSWORD},
                400,
                "Incorrect login format (not email)",
                marks=pytest.mark.xfail(
                    reason="API erratically returns 500 instead of 400", raises=AssertionError
                ),
                id="bad_login_format_xfail",
            ),
        ],
    )
    def test_login_malformed_payload(
        self,
        auth_client: AuthClient,
        payload_dict: dict[str, str | None],
        expected_status: int,
        description: str,
    ) -> None:
        """
        Verify API behavior with malformed payload.

        Expected result: status code 400 Bad Request.
        """
        logger.info("\nTest: %s", description)
        response = auth_client.http.post(endpoint=auth_client.AUTH_ENDPOINT, json=payload_dict)
        assert response.status == expected_status, (
            f"Expected status {expected_status}, got {response.status}"
        )
        logger.info("Response status: %s, Body: %s", response.status, response.text())

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_login_success(self, auth_client: AuthClient) -> None:
        """
        Verify successful authorization with valid credentials.

        Expected result: 200 OK status and a valid JWT token in the response.
        """
        logger.info("\nTest: Successful authorization")
        if not TEST_USER_LOGIN or not TEST_USER_PASSWORD:
            pytest.skip("Test Skip: The test user credentials are not configured.")

        payload = AuthPayload(login=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = auth_client.login(payload=payload, expected_status=200)

        assert isinstance(response, AuthSuccessResponse), (
            "The response must be of type AuthSuccessResponse"
        )
        assert response.auth is True, "The 'auth' field must be true"
        assert response.token is not None, "The 'token' field must not be empty (None)"
        assert len(response.token) >= 10, (
            f"Token length ({len(response.token)}) less than expected (>=10)"
        )
        logger.info("Token successfully received (first 10 characters): %s...", response.token[:10])
