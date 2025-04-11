import logging

import pytest
from playwright.sync_api import APIResponse

from api.user.client import UserClient

TEST_REQUEST_ID = "request-id-for-test-123"
ANOTHER_REQUEST_ID = "another-request-id-456"

logger = logging.getLogger(__name__)


@pytest.mark.user
@pytest.mark.favourites
class TestUserFavouritesAPI:
    """Класс тестов для эндпоинтов /api/user/favourites."""

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_favourites_success(self, authenticated_user_client: UserClient) -> None:
        """
        Проверка успешного получения списка избранного для аутентифицированного пользователя.

        Ожидаемый результат: статус 200 и список строк (возможно, пустой).
        """
        logger.info("\nTest: Успешное получение избранного (GET /api/user/favourites)")
        response = authenticated_user_client.get_favourites(expected_status=200)

        assert isinstance(response, list), f"Ожидался тип list, получен {type(response)}"
        if response:
            assert all(isinstance(item, str) for item in response), (
                "He все элементы в списке избранного являются строками"
            )
        logger.info("Получен список избранного: %s", response)

    @pytest.mark.negative
    def test_get_favourites_unauthorized(self, user_client: UserClient) -> None:
        """
        Проверка получения списка избранного без аутентификации.

        Ожидаемый результат: статус 403 Unauthorized.
        """
        logger.info("\nTest: Получение избранного без авторизации (GET /api/user/favourites)")
        response = user_client.get_favourites(expected_status=403)
        assert isinstance(response, APIResponse), "Ожидался сырой ответ APIResponse"
