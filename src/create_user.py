import asyncio

from sqlalchemy import update, select, insert
from sqlalchemy.exc import DBAPIError

from db import get_session
from models.models import User
from time import sleep


async def create_user():
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
        print("Данные профиля уже существуют в системе.")
        sleep(10)
        return
    async with get_session() as session:
        stmt = insert(User).values(
            name=name,
            tg_id=int(tg_id),
        )
        await session.execute(stmt)
        await session.commit()
    print("Пользователь успешно зарегистрирован")
    sleep(10)
    return


if __name__ == "__main__":
    asyncio.run(create_user())