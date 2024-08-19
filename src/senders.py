from static_text.static_text import NO_USER_FOUND_TEXT, START_TEXT, REGISTRATION_REQUEST_MESSAGE
from aiogram.types import Message
from services.handlers_services import get_admin_tg_ids_from_db
from keyboards.keyboards import confirm_registration_kb
from keyboards.keyboards import survey_keyboard


async def send_start_message(message: Message):
    return await message.answer(
        text=START_TEXT,
        parse_mode="HTML",
        reply_markup=survey_keyboard
    )


async def send_not_registered_message(message: Message):
    return await message.answer(NO_USER_FOUND_TEXT)


async def send_registration_request_to_admin(message: Message):

    admin_chat_ids = await get_admin_tg_ids_from_db()
    for admin_id in admin_chat_ids:
        await message.bot.send_message(
            chat_id=admin_id,
            text=REGISTRATION_REQUEST_MESSAGE.format(user_id=message.from_user.id, username=message.from_user.username, first_name=message.from_user.first_name, last_name=message.from_user.last_name),  # type: ignore
            reply_markup=confirm_registration_kb(message.from_user),
        )
