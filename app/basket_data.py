import aiohttp
import json


class Euro_endpoints():
    server = 'https://api-live.euroleague.net/'

    def games(self, version='V2', competitionCode='E', seasonCode='E2024'):
        url = f'{Euro_endpoints.server}{version}/competitions/{competitionCode}/seasons/{seasonCode}/games'
        return url

async def fetch_euro_games():
    async with aiohttp.ClientSession() as session:
        async with session.get(Euro_endpoints().games()) as response:
            return await response.json()
