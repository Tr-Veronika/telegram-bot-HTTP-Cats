import logging
import random

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.data.http_statuses import KNOWN_CODES
from data.messages import START_MESSAGE, UNKNOWN_MESSAGES
from services.http_cat import get_description, is_supported_code
from bot.keyboards.status import (
    get_main_keyboard,
    get_popular_statuses_keyboard,
)

logger = logging.getLogger(__name__)
router = Router()


async def send_status_cat(message: Message, code: int) -> None:
    """Send the cat image and description for an HTTP status code"""
    title, description = await get_description(code)
    photo_url = f"https://http.cat/{code}"

    try:
        caption = f"🐱 HTTP {code} — {title}\n\n{description}"

        if len(caption) <= 1024:
            # Short description: send the image with its caption
            await message.answer_photo(
                photo=f"https://http.cat/{code}",
                caption=caption,
            )
        else:
            # Long description: send the image first, then the text
            await message.answer_photo(
                photo=f"https://http.cat/{code}",
            )
            await message.answer(caption)
    except Exception:
        logger.exception("Failed to send the image for HTTP %s", code)
        await message.answer(
            f"😿 I couldn't send the image for HTTP {code}.\n\n"
            f"{title}\n\n{description}"
        )


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """Show the welcome message and main menu"""
    await message.answer(
        START_MESSAGE,
        reply_markup=get_main_keyboard(),
    )


@router.message(Command("random"))
async def random_handler(message: Message) -> None:
    """Send a cat for a randomly selected supported status code"""
    code = random.choice(sorted(KNOWN_CODES))
    await send_status_cat(message, code)


@router.callback_query(F.data == "show_popular_statuses")
async def popular_statuses_handler(callback: CallbackQuery) -> None:
    """Display the keyboard with popular HTTP status codes"""
    if callback.message:
        await callback.message.answer(
            "📋 Choose an HTTP status code:",
            reply_markup=get_popular_statuses_keyboard(),
        )

    await callback.answer()


@router.callback_query(F.data.startswith("status:"))
async def status_callback_handler(callback: CallbackQuery) -> None:
    """Handle a status code selected from the inline keyboard"""
    if not callback.data:
        await callback.answer("Invalid status code.", show_alert=True)
        return

    try:
        code = int(callback.data.split(":", maxsplit=1)[1])
    except (ValueError, IndexError):
        await callback.answer("Invalid status code.", show_alert=True)
        return

    if not is_supported_code(code):
        await callback.answer("Unsupported status code.", show_alert=True)
        return

    await callback.answer()

    if callback.message:
        await send_status_cat(callback.message, code)


@router.message(F.text)
async def status_code_handler(message: Message) -> None:
    """Handle a status code entered as a text message"""
    code_text = (message.text or "").strip()

    if not code_text.isdigit() or len(code_text) != 3:
        await message.answer(random.choice(UNKNOWN_MESSAGES))
        return

    code = int(code_text)
    if not is_supported_code(code):
        await message.answer(random.choice(UNKNOWN_MESSAGES))
        return

    title, description = await get_description(code)
    photo_url = f"https://http.cat/{code}"

    try:
        caption = f"🐱 HTTP {code} — {title}\n\n{description}"

        if len(caption) <= 1024:
            # Short description: send the image with its caption
            await message.answer_photo(
                photo=f"https://http.cat/{code}",
                caption=caption,
            )
        else:
            # Long description: send the image first, then the text
            await message.answer_photo(
                photo=f"https://http.cat/{code}",
            )
            await message.answer(caption)
    except Exception:
        logger.exception("Failed to send the image for HTTP %s", code)
        await message.answer(
            f"😿 I couldn't send the image for HTTP {code}.\n\n"
            f"{title}\n\n{description}"
        )
