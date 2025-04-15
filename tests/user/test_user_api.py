import logging
import uuid

import allure
import pytest

from api.user.client import UserClient
from api.user.models import Contacts, SocialContacts, UserDataResponse

FAV_REQUEST_ID_TO_TEST = f"test-fav-{uuid.uuid4()}"
NON_EXISTENT_ID = f"non-existent-{uuid.uuid4()}"

logger = logging.getLogger(__name__)


@allure.epic("Управление пользователем")
@pytest.mark.user
class TestUserAPI:
    """Класс тестов для эндпоинтов /api/user и /api/user/favourites/{id}."""

    @allure.feature("Профиль пользователя (GET /api/user)")
    @allure.story("Получение профиля")
    @allure.title("Тест успешного получения данных пользователя")
    @allure.description("Проверяем получение данных профиля для аутентифицированного пользователя.")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_user_info_success(self, authenticated_user_client: UserClient) -> None:
        """
        Проверка успешного получения информации o текущем пользователе.

        Ожидаемый результат: статус 200 и валидные данные пользователя.
        """
        logger.info("Тест: Успешное получение данных пользователя (GET /api/user)")
        response = authenticated_user_client.get_user_info(expected_status=200)  # type: ignore

        with allure.step("Проверка данных пользователя"):  # type: ignore
            assert isinstance(response, UserDataResponse), "Ответ должен быть типа UserDataResponse"
            assert response.id is not None, "Поле 'id' пользователя не должно быть пустым"
            assert isinstance(response.id, str), "Поле 'id' пользователя должно быть типа str"
            assert len(response.base_locations) == 2

            education = response.educations[0]
            assert education is not None
            assert education.model_dump(by_alias=True)["organizationName"] == "НПГУ ДПИ"
            assert education.model_dump(by_alias=True)["level"] == "Высшее"
            assert (
                education.model_dump(by_alias=True)["specialization"]
                == "Районный маркетинговый администратор"
            )
            assert education.model_dump(by_alias=True)["graduationYear"] == 2006
            assert (
                response.additional_info
                == "Очень хороший человек. Добрый, отзывчивый, честный и замечательный"
            ), "Ожидался дополнительная информация o пользователе"

            contacts: Contacts | None = response.contacts
            assert contacts is not None, "Поле 'contacts' не должно быть пустым"
            assert response.status == "Опытный", "Ожидался статус 'Опытный'"
            assert contacts.email == "test@test.com", "Ожидался email 'test@test.com'"
            assert contacts.phone == "+79786959942", "Ожидался телефон '+79786959942'"

            social: SocialContacts | None = contacts.social
            assert social is not None, "Поле 'social' не должно быть пустым"
            assert social.telegram == "@test", "Ожидался telegram '@test'"
            assert social.whatsapp == "@test", "Ожидался whatsapp '@test'"
            assert social.vk == "test@test.com", "Ожидался vk 'test@test.com'"

            assert response.favourite_requests == []
        logger.info("Получены данные пользователя ID: %s", response.id)
