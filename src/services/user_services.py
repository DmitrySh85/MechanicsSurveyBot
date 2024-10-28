from typing import Union

from db import get_session
from sqlalchemy import select, update
from models.models import User
from bot_logger import init_logger
from apis.users_manager import UsersBackendAPIManager

logger = init_logger(__name__)


async def register_user(tg_id: int, username: str):
    api_manager = UsersBackendAPIManager()
    await api_manager.send_registration_request(tg_id, username)

async def reject_user(tg_id: int, username: str):
    await create_blocked_user(tg_id, username)


async def create_blocked_user(tg_id: int, username: str):
    api_manager = UsersBackendAPIManager()
    await api_manager.send_registration_request(tg_id=tg_id, username=username, is_blocked=True)


async def set_user_is_not_blocked(tg_id: int):
    async with get_session() as session:
        stmt = update(User).where(User.tg_id == tg_id).values(is_blocked=False)
        await session.execute(stmt)
        await session.commit()


async def get_all_users_tg_ids():

    api_manager = UsersBackendAPIManager()
    users = await api_manager.get_users_from_backend(is_blocked=False)
    try:    
        tg_ids = [user.get("tg_id") for user in users]
        return tg_ids
    except TypeError:
        return []



async def check_user_is_admin(tg_id: int) -> bool:
    api_manager = UsersBackendAPIManager()
    user = await api_manager.get_user_from_backend(tg_id)
    return user.get("role") == "ADMIN"


async def set_user_is_blocked(tg_id: int):
    api_manager = UsersBackendAPIManager()
    await api_manager.set_user_is_blocked()


async def get_user(tg_id: int):
    api_manager = UsersBackendAPIManager()
    user = await api_manager.get_user_from_backend(tg_id)
    return user

