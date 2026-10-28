import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from bot.handlers.handlers_status_code import router
from bot.config import BOT_TOKEN, PROXY_URL


def create_bot() -> Bot:
    """Create the Telegram bot with an optional proxy"""
    if PROXY_URL:
        session = AiohttpSession(proxy=PROXY_URL)
        return Bot(token=BOT_TOKEN, session=session)

    return Bot(token=BOT_TOKEN)


async def main() -> None:
    """Configure the application and start long polling"""
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing. Set it in your .env file.")

    bot = create_bot()
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
               '%(lineno)d - %(name)s - %(message)s'
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

