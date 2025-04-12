import json

import allure
from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from api.endpoints import APIEndpoints
from api.user.models import (
    FavouritesListResponse,
)
from utils.helpers import handle_api_parsing_error, validate_list_of_strings


class UserClient(BaseAPI):
    """API клиент для эндпоинтов, связанных c пользователем (/api/user/*)."""

    def get_favourites(self, expected_status: int = 200) -> FavouritesListResponse | APIResponse:
        """
        Выполняет GET /api/user/favourites. Требует аутентификации.

        Возвращает список ID (List[str]) при успехе (200) или APIResponse при ошибке (403, 500).
        """
        endpoint = APIEndpoints.USER_FAVOURITES
        response = self.http.get(endpoint=endpoint.format())

        processed_response = self._handle_response(response, expected_status)

        if expected_status == 200:
            try:
                body_json = processed_response.json()
                validated_list: FavouritesListResponse = validate_list_of_strings(body_json)

                allure.attach(
                    name="Список избранного (ответ 200 OK)",
                    body=str(validated_list),
                    attachment_type=allure.attachment_type.JSON,
                )
            except (json.JSONDecodeError, ValueError) as e:
                handle_api_parsing_error(
                    e, processed_response, context_message="Ошибка ответа get_favourites"
                )
            else:
                return validated_list
        return processed_response
