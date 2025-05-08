# Проект автоматизации тестирования API "Charity Event"

[![Code Quality](https://github.com/ZhikharevAl/fake_it_till_you_make_it/actions/workflows/code-quality.yaml/badge.svg)](https://github.com/ZhikharevAl/fake_it_till_you_make_it/actions/workflows/code-quality.yaml) ![Codecov](https://img.shields.io/codecov/c/github/ZhikharevAl/fake_it_till_you_make_it) ![Ruff](https://img.shields.io/badge/linting-Ruff-323330?logo=ruff) ![uv](https://img.shields.io/badge/dependencies-uv-FFA500) ![Pyright](https://img.shields.io/badge/typing-Pyright-007ACC) [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ZhikharevAl/fake_it_till_you_make_it) ![License](https://img.shields.io/badge/License-MIT-blue.svg)

## Описание

Этот репозиторий содержит набор автоматизированных тестов для API бэкенда "ExpressJS API". Проект был разработан на основе хакатона на тему **"Помощь пожилым людям"**. Цель проекта — обеспечить качество и стабильность API, используемого для управления пользователями, их авторизацией, избранными запросами и запросами о помощи.

Тесты написаны на Python с использованием pytest и Playwright (для взаимодействия с API).

## Содержание

* [Основные возможности и покрытие](#основные-возможности-и-покрытие)
* [Технологический стек](#технологический-стек)
* [Структура проекта](#структура-проекта)
* [Установка и настройка](#установка-и-настройка)
* [Запуск тестов](#запуск-тестов)
  * [Локальный запуск pytest](#локальный-запуск-pytest)
  * [Запуск в контейнерах Podman (сеть)](#запуск-в-контейнерах-podman-сеть)
  * [Просмотр отчетов](#просмотр-отчетов)
* [Тестирование с Моками](#тестирование-с-моками)
* [CI/CD](#инструменты-контроля-качества)
* [Планы и улучшения](#планы-и-улучшения)

## Основные возможности и покрытие

На данный момент проект включает тесты для следующих эндпоинтов:

* **Аутентификация:**
  * `POST /api/auth`: Вход пользователя и получение JWT токена.
* **Управление пользователем:**
  * `GET /api/user`: Получение данных профиля текущего пользователя.
  * `GET /api/user/favourites`: Получение списка избранных запросов.
  * `POST /api/user/favourites`: Добавление запроса в избранное.
  * `DELETE /api/user/favourites/{requestId}`: Удаление запроса из избранного.
* **Запросы помощи:**
  * `GET /api/request`: Получение списка всех запросов помощи.
  * `GET /api/request/{id}`: Получение деталей конкретного запроса.
  * `POST /api/request/{id}/contribution`: Внесение вклада в запрос.

## Технологический стек

* **Язык:** Python 3.13+
* **Тест-фреймворк:** pytest
* **HTTP Клиент:** Playwright (APIRequestContext)
* **Валидация данных:** Pydantic
* **Отчетность:** Allure Report
* **Мокирование:** `unittest.mock` (через `MockHTTPClient` и `MockFactory`)
* **Менеджер пакетов:** uv
* **Контейнеризация:** Podman
* **CI/CD:** GitHub Actions

## Структура проекта

```bash
.
├── .github/          # Настройки CI/CD (GitHub Actions)
│   ├── actions/      # Reusable actions (setup, run-linters)
│   └── workflows/    # Пайплайны CI/CD
├── api/              # Клиенты API и модели данных (Pydantic)
│   ├── auth/
│   ├── request/
│   └── user/
├── config/           # Конфигурационные файлы (базовый URL, таймауты)
├── core/             # Базовые компоненты фреймворка (HTTP клиент, MockHTTPClient)
├── tests/            # Тестовые сценарии pytest
│   ├── auth/         # Тесты аутентификации (+ test_auth_api_mocked.py)
│   ├── mocks/        # Инфраструктура для мок-тестов (фикстуры, хендлеры, данные)
│   ├── request/      # Тесты запросов помощи (+ test_request_api_mocked.py)
│   └── user/         # Тесты пользователя (+ test_user_api_mocked.py)
├── utils/            # Вспомогательные утилиты (Allure, хелперы, MockFactory)
├── .env.example      # Пример файла с переменными окружения
├── .gitignore
├── Containerfile        # Containerfile для сборки образа тестов
├── pyproject.toml    # Определение зависимостей и конфигурация инструментов
└── README.md
```

## Установка и настройка

1. **Клонировать репозиторий:**

    ```bash
    git clone https://github.com/ZhikharevAl/fake_it_till_you_make_it.git
    cd fake_it_till_you_make_it
    ```

2. **Установить Python** (версия 3.13 или выше).
3. **Установить `uv`** (если еще не установлен):

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Не забудьте добавить путь к uv в PATH
    ```

4. **Создать и активировать виртуальное окружение**:

    ```bash
    uv venv
    source .venv/bin/activate # Linux/macOS
    # .\.venv\Scripts\activate # Windows
    ```

5. **Установить зависимости:**

    ```bash
    uv pip install -e '.[dev]'
    ```

6. **Настроить окружение:**
    * Создайте файл `.env` из `.env.example` (если его нет).
    * Заполните `.env` необходимыми значениями: `API_BASE_URL`, `TEST_USER_LOGIN`, `TEST_USER_PASSWORD`, `INVALID_USER_PASSWORD`. **Примечание:** `API_BASE_URL` будет разным для локального запуска и запуска в Podman (см. ниже).

## Запуск тестов

### Локальный запуск pytest

Этот способ подходит, если API сервер запущен локально (не в контейнере).

1. **Убедитесь, что API сервер запущен** и доступен по адресу, указанному в `API_BASE_URL` вашего `.env` файла (например, `http://localhost:4040`).
2. **Активируйте виртуальное окружение**: `source .venv/bin/activate`.
3. **Запустите все тесты:**

    ```bash
    pytest
    ```

4. **Запустите только интеграционные тесты:**

    ```bash
    pytest -m "not mocked"
    ```

5. **Запустите только мок-тесты:**

    ```bash
    pytest -m mocked
    ```

### Запуск в контейнерах Podman (сеть)

Этот способ запускает и API сервер, и тесты в отдельных контейнерах, соединенных через сеть Podman. Это обеспечивает лучшую изоляцию.

**Предварительные требования:**

* Установлен Podman.  [Инструкции по установке](https://podman.io/getting-started/installation).
* Собран образ для API сервера (например, `api-server-image:local`). [Инструкции по сборке](https://github.com/ZhikharevAl/charity_event_comeback_oct2024.git).
* Собран образ для тестов из этого репозитория (например, `charity-tests-runner:local`):

  ```bash
  podman build -t charity-tests-runner:local -f Containerfile .
  ```

**Шаги запуска:**

1. **Создайте сеть Podman** (если еще не создана):

    ```bash
    podman network create my-test-net
    ```

2. **Настройте `.env` файл:** Убедитесь, что в вашем `.env` файле (в корне этого репозитория) `API_BASE_URL` указывает на имя контейнера сервера и его внутренний порт:

    ```dotenv
    API_BASE_URL=http://api-server:4040
    # Остальные переменные TEST_USER_LOGIN и т.д.
    ```

3. **Запустите контейнер с API сервером** в созданной сети:

    ```bash
    podman run -d --rm --network my-test-net --name api-server api-server-image:local
    ```

    * `-d`: фоновый режим.
    * `--rm`: удалить контейнер после остановки.
    * `--network my-test-net`: подключить к сети.
    * `--name api-server`: дать имя контейнеру (важно для `API_BASE_URL`).
    * `api-server-image:local`: **Замените** на имя и тег вашего локально собранного образа сервера.
    * *(Опционально)* Добавьте `-p 4040:4040`, если хотите иметь доступ к API и с хост-машины.

4. **Запустите контейнер с тестами** в той же сети, передав `.env` файл:

    ```bash
    podman run --rm --network my-test-net --env-file .env charity-tests-runner:local
    ```

    * `--network my-test-net`: подключить к той же сети.
    * `--env-file .env`: передать переменные из `.env` файла.
    * `charity-tests-runner:local`: **Замените** на имя и тег вашего локально собранного образа тестов.
    * *(Опционально)* Добавьте `-v $(pwd)/allure-results:/app/allure-results`, чтобы сохранить Allure результаты на хост.

5. **Остановите контейнер сервера** после завершения тестов:

    ```bash
    podman stop api-server
    ```

<pre lang="markdown">
┌────────────────────────────┐
│    Podman Network:         │
│      my-test-net           │
│                            │
│  ┌──────────────────────┐  │
│  │  Container:          │  │
│  │  api-server          │  │
│  │  Image:              │  │
│  │  api-server-image:   │  │
│  │  local               │  │
│  │  Port: 4040          │  │
│  └──────────────────────┘  │
│              ▲             │
│              │             │  HTTP Requests
│              ▼             │
│  ┌──────────────────────┐  │
│  │  Container:          │  │
│  │  charity-tests-runner│  │
│  │  Image:              │  │
│  │  charity-tests-runner│  │
│  │  :local              │  │
│  └──────────────────────┘  │
│                            │
└────────────────────────────┘
</pre>

### Просмотр отчетов

1. **Сгенерируйте Allure отчет** (если запускали с `--alluredir`):

    ```bash
    allure generate allure-results --clean
    ```

2. **Откройте отчет в браузере:**

    ```bash
    allure open
    ```

    Или используйте `allure serve allure-results`.

## Тестирование с Моками

В проекте реализованы мок-тесты для изоляции от реального бэкенда и обеспечения стабильности и скорости CI.

* **Подход:** Используется **мокирование на уровне Python клиента** с помощью библиотеки `unittest.mock`. Создан специальный класс `MockHTTPClient` (`core/mock_http_client.py`), который наследуется от реального `HTTPClient`, но перехватывает вызовы методов (`get`, `post` и т.д.) и возвращает заранее настроенные ответы (`unittest.mock.Mock`), имитирующие `APIResponse`. Для удобной настройки этих мок-ответов используется класс-фабрика `MockFactory` (`utils/mock_factory.py`).
* **Структура:** Инфраструктура для моков (фикстуры для `MockHTTPClient` и `MockFactory`, мок-данные) находится в папке `tests/mocks/`. Тестовые файлы с моками (например, `test_auth_api_mocked.py`) используют фикстуры мокированных API клиентов (например, `mock_auth_client`) и `MockFactory` для настройки ожидаемых ответов перед вызовом методов клиента.
* **Запуск:** Мок-тесты помечены маркером `mocked` (`pytest -m mocked`).

## Инструменты контроля качества

Проект использует GitHub Actions для автоматической проверки качества кода (linting, formatting, type checking) и запуска тестов при каждом пуше. Используется Podman для запуска интеграционных тестов в контейнеризованном окружении. Результаты тестов и отчет о покрытии загружаются автоматически. Allure отчет генерируется и деплоится на GitHub Pages.

**Интеграция в рабочий процесс разработки**
![Интеграция](./attachment/integretion.png)

**Allure отчёт**
![Allure All Tests](./attachment/allure-all-test-06-05-2025.png)
![Allure Report](./attachment/allure-report.png)

**Покрытие тестами**
![Codecov Coverage](./attachment/codecov.png)
![Codecov Coverage](./attachment/codecov_05-05-2025.png)

## Планы и улучшения

* **Стабилизация API:** Основная цель — добиться стабильной работы реального API сервера, чтобы убрать метки `xfail` из интеграционных тестов.
* **Расширение покрытия:** Добавить больше негативных тестов, тестов на граничные значения для всех эндпоинтов (как интеграционных, так и моков).
* **Улучшение обработки данных:** Использовать фабрики данных или `faker` для генерации тестовых данных, особенно в моках.
* **Визуализация результатов:** Рассмотреть интеграцию с Grafana (через TSDB или Allure TestOps) для отслеживания динамики качества тестов.
