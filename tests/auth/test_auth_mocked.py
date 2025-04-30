import logging  # noqa: I001

import allure
import pytest

from api.auth.client import AuthClient
from api.auth.models import AuthPayload, AuthSuccessResponse
from config.config import TEST_USER_LOGIN, TEST_USER_PASSWORD
from tests.mocks.conftest import mock_auth_client, mock_http_client, mock_factory  # noqa: F401
from tests.mocks.mock_data import MOCK_TOKEN
from utils.mock_factory import MockFactory

logger = logging.getLogger(__name__)


@allure.epic("Аутентификация (Моки)")
@allure.feature("Вход пользователя (POST /api/auth)")
@pytest.mark.auth
@pytest.mark.mocked
class TestAuthenticationMockedFactory:
    """
    Мок-тесты для эндпоинта авторизации POST /api/auth.

    Используют MockFactory для настройки ответов.
    """

    @allure.story("Успешный вход (Мок)")
    @allure.title("Тест успешной авторизации пользователя (c MockFactory)")
    @allure.description("Проверяем успешный ответ и валидацию токена при мокированном ответе API.")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_login_success_mocked(
        self,
        mock_auth_client: AuthClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка успешного входа c мокированным ответом 200."""
        logger.info("Тест: Успешная авторизация (Мок Factory)")

        mock_factory.auth.success()

        payload = AuthPayload(login=TEST_USER_LOGIN, password=TEST_USER_PASSWORD)
        response = mock_auth_client.login(payload=payload, expected_status=200)

        with allure.step("Проверка типа и полей ответа"): # type: ignore
            assert isinstance(response, AuthSuccessResponse), (
                "Ответ должен быть типа AuthSuccessResponse"
            )
            assert response.auth is True
            assert response.token == MOCK_TOKEN
        logger.info("Мок-токен успешно получен и провалидирован.")
