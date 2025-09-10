# FastAI

## Репозиторий для бэкенд-разработчиков.

Инструкции и справочная информация по разворачиванию локальной инсталляции собраны
в документе [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Использование файла окружения `.env`

Для корректной работы проекта требуется создать файл `.env` на основе шаблона `example.env`, который находится в корне репозитория.  
**Внимание:** файл `.env` должен быть добавлен в `.gitignore` и не попадать в систему контроля версий, так как содержит чувствительные данные (API-ключи и секреты).

### Шаги по настройке:

1. Скопируйте файл-шаблон:
   ```bash
   cp example.env .env
   ```
2. Заполните значения переменных в `.env` согласно описанию ниже.

---

## Описание необходимых переменных

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

### Общие переменные

- `DEBUG` — режим отладки (`True` или `False`).

---

**Важно:**  
Не публикуйте и не передавайте файл `.env` третьим лицам.  
Убедитесь, что `.env` добавлен в `.gitignore`!
