import logging
from collections.abc import Generator
from typing import Any

import pytest

from api.auth.client import AuthClient
from api.request.client import RequestClient
from api.user.client import UserClient
from core.mock_http_client import MockHTTPClient
from utils.mock_factory import MockFactory, MockHTTPClientProtocol

logger = logging.getLogger(__name__)


@pytest.fixture
def mock_http_client() -> Generator[MockHTTPClient, Any]:
    """Предоставляет экземпляр MockHTTPClient."""
    client = MockHTTPClient()
    yield client
    client.clear_mocks()


@pytest.fixture
def mock_factory(mock_http_client: MockHTTPClientProtocol) -> MockFactory:
    """Предоставляет экземпляр MockFactory."""
    return MockFactory(mock_http_client)


@pytest.fixture
def mock_auth_client(mock_http_client: MockHTTPClient) -> AuthClient:
    """Предоставляет экземпляр AuthClient, использующий MockHTTPClient."""
    return AuthClient(http_client=mock_http_client)


@pytest.fixture
def mock_user_client(mock_http_client: MockHTTPClient) -> UserClient:
    """Предоставляет экземпляр UserClient, использующий MockHTTPClient."""
    return UserClient(http_client=mock_http_client)


@pytest.fixture
def mock_request_client(mock_http_client: MockHTTPClient) -> RequestClient:
    """Предоставляет экземпляр RequestClient, использующий MockHTTPClient."""
    return RequestClient(http_client=mock_http_client)
