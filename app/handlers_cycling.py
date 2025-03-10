import json
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery
from datetime import datetime, timezone, timedelta

from app import keyboards as kb
import app.sports as sports
import app.cycling_data as cdata
import app.db.requests as rq

logger = logging.getLogger(__name__)
router = Router()

with open("app/messages.json", "r", encoding="utf-8") as file:
    messages = json.load(file)

@router.callback_query(F.data == "CYCLING")
async def cycling(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(messages[0]["cycling"],
                         reply_markup= await kb.cycling())


dateFrom = f"{datetime.now().year}-01-01"
dateTo = f"{datetime.now().year}-12-31"


@router.callback_query(F.data == "CLASSICS")
async def classics(callback: CallbackQuery):
    await callback.answer(messages[0]["classics"])

    results = []
    for event in sports.Classics:
        url = cdata.Cycling_endpoints().calendar(dateFrom, dateTo, event.value)
        data = await cdata.fetch_data(url)
        # logger.warning(data)
        if data:
            race = await rq.set_cycling(eventId=int(event.value),
                                        name=data[0]["name"],
                                        dateFrom=datetime.strptime(data[0]["dateFrom"], "%Y-%m-%dT%H:%M:%S"),
                                        dateTo=datetime.strptime(data[0]["dateTo"], "%Y-%m-%dT%H:%M:%S"),
                                        url=data[0]["webUrl"],
                                        location=data[0]["location"][0]["name"],
                                        location_code=data[0]["location"][0]["code"])
        else:
            race = await rq.get_cycling(eventId=int(event.value))

        output = (f"{race.dateFrom.strftime('%Y-%m-%d')} | <b>{race.name.split('-', 1)[-1].strip()}</b> "
                  f"{sports.Countries[race.location_code.upper()].value}\n")

        if datetime.today() > race.dateTo:
            output += f"✅ Winner: {race.winner}\n"

        results.append(output)

    message = "\n".join(results)
    await callback.message.answer(message, reply_markup=await kb.cycling())
        
@router.callback_query(F.data == "GT")
async def gt(callback: CallbackQuery):
    await callback.answer()

    results = []
    for event in sports.GT:
        url = cdata.Cycling_endpoints().calendar(dateFrom, dateTo, event.value)
        data = await cdata.fetch_data(url)
        if data:
            race = await rq.set_cycling(eventId=int(event.value),
                                        name=data[0]["name"],
                                        dateFrom=datetime.strptime(data[0]["dateFrom"], "%Y-%m-%dT%H:%M:%S"),
                                        dateTo=datetime.strptime(data[0]["dateTo"], "%Y-%m-%dT%H:%M:%S"),
                                        url=data[0]["webUrl"],
                                        location=data[0]["location"][0]["name"],
                                        location_code=data[0]["location"][0]["code"])
        else:
            race = await rq.get_cycling(eventId=int(event.value))

        output = (f"{race.dateFrom.strftime('%Y-%m-%d')} - {race.dateTo.strftime('%Y-%m-%d')} | "
                  f"<b>{race.name[5:]}</b> "
                  f"{sports.Countries[race.location_code.upper()].value}\n")

        if datetime.today() > race.dateTo:
            output += f"✅ Winners: {race.winner}\n"

        results.append(output)

    message = "\n".join(results)
    await callback.message.answer(message)


@router.callback_query(F.data == "CYCLING_WC")
async def cycling_wc(callback: CallbackQuery):
    await callback.answer()
    url = cdata.Cycling_endpoints().calendar(dateFrom, dateTo, sports.CYCLING_WC)
    data = await cdata.fetch_data(url)
    if data:
        race = await rq.set_cycling(eventId=int(sports.CYCLING_WC),
                                name=data[0]["name"],
                                dateFrom=datetime.strptime(data[0]["dateFrom"], "%Y-%m-%dT%H:%M:%S"),
                                dateTo=datetime.strptime(data[0]["dateTo"], "%Y-%m-%dT%H:%M:%S"),
                                url=data[0]["webUrl"],
                                location=data[0]["location"][0]["name"],
                                location_code=data[0]["location"][0]["code"])
    else:
        race = await rq.get_cycling(eventId=int(event.value))

    output = (f"{race.dateFrom.strftime('%Y-%m-%d')} - {race.dateTo.strftime('%Y-%m-%d')} | "
              f"<b>{race.name[5:]}</b> "
              f"{sports.Countries[race.location_code.upper()].value}\n")

    if datetime.today() > race.dateTo:
        output += f"✅ Winners: {race.winner}\n"

    await callback.message.answer(output)






