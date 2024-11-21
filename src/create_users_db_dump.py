import asyncio
import json

from sqlalchemy import select

from db import get_session
from models.models import User


async def main():
    data = await get_users_from_db()
    result = []
    for user in data:
        print(user.id, user.is_admin, user.tg_id, user.is_blocked, user.points, user.name)
        if user.is_admin:
            role = "ADMIN"
        else:
            role = "MASTER"
        user_data = {
            "tg_id": user.tg_id,
            "name": user.name,
            "role": role,
            "points": user.points,
            "is_blocked": user.is_blocked
        }
        result.append(user_data)
    with open ("files/users.json", "w") as file:
        file.write(json.dumps(result))



async def get_users_from_db():
    stmt = select(User)
    async with get_session() as session:
        result = await session.execute(stmt)
        return result.scalars().all()


if __name__ == "__main__":
    asyncio.run(main())



