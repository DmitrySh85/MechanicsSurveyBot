from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, User
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, User
from static_text.static_text import (
    registration_confirm_callback_data, 
    registration_reject_callback_data,
    REGISTRATION_CONFIRM_BTN,
    REGISTRATION_REJECT_BTN

)


survey_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Пройти опрос"),
                ]
            ],
            resize_keyboard=True,
        )

answer_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="A", callback_data="0",),
            InlineKeyboardButton(text="B", callback_data="1"),
            InlineKeyboardButton(text="C", callback_data="2"),
            InlineKeyboardButton(text="D", callback_data="3"),
        ]
    ]
)


def confirm_registration_kb(user: User) -> InlineKeyboardMarkup:
    """Returns the inline keyboard for confirming a registration request."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=REGISTRATION_CONFIRM_BTN,
                    callback_data=f"{registration_confirm_callback_data}:{user.id}:{user.username}",
                ),
                InlineKeyboardButton(
                    text=REGISTRATION_REJECT_BTN,
                    callback_data=f"{registration_reject_callback_data}:{user.id}:{user.username}",
                ),
            ]
        ]
    )
    return keyboard