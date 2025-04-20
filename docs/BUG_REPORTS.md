# 🐞 Баг-репорты по API

Собраны основные проблемы, выявленные при запуске автоматизированных тестов API благотворительного сервиса.

## 🐞 Баг Репорт #1: Некорректная проверка токена (403 Forbidden)

- **Серьезность:** 🔥 Критическая (Critical)
- **Приоритет:** 🔺 Высокий (High)
- **Компонент / Эндпоинты:**
  - `GET /api/request`
  - `GET /api/request/{id}`
  - `POST /api/request/{id}/contribution`
  - `POST /api/auth` (некоторые невалидные запросы)
  - `GET /api/user` (без токена)
  - `DELETE /api/user/favourites/{id}` (без токена)

### 📝 Описание

Многие эндпоинты, которые не требуют авторизации или должны обрабатывать её ошибки, возвращают `403 Forbidden` с телом `{"message":"No token provided."}`. Middleware авторизации работает некорректно — особенно это касается `POST /api/auth`, который не должен требовать токен, так как сам его генерирует.

### 🔁 Шаги для воспроизведения

1. `GET /api/request`
2. `GET /api/request/some-id`
3. `POST /api/request/some-id/contribution`
4. `POST /api/auth` с отсутствующим `password`, `login`, или с невалидным `login`
5. `GET /api/user` без заголовка `Authorization`
6. `DELETE /api/user/favourites/any-id` без заголовка `Authorization`

### ✅ Ожидаемый результат

- **1–3:** `200 OK` (или `404 Not Found`, если ID не существует)
- **4:** `400 Bad Request`
- **5–6:** `401 Unauthorized`

### ❌ Фактический результат

`403 Forbidden`, тело `{"message":"No token provided."}`

---

## 🐞 Баг Репорт #2: Некорректный статус 500 вместо 4xx для ошибок клиента

- **Серьезность:** 🔴 Высокая (Major)
- **Приоритет:** 🔺 Высокий (High)
- **Компонент / Эндпоинты:**
  - `POST /api/auth`
  - `GET /api/user`
  - `GET /api/user/favourites`
  - `GET /api/request/{id}`

### 📝 Описание

API возвращает `500 Internal Server Error` в ситуациях, когда ожидаются ошибки клиента (неверные данные, пустой payload, несуществующий ресурс). Иногда тело ответа содержит `"Planned Server Error"`.

### 🔁 Шаги для воспроизведения

1. `POST /api/auth` с неверным логином/паролем
2. `POST /api/auth` с пустым телом (`{}`)
3. `GET /api/user` (успешный запрос)
4. `GET /api/user/favourites` (успешный запрос)
5. `GET /api/request/{id}` с несуществующим ID

### ✅ Ожидаемый результат

- **1–2:** `400 Bad Request`
- **3–4:** `200 OK`
- **5:** `404 Not Found`

### ❌ Фактический результат

`500 Internal Server Error`, иногда с телом `"Planned Server Error"`

---

## 🐞 Баг Репорт #3: Некорректная логика удаления из избранного

- **Серьезность:** ⚠️ Средняя (Normal)
- **Приоритет:** 🟡 Средний (Medium)
- **Компонент / Эндпоинт:** `DELETE /api/user/favourites/{requestId}`

### 📝 Описание

Если попытаться удалить `requestId`, которого нет в избранном, API всё равно возвращает `200 OK` с сообщением `"Request is removed from Favourites successfully."`, хотя удалять нечего.

### 🔁 Шаги для воспроизведения

1. Получить токен авторизации
2. Отправить `DELETE` на `/api/user/favourites/{non_existent_id}`

### ✅ Ожидаемый результат

`400 Bad Request` или `404 Not Found` (согласно Swagger)

### ❌ Фактический результат

`200 OK`, тело: `"Request is removed from Favourites successfully."`

---

## 🐞 Баг Репорт #4: Неожиданная ошибка при добавлении в избранное

- **Серьезность:** ⚠️ Средняя (Normal)
- **Приоритет:** 🟡 Средний (Medium)
- **Компонент / Эндпоинт:** `POST /api/user/favourites`

### 📝 Описание

При добавлении валидного `requestId` в избранное API возвращает `400 Bad Request` с сообщением `"Failed to add request to favourites"`, без объяснения причины.

### 🔁 Шаги для воспроизведения

1. Получить токен авторизации
2. Отправить `POST` на `/api/user/favourites` с телом:

   ```json
   {
     "requestId": "request-id-1"
   }
   ```

### ✅ Ожидаемый результат

`200 OK`, тело: `"Запрос успешно добавлен в избранное."`

### ❌ Фактический результат

`400 Bad Request`, тело: `"Failed to add request to favourites"`

### 💡 Примечание

Требуется серверное исследование для выяснения причины.

---
