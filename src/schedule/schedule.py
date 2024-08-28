from bot_logger import init_logger
from services.user_services import get_all_users_tg_ids
from dispatcher import bot
from services.schedule_services import get_survey_reminder_text
from keyboards.keyboards import survey_reminder_kb


logger = init_logger(__name__)


async def send_survey_notification():
    users_tg_ids = await get_all_users_tg_ids()
    logger.info(f"Received users tg_ids:{users_tg_ids}")
    for tg_id in users_tg_ids:
        message_text = get_survey_reminder_text()
        await bot.send_message(tg_id, message_text, reply_markup=survey_reminder_kb())




