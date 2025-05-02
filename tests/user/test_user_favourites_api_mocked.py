import logging

import allure
import pytest

from api.user.client import UserClient
from tests.mocks.conftest import mock_factory, mock_http_client, mock_user_client  # noqa: F401
from tests.mocks.mock_data import (
    MOCK_FAVOURITES_LIST,
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
