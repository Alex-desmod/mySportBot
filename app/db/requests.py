from app.db.models import async_session
from app.db.models import User, Cycling, Athletics
from sqlalchemy import select


async def set_user(tg_id, name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, name=name))
            await session.commit()


async def get_cycling(eventId, name, dateFrom, dateTo, url, location, location_code):
    async with async_session() as session:
        race = await session.scalar(select(Cycling).where(Cycling.eventId == eventId))
        if not race:
            session.add(Cycling(eventId=eventId,
                                name=name,
                                dateFrom=dateFrom,
                                dateTo=dateTo,
                                url=url,
                                location= location,
                                location_code=location_code))
            await session.commit()
        return await session.scalar(select(Cycling).where(Cycling.eventId == eventId))


async def get_athletics(eventId, name, dateFrom, dateTo, url, location, location_name, location_code):
    async with async_session() as session:
        race = await session.scalar(select(Athletics).where(Athletics.eventId == eventId))
        if not race:
            session.add(Athletics(eventId=eventId,
                                name=name,
                                dateFrom=dateFrom,
                                dateTo=dateTo,
                                url=url,
                                location=location,
                                location_name=location_name,
                                location_code=location_code))
            await session.commit()
        return await session.scalar(select(Athletics).where(Athletics.eventId == eventId))

#Временная функция, чтобы исправить косячные даты в DB
# async def correct_date(eventId, dateFrom, dateTo):
#     async with async_session() as session:
#         stmt = select(Athletics).filter_by(eventId=eventId)  # Формируем запрос
#         result = await session.execute(stmt)  # Выполняем
#         race = result.scalar_one_or_none()  # Получаем объект или None
#
#         if race:
#             race.dateFrom = dateFrom
#             race.dateTo = dateTo# Обновляем поле
#             await session.commit()  # Фиксируем изменения








