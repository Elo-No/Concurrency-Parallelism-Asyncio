from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import asyncio
from environs import Env

env = Env()
env.read_env()


async def api_link(limit):
    api_key = env('APIKEY')
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
        'start': '1',
        'limit': limit,
        'cryptocurrency_type': 'all',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    session = Session()
    session.headers.update(headers)

    try:
        if limit >= '500000':
            await asyncio.sleep(0.1)
        print('start with limit ', limit)
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print('end with limit', limit)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


async def get_data():
    limits = ['500000', '100000', '100', '60000']
    tasks = []
    for limit in limits:
        tasks.append(loop.create_task(api_link(limit)))
    await asyncio.wait(tasks)

if __name__ == '__main__':
    start_time = time.time()
    try:
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(get_data())
    except Exception as e:
        print(e)
    finally:
        loop.close()
    end_time = time.time()
    print(f'duration time {int(end_time - start_time)} seconds')
