import asyncio
from sqlalchemy import select

from db import get_session
from models.models import User
from settings import BACKEND_API_URL, BACKEND_API_TOKEN
from aiohttp import ClientSession


async def migrate_from_alchemy_to_django():
    users = await get_users_from_db()
    url = f"{BACKEND_API_URL}/api/employees/"
    headers = {"Authorization": f"Token {BACKEND_API_TOKEN}"}
    for user in users:
        if user.is_admin:
            role = "ADMIN"
        else: 
            role = "MASTER"
        payload = {
            "tg_id": user.tg_id,
            "name": user.name,
            "role": role,
            "is_blocked": user.is_blocked
        }
        async with ClientSession() as session:
            response = await session.post(url=url, json=payload, headers=headers)
            print(response)

    


async def  get_users_from_db():
    async with get_session() as session:
        stmt = select(User)
        results = await session.execute(stmt)
        return results.scalars().all()
    


if __name__ == "__main__":
    asyncio.run(migrate_from_alchemy_to_django())