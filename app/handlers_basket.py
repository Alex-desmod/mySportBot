from aiogram import F, Router
from aiogram.types import CallbackQuery

from app import keyboards as kb
from app.basket_data import fetch_euro_games


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


@router.callback_query(F.data.startswith("PAST_EURO"))
async def past_games(callback: CallbackQuery):
    await callback.answer()

    data = await fetch_euro_games()

    # Defining the latest round (max round)
    played_games = [game for game in data["data"] if game["played"]]
    if not played_games:
        await callback.message.answer("Нет сыгранных матчей.")

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
    await callback.message.answer(output)




@router.callback_query(F.data.startswith("FUTURE_EURO"))
async def future_games(callback: CallbackQuery):
    await callback.answer()

    data = await fetch_euro_games()

    # Defining the latest round (max round)
    played_games = [game for game in data["data"] if game["played"]]
    latest_round = max(game["round"] for game in played_games) if played_games else 0

    upcoming_round = latest_round + 1

    # Filtering the upcoming games of the current or the next round
    upcoming_games = [game for game in data["data"] if
                      not game["played"] and game["round"] in {latest_round, upcoming_round}]

    if not upcoming_games:
        await callback.message.answer("Нет предстоящих матчей.")

    # Sorting games by date
    upcoming_games.sort(key=lambda game: game["date"])

    # Formatting the results
    results = []
    for game in upcoming_games:
        local_team = game["local"]["club"]["abbreviatedName"]
        road_team = game["road"]["club"]["abbreviatedName"]
        game_date = game["date"][:10]
        results.append(f"{game_date} | {local_team:<20} vs {road_team:>20}")

    output = f"Предстоящие матчи:\n" + "\n".join(results)
    await callback.message.answer(output)
