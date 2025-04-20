import logging

import allure
import pytest

from api.auth.client import AuthClient
from api.auth.models import AuthPayload, AuthSuccessResponse
from config.config import TEST_USER_LOGIN, TEST_USER_PASSWORD

logger = logging.getLogger(__name__)


@allure.epic("Аутентификация (Моки)")
@allure.feature("Вход пользователя (POST /api/auth)")
@pytest.mark.auth
@pytest.mark.mocked
class TestAuthenticationAPIMocked:
    """Тесты мок-тестов для эндпоинта авторизации POST /api/auth."""

    @allure.story("Успешный вход (Мок)")
    @allure.title("Тест успешной авторизации пользователя (c моком)")
    @allure.description("Проверяем успешный ответ и валидацию токена при мокированном ответе API.")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_login_success_mocked(self, mocked_auth_client: AuthClient) -> None:
        """Проверка успешного входа c мокированным ответом 200."""
        logger.info("Тест: Успешная авторизация (Мок)")
        payload = AuthPayload(login=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = mocked_auth_client.login(payload=payload, expected_status=200)

        with allure.step("Проверка типа и полей ответа"):  # type: ignore
            assert isinstance(response, AuthSuccessResponse), (
                "Ответ должен быть типа AuthSuccessResponse"
            )
            assert response.auth is True, "Поле 'auth' должно быть true"
            assert response.token is not None, "Поле 'token' не должно быть пустым (None)"
            assert response.token.startswith("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"), (
                "Токен не совпадает c моком"
            )
        logger.info("Мок-токен успешно получен и провалидирован.")
