from enum import Enum

from config.config import API_PREFIX


class APIEndpoints(Enum):
    """Класс для хранения эндпоинтов API."""

    AUTH = f"{API_PREFIX}/auth"

    USER = f"{API_PREFIX}/user"
    USER_FAVOURITES = f"{API_PREFIX}/user/favourites"
    USER_FAVOURITES_DETAIL = f"{USER_FAVOURITES}/{{requestId}}"

    REQUESTS = f"{API_PREFIX}/request"
    REQUEST_DETAIL = f"{REQUESTS}/{{id}}"
    REQUEST_CONTRIBUTION = f"{REQUEST_DETAIL}/contribution"

    def format(self, **kwargs: str) -> str:
        """Форматирует URL эндпоинта, подставляя значения для path-параметров."""
        return self.value.format(**kwargs)
