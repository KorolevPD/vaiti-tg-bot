from asyncio import CancelledError, create_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types.bot_command_scope_all_private_chats import (
    BotCommandScopeAllPrivateChats,
)
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import HTTPException

from app.api.routers import router as api_router
from app.bot.middlewares.auth import AuthMiddleware
from app.bot.routers import all_commands, all_routers
from app.clients.proxy.session import ProxySession
from app.clients.redis import create_redis_client
from app.core.config import UpdateMethod, settings
from app.services.cover_letters.storage import CoverLettersStorage

logger = settings.logger

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=ProxySession(settings.PROXIES) if settings.PROXIES else None,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

    # Подключение Redis и настройка хранилища.
    redis = await create_redis_client()
    storage: RedisStorage | MemoryStorage = MemoryStorage()
    if redis:
        storage = RedisStorage(
            redis=redis, key_builder=settings.REDIS_KEY_BUILDER
        )
    else:
        logger.warning(
            "Failed to create RedisStorage, using MemoryStorage instead."
        )

    # Создание диспетчера.
    dp = Dispatcher(storage=storage)
    dp.include_routers(*all_routers)
    dp.update.middleware(AuthMiddleware(redis))

    cl_storage = None
    if redis:
        cl_storage = CoverLettersStorage(redis)

    dp["cl_storage"] = cl_storage
    dp["redis"] = redis

    app.state.bot = bot
    app.state.dp = dp

    # Создание команд.
    try:
        await bot.set_my_commands(
            all_commands, scope=BotCommandScopeAllPrivateChats()
        )
        logger.info("The bot commands are set.")
    except Exception as e:
        logger.warning(f"Unable to set up bot commands: {e}")

    # Запуск бота в нужном режиме.
    await bot.delete_webhook(drop_pending_updates=True)
    match settings.BOT_UPDATE_METHOD:
        case UpdateMethod.POLLING:
            polling_task = create_task(dp.start_polling(bot))
        case UpdateMethod.WEBHOOK:
            await bot.set_webhook(
                url=settings.WEBHOOK_URL,
                secret_token=settings.WEBHOOK_SECRET,
                allowed_updates=dp.resolve_used_update_types(),
                drop_pending_updates=True,
            )
            logger.info("Webhook is set up.")
        case _:
            raise NotImplementedError

    yield

    match settings.BOT_UPDATE_METHOD:
        case UpdateMethod.POLLING:
            polling_task.cancel()
            try:
                await polling_task
            except CancelledError:
                pass
            except Exception as e:
                logger.error(f"Error while stopping polling: {e}")
        case UpdateMethod.WEBHOOK:
            await bot.delete_webhook()

    if redis:
        await redis.aclose()

    await bot.session.close()


app = FastAPI(
    title="Bot API",
    description="API для работы с телеграм-ботом.",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(api_router, prefix="/api/v1", tags=["Bot"])

if settings.BOT_UPDATE_METHOD == UpdateMethod.WEBHOOK:

    @app.get(f"/{settings.WEBHOOK_PATH}/status", include_in_schema=False)
    async def bot_status_check() -> Response:
        return Response(content="OK", media_type="text/plain")

    @app.post(f"/{settings.WEBHOOK_PATH}", include_in_schema=False)
    async def bot_webhook(request: Request) -> None:
        secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret != settings.WEBHOOK_SECRET:
            raise HTTPException(status_code=403)
        data = await request.json()
        update = types.Update.model_validate(data)
        dp: Dispatcher = request.app.state.dp
        await dp.feed_update(bot, update)
