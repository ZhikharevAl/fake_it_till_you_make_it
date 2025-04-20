import json
import logging

import allure
import pytest
from playwright.sync_api import APIResponse

from api.auth.client import AuthClient
from api.auth.models import AuthPayload, AuthSuccessResponse
from config.config import INVALID_USER_PASSWORD, TEST_USER_LOGIN, TEST_USER_PASSWORD
from tests.mocks.mock_data import MOCK_AUTH_FAILURE_400

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

    @allure.story("Неуспешный вход (Мок)")
    @allure.title("Тест неуспешного входа: {description} (c моком)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    @pytest.mark.parametrize(
        ("login", "password", "description"),
        [
            pytest.param(
                TEST_USER_LOGIN,
                INVALID_USER_PASSWORD,
                "Неверный пароль",
                id="invalid_password_mock",
            ),
            pytest.param(
                "nonexistent@example.com",
                TEST_USER_PASSWORD,
                "Неверный логин",
                id="invalid_login_mock",
            ),
            pytest.param(
                "nonexistent@example.com",
                INVALID_USER_PASSWORD,
                "Неверные логин и пароль",
                id="invalid_both_mock",
            ),
        ],
    )
    def test_login_failure_mocked(
        self,
        mocked_auth_client: AuthClient,
        login: str,
        password: str,
        description: str,
    ) -> None:
        """Проверка неуспешного входа c мокированным ответом 400."""
        allure.dynamic.description(f"Проверяем получение ответа 400 (мок) при: {description}")
        logger.info("Тест: %s (Мок)", description)
        payload = AuthPayload(login=login, password=password)
        response = mocked_auth_client.login(payload=payload, expected_status=400)

        with allure.step("Проверка типа ответа и статус кода"):  # type: ignore
            assert isinstance(response, APIResponse), (
                "Ожидался сырой ответ APIResponse при статусе 400"
            )
            assert response.status == 400, "Ожидался статус 400"
            try:
                error_body = response.json()
                assert error_body.get("message") == MOCK_AUTH_FAILURE_400["message"]
            except json.JSONDecodeError:
                pytest.fail("Тело ответа 400 не является валидным JSON")
