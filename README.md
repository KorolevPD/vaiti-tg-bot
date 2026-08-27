# Vaiti Telegram Bot

Telegram-бот карьерного сервиса [«Вайти»](https://vaiti.tech/). Бот работает как пользовательский интерфейс к backend-сервисам: помогает пользователям управлять резюме, искать вакансии и компании, генерировать сопроводительные письма, проходить тренажер собеседований, смотреть статистику и отправлять обращения в поддержку.

## Описание

Проект представляет собой Telegram-бота на `aiogram 3` и небольшое HTTP API на `FastAPI`.

Бот запускается в одном приложении с API и поддерживает два способа получения обновлений от Telegram:

- `polling` - бот сам запрашивает обновления у Telegram;
- `webhook` - Telegram отправляет обновления на HTTP endpoint приложения.

Основная логика бота вынесена в роутеры по пользовательским разделам:

- главное меню;
- профиль;
- компании и отзывы;
- каталог навыков;
- вакансии;
- статистика откликов;
- резюме;
- генерация сопроводительных писем;
- тренажер собеседований;
- поддержка.

Дополнительно приложение предоставляет API endpoint для отправки уведомлений пользователям по Telegram ID.

## Архитектура

Проект построен слоями:

```text
main.py
├── FastAPI app
│   ├── /api/v1/notifications/send
│   └── webhook endpoint, если выбран BOT_UPDATE_METHOD=webhook
│
├── aiogram Bot + Dispatcher
│   ├── bot routers
│   ├── FSM storage
│   └── AuthMiddleware
│
├── app/bot
│   ├── routers/              # Telegram-разделы и команды
│   ├── flows/                # составные пользовательские сценарии
│   ├── middlewares/          # middleware авторизации
│   └── redis/                # key builders и вспомогательные ключи
│
├── app/services
│   ├── auth/                 # авторизация Telegram-пользователя во внешнем API
│   ├── vacancies/            # вакансии и взаимодействия с ними
│   ├── companies/            # компании и отзывы
│   ├── resume/               # резюме
│   ├── cover_letters/        # генерация и хранение черновиков сопроводительных писем
│   ├── trainer/              # тренажер собеседований
│   ├── knowledge/            # дерево специализаций, навыки и типовые вопросы
│   ├── application/          # статистика откликов
│   └── support/              # обратная связь
│
├── app/clients
│   ├── APIClient             # общий httpx-клиент для backend API
│   ├── redis/                # подключение к Redis
│   └── proxy/                # Telegram proxy session
│
└── app/core
    ├── config.py             # настройки через переменные окружения
    └── logging.yaml          # конфигурация логирования
```

### Поток обработки Telegram-события

1. Telegram update попадает в `Dispatcher` через polling или webhook.
2. `AuthMiddleware` получает Telegram-пользователя и запрашивает auth header во внешнем сервисе `SERVICES_URL`.
3. Если Redis доступен, auth header кешируется по ключу `tg-bot:auth:<telegram_id>` на 15 минут.
4. Роутер обрабатывает команду, callback или состояние FSM.
5. При необходимости сервисный слой обращается во внешний backend API.
6. Бот отправляет пользователю сообщение, файл или inline-клавиатуру.

## Технологический стек

- Python 3.11+
- aiogram 3 - Telegram Bot API framework
- FastAPI - HTTP API и webhook endpoint
- Uvicorn - ASGI-сервер
- httpx - асинхронные HTTP-запросы к backend API
- Redis - FSM storage, кеш авторизации и временные данные
- Pydantic / pydantic-settings - схемы данных и конфигурация
- PyYAML - чтение конфигурации прокси
- aiohttp-socks - SOCKS/proxy-сессии для Telegram
- Poetry - управление зависимостями
- Docker - контейнеризация приложения

## Переменные окружения

Настройки читаются из переменных окружения или файла `.env` в корне проекта.

| Переменная | Обязательная | По умолчанию | Описание |
| --- | --- | --- | --- |
| `BOT_TOKEN` | да | - | Токен Telegram-бота от BotFather. |
| `SERVICES_URL` | нет | `http://caddy` | Базовый URL внешнего backend API сервиса «Вайти». |
| `BOT_SUPPORT_USERNAME` | нет | `vaiti_support` | Username поддержки, который используется в сценариях поддержки. |
| `BOT_UPDATE_METHOD` | нет | `polling` | Способ получения обновлений: `polling` или `webhook`. |
| `WEBHOOK_DOMAIN` | для webhook | - | Домен, на котором доступно приложение. |
| `WEBHOOK_PATH` | для webhook | - | Путь webhook endpoint. |
| `WEBHOOK_SECRET` | для webhook | - | Секрет для проверки заголовка `X-Telegram-Bot-Api-Secret-Token`. |
| `REDIS_HOST` | нет | - | Host Redis. Если не задан, используется `MemoryStorage`. |
| `REDIS_PORT` | нет | - | Port Redis. Если не задан, используется `MemoryStorage`. |
| `REDIS_PASSWORD` | нет | - | Пароль Redis. |
| `REDIS_KEY_PREFIX` | нет | `tg-bot` | Префикс ключей Redis. |

Пример `.env` для локального запуска через polling:

```env
BOT_TOKEN=123456:telegram_bot_token
SERVICES_URL=http://localhost:8081
BOT_UPDATE_METHOD=polling

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_KEY_PREFIX=tg-bot
```

Пример webhook-настроек:

```env
BOT_TOKEN=123456:telegram_bot_token
SERVICES_URL=https://api.example.com
BOT_UPDATE_METHOD=webhook
WEBHOOK_DOMAIN=bot.example.com
WEBHOOK_PATH=telegram/webhook
WEBHOOK_SECRET=change-me
```

Если рядом с приложением доступен файл `../config/proxies.yaml`, бот попытается загрузить из него список Telegram-прокси. При ошибке чтения прокси приложение продолжит запуск без них.

## Бизнес-логика

### Авторизация

Каждый пользователь Telegram проходит авторизацию через внешний backend API. Middleware отправляет данные Telegram-пользователя в `/api/v1/auth/telegram`, получает auth header и передает его в обработчики. Этот header используется сервисами для запросов, требующих авторизации.

### Главное меню

Команды `/start` и `/menu` сбрасывают текущее FSM-состояние и показывают главное меню. Через меню пользователь переходит в основные разделы бота.

### Вакансии

Бот обращается к backend API для поиска вакансий, просмотра карточки вакансии и записи взаимодействий пользователя с вакансией. Основные endpoint'ы:

- `POST /api/v1/vacancies/search`
- `GET /api/v1/vacancies/{vacancy_id}`
- `POST /api/v1/profile/interactions/`

### Компании

Пользователь может просматривать список компаний, искать компанию, смотреть карточку, читать отзывы и добавлять собственные отзывы.

### Резюме

Раздел резюме поддерживает:

- список резюме пользователя;
- просмотр детальной информации;
- создание резюме из JSON-данных;
- загрузку файла резюме;
- редактирование и удаление;
- выбор основного резюме;
- экспорт резюме в PDF;
- получение черновика резюме.

### Сопроводительные письма

Бот может отправлять запрос на генерацию сопроводительного письма и получать готовый черновик. Временное хранение данных черновиков реализовано через Redis при наличии подключения.

### Тренажер собеседований

Пользователь запускает тренировочную сессию собеседования, получает вопросы, отправляет ответы, завершает интервью и получает результат. Сессии обслуживаются внешним backend API.

### Каталог навыков и база знаний

Бот получает дерево специализаций, матрицу домена, типовые вопросы и инструменты/навыки из knowledge-сервиса backend API.

### Статистика

Бот запрашивает статистику откликов за выбранный период через сервис application stats.

### Поддержка

Пользователь может отправить обратную связь. Бот передает обращение во внешний backend API через `/api/v1/support/feedback`.

### Уведомления

FastAPI endpoint `POST /api/v1/notifications/send` отправляет сообщение списку пользователей по Telegram ID и возвращает статус по каждому пользователю:

- `ok` - сообщение отправлено;
- `bot_blocked` - пользователь заблокировал бота;
- `not_found` - чат не найден;
- `error: ...` - другая ошибка Telegram API или приложения.

## Локальный запуск

### Требования

- Python 3.11 или выше
- Poetry
- Telegram bot token
- Доступный backend API, указанный в `SERVICES_URL`
- Redis, если нужно сохранять FSM-состояния между перезапусками

### Установка зависимостей

```bash
poetry install
```

### Настройка окружения

Создайте `.env` в корне проекта и заполните как минимум `BOT_TOKEN`.

Минимальный вариант:

```env
BOT_TOKEN=123456:telegram_bot_token
BOT_UPDATE_METHOD=polling
SERVICES_URL=http://localhost:8081
```

### Запуск через Poetry

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8080 --log-config app/core/logging.yaml
```

После запуска:

- Telegram-бот начнет получать обновления через polling, если `BOT_UPDATE_METHOD=polling`;
- HTTP API будет доступно на `http://localhost:8080`;
- документация FastAPI будет доступна на `http://localhost:8080/docs`.

### Запуск с Redis

Поднимите Redis локально и добавьте настройки в `.env`:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
```

Если Redis недоступен или не настроен, приложение автоматически использует in-memory FSM storage. Такой режим подходит для разработки, но состояния будут теряться при перезапуске.

### Запуск в Docker

Сборка образа:

```bash
docker build -t vaiti-tg-bot .
```

Запуск контейнера:

```bash
docker run --env-file .env -p 8080:8080 vaiti-tg-bot
```

Контейнер запускает:

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --log-config app/core/logging.yaml
```

### Проверка webhook-режима

При `BOT_UPDATE_METHOD=webhook` приложение регистрирует webhook в Telegram и открывает служебный endpoint:

```text
GET /<WEBHOOK_PATH>/status
```

Он возвращает `OK`, если приложение доступно.
