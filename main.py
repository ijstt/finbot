import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import keyboard as kb
from db import Database

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)

db = Database("fin.db")


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        db.set_nickname(message.from_user.id, message.from_user.full_name)
    await message.answer("Привет, я твой чат-бот по финансовой грамотности", reply_markup=kb.menu)


@dp.message_handler(text=["Личный кабинет"])
async def mycabinet(message: types.Message):
    id = message.from_user.id
    full_name = message.from_user.full_name
    await message.answer(f"Твой ник - {full_name}\n"
                         f"Уровень знаний - {db.get_level(id)}\n"
                         f"Баллы за викторину - ")


@dp.message_handler(text=["Меню"])
async def menu(message: types.Message):
    await message.answer(text="Выбери раздел", reply_markup=kb.menu_next)


@dp.message_handler(command=["help"])
async def help(message: types.Message):
    await message.answer("Обратитесь в тех поддержку")


@dp.message_handler(command=["finhelp"])
async def finhelp(message: types.Message):
    await message.answer("Терминология:", reply_markup=kb.finhelp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
