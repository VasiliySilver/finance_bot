import asyncio
import logging
from typing import Any, Awaitable, Callable, Dict
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from bot.database.base import get_session
from bot.database.repository import Repository

from config import load_config
from bot.handlers import register_all_handlers
from bot.utils.reminders import send_reminders  # Импортируем функцию напоминаний

logger = logging.getLogger(__name__)

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        async for session in get_session():
            repo = Repository(session)
            data["repository"] = repo  # Set the repository in the data
            logger.info("Repository has been set in the data.")
            return await handler(event, data)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    config = load_config()
    bot = Bot(token=config.bot.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    # Register the DatabaseMiddleware
    dp.update.outer_middleware(DatabaseMiddleware())
    
    register_all_handlers(dp)

    # Запускаем задачу напоминаний
    asyncio.create_task(send_reminders(bot))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!") 