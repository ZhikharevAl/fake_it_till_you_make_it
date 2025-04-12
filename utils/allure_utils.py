import json
import logging

import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import APIResponse

logger = logging.getLogger(__name__)


class AllureUtils:
    """Утилиты для добавления деталей API ответов в Allure отчеты."""

    @staticmethod
    def attach_response(response: APIResponse) -> None:
        """Добавляет детали ответа API в Allure отчет."""
        # Статус код и URL
        allure.attach(
            body=str(response.status),
            name=f"Status Code: {response.status}",
            attachment_type=AttachmentType.TEXT,
        )
        allure.attach(
            body=response.url,
            name="Request URL",
            attachment_type=AttachmentType.URI_LIST,
        )

        # Заголовки ответа
        try:
            headers_dict: dict[str, str] = response.headers
            headers_json = json.dumps(headers_dict, indent=4, ensure_ascii=False)
            headers_name = "Response Headers (JSON)"
            headers_attach_type = AttachmentType.JSON
        except Exception as e:  # noqa: BLE001
            logger.warning("He удалось сериализовать заголовки ответа для Allure: %s", e)
            try:
                headers_raw = str(response.headers)
            except Exception:  # noqa: BLE001
                headers_raw = "[He удалось получить заголовки]"
            headers_json = headers_raw
            headers_name = "Response Headers (Raw)"
            headers_attach_type = AttachmentType.TEXT
        allure.attach(
            body=headers_json,
            name=headers_name,
            attachment_type=headers_attach_type,
        )

        # Тело ответа
        formatted_body: str
        attach_type: AttachmentType
        body_name: str

        try:
            response_json = response.json()
            formatted_body = json.dumps(response_json, indent=4, ensure_ascii=False)
            attach_type = AttachmentType.JSON
            body_name = "Response Body (JSON)"

        except json.JSONDecodeError:
            logger.warning("Ответ не является валидным JSON, аттачим как текст.")
            try:
                formatted_body = response.text() or "[Тело ответа пустое]"
            except Exception as text_error:  # noqa: BLE001
                logger.warning("He удалось прочитать тело ответа как текст: %s", text_error)
                formatted_body = f"[He удалось прочитать тело ответа: {text_error!s}]"
            attach_type = AttachmentType.TEXT
            body_name = "Response Body (Text)"

        except Exception as e:  # noqa: BLE001
            logger.warning("He удалось получить тело ответа для Allure: %s", e)
            formatted_body = f"[He удалось обработать тело ответа: {e!s}]"
            attach_type = AttachmentType.TEXT
            body_name = "Response Body (Error)"

        allure.attach(
            body=formatted_body,
            name=body_name,
            attachment_type=attach_type,
        )
