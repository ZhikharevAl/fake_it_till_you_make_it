# Успешный ответ для /api/auth
MOCK_AUTH_SUCCESS = {
    "auth": True,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY4MTMyYmU1LWI5MzEtNGU0Mi1iMGEyLWUzYjZkYzkwY2NkYyIsImlhdCI6MTc0NDkzNDg3NCwiZXhwIjoxNzQ0OTM4NDc0fQ.Dncd86bi-n39dRzSbsuYxqBWH_PXqQSb9GediREUtq0",  # noqa: E501
}

# Ошибка 400 для /api/auth
MOCK_AUTH_FAILURE_400 = {"error": "Invalid credentials", "message": "Неверный логин или пароль"}

# Ошибка 403 (например, для токена)
MOCK_FORBIDDEN_403 = {"message": "No token provided."}

# Ошибка 401
MOCK_UNAUTHORIZED_401 = {"error": "Unauthorized", "message": "Требуется аутентификация"}

# Ошибка 500
MOCK_SERVER_ERROR_500 = {
    "error": "Internal Server Error",
    "message": "Запланированная ошибка сервера",
}
