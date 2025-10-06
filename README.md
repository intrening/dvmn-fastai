# FastAI

FastAI — бэкенд-сервис на FastAPI, который по текстовому запросу собирает статический сайт: генерирует HTML, подбирает изображения и делает превью страницы. Это помогает быстро прототипировать лендинги и демо-проекты без участия фронтенда.

## Чем полезен проект

- API для создания и генерации сайтов, потоковая отдача HTML позволяет клиенту видеть результат в реальном времени.
- Автоматическая выгрузка HTML и ресурсов в S3-совместимое хранилище для последующей публикации.

## Внешние сервисы и интеграции

- DeepSeek API — генерация текстовых блоков и описаний.
- Unsplash API — подбор изображений для секций страницы.
- Gotenberg — создание скриншотов сгенерированного HTML.
- S3/MinIO — хранение HTML и превью.

Подробные инструкции по локальному разворачиванию и дев-среде описаны в [CONTRIBUTING.md](./CONTRIBUTING.md).

## Быстрый старт

### Установка зависимостей
- Установите менеджер пакетов [uv](https://docs.astral.sh/uv/getting-started/).
- В корне репозитория выполните команду, которая создаст виртуальное окружение, скачает Python 3.13 и установит зависимости:
  ```bash
  uv sync
  ```
- Скопируйте шаблон переменных окружения и заполните значения, пользуясь описанием ниже:
  ```bash
  cp example.env .env
  ```

### Запуск приложения
- Запустите сервер в режиме разработки (команда работает без явной активации `.venv`, uv сделает это сам):
  ```bash
  uv run fastapi dev src/main.py
  ```
- После запуска приложение доступно в браузере по адресу `http://127.0.0.1:8000/`, API-документация — на `http://127.0.0.1:8000/frontend-api/docs`.

### Пример вывода в консоль
```console
$ uv run fastapi dev src/main.py
INFO     Using uvicorn with autoreload
INFO     Will watch for changes in these directories: ['/Users/nick/Github/fastai']
INFO     Application startup complete.
INFO     Uvicorn running on http://127.0.0.1:8000 (CTRL+C to quit)
```

Чтобы остановить сервер, нажмите `Ctrl+C` в терминале.

---

## Использование файла окружения `.env`

Для корректной работы проекта требуется создать файл `.env` на основе шаблона `example.env`, который находится в корне репозитория.

### Шаги по настройке:

1. Скопируйте файл-шаблон:
   ```bash
   cp example.env .env
   ```
2. Заполните значения переменных в `.env` согласно описанию ниже.

---

## Описание необходимых переменных

### Общие переменные

- `DEBUG` — режим отладки (`True` или `False`).

### Переменные для DeepSeek API

- `DEEPSEEK__API_KEY` — API-ключ для доступа к DeepSeek.
- `DEEPSEEK__MAX_CONNECTIONS` — максимальное количество одновременных соединений (опционально).
- `DEEPSEEK__TIMEOUT` — таймаут запросов в секундах (по умолчанию 120).
- `DEEPSEEK__BASE_URL` — базовый URL для API DeepSeek (по умолчанию: `https://api.deepseek.com/v1`).
- `DEEPSEEK__MODEL` — название используемой модели DeepSeek (по умолчанию: `deepseek-chat`).

**Где получить:**  
Зарегистрируйтесь и получите API-ключ на [DeepSeek API](https://platform.deepseek.com/docs/overview/authentication).

### Переменные для Unsplash API

- `UNSPLASH__APP_ID` — ID приложения Unsplash.
- `UNSPLASH__ACCESS_KEY` — Access Key для Unsplash API.
- `UNSPLASH__SECRET_KEY` — Secret Key для Unsplash API.
- `UNSPLASH__MAX_CONNECTIONS` — максимальное количество одновременных соединений (опционально).
- `UNSPLASH__TIMEOUT` — таймаут запросов в секундах (по умолчанию 20).

**Где получить:**
Создайте приложение и получите ключи на [Unsplash Developers](https://unsplash.com/documentation#registering-your-application).

### Переменные для Gotenberg API

- `GOTENBERG__URL` — URL сервиса Gotenberg для создания скриншотов (по умолчанию: `https://demo.gotenberg.dev`).
- `GOTENBERG__SCREENSHOT_WIDTH` — ширина скриншота в пикселях (по умолчанию: 600).
- `GOTENBERG__SCREENSHOT_FORMAT` — формат скриншота: `png`, `jpeg` или `webp` (по умолчанию: `png`).
- `GOTENBERG__MAX_CONNECTIONS` — максимальное количество одновременных соединений (по умолчанию: 5).
- `GOTENBERG__TIMEOUT` — таймаут запросов в секундах (по умолчанию: 10).
- `GOTENBERG__WAIT_DELAY` — задержка перед созданием скриншота в секундах, должна быть строго меньше `TIMEOUT` (по умолчанию: 8).

**Где получить:**
Gotenberg — это open-source сервис для конвертации документов и создания скриншотов. Вы можете использовать публичное демо `https://demo.gotenberg.dev` или развернуть собственный инстанс. Подробнее на [Gotenberg](https://gotenberg.dev/).

### Переменные для S3

- `S3__ACCESS_KEY` — access key для подключения к S3/MinIO.
- `S3__SECRET_KEY` — secret key для авторизации в S3/MinIO.
- `S3__ENDPOINT_URL` — адрес S3-совместимого хранилища.
- `S3__BUCKET_NAME` — имя бакета, куда складываются сгенерированные файлы.
- `S3__READ_TIMEOUT` — _опционально_, таймаут чтения запросов (по умолчанию: 20).
- `S3__CONNECT_TIMEOUT` — _опционально_, таймаут подключения (по умолчанию: 10).
- `S3__MAX_POOL_CONNECTIONS` — _опционально_, лимит одновременных соединений клиента (по умолчанию: 10).
