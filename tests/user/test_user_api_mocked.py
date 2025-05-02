import datetime
import logging
import uuid

import allure
import pytest

from api.user.client import UserClient
from api.user.models import (
    UserDataResponse,
)
from tests.mocks.conftest import mock_factory, mock_http_client, mock_user_client  # noqa: F401
from tests.mocks.mock_data import (
    MOCK_FAVOURITES_LIST,
    MOCK_USER_DATA,
)
from utils.mock_factory import MockFactory

logger = logging.getLogger(__name__)

# ID для тестов
MOCK_FAV_ID_EXISTS = MOCK_FAVOURITES_LIST[0]
MOCK_NON_EXISTENT_FAV_ID = f"non-existent-fav-{uuid.uuid4()}"


@allure.epic("Управление пользователем (Моки)")
@pytest.mark.user
@pytest.mark.mocked
class TestUserAPIMockedFactory:
    """
    Мок-тесты для GET /api/user и DELETE /api/user/favourites/{id}.

    c использованием MockFactory.
    """

    @allure.feature("Профиль пользователя (GET /api/user)")
    @allure.story("Получение профиля (Мок)")
    @allure.title("Тест успешного получения данных пользователя (c MockFactory)")
    @allure.description(
        "Проверяем получение и валидацию данных профиля при мокированном ответе API."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_user_info_success_mocked(
        self,
        mock_user_client: UserClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка успешного получения UserDataResponse c моком."""
        logger.info("Тест: Успешное получение данных пользователя (GET /api/user) - MOK Factory")
        mock_factory.user.get_info_success()
        response = mock_user_client.get_user_info(expected_status=200)  # type: ignore

        with allure.step("Проверка типа и данных ответа"):  # type: ignore
            assert isinstance(response, UserDataResponse)
            assert response.id == MOCK_USER_DATA["id"]
            assert response.name == MOCK_USER_DATA["name"]
            assert isinstance(response.birthdate, datetime.datetime)
        logger.info("Мок-данные пользователя успешно получены: ID=%s", response.id)
