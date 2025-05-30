import json
import logging
from json import JSONDecodeError

import allure
from playwright.sync_api import APIResponse
from pydantic import ValidationError

from api.base_api import BaseAPI
from api.endpoints import APIEndpoints
from api.request.models import HelpRequestData, RequestsListResponse
from utils.helpers import handle_api_parsing_error

logger = logging.getLogger(__name__)


class RequestClient(BaseAPI):
    """API клиент для эндпоинтов, связанных c запросами помощи (/api/request/*)."""

    @allure.step("Получение всех запросов помощи")
    def get_all_requests(self, expected_status: int = 200) -> RequestsListResponse | APIResponse:
        """
        Выполняет GET /api/request. Аутентификация не требуется по Swagger.

        Возвращает список HelpRequestData при успехе (200) или APIResponse при ошибке (500).
        """
        endpoint = APIEndpoints.REQUESTS
        logger.info("Вызов GET %s", endpoint.value)
        response = self.http.get(endpoint=endpoint.value)
        processed_response = self._handle_response(response, expected_status)

        if expected_status == 200:
            try:
                body_json = processed_response.json()
                validated_list = [HelpRequestData.model_validate(item) for item in body_json]
            except (JSONDecodeError, ValidationError, TypeError) as e:
                handle_api_parsing_error(
                    e, processed_response, context_message="Ошибка ответа get_all_requests"
                )
            else:
                allure.attach(
                    name="Список запросов (ответ 200 OK)",
                    body=json.dumps(
                        [m.model_dump(mode="json") for m in validated_list],
                        indent=2,
                        ensure_ascii=False,
                    ),
                    attachment_type=allure.attachment_type.JSON,
                )
                return validated_list
        return processed_response

    @allure.step("Получение деталей запроса помощи: id={request_id}")
    def get_request_details(
        self, request_id: str, expected_status: int = 200
    ) -> HelpRequestData | APIResponse:
        """
        Выполняет GET /api/request/{id}. Аутентификация не требуется по Swagger.

        Возвращает HelpRequestData при успехе (200) или APIResponse при ошибке (400, 404, 500).
        """
        endpoint = APIEndpoints.REQUEST_DETAIL.format(id=request_id)
        logger.info("Вызов GET %s", endpoint)
        response = self.http.get(endpoint=endpoint)
        return self._handle_response(
            response,
            expected_status,
            response_model=HelpRequestData if expected_status == 200 else None,
        )

    @allure.step("Внесение вклада в запрос помощи: id={request_id}")
    def contribute_to_request(self, request_id: str, expected_status: int = 200) -> APIResponse:
        """
        Выполняет POST /api/request/{id}/contribution. Аутентификация не требуется по Swagger.

        Возвращает APIResponse. Тело при успехе (200) - text/plain.
        """
        endpoint = APIEndpoints.REQUEST_CONTRIBUTION.format(id=request_id)
        logger.info("Вызов POST %s", endpoint)
        response = self.http.post(endpoint=endpoint)  # POST без тела
        processed_response = self._handle_response(response, expected_status)
        if response.status == 200 and expected_status == 200:
            allure.attach(
                name="Тело ответа (200 OK, text/plain)",
                body=response.text(),
                attachment_type=allure.attachment_type.TEXT,
            )
        return processed_response
