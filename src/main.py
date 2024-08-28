import asyncio
from datetime import datetime

from apscheduler.triggers.cron import CronTrigger

from dispatcher import start_polling
from bot_logger import init_logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from schedule.schedule import send_survey_notification


logger = init_logger(__name__)


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

trigger = CronTrigger(hour=10, minute=0, day='*/2')

scheduler.add_job(send_survey_notification, trigger)


if __name__ == "__main__":
    scheduler.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_polling())