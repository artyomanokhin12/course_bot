import asyncio
from datetime import datetime

import aiohttp
import xml.etree.ElementTree as elem_tree
import redis.asyncio as redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config import bot_settings


def xml_to_dict(xml_string) -> dict:
    result = {}
    for elem in xml_string:
        result[elem[1].text] = float(elem[4].text.replace(',', '.'))

    return result


async def to_redis(data: dict):
    r = await redis.Redis(host=bot_settings.HOST, port=bot_settings.PORT)
    async with r.pipeline() as pipe:
        await pipe.flushdb()
        for key, val in data.items():
            await pipe.set(key, val)
        await pipe.execute()


async def data_to_redis(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                xml_text = await response.text()
                xml_format_string = elem_tree.fromstring(xml_text)
                cource_dict = xml_to_dict(xml_format_string)
                await to_redis(cource_dict)
            else:
                raise Exception(f"Нет доступа: {response.status}")


async def main():
    url = bot_settings.URL
    try:
        await data_to_redis(url)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, trigger=IntervalTrigger(days=1), next_run_time=datetime.now())
    scheduler.start()
    asyncio.get_event_loop().run_forever()
