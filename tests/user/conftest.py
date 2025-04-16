import logging
from collections.abc import Generator
from typing import Any

import pytest

from api.user.client import UserClient
from api.user.models import AddToFavouritesPayload
from tests.user.test_user_api import FAV_REQUEST_ID_TO_TEST

logger = logging.getLogger(__name__)


@pytest.fixture(name="setup_favourite")
def setup_favourite(authenticated_user_client: UserClient) -> Generator[str, Any]:
    """Фикстура для добавления элемента в избранное перед тестами удаления."""
    logger.info("Setup: Добавление %s в избранное...", FAV_REQUEST_ID_TO_TEST)
    payload = AddToFavouritesPayload(requestId=FAV_REQUEST_ID_TO_TEST)
    try:
        response = authenticated_user_client.add_to_favourites(payload=payload, expected_status=200)  # type: ignore
        assert "Запрос успешно добавлен" in response.text()
        logger.info("Setup: Элемент %s успешно добавлен.", FAV_REQUEST_ID_TO_TEST)
        yield FAV_REQUEST_ID_TO_TEST
    except AssertionError as e:
        logger.exception(
            "Setup: He удалось добавить элемент %s в избранное", FAV_REQUEST_ID_TO_TEST
        )
        pytest.skip(f"He удалось добавить элемент в избранное для тестов удаления: {e}")

    logger.info("Teardown: Попытка удалить %s из избранного...", FAV_REQUEST_ID_TO_TEST)
    try:
        current_favs = authenticated_user_client.get_favourites(expected_status=200)
        if isinstance(current_favs, list) and FAV_REQUEST_ID_TO_TEST in current_favs:
            authenticated_user_client.remove_from_favourites(
                request_id=FAV_REQUEST_ID_TO_TEST, expected_status=200
            )  # type: ignore
            logger.info("Teardown: Элемент %s удален.", FAV_REQUEST_ID_TO_TEST)
        else:
            logger.info("Teardown: Элемент %s уже был удален.", FAV_REQUEST_ID_TO_TEST)
    except Exception as e:  # noqa: BLE001
        message = f"Teardown: He удалось удалить элемент {FAV_REQUEST_ID_TO_TEST}: {e}"
        logger.warning(message)
