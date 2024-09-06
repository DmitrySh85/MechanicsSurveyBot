from aiogram.exceptions import TelegramBadRequest, TelegramServerError, TelegramForbiddenError
from bot_logger import init_logger
from services.user_services import get_all_users_tg_ids, set_user_is_blocked
from dispatcher import bot
from services.schedule_services import get_survey_reminder_text
from keyboards.keyboards import survey_reminder_kb


logger = init_logger(__name__)


async def send_survey_notification():
    users_tg_ids = await get_all_users_tg_ids()
    logger.info(f"Received users tg_ids:{users_tg_ids}")
    for tg_id in users_tg_ids:
        message_text = get_survey_reminder_text()
        try:
            await bot.send_message(tg_id, message_text, reply_markup=survey_reminder_kb())
        except (TelegramBadRequest, TelegramServerError) as e:
            logger.debug(f"failed to send message to {tg_id}: {e}")
        except TelegramForbiddenError:
            logger.info(f"User {tg_id} has blocked bot")
            await set_user_is_blocked(tg_id)








