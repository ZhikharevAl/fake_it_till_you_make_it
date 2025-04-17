import logging

import allure
import pytest
from playwright.sync_api import APIResponse

from api.user.client import UserClient
from api.user.models import AddToFavouritesPayload

TEST_REQUEST_ID = "request-id-for-test-123"
ANOTHER_REQUEST_ID = "another-request-id-456"

logger = logging.getLogger(__name__)


@pytest.mark.user
@pytest.mark.favourites
class TestUserFavouritesAPI:
    """Класс тестов для эндпоинтов /api/user/favourites."""

    @allure.story("Получение списка избранного")
    @allure.title("Тест успешного получения списка избранного")
    @allure.description(
        "Проверяем получение списка избранного для аутентифицированного пользователя."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_favourites_success(self, authenticated_user_client: UserClient) -> None:
        """
        Проверка успешного получения списка избранного для аутентифицированного пользователя.

        Ожидаемый результат: статус 200 и список строк (возможно, пустой).
        """
        logger.info("Тест: Успешное получение избранного (GET /api/user/favourites)")
        response = authenticated_user_client.get_favourites(expected_status=200)

        with allure.step("Проверка типа ответа и содержимого списка"):  # type: ignore
            assert isinstance(response, list), f"Ожидался тип list, получен {type(response)}"
            if response:
                assert all(isinstance(item, str) for item in response), (
                    "He все элементы в списке избранного являются строками"
                )
        logger.info("Получен список избранного: %s", response)

    @allure.story("Получение списка избранного")
    @allure.title("Тест получения списка избранного без аутентификации")
    @allure.description("Проверяем, что неавторизованный пользователь получает ошибку 403.")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_get_favourites_unauthorized(self, user_client: UserClient) -> None:
        """
        Проверка получения списка избранного без аутентификации.

        Ожидаемый результат: статус 403 Unauthorized.
        """
        logger.info("Тест: Получение избранного без авторизации (GET /api/user/favourites)")
        response = user_client.get_favourites(expected_status=403)  # Swagger 401
        assert isinstance(response, APIResponse), "Ожидался объект HTTP-ответа"

    @allure.story("Добавление в избранное")
    @allure.title("Тест успешного добавления запроса в избранное")
    @allure.description("Проверяем добавление запроса в избранное и  появление в списке.")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.dependency(name="add_favourite_success")
    def test_add_to_favourites_success(self, authenticated_user_client: UserClient) -> None:
        """
        Проверка успешного добавления запроса в избранное.

        Ожидаемый результат: статус 200 и текстовое сообщение o успехе.
        """
        logger.info(
            "Тест: Успешное добавление в избранное (POST /api/user/favourites), ID: %s",
            TEST_REQUEST_ID,
        )

        payload = AddToFavouritesPayload(requestId=TEST_REQUEST_ID)
        response = authenticated_user_client.add_to_favourites(payload=payload, expected_status=200)  # type: ignore

        with allure.step("Проверка статус кода и текста ответа"):  # type: ignore
            assert isinstance(response, APIResponse), "Ожидался объект HTTP-ответа"
            expected_text = "Запрос успешно добавлен в избранное."
            assert expected_text in response.text(), (
                f"Ожидался текст '{expected_text}', получен '{response.text()}'"
            )
        logger.info("Ответ сервера: %s", response.text())

        with allure.step("Проверка наличия элемента в списке избранного после добавления"):  # type: ignore
            favourites_list = authenticated_user_client.get_favourites(expected_status=200)
            assert isinstance(favourites_list, list)
            assert TEST_REQUEST_ID in favourites_list, (
                f"ID {TEST_REQUEST_ID} не найден в списке избранного после добавления"
            )
            logger.info("Список избранного после добавления: %s", favourites_list)
