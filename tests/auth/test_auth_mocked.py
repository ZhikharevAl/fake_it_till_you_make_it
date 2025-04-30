import allure
import pytest

from api.auth.client import AuthClient
from api.auth.models import AuthPayload, AuthSuccessResponse
from core.mock_http_client import MockHTTPClient
from utils.mock_factory import MockFactory


@allure.epic("Аутентификация")
@allure.feature("POST /api/auth")
@pytest.mark.mocked
class TestAuthenticationMocked:
    """Тесты для эндпоинта авторизации POST /api/auth c использованием моков."""

    @allure.story("Успешная авторизация")
    @allure.title("Авторизация c валидными данными")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_authentication(
        self, mock_auth_client: AuthClient, mock_http_client: MockHTTPClient
    ) -> None:
        """Проверка успешной авторизации c валидными учетными данными."""
        factory = MockFactory(mock_http_client)
        factory.auth.successful_login()

        payload = AuthPayload(login="user@example.com", password="password123")  # noqa: S106

        result = mock_auth_client.login(payload=payload, expected_status=200)

        assert isinstance(result, AuthSuccessResponse)
        assert result.auth is True
        assert result.token == "valid-jwt-token-12345"
