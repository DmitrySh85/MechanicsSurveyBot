import asyncio
from dispatcher import start_polling
from bot_logger import init_logger


logger = init_logger(__name__)


if __name__ == "__main__":
    asyncio.run(start_polling())