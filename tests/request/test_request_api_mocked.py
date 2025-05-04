import logging
import uuid

import allure
import pytest

from api.request.client import RequestClient
from api.request.models import HelpRequestData
from tests.mocks.conftest import mock_factory, mock_http_client, mock_request_client  # noqa: F401
from tests.mocks.mock_data import (
    MOCK_HELP_REQUEST_DATA,
    MOCK_REQUESTS_LIST,
)
from utils.mock_factory import MockFactory

logger = logging.getLogger(__name__)


MOCK_EXISTING_REQUEST_ID = MOCK_HELP_REQUEST_DATA["id"]
MOCK_NON_EXISTENT_REQUEST_ID = f"non-existent-req-{uuid.uuid4()}"


@allure.epic("Запросы помощи (Моки)")
@pytest.mark.request
@pytest.mark.mocked
class TestRequestAPIMockedFactory:
    """
    Мок-тесты для эндпоинтов /api/request/*.

    c использованием MockFactory.
    """

    @allure.feature("Список запросов (GET /api/request)")
    @allure.story("Получение списка (Мок)")
    @allure.title("Тест успешного получения списка всех запросов (c MockFactory)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_all_requests_success_mocked(
        self,
        mock_request_client: RequestClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка получения списка запросов c моком."""
        logger.info("Тест: Успешное получение всех запросов (GET /api/request) - MOK Factory")
        mock_factory.request.get_all_success()
        response = mock_request_client.get_all_requests(expected_status=200)  # type: ignore
        with allure.step("Проверка типа и содержимого ответа"):  # type: ignore
            assert isinstance(response, list)
            assert len(response) == len(MOCK_REQUESTS_LIST)
            if response:
                assert isinstance(response[0], HelpRequestData)
                assert response[0].id == MOCK_REQUESTS_LIST[0]["id"]
        logger.info("Мок-список запросов получен.")
