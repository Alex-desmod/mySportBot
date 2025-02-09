import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()
NBA_API_KEY = os.getenv('NBA_API_KEY')

class Euro_endpoints():
    server = 'https://api-live.euroleague.net/'

    def games(self, version='V2', competitionCode='E', seasonCode='E2024'):
        url = f'{Euro_endpoints.server}{version}/competitions/{competitionCode}/seasons/{seasonCode}/games'
        return url

    def standings(self, roundNumber, version='V2', competitionCode='E', seasonCode='E2024'):
        url = f'{Euro_endpoints.server}{version}/competitions/{competitionCode}/seasons/{seasonCode}/rounds/{roundNumber}/standings'
        return url


class NBA_endpoints():
    server = 'https://api.sportsdata.io/'

    def standings(self, version='v3', season='2025'):
        url = f'{NBA_endpoints.server}{version}/nba/scores/json/Standings/{season}?key={NBA_API_KEY}'
        return url


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return "No server answer"




