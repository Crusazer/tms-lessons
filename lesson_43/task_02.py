import asyncio
import time

import requests
import aiohttp

cities = ['Moscow', 'St. Petersburg', 'Rostov-on-Don', 'Kaliningrad', 'Vladivostok',
          'Minsk', 'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York']
URL_PATTERN = 'https://api.openweathermap.org/data/2.5/weather' \
              f'?appid=2a4ff86f9aaa70041ec8e82db64abf56&q=city&units=metric'


def request_fanc():
    for city in cities:
        url = URL_PATTERN.format(city=city)
        response = requests.get(url)
        print(response.text)


async def aiohttp_fanc():
    async with aiohttp.ClientSession() as session:
        for city in cities:
            url = URL_PATTERN.format(city=city)
            async with session.get(url) as aio_response:
                text = await aio_response.text()
                print(text)
                json = await aio_response.json()
                print(json)


time_start = time.time()
request_fanc()
time_middle = time.time()

asyncio.run(aiohttp_fanc())
time_end = time.time()
print(f"Sync {time_middle - time_start}")
print(f"Async {time_end - time_middle}")
