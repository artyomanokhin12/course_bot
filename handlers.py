from aiogram import Router
import aiogram.filters as aio_fiters
from aiogram.types import Message

import redis.asyncio as redis

from config import bot_settings


router = Router()

@router.message(aio_fiters.Command(commands=['exchange']))
async def start_command(message: Message, command: aio_fiters.command.CommandObject) -> Message | None:
    if command.args is None:
        return await message.answer('Вы не передали никаких аргументов. Пожалуйста, передайте валюты и сумму, которую нужно конвертировать')
    try:
        base_val, new_val, quantity = command.args.split(' ', maxsplit=2)
        r = await redis.Redis(host=bot_settings.HOST, port=bot_settings.PORT)
        async with r.pipeline() as pipe:
            await pipe.get(base_val)
            if new_val != "RUB":
                await pipe.get(new_val)
            val_bytes = await pipe.execute()
        if len(val_bytes) > 1:
            final_price = round((float(val_bytes[0].decode())/float(val_bytes[1].decode())) * int(quantity), 4)
        else:
            final_price = round(float(val_bytes[0].decode()) * int(quantity), 4)
        await message.answer(f"Текущая стоимость {quantity} {base_val} в {new_val} - {final_price}")
    except ValueError:
        await message.answer(
            'Ошибка: неправильный формат команды. Пример\n'
            '/exchange <Конвертируемая валюта> <Валюта, в которую нужно конвертировать цену> <Количество, которое нужно конвертировать>'
        )


@router.message(aio_fiters.Command(commands=['rates']))
async def get_rates(message: Message) -> Message:
    current_rates = ''
    r = await redis.Redis(host=bot_settings.HOST, port=bot_settings.PORT)
    async with r.pipeline() as pipe:
        await pipe.keys('*')
        keys = await pipe.execute()
        for key in keys[0]:
            await pipe.get(key)
        result = await pipe.execute()
        for key, value in zip(keys[0], result):
            current_rates = current_rates + key.decode() + " " + value.decode() + '\n'
    return await message.answer(current_rates)

@router.message()
async def empty_message(message: Message):
    await message.answer('Увы, но я не понимаю эту команду')
