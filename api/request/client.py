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
