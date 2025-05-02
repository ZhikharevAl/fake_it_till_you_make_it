import json
import logging
from unittest.mock import Mock

import allure
import pytest

from api.user.client import UserClient
from tests.mocks.conftest import mock_factory, mock_http_client, mock_user_client  # noqa: F401
from tests.mocks.mock_data import (
    MOCK_FAVOURITES_LIST,
    MOCK_UNAUTHORIZED_401,
)
from utils.mock_factory import MockFactory

logger = logging.getLogger(__name__)


@allure.epic("Управление пользователем (Моки)")
@allure.feature("Избранное пользователя (GET, POST /api/user/favourites)")
@pytest.mark.user
@pytest.mark.favourites
@pytest.mark.mocked
class TestUserFavouritesAPIMockedFactory:
    """
    Мок-тесты для GET и POST /api/user/favourites.

    c использованием MockFactory.
    """

    @allure.story("Получение списка избранного (Мок)")
    @allure.title("Тест успешного получения списка избранного (c MockFactory)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_get_favourites_success_mocked(
        self,
        mock_user_client: UserClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка получения списка избранного c моком."""
        logger.info("Тест: Успешное получение избранного (GET /api/user/favourites) - MOK Factory")
        mock_factory.user.get_favourites_success_list()
        response = mock_user_client.get_favourites(expected_status=200)
        with allure.step("Проверка типа и содержимого ответа"):  # type: ignore
            assert isinstance(response, list)
            assert response == MOCK_FAVOURITES_LIST
        logger.info("Мок-список избранного получен: %s", response)

    @allure.story("Получение списка избранного (Мок)")
    @allure.title("Тест получения списка избранного без аутентификации (c MockFactory)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_get_favourites_unauthorized_mocked(
        self,
        mock_user_client: UserClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка получения 401 при запросе избранного без аутентификации."""
        logger.info(
            "Тест: Получение избранного без авторизации (GET /api/user/favourites) - MOK 401"
        )
        mock_factory.user.get_favourites_unauthorized()
        response = mock_user_client.get_favourites(expected_status=401)
        with allure.step("Проверка типа и тела ответа"):  # type: ignore
            assert isinstance(response, Mock)
            assert response.status == 401
            try:
                error_body = response.json()
                assert error_body.get("message") == MOCK_UNAUTHORIZED_401["message"]
            except json.JSONDecodeError:
                pytest.fail("Тело ответа 401 не является валидным JSON")
        logger.info("Мок-ответ 401 для GET favourites успешно обработан.")
