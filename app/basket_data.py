import aiohttp


class Euro_endpoints():
    server = 'https://api-live.euroleague.net/'

    def games(self, version='V2', competitionCode='E', seasonCode='E2024'):
        url = f'{Euro_endpoints.server}{version}/competitions/{competitionCode}/seasons/{seasonCode}/games'
        return url

    def standings(self, roundNumber, version='V2', competitionCode='E', seasonCode='E2024'):
        url = f'{Euro_endpoints.server}{version}/competitions/{competitionCode}/seasons/{seasonCode}/rounds/{roundNumber}/standings'
        return url


async def fetch_euro_games(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return "No server answer"




