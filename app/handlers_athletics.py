from aiogram import F, Router
from aiogram.types import CallbackQuery
from datetime import datetime, timezone, timedelta

from app import keyboards as kb
import app.sports as sports
import app.athletics_data as adata
import app.db.requests as rq

router = Router()

@router.callback_query(F.data.startswith("ATHLETICS"))
async def athletics(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Большие события из мира легкой атлетики',
                                  reply_markup= await kb.athletics())


dateFrom = f"{datetime.now().year}-01-01"
dateTo = f"{datetime.now().year}-12-31"


@router.callback_query(F.data == "MAJORS")
async def classics(callback: CallbackQuery):
    await callback.answer()

    data = []
    for i in range(1, 10):
        url = adata.Athletics_endpoints().calendar(dateFrom, dateTo, competitionId=sports.MAJORS, page=i)
        response = await adata.fetch_data(url)
        if not response:
            break
        data += response

    results = []
    for event in data:
        race = await rq.get_athletics(eventId=event["id"],
                                    name=event["name"],
                                    dateFrom=datetime.strptime(event["dateFrom"], "%Y-%m-%dT%H:%M:%S"),
                                    dateTo=datetime.strptime(event["dateTo"], "%Y-%m-%dT%H:%M:%S"),
                                    url=event["webUrl"],
                                    location=event["location"][0]["name"],
                                    location_code=event["location"][0]["code"])

        output = (f"{race.dateFrom.strftime("%Y-%m-%d")} | <b>{race.name[5:]}</b> "
                  f"{sports.Countries[race.location_code.upper()].value}\n")

        if datetime.today() > race.dateTo:
            output += f"✅ Winners: {race.winner}\n"

        results.append(output)

    await callback.message.answer("\n".join(results))
    await callback.message.answer('Что-нибудь еще?', reply_markup=await kb.athletics())