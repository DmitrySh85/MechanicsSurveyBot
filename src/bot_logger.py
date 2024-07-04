import logging
from logging.handlers import RotatingFileHandler
import os
import settings


def init_logger(logger_name: str | None = None):
    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler("bot.log", maxBytes=20000, backupCount=1)

    # Set levels for handlers
    console_handler.setLevel(settings.LOG_LEVEL)
    file_handler.setLevel(settings.LOG_LEVEL)

    # Create formatters and add them to handlers
    console_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Get the logger
    # bot_logger = logging.getLogger(f"bot_logger")
    bot_logger = logging.getLogger()

    # Clear any default handlers that may be present
    bot_logger.handlers.clear()

    # Add handlers to the logger
    bot_logger.addHandler(console_handler)
    bot_logger.addHandler(file_handler)

    # Set the overall log level for the logger
    bot_logger.setLevel(int(os.environ.get("LOG_LEVEL", logging.DEBUG)))

    if logger_name:
        return logging.getLogger(f"root.{logger_name}")

    return bot_logger