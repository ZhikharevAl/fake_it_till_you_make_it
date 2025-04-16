import logging
import uuid

import allure
import pytest

from api.request.client import RequestClient
from api.request.models import HelpRequestData

EXISTING_REQUEST_ID = "request-id-1"
NON_EXISTENT_REQUEST_ID = f"non-existent-{uuid.uuid4()}"

logger = logging.getLogger(__name__)


@allure.epic("Запросы помощи")
@pytest.mark.request
class TestRequestAPI:
    """Класс тестов для эндпоинтов /api/request/*."""

    @allure.feature("Список запросов (GET /api/request)")
    @allure.story("Получение списка")
    @allure.title("Тест успешного получения списка всех запросов помощи")
    @allure.description(
        "Проверяем получение списка всех запросов, ожидаем статус 200 и массив данных."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_all_requests_success(self, request_client: RequestClient) -> None:
        """
        Проверка успешного получения списка всех запросов помощи.

        Ожидаемый результат: статус 200 и список объектов HelpRequestData.
        """
        logger.info("Тест: Успешное получение всех запросов (GET /api/request)")
        response = request_client.get_all_requests(expected_status=200)  # type: ignore

        with allure.step("Проверка типа ответа и содержимого списка"):  # type: ignore
            assert isinstance(response, list), f"Ожидался тип list, получен {type(response)}"
            if response:
                assert isinstance(response[0], HelpRequestData), (
                    "Элементы списка должны быть типа HelpRequestData"
                )
                logger.info("Получено %s запросов. Первый ID: %s", len(response), response[0].id)
            else:
                logger.info("Получен пустой список запросов.")
