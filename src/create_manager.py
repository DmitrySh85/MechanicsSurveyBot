import asyncio

from sqlalchemy import update, select, insert
from sqlalchemy.exc import DBAPIError

from db import get_session
from models.models import User
from time import sleep


async def create_manager():
    tg_id = input("Введите telegram id: ")
    name = input("Введите имя: ")
    async with get_session() as session:
        try:
            stmt = select(User.id).where(User.tg_id == int(tg_id))
            result = await session.execute(stmt)
        except DBAPIError:
            print("Неправильный telegram_id")
            sleep(10)
            return
        except ValueError:
            print("Неправильный telegram_id")
            sleep(10)
            return
        master_id = result.scalar()
    if master_id:
        async with get_session() as session:
            stmt = update(User).values(
                is_admin=True, name=name, is_blocked=False
            ).where(User.id == master_id)
            await session.execute(stmt)
            await session.commit()
        print("Данные профиля успешно изменены")
        sleep(10)
        return
    async with get_session() as session:
        stmt = insert(User).values(
            name=name,
            tg_id=int(tg_id),
            is_admin=True,
            is_blocked=False
        )
        await session.execute(stmt)
        await session.commit()
    print("Администратор успешно зарегистрирован")
    sleep(10)
    return


if __name__ == "__main__":
    asyncio.run(create_manager())