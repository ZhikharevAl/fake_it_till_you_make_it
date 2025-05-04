import json
import logging
import uuid
from unittest.mock import Mock

import allure
import pytest

from api.request.client import RequestClient
from api.request.models import HelpRequestData
from tests.mocks.conftest import mock_factory, mock_http_client, mock_request_client  # noqa: F401
from tests.mocks.mock_data import (
    MOCK_HELP_REQUEST_DATA,
    MOCK_NOT_FOUND_404,
    MOCK_REQUESTS_LIST,
    MOCK_SERVER_ERROR_500,
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

    @allure.feature("Список запросов (GET /api/request)")
    @allure.story("Получение списка (Мок)")
    @allure.title("Тест ошибки сервера при получении списка запросов (c MockFactory)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_get_all_requests_error_mocked(
        self,
        mock_request_client: RequestClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка обработки 500 ошибки при получении списка запросов."""
        logger.info("Тест: Ошибка сервера при получении всех запросов (GET /api/request) - MOK 500")
        mock_factory.request.get_all_server_error()
        response = mock_request_client.get_all_requests(expected_status=500)  # type: ignore
        with allure.step("Проверка типа и тела ответа"):  # type: ignore
            assert not isinstance(response, list)
            assert isinstance(response, Mock)
            assert response.status == 500
            try:
                error_body = response.json()
                assert error_body.get("message") == MOCK_SERVER_ERROR_500["message"]
            except json.JSONDecodeError:
                pytest.fail("Тело ответа 500 не является валидным JSON")
        logger.info("Мок-ответ 500 для GET /api/request обработан.")

    @allure.feature("Детали запроса (GET /api/request/{id})")
    @allure.story("Получение деталей (Мок)")
    @allure.title("Тест успешного получения деталей существующего запроса (c MockFactory)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_get_request_details_success_mocked(
        self,
        mock_request_client: RequestClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка получения деталей существующего запроса c моком."""
        logger.info(
            "Тест: Успешное получение деталей запроса (GET /api/request/{id}) - MOK Factory"
        )
        mock_factory.request.get_details_success(request_id=MOCK_EXISTING_REQUEST_ID)
        response = mock_request_client.get_request_details(
            request_id=MOCK_EXISTING_REQUEST_ID, expected_status=200
        )  # type: ignore
        with allure.step("Проверка типа и данных ответа"):  # type: ignore
            assert isinstance(response, HelpRequestData)
            assert response.id == MOCK_HELP_REQUEST_DATA["id"]
            assert response.title == MOCK_HELP_REQUEST_DATA["title"]
            assert response.description == MOCK_HELP_REQUEST_DATA["description"]

        logger.info("Мок-детали запроса успешно получены и проверены.")

    @allure.feature("Детали запроса (GET /api/request/{id})")
    @allure.story("Получение деталей (Мок)")
    @allure.title("Тест получения деталей несуществующего запроса (c MockFactory)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_get_request_details_not_found_mocked(
        self,
        mock_request_client: RequestClient,  # noqa: F811
        mock_factory: MockFactory,  # noqa: F811
    ) -> None:
        """Проверка получения 404 для несуществующего запроса c моком."""
        logger.info(
            "Тест: Получение деталей несуществующего запроса (GET /api/request/{id}) - MOK 404"
        )
        mock_factory.request.get_details_not_found(request_id=MOCK_NON_EXISTENT_REQUEST_ID)
        response = mock_request_client.get_request_details(
            request_id=MOCK_NON_EXISTENT_REQUEST_ID, expected_status=404
        )  # type: ignore
        with allure.step("Проверка типа и тела ответа"):  # type: ignore
            assert not isinstance(response, HelpRequestData)
            assert isinstance(response, Mock)
            assert response.status == 404
            try:
                error_body = response.json()
                assert error_body.get("message") == MOCK_NOT_FOUND_404["message"]
            except json.JSONDecodeError:
                pytest.fail("Тело ответа 404 не является валидным JSON")
