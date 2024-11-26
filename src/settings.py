import os
import logging
from dotenv import load_dotenv
load_dotenv()


DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
BOT_TOKEN = os.environ.get("BOT_TOKEN")

BACKEND_API_URL = os.environ.get("BACKEND_API_URL")
BACKEND_API_TOKEN = os.environ.get("BACKEND_API_TOKEN")

DEBUG = os.environ.get("DEBUG", "False") == "True"
if DEBUG:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

MAX_SURVEY_ATTEMPTS_PER_DAY = 3