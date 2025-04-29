import allure
import pytest

from api.auth.client import AuthClient
from api.auth.models import AuthPayload, AuthSuccessResponse
from config.config import TEST_USER_LOGIN, TEST_USER_PASSWORD


@allure.epic("Аутентификация")
@allure.feature("Вход пользователя (POST /api/auth)")
@pytest.mark.auth
class TestAuthenticationAPI:
    """Тесты для эндпоинта POST /api/auth (авторизация)."""

    @allure.story("Успешная авторизация")
    @allure.title("Позитивный кейс: Валидные данные → Получаем JWT")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_successful_login(self, auth_client: AuthClient) -> None:
        """Проверка успешной авторизации c валидными данными."""
        if not TEST_USER_LOGIN or not TEST_USER_PASSWORD:
            pytest.skip("Учетные данные не настроены.")

        payload = AuthPayload(login=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        result = auth_client.login(payload=payload, expected_status=200)

        assert isinstance(result, AuthSuccessResponse)
        assert result.auth is True
        assert len(result.token) >= 10
