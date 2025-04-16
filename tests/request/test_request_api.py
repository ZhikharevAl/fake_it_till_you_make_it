import datetime
import logging
import uuid

import allure
import pytest

from api.request.client import RequestClient
from api.request.models import (
    ActionStep,
    HelperRequirements,
    HelpRequestData,
    Organization,
    RequestContacts,
)
from api.user.models import Location

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

    @allure.feature("Детали запроса (GET /api/request/{id})")
    @allure.story("Получение деталей")
    @allure.title("Тест успешного получения деталей существующего запроса")
    @allure.description(
        "Проверяем получение деталей запроса по существующему ID и валидируем поля."
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_get_request_details_success(self, request_client: RequestClient) -> None:
        """
        Проверка успешного получения деталей существующего запроса.

        Ожидаемый результат: статус 200 и объект HelpRequestData c корректными полями.
        """
        logger.info(
            "Тест: Успешное получение деталей запроса (GET /api/request/%s)", EXISTING_REQUEST_ID
        )
        response = request_client.get_request_details(
            request_id=EXISTING_REQUEST_ID, expected_status=200
        )  # type: ignore

        with allure.step("Проверка типа ответа и основных полей"):  # type: ignore
            assert isinstance(response, HelpRequestData), "Ответ должен быть типа HelpRequestData"
            assert response.id == EXISTING_REQUEST_ID, "ID в ответе не совпадает c запрошенным"
            assert response.title == "Помощь в проекте"

        with allure.step("Проверка данных организации"):  # type: ignore
            assert isinstance(response.organization, Organization)
            assert response.organization.title == "Благотворительная организация"
            assert response.organization.is_verified is True

        with allure.step("Проверка описаний"):  # type: ignore
            assert response.description == "Описание запроса на помощь."
            assert response.goal_description == "Цель данного запроса."

        with allure.step("Проверка плана действий"):  # type: ignore
            assert isinstance(response.actions_schedule, list)
            assert len(response.actions_schedule) == 1
            assert isinstance(response.actions_schedule[0], ActionStep)
            assert response.actions_schedule[0].step_label == "Шаг 1"
            assert response.actions_schedule[0].is_done is True

        with allure.step("Проверка даты окончания"):  # type: ignore
            assert isinstance(response.ending_date, datetime.date)
            assert response.ending_date == datetime.date(2023, 12, 31)

        with allure.step("Проверка локации"):  # type: ignore
            assert isinstance(response.location, Location)
            assert response.location.latitude == 40.712776
            assert response.location.longitude == -74.005974
            assert response.location.district == "Пресненский"
            assert response.location.city == "Москва"

        with allure.step("Проверка контактов"):  # type: ignore
            assert isinstance(response.contacts, RequestContacts)
            assert response.contacts.email == "contact@example.com"
            assert response.contacts.phone == "+123456789"
            assert response.contacts.website == "https://example.com"

        with allure.step("Проверка типов запроса и требований"):  # type: ignore
            assert response.requester_type == "person"
            assert response.help_type == "finance"
            assert isinstance(response.helper_requirements, HelperRequirements)
            assert response.helper_requirements.helper_type == "group"
            assert response.helper_requirements.is_online is True
            assert response.helper_requirements.qualification == "professional"

        with allure.step("Проверка числовых полей"):  # type: ignore
            assert response.contributors_count == 10
            assert response.request_goal == 10000
            assert response.request_goal_current_value == 2500

        logger.info(
            "Получены и провалидированы детали запроса ID: %s, Title: %s",
            response.id,
            response.title,
        )
