import datetime

# Auth
MOCK_TOKEN = "mocked-jwt-via-factory-abc123xyz"
MOCK_AUTH_SUCCESS = {"auth": True, "token": MOCK_TOKEN}
MOCK_AUTH_FAILURE_400_CREDENTIALS = {
    "error": "Invalid credentials",
    "message": "Неверный логин или пароль (мок Factory)",
}
MOCK_AUTH_FAILURE_400_BAD_REQUEST = {
    "error": "Bad Request",
    "message": "Некорректный запрос (мок Factory)",
}
MOCK_SERVER_ERROR_500 = {
    "error": "Server error",
    "message": "Запланированная ошибка сервера (мок Factory)",
}

# User
MOCK_UNAUTHORIZED_401 = {
    "error": "Unauthorized",
    "message": "Требуется аутентификация (мок Factory)",
}
MOCK_FORBIDDEN_403 = {"message": "Forbidden (мок Factory)"}
MOCK_USER_DATA = {
    "id": "mock-user-factory-456",
    "name": "Фабрика",
    "lastName": "Моков",
    "birthdate": datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
    "status": "Опытный",
    "baseLocations": [],
    "educations": [],
    "additionalInfo": "Инфо (мок Factory)",
    "contacts": {"email": "factory@example.com", "phone": "+79994445566", "social": {}},
    "favouriteRequests": ["factory-req-1"],
}
MOCK_FAVOURITES_LIST = ["factory-req-1", "factory-req-2"]
MOCK_FAVOURITES_EMPTY = []
MOCK_FAVOURITES_ADD_SUCCESS_TEXT = "Запрос успешно добавлен в избранное."
MOCK_FAVOURITES_DELETE_SUCCESS_TEXT = "Запрос успешно удален из избранного."
MOCK_FAVOURITES_ERROR_400 = {
    "error": "Bad Request",
    "message": "Ошибка операции c избранным (мок Factory)",
}
# --- Request ---
MOCK_HELP_REQUEST_DATA = {
    "id": "mock-factory-request-789",
    "title": "Мок Запрос (Factory)",
    "organization": {"title": "Мок Фонд (Factory)", "isVerified": True},
    "description": "Описание (мок Factory).",
    "goalDescription": "Цель (мок Factory).",
    "actionsSchedule": [],
    "endingDate": datetime.date.today().isoformat(),  # noqa: DTZ011
    "location": None,
    "contacts": {"email": "req.factory@example.com"},
    "requesterType": "organization",
    "helpType": "finance",
    "helperRequirements": None,
    "contributorsCount": 2,
    "requestGoal": 1000,
    "requestGoalCurrentValue": 20,
}
MOCK_REQUESTS_LIST = [MOCK_HELP_REQUEST_DATA]
MOCK_NOT_FOUND_404 = {"error": "Not Found", "message": "Resource не найден (мок Factory)"}
MOCK_CONTRIBUTION_SUCCESS_TEXT = "Вклад успешно внесен."
