from aiogram import F, Router
from aiogram.types import CallbackQuery
from datetime import datetime, timezone, timedelta

from app import keyboards as kb
import app.basket_data as bdata

router = Router()

@router.callback_query(F.data.startswith("BASKET"))
async def basket(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Выбери турнир', reply_markup= await kb.basket())


@router.callback_query(F.data.startswith("EURO"))
async def euroleague(callback: CallbackQuery):
    await callback.answer('I feel devotion')
    await callback.message.answer('Здесь ты можешь посмотреть последние результаты, '
                                  'расписание предстоящих игр и турнирную таблицу',
                                  reply_markup= await kb.euro())


@router.callback_query(F.data.startswith("NBA"))
async def nba(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('В процессе разработки...')


@router.callback_query(F.data.startswith("PAST_EURO"))
async def past_euro_games(callback: CallbackQuery):
    await callback.answer()

    URL_GAMES = bdata.Euro_endpoints().games()
    data = await bdata.fetch_euro_games(URL_GAMES)
    if data == "No server answer":
        await callback.message.answer("Нет ответа от сервера.", reply_markup= await kb.euro())

    # Defining the latest round (max round)
    played_games = [game for game in data["data"] if game["played"]]
    if not played_games:
        await callback.message.answer("Нет сыгранных матчей.", reply_markup= await kb.euro())

    latest_round = max(game["round"] for game in played_games)
    latest_round_games = [game for game in played_games if game["round"] == latest_round]

    # Formatting the results
    results = []
    for game in latest_round_games:
        local_team = game["local"]["club"]["abbreviatedName"]
        road_team = game["road"]["club"]["abbreviatedName"]
        local_score = game["local"]["score"]
        road_score = game["road"]["score"]
        game_date = game["date"][:10]
        results.append(f"{game_date} | {local_team:<20} {local_score:>3} - {road_score:<3} {road_team:>20}")

    output = f'Матчи последнего тура ({latest_round}):\n' + "\n".join(results)
    await callback.message.answer(output, reply_markup= await kb.euro())


@router.callback_query(F.data.startswith("FUTURE_EURO"))
async def future_euro_games(callback: CallbackQuery):
    await callback.answer()

    URL_GAMES = bdata.Euro_endpoints().games()
    data = await bdata.fetch_euro_games(URL_GAMES)
    if data == "No server answer":
        await callback.message.answer("Нет ответа от сервера.", reply_markup= await kb.euro())

    # Defining the latest round (max round)
    played_games = [game for game in data["data"] if game["played"]]
    latest_round = max(game["round"] for game in played_games) if played_games else 0

    upcoming_round = latest_round + 1

    # Filtering the upcoming games of the current or the next round
    upcoming_games = [game for game in data["data"] if
                      not game["played"] and game["round"] in {latest_round, upcoming_round}]

    if not upcoming_games:
        await callback.message.answer("Нет предстоящих матчей.", reply_markup= await kb.euro())

    # Sorting games by date
    upcoming_games.sort(key=lambda game: game["date"])

    # Formatting the results
    results = []
    MOSCOW_TZ = timezone(timedelta(hours=3))  # Noscow TZ
    for game in upcoming_games:
        local_team = game["local"]["club"]["abbreviatedName"]
        road_team = game["road"]["club"]["abbreviatedName"]
        game_date = game["date"][:10]
        utc_time = datetime.strptime(game["utcDate"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        moscow_time = utc_time.astimezone(MOSCOW_TZ).strftime("%H:%M")
        results.append(f"{game_date} {moscow_time} | {local_team:<20} vs {road_team:<20}")

    output = f"Предстоящие матчи (время Мск):\n" + "\n".join(results)
    await callback.message.answer(output, reply_markup= await kb.euro())


@router.callback_query(F.data.startswith("STANDINGS_EURO"))
async def standings_euro(callback: CallbackQuery):
    await callback.answer()

    URL_GAMES = bdata.Euro_endpoints().games()
    data = await bdata.fetch_euro_games(URL_GAMES)
    if data == "No server answer":
        await callback.message.answer("Нет ответа от сервера.", reply_markup= await kb.euro())

    # Defining the latest round (max round)
    played_games = [game for game in data["data"] if game["played"]]
    latest_round = max(game["round"] for game in played_games)

    URL_STANDINGS = bdata.Euro_endpoints().standings(latest_round)

    sdata = await bdata.fetch_euro_games(URL_STANDINGS)

    standings = sdata[0].get("standings", [])
    if not standings:
        await callback.message.answer("Нет данных о турнирной таблице.")

    # Formatting the table
    results = [f"{' ':<15} {'Команда':<35} {'Игры':<25} {'%':<10}\n", f"{"-" * 80}"]
    for team in standings:
        position = team["data"]["position"]
        name = team["club"]["abbreviatedName"]
        games_played = team["data"]["gamesPlayed"]
        games_won = team["data"]["gamesWon"]
        win_percentage = (games_won / games_played * 100) if games_played else 0
        results.append(f"{position:<5} {name:<35} {games_played:<20} {win_percentage:.2f}%")

    output = "\n".join(results)
    await callback.message.answer(output, reply_markup=await kb.euro())
