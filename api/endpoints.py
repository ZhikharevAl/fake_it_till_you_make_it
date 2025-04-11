from enum import Enum

from config.config import API_PREFIX


class APIEndpoints(Enum):
    """Класс для хранения эндпоинтов API."""

    AUTH = f"{API_PREFIX}/auth"
    USER = f"{API_PREFIX}/user"
    USER_FAVOURITES = f"{API_PREFIX}/user/favourites"

    def format(self, **kwargs: str) -> str:
        """Форматирует URL эндпоинта, подставляя значения для path-параметров."""
        return self.value.format(**kwargs)
