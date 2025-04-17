import logging

import pytest

from api.request.client import RequestClient
from core.http_client import HTTPClient

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", name="request_client")
def request_client(http_client: HTTPClient) -> RequestClient:
    """Предоставляет неаутентифицированный экземпляр клиента API пользователя."""
    logger.info("Создание UserClient...")
    return RequestClient(http_client)
