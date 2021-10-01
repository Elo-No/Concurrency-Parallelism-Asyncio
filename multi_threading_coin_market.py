from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
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
        for i in range(100):
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def CallThread(num_thread):
    with ThreadPoolExecutor(max_workers=num_thread) as executor:
        limits = ["500000", "100000"]
        executor.map(api_link, limits)


if __name__ == '__main__':
    num_thread = 2
    start_time = time.time()
    ##### version of with-out thread #####
    # api_link("500000")
    # api_link("100000")
    ##### version of with thread ######
    CallThread(num_thread)
    end_time = time.time()
    print(f'duration time {int(end_time - start_time)} seconds')
