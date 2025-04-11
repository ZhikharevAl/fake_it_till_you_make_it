import logging
from typing import Any, NoReturn

import allure
from playwright.sync_api import APIResponse

logger = logging.getLogger(__name__)


def validate_list_of_strings(data: Any) -> list[str]:
    """
    Проверяет, что переданные данные являются списком строк.

    Args:
        data: Данные для проверки (ожидается list).

    Returns:
        List[str]: Валидированный список строк.

    Raises:
        ValueError: Если данные не являются списком строк.
    """
    if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
        raise ValueError("Данные не являются списком строк")
    return data


def handle_api_parsing_error(
    error: Exception, response: APIResponse, context_message: str = "Ошибка обработки ответа"
) -> NoReturn:
    """
    Логирует и выбрасывает AssertionError при ошибке парсинга/валидации ответа API.

    Args:
        error: Исключение, возникшее при обработке.
        response: Сырой ответ APIResponse.
        context_message (str): Дополнительное сообщение для контекста ошибки.

    Raises:
        AssertionError: Оборачивает исходную ошибку.
    """
    error_details = f"{error}\nBody:{response.text()}"
    allure.attach(
        name=f"{context_message}: Ошибка парсинга/валидации",
        body=error_details,
        attachment_type=allure.attachment_type.TEXT,
    )
    msg = f"{context_message}: {error}"
    logger.error(msg, exc_info=True)
    raise AssertionError(msg) from error
