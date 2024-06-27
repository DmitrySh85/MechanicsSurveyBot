from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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