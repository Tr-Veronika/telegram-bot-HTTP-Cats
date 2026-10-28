from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Create the main menu keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Popular status codes",
                    callback_data="show_popular_statuses",
                )
            ]
        ]
    )


def get_popular_statuses_keyboard() -> InlineKeyboardMarkup:
    """Create an inline keyboard with popular HTTP status codes"""
    statuses = [
        (200, "200 OK"),
        (201, "201 Created"),
        (301, "301 Redirect"),
        (400, "400 Bad Request"),
        (401, "401 Unauthorized"),
        (403, "403 Forbidden"),
        (404, "404 Not Found"),
        (418, "418 I'm a teapot"),
        (429, "429 Too Many Requests"),
        (500, "500 Server Error"),
        (502, "502 Bad Gateway"),
        (503, "503 Unavailable"),
    ]

    buttons = [
        InlineKeyboardButton(
            text=label,
            callback_data=f"status:{code}",
        )
        for code, label in statuses
    ]

    rows = [buttons[index:index + 2] for index in range(0, len(buttons), 2)]

    return InlineKeyboardMarkup(inline_keyboard=rows)
