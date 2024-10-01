from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, User
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, User
from static_text.static_text import (
    registration_confirm_callback_data, 
    registration_reject_callback_data,
    REGISTRATION_CONFIRM_BTN,
    REGISTRATION_REJECT_BTN,
    START_SURVEY_BTN,
    LEADERBOARD_BTN,
    SURVEY_ACCEPT_BTN,
    survey_accept_callback_data,
    SURVEY_REJECT_BTN,
    survey_reject_callback_data,
    MY_POSITION_BTN,
)
from services.user_services import check_user_is_admin

async def survey_keyboard(tg_id: int) -> ReplyKeyboardMarkup:
    user_is_admin = await check_user_is_admin(tg_id)
    if user_is_admin:
        btn_text = LEADERBOARD_BTN
    else:
        btn_text = MY_POSITION_BTN
    keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=START_SURVEY_BTN),
                    ],
                    [
                        KeyboardButton(text=btn_text),
                    ],

                ],
                resize_keyboard=True,
            )
    return keyboard

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


def survey_reminder_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=SURVEY_ACCEPT_BTN,
                    callback_data=survey_accept_callback_data,
                ),
                InlineKeyboardButton(
                    text=SURVEY_REJECT_BTN,
                    callback_data=survey_reject_callback_data,
                ),
            ]
        ]
    )
    return keyboard