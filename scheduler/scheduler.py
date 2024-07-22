from aiogram import Bot
from arq import cron
from arq.connections import RedisSettings

from config import bot_settings
from redis_cache import main

pool_settins = RedisSettings(host=bot_settings.HOST, port=bot_settings.PORT)


# async def startup(ctx):
#     ctx['bot'] = Bot(token=bot_settings.BOT_API)


# async def shutdown(ctx):
#     await ctx['bot'].session.close()

# async def get_current_cources(ctx):
    # _token = bot_settings.BOT_API
    # bot: Bot = ctx['bot']
    # await main()



class WorkerSettings:
    redis_settings = pool_settins
    on_startup = startup
    on_shutdown = shutdown
    functions = [get_current_cources, ]
    cron_jobs = [
        cron('scheduler.scheduler.get_current_cources', second=0) #hour=13, minute=0)
    ]
    