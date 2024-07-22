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

def answer_keyboard(length_of_answers: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="ABCD"[i], callback_data=str(i)) for i in range(length_of_answers)
            ]
        ]
    )
    return keyboard


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