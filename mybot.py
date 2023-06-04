import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types

load_dotenv()

bot = Bot(token=os.getenv('API_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer("Привет!\nЯ - InstagramDownloaderBot!\nЯ помогу тебе скачать что угодно из Instagram!\nВыбери нужное тебе:")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
