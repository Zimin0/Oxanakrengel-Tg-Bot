import logging
import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = "YOUR_TOKEN_HERE"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def command_start_handler(message: types.Message):
    asyncio.run(message.answer(f"Hello, {message.from_user.full_name}!"))

def echo_handler(message: types.Message):
    asyncio.run(message.answer(message.text))

if __name__ == '__main__':
    @dp.message_handler(commands=['start'])
    def start(message: types.Message):
        command_start_handler(message)

    @dp.message_handler(func=lambda message: True)
    def echo(message: types.Message):
        echo_handler(message)

    asyncio.run(dp.start_polling())
