import logging
import os
import aiohttp
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()
ALLSPORTDB_TOKEN = os.getenv('ALLSPORTDB_TOKEN')

class Athletics_endpoints():
    server = 'https://api.allsportdb.com/v3/'

    def calendar(self, dateFrom, dateTo, competitionId, page=1):
        url = (f'{Athletics_endpoints.server}calendar?dateFrom={dateFrom}&dateTo={dateTo}&competitionId={competitionId}'
               f'&page={page}')
        return url


async def fetch_data(url: str):
    headers = {
        "Authorization": f"Bearer {ALLSPORTDB_TOKEN}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                logger.error(f'No server answer {response.status}')
                return None