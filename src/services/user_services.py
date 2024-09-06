from db import get_session
from sqlalchemy import select, update
from models.models import User
from .handlers_services import check_user,  check_blocked_user
from bot_logger import init_logger

logger = init_logger(__name__)


async def register_user(tg_id: int, username: str):
    user = await check_user(tg_id)
    if not user:
        await insert_user_to_db(tg_id, username)
    else:
        if await check_blocked_user(tg_id):
            await set_user_is_not_blocked(tg_id)
            return
        raise ValueError(f"User {tg_id} is already registered")


async def insert_user_to_db(tg_id: int, username: str):
    async with get_session() as session:
        user = User(tg_id=tg_id, name=username)
        session.add(user)
        await session.commit()


async def reject_user(tg_id: int, username: str):
    user = await check_user(tg_id)
    if not user:
        await create_blocked_user(tg_id, username)
    else:
        await set_user_is_blocked(tg_id)


async def create_blocked_user(tg_id: int, username: str):
    async with get_session() as session:        
        user = User(tg_id=tg_id, name=username, is_blocked=True)
        session.add(user)
        await session.commit()


async def set_user_is_blocked(tg_id: int):
    async with get_session() as session:
        stmt = update(User).where(User.tg_id == tg_id).values(is_blocked=True)
        await session.execute(stmt)
        await session.commit()


async def set_user_is_not_blocked(tg_id: int):
    async with get_session() as session:
        stmt = update(User).where(User.tg_id == tg_id).values(is_blocked=False)
        await session.execute(stmt)
        await session.commit()


async def get_all_users_tg_ids():
    async with get_session() as session:
        stmt = select(User.tg_id).where(User.is_blocked == False)
        result = await session.execute(stmt)
        users_tg_ids = result.scalars().all()
    return users_tg_ids


