import logging

import allure
import pytest
from playwright.sync_api import APIResponse

from api.auth.client import AuthClient
from api.auth.models import AuthPayload, AuthSuccessResponse
from api.endpoints import APIEndpoints
from config.config import (
    INVALID_USER_PASSWORD,
    TEST_USER_LOGIN,
    TEST_USER_PASSWORD,
)

logger = logging.getLogger(__name__)


@allure.epic("Аутентификация")
@allure.feature("Вход пользователя (POST /api/auth)")
@pytest.mark.auth
class TestAuthenticationAPI:
    """Класс тестов для эндпоинта авторизации POST /api/auth."""

    @allure.story("Неуспешный вход - Неверные учетные данные")
    @allure.title("Тест неуспешного входа: {description}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    @pytest.mark.parametrize(
        ("login", "password", "expected_status", "description"),
        [
            pytest.param(
                TEST_USER_LOGIN,
                INVALID_USER_PASSWORD,
                400,
                "Корректный логин, неверный пароль",
                id="invalid_password",
            ),
            pytest.param(
                "nonexistent.user@example.com",
                TEST_USER_PASSWORD,
                400,
                "Неверный логин, корректный пароль",
                id="invalid_login",
            ),
            pytest.param(
                "nonexistent.user@example.com",
                INVALID_USER_PASSWORD,
                400,
                "Неверный логин, неверный пароль",
                id="invalid_login_and_pass",
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
        Проверка неуспешной авторизации c неверными учетными данными.

        Ожидаемый результат: статус код 400 Bad Request.
        """
        allure.dynamic.description(
            f"Проверяем, что API возвращает {expected_status} при попытке входа c: {description}"
        )
        logger.info("Тест: %s", description)
        payload = AuthPayload(login=login, password=password)
        response = auth_client.login(payload=payload, expected_status=expected_status)
        assert isinstance(response, APIResponse), (
            f"Ожидался тип APIResponse при статусе {expected_status}"
        )

    @allure.story("Неуспешный вход - Некорректное тело запроса")
    @allure.title("Тест неуспешного входа: {description}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.parametrize(
        ("payload_dict", "expected_status", "description"),
        [
            pytest.param(
                {"login": TEST_USER_LOGIN},
                400,
                "Отсутствует поле password",
                id="missing_password",
            ),
            pytest.param(
                {"password": TEST_USER_PASSWORD},
                400,
                "Отсутствует поле login",
                id="missing_login",
            ),
            pytest.param({}, 400, "Пустое тело запроса", id="empty_payload_400"),
            pytest.param(
                {"login": "", "password": TEST_USER_PASSWORD},
                400,
                "Пустая строка в поле login",
                id="empty_login_str_400",
            ),
            pytest.param(
                {"login": TEST_USER_LOGIN, "password": ""},
                400,
                "Пустая строка в поле password",
                id="empty_pass_str",
            ),
            pytest.param(
                {"login": "не email", "password": TEST_USER_PASSWORD},
                400,
                "Некорректный формат login (не email)",
                id="bad_login_format",
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
        Проверка реакции API на некорректно сформированное тело запроса.

        Ожидаемый результат: код состояния 400 Bad Request.
        """
        allure.dynamic.description(
            f"Проверяем, что API возвращает {expected_status} при отправке некорректного тела: "
            f"{description}"
        )
        logger.info("Тест: %s", description)
        endpoint = APIEndpoints.AUTH
        response = auth_client.http.post(endpoint=str(endpoint), json=payload_dict)
        assert response.status == expected_status, (
            f"Ожидался статус {expected_status}, но получен {response.status}. "
            f"Тело: {response.text()}"
        )
        logger.info("Response status: %s, Body: %s", response.status, response.text())

    @allure.story("Успешный вход")
    @allure.title("Тест успешной авторизации пользователя")
    @allure.description(
        "Проверяем, что при валидных учетных данных возвращается статус 200 и JWT токен."
    )
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_login_success(self, auth_client: AuthClient) -> None:
        """
        Убедитесь в успешной авторизации c помощью действительных учетных данных.

        Ожидаемый результат: статус 200 OK и действительный JWT-токен в ответе.
        """
        logger.info("Тест: Успешная авторизация")
        if not TEST_USER_LOGIN or not TEST_USER_PASSWORD:
            pytest.skip("Пропуск теста: Учетные данные тестового пользователя не настроены.")

        payload = AuthPayload(login=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = auth_client.login(payload=payload, expected_status=200)

        with allure.step("Проверка типа и полей ответа"):  # type: ignore
            assert isinstance(response, AuthSuccessResponse), (
                "Ответ должен быть типа AuthSuccessResponse"
            )
            assert response.auth is True, "Поле 'auth' должно быть true"
            assert response.token is not None, "Поле 'token' не должно быть пустым (None)"
            assert len(response.token) >= 10, (
                f"Длина токена ({len(response.token)}) меньше ожидаемой (>=10)"
            )
        logger.info("Токен успешно получен (первые 10 символов): %s...", response.token[:10])
