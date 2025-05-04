import datetime
import json
import logging
import uuid
from unittest.mock import Mock

import allure
import pytest

from api.user.client import UserClient
from api.user.models import (
    UserDataResponse,
)
from tests.mocks.conftest import mock_factory, mock_http_client, mock_user_client  # noqa: F401
from tests.mocks.mock_data import (
    MOCK_FAVOURITES_DELETE_SUCCESS_TEXT,
    MOCK_FAVOURITES_ERROR_400,
    MOCK_FAVOURITES_LIST,
    MOCK_UNAUTHORIZED_401,
    MOCK_USER_DATA,
)
from utils.mock_factory import MockFactory

logger = logging.getLogger(__name__)

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

    @allure.feature("Профиль пользователя (GET /api/user)")
    @allure.story("Получение профиля (Мок)")
    @allure.title("Тест получения данных пользователя без аутентификации (c моком 401)")
    @allure.description("Проверяем обработку ответа 401 при мокированном ответе API.")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_get_user_info_unauthorized_mocked(
        self,
        mock_user_client: UserClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка обработки ошибки 401 Unauthorized c мокированным ответом."""
        logger.info("Тест: Получение данных пользователя без авторизации (GET /api/user) - MOK 401")
        mock_factory.user.get_info_unauthorized()
        response = mock_user_client.get_user_info(expected_status=401)  # type: ignore

        with allure.step("Проверка типа ответа и статус кода"):  # type: ignore
            assert not isinstance(response, UserDataResponse), (
                "При ошибке 401 не должен возвращаться UserDataResponse"
            )
            assert isinstance(response, Mock), "Ожидался объект Mock при статусе 401"
            assert response.status == 401, "Ожидался статус 401"
            try:
                error_body = response.json()
                assert error_body.get("message") == MOCK_UNAUTHORIZED_401["message"]
            except json.JSONDecodeError:
                pytest.fail("Тело ответа 401 не является валидным JSON")
        logger.info("Мок-ответ 401 успешно обработан")

    @allure.feature("Избранное пользователя (GET, POST, DELETE)")
    @allure.story("Удаление из избранного (Мок)")
    @allure.title("Тест успешного удаления из избранного (c MockFactory)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_remove_from_favourites_success_mocked(
        self,
        mock_user_client: UserClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка успешного удаления из избранного c моком."""
        logger.info("Тест: Успешное удаление из избранного (DELETE ...) - MOK")
        mock_factory.user.remove_favourite_success(request_id=MOCK_FAV_ID_EXISTS)
        response = mock_user_client.remove_from_favourites(
            request_id=MOCK_FAV_ID_EXISTS, expected_status=200
        )  # type: ignore
        with allure.step("Проверка типа и текста ответа"):  # type: ignore
            assert isinstance(response, Mock), "Ожидался объект Mock при статусе 200 (text/plain)"
            assert response.status == 200
            assert MOCK_FAVOURITES_DELETE_SUCCESS_TEXT in response.text()
        logger.info("Мок-ответ o успешном удалении получен.")

    @allure.feature("Избранное пользователя (GET, POST, DELETE)")
    @allure.story("Удаление из избранного (Мок)")
    @allure.title("Тест удаления несуществующего ID из избранного (c MockFactory)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_remove_from_favourites_not_found_mocked(
        self,
        mock_user_client: UserClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка удаления несуществующего ID c моком 400."""
        logger.info("Тест: Удаление несуществующего ID из избранного (DELETE ...) - MOK 400")
        mock_factory.user.remove_favourite_bad_request(request_id=MOCK_NON_EXISTENT_FAV_ID)
        response = mock_user_client.remove_from_favourites(
            request_id=MOCK_NON_EXISTENT_FAV_ID, expected_status=400
        )  # type: ignore
        with allure.step("Проверка типа и тела ответа"):  # type: ignore
            assert isinstance(response, Mock), "Ожидался объект Mock при статусе 400"
            assert response.status == 400
            try:
                error_body = response.json()
                assert error_body.get("message") == MOCK_FAVOURITES_ERROR_400["message"]
            except json.JSONDecodeError:
                pytest.fail("Тело ответа 400 не является валидным JSON")

    @allure.feature("Избранное пользователя (GET, POST, DELETE)")
    @allure.story("Удаление из избранного (Мок)")
    @allure.title("Тест удаления из избранного без аутентификации (c MockFactory)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_remove_from_favourites_unauthorized_mocked(
        self,
        mock_user_client: UserClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка получения 401 при удалении из избранного без аутентификации."""
        logger.info("Тест: Удаление из избранного без авторизации (DELETE ...) - MOK 401")
        mock_factory.user.remove_favourite_unauthorized(request_id="any-id")
        response = mock_user_client.remove_from_favourites(request_id="any-id", expected_status=401)  # type: ignore
        with allure.step("Проверка типа и тела ответа"):  # type: ignore
            assert isinstance(response, Mock), "Ожидался объект Mock при статусе 401"
            assert response.status == 401
            try:
                error_body = response.json()
                assert error_body.get("message") == MOCK_UNAUTHORIZED_401["message"]
            except json.JSONDecodeError:
                pytest.fail("Тело ответа 401 не является валидным JSON")
        logger.info("Мок-ответ 401 для DELETE favourites успешно обработан.")
