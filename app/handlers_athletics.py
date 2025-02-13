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
async def majors(callback: CallbackQuery):
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
                                    location_name=event["location"][0]["locations"][0]["name"],
                                    location_code=event["location"][0]["code"])

        output = (f"{race.dateFrom.strftime("%Y-%m-%d")} | <b>{race.name.split("-", 1)[-1].strip()}</b> "
                  f"{sports.Countries[race.location_code.upper()].value}\n")

        if datetime.today() > race.dateTo:
            output += f"✅ Winners: {race.winner}\n"

        results.append(output)

    #Temporary call to correct wrong dates
    await  rq.correct_date(18167,
                           dateFrom=datetime.strptime("2025-09-21T00:00:00", "%Y-%m-%dT%H:%M:%S"),
                           dateTo=datetime.strptime("2025-09-21T00:00:00", "%Y-%m-%dT%H:%M:%S"))

    await rq.correct_date(18168,
                    dateFrom=datetime.strptime("2025-10-12T00:00:00", "%Y-%m-%dT%H:%M:%S"),
                    dateTo=datetime.strptime("2025-10-12T00:00:00", "%Y-%m-%dT%H:%M:%S"))

    await rq.correct_date(18169,
                          dateFrom=datetime.strptime("2025-11-02T00:00:00", "%Y-%m-%dT%H:%M:%S"),
                          dateTo=datetime.strptime("2025-11-02T00:00:00", "%Y-%m-%dT%H:%M:%S"))

    #Since the API doesn't know about the Sydney Marathon I had to add it manually to my DB
    set_sydney = await rq.get_athletics(eventId=777,
                                    name="2025 World Marathon Majors - Sydney Marathon",
                                    dateFrom=datetime.strptime("2025-08-31T00:00:00", "%Y-%m-%dT%H:%M:%S"),
                                    dateTo=datetime.strptime("2025-08-31T00:00:00", "%Y-%m-%dT%H:%M:%S"),
                                    url="https://www.tcssydneymarathon.com/",
                                    location="Australia",
                                    location_name="Sydney",
                                    location_code="au")

    get_sydney = (f"{set_sydney.dateFrom.strftime("%Y-%m-%d")} | <b>{set_sydney.name.split("-", 1)[-1].strip()}</b> "
                  f"{sports.Countries[set_sydney.location_code.upper()].value}\n")

    if datetime.today() > set_sydney.dateTo:
        get_sydney += f"✅ Winners: {set_sydney.winner}\n"

    results.append(get_sydney)

    #My dumb way to sort the marathon by date
    sydney = results.pop(-1)
    results.insert(3, sydney)

    await callback.message.answer("\n".join(results))
    await callback.message.answer('Что-нибудь еще?', reply_markup=await kb.athletics())


@router.callback_query(F.data == "DIAMOND_LEAGUE")
async def diamonds(callback: CallbackQuery):
    await callback.answer()

    data = []
    for i in range(1, 10):
        url = adata.Athletics_endpoints().calendar(dateFrom, dateTo, competitionId=sports.DIAMONDS, page=i)
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
                                    location_name=event["location"][0]["locations"][0]["name"],
                                    location_code=event["location"][0]["code"])

        output = (f"{race.dateFrom.strftime("%Y-%m-%d")} | "
                  f"<b>{race.name[5:]}</b>\n"
                  f"{race.location:>40}, {race.location_name} {sports.Countries[race.location_code.upper()].value}\n")

        if datetime.today() > race.dateTo:
            output += f"✅\n"

        results.append(output)

    await callback.message.answer("\n".join(results))
    await callback.message.answer('Что-нибудь еще?', reply_markup=await kb.athletics())