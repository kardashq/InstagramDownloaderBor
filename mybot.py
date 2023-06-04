import os
from dotenv import load_dotenv
import instaloader

from aiogram import Bot, Dispatcher, executor, types, filters

load_dotenv()

inst = instaloader.Instaloader()

bot = Bot(token=os.getenv('API_TOKEN'))
dp = Dispatcher(bot)

username = os.getenv('username')
password = os.getenv('pass')

kb_open_close = types.ReplyKeyboardMarkup(resize_keyboard=True)
b1 = types.KeyboardButton(text='Открытый')
b2 = types.KeyboardButton(text='Закрытый')
kb_open_close.add(b1, b2)

inline_buttons = types.InlineKeyboardMarkup(row_width=2)
button1 = types.InlineKeyboardButton(text='Открытый аккаунт', callback_data='open')
button2 = types.InlineKeyboardButton(text='Закрытый аккаунт', callback_data='private')

inline_buttons.add(button1, button2)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет!\nЯ - InstagramDownloaderBot!"
                         "\nЯ помогу тебе скачать что угодно из Instagram!\nВыбери тип аккаунта:",
                         reply_markup=kb_open_close)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Я могу скачать фото или видео из инстаграма, тебе нужно только отправить ссылку на фото.\n"
                        "Однако, мне необходимо авторизоваться под твоим логином и паролем")


@dp.message_handler(filters.Text(equals='Открытый'))
async def check_open_ac(message: types.Message):
    await message.reply("Была нажата кнопка Отк")


@dp.message_handler(filters.Text(equals='Закрытый'))
async def check_private_ac(message: types.Message):
    await message.reply("Т.к. аккаунт закрытый, необходимо войти.\n"
                        "Отправьте логин и пароль в следующем сообщении через :: ,\n"
                        "Например login::password", reply_markup=types.ReplyKeyboardRemove())


kb_acc_post = types.ReplyKeyboardMarkup(resize_keyboard=True)
acc_b1 = types.KeyboardButton(text='Аккаунт')
acc_b2 = types.KeyboardButton(text='Пост')
kb_acc_post.add(acc_b1, acc_b2)


@dp.message_handler(filters.Text(contains='::'))
async def process_upass(message: types.Message):
    username, password = message.text.split('::')
    await message.reply('Логин и пароль сохранены. Выберите что скачивать: ', reply_markup=kb_acc_post)


@dp.message_handler(filters.Text(equals='Пост'))
async def check_private_ac(message: types.Message):
    await message.reply("Отправьте ссылку на пост: ", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(filters.Text(contains='instagram.com/'))
async def process_upass(message: types.Message):
    if '/p/' in message.text:
        link = message.text.split('/p/')[1]
        p = inst.download_post(link)
    else:
        link = message.text.split('instagram.com/')[1][:-1]
        inst.download_profile(link)
        await message.reply('OK')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
