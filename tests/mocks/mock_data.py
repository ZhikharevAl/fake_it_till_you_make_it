# --- Auth ---
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
