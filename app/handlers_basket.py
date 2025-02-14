from aiogram import F, Router
from aiogram.types import CallbackQuery
from datetime import datetime, timezone, timedelta


from app import keyboards as kb
import app.basket_data as bdata
import app.sports as sports

router = Router(name=__name__)

MOSCOW_TZ = timezone(timedelta(hours=3))  # Noscow TZ
current_year = datetime.now().year

@router.callback_query(F.data == "BASKET")
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
    await callback.message.answer('Здесь ты можешь посмотреть последние результаты, '
                                  'расписание предстоящих игр и турнирную таблицу',
                                  reply_markup=await kb.nba())


if datetime.now() < datetime(current_year, 10, 1):
    #for Euroleague urls
    seasonCode = f'E{current_year - 1}'
    #for NBA urls
    season = current_year
    season_po = f'{current_year}POST'
else:
    seasonCode = f'E{current_year}'
    season = current_year + 1
    season_po = f'{current_year + 1}POST'

@router.callback_query(F.data == "PAST_EURO_GAMES")
async def past_euro_games(callback: CallbackQuery):
    await callback.answer()

    url_games = bdata.Euro_endpoints().games(seasonCode=seasonCode)
    data = await bdata.fetch_data(url_games)
    if not data:
        await callback.message.answer("Нет ответа от сервера.", reply_markup= await kb.euro())

    # Defining the latest round (max round)
    played_games = [game for game in data["data"] if game["played"]]
    if not played_games:
        await callback.message.answer("Нет сыгранных матчей.", reply_markup= await kb.euro())

    latest_round = max(game["round"] for game in played_games)
    phase = played_games[0]["phaseType"]["code"]

    if phase == "RS":
        latest_round_games = [game for game in played_games if game["round"] == latest_round]
        results = [f'Матчи последнего тура ({latest_round}):\n\n']

    if phase == "PI":
        latest_round_games = [game for game in played_games if game["phaseType"]["code"] == phase]
        results = ['Плей-ин:\n\n']

    if phase == "PO":
        latest_round_games = [game for game in played_games if game["phaseType"]["code"] == phase]
        results = ['Плей-офф:\n\n']

    if phase == "FF":
        latest_round_games = [game for game in played_games if game["phaseType"]["code"] == phase]
        results = ['<b>Final Four!</b>\n\n']

    # Formatting the results
    for game in latest_round_games:
        local_team = game["local"]["club"]["abbreviatedName"]
        road_team = game["road"]["club"]["abbreviatedName"]
        local_score = game["local"]["score"]
        road_score = game["road"]["score"]
        game_date = game["date"][:10]
        results.append(f"{game_date} | <b>{local_team}</b> - <b>{road_team:<15}</b> {local_score:>3}:{road_score:<3}")

    message = "\n\n".join(results)
    await callback.message.answer(message, reply_markup= await kb.euro())


@router.callback_query(F.data == "FUTURE_EURO_GAMES")
async def future_euro_games(callback: CallbackQuery):
    await callback.answer()

    url_games = bdata.Euro_endpoints().games(seasonCode=seasonCode)
    data = await bdata.fetch_data(url_games)
    if not data:
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
    for game in upcoming_games:
        local_team = game["local"]["club"]["abbreviatedName"]
        road_team = game["road"]["club"]["abbreviatedName"]
        game_date = game["date"][:10]
        utc_time = datetime.strptime(game["utcDate"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        moscow_time = utc_time.astimezone(MOSCOW_TZ).strftime("%H:%M")
        results.append(f"{game_date} {moscow_time} | <b>{local_team:<15}</b> vs <b>{road_team:<15}</b>")

    message = f"Предстоящие матчи (время Мск):\n\n" + "\n\n".join(results)
    await callback.message.answer(message, reply_markup= await kb.euro())


@router.callback_query(F.data == "STANDINGS_EURO")
async def standings_euro(callback: CallbackQuery):
    await callback.answer()

    url_games = bdata.Euro_endpoints().games(seasonCode=seasonCode)
    data = await bdata.fetch_data(url_games)
    if not data:
        await callback.message.answer("Нет ответа от сервера.", reply_markup= await kb.euro())

    # Defining the latest round (max round)
    played_games = [game for game in data["data"] if game["played"]]
    latest_round = max(game["round"] for game in played_games)

    if latest_round <= 34:
        roundNumber = latest_round
    else:
        roundNumber = 34

    url_standings = bdata.Euro_endpoints().standings(roundNumber)

    sdata = await bdata.fetch_data(url_standings)

    standings = sdata[0].get("standings", [])
    if not standings:
        await callback.message.answer("Нет данных о турнирной таблице.")

    # Formatting the table
    results = [f"{' ':<5} {'Команда':<30} {'Игры':<10}%\n", f"{"-" * 33}"]
    for team in standings:
        position = team["data"]["position"]
        name = team["club"]["abbreviatedName"]
        games_played = team["data"]["gamesPlayed"]
        games_won = team["data"]["gamesWon"]
        win_percentage = (games_won / games_played * 100) if games_played else 0
        results.append(f"{position:<5} {name:<20} {games_played:<5} {win_percentage:.1f}%")

    message = "\n".join(results)
    await callback.message.answer(message, reply_markup=await kb.euro())


@router.callback_query(F.data == "STANDINGS_NBA")
async def standings_nba(callback: CallbackQuery):
    await callback.answer()

    URL_STANDINGS = bdata.NBA_endpoints().standings(season=season)
    data = await bdata.fetch_data(URL_STANDINGS)
    if not data:
        await callback.message.answer("Нет ответа от сервера.", reply_markup=await kb.nba())

    eastern_conf = [team for team in data if team["Conference"] == "Eastern"]
    western_conf = [team for team in data if team["Conference"] == "Western"]

    async def format_table(teams, conference_name):
        sorted_teams = sorted(teams, key=lambda x: x["ConferenceRank"])
        results = [f"<b>{conference_name}</b>\n", f"{' ':<5} {'Команда':<30} {'Игры':<10}%\n", f"{"-" * 33}"]

        for team in sorted_teams:
            position = team["ConferenceRank"]
            city = team["City"]
            games_played = team["Wins"] + team["Losses"]
            win_percentage = team["Percentage"]
            results.append(f"{position:<8} {city:<20} {games_played:<5} {win_percentage*100:.1f}%")

        output = "\n".join(results)
        await callback.message.answer(output)

    await format_table(eastern_conf, "Восточная конеренция")
    await format_table(western_conf, "Западная конференция")
    await callback.message.answer('Что-нибудь еще?', reply_markup=await kb.nba())


@router.callback_query(F.data == "PAST_NBA_GAMES")
async def past_nba_games(callback: CallbackQuery):
    await callback.answer()
    if datetime.today() < datetime(current_year, 4, 14):
        await callback.message.answer('Регулярка НБА настолько длинная и бессмысленная,'
                                      'что разработчику лень заморачиваться с этим.'
                                      'Подожди, пожалуйста, до начала плей-офф 🤷‍♂️',
                                      reply_markup=await kb.nba())
    else:
        url_games = bdata.NBA_endpoints().po_games(season=season_po)
        games = await bdata.fetch_data(url_games)
        if not games:
            await callback.message.answer("Нет ответа от сервера.", reply_markup=await kb.nba())

        results = []
        for game in games:
            gameday = datetime.strptime(game["Day"], "%Y-%m-%dT%H:%M:%S")

            if (datetime.today() - timedelta(weeks=1)) < gameday < datetime.today():
                results.append(f"{game["Day"][:10]} | <b>{sports.NBA_teams[game["HomeTeam"]].value}</b> - "
                               f"<b>{sports.NBA_teams[game["AwayTeam"]].value:<15}</b> "
                               f"{game["HomeTeamScore"]}:{game["AwayTeamScore"]}")

        message = "\n".join(results)
        await callback.message.answer(message, reply_markup=await kb.nba())


@router.callback_query(F.data == "FUTURE_NBA_GAMES")
async def future_nba_games(callback: CallbackQuery):
    await callback.answer()
    if datetime.today() < datetime(current_year, 4, 14):
        await callback.message.answer('Регулярка НБА настолько длинная и бессмысленная,'
                                      'что разработчику лень заморачиваться с этим.'
                                      'Подожди, пожалуйста, до начала плей-офф 🤷‍♂️',
                                      reply_markup=await kb.nba())
    else:
        url_games = bdata.NBA_endpoints().po_games(season=season_po)
        games = await bdata.fetch_data(url_games)
        if not games:
            await callback.message.answer("Нет ответа от сервера.", reply_markup=await kb.nba())

        results = []
        for game in games:
            gameday = datetime.strptime(game["Day"], "%Y-%m-%dT%H:%M:%S")
            utc_time = datetime.strptime(game["DateTimeUTC"], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
            moscow_time = utc_time.astimezone(MOSCOW_TZ).strftime("%H:%M")

            if datetime.today() <= gameday < (datetime.today() + timedelta(weeks=1)):
                results.append(f"{game["Day"][:10]} {moscow_time} | "
                               f"<b>{sports.NBA_teams[game["HomeTeam"]].value:<15}</b> - "
                               f"<b>{sports.NBA_teams[game["AwayTeam"]].value:>15}</b>")

        message = f"Предстоящие матчи (время Мск):\n\n" + "\n\n".join(results)
        await callback.message.answer(message, reply_markup=await kb.nba())




