import logging
import requests

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
        db.set_level(message.from_user.id, "Null")
        await message.answer("Привет, я твой чат-бот по финансовой грамотности", reply_markup=kb.menu)
    else:
        await message.answer(f"Привет {db.get_nickname(message.from_user.id)}!", reply_markup=kb.menu)


@dp.message_handler(text=["Личный кабинет"])
async def mycabinet(message: types.Message):
    id = message.from_user.id
    full_name = message.from_user.full_name
    await message.answer(f"Твой ник - {full_name}\n"
                         f"Уровень знаний - {db.get_level(id)}\n"
                         f"Баллы за викторину - {db.get_quiz(id)}")


@dp.message_handler(text=["Меню"])
async def menu(message: types.Message):
    await message.answer(text="Выбери раздел", reply_markup=kb.menu_next)


@dp.message_handler(commands=["help"])
async def help_to_user(message: types.Message):
    await message.answer(text="Обратитесь в тех поддержку")


@dp.message_handler(commands=["finhelp"])
async def finhelp(message: types.Message):
    await message.answer("Терминология:", reply_markup=kb.fin_help)


@dp.callback_query_handler(lambda x: x.data[:5] == "curse")
async def curse(callback_query: types.CallbackQuery):
    data = callback_query.data
    valut = data[5:]
    data_curse = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

    if data == "curse":
        await bot.send_message(callback_query.from_user.id, "Выберите валюту:", reply_markup=kb.curse)

    elif valut == "usd":
        if float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) > 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Доллар к рублю:\n" + str(data_curse['Valute'][valut.upper()]['Value']) + " рублей↑")

        elif float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) < 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Доллар к рублю:\n" + str(data_curse['Valute'][valut.upper()]['Value']) + " рублей↓")

        else:
            await bot.send_message(callback_query.from_user.id,
                                   "Доллар к рублю:\n" + data_curse['Valute'][valut.upper()]['Value'] + " рублей")

    elif valut == "eur":
        if float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) > 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Евро к рублю:\n" + str(data_curse['Valute'][valut.upper()]['Value']) + " рублей↑")

        elif float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) < 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Евро к рублю:\n" + str(data_curse['Valute'][valut.upper()]['Value']) + " рублей↓")

        else:
            await bot.send_message(callback_query.from_user.id,
                                   "Евро к рублю:\n" + data_curse['Valute'][valut.upper()]['Value'] + " рублей")

    elif valut == "cny":
        if float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) > 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Юань к рублю:\n" + str(data_curse['Valute'][valut.upper()]['Value']) + " рублей↑")

        elif float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) < 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Юань к рублю:\n" + str(data_curse['Valute'][valut.upper()]['Value']) + " рублей↓")

        else:
            await bot.send_message(callback_query.from_user.id,
                                   "Юань к рублю:\n" + data_curse['Valute'][valut.upper()]['Value'] + " рублей")

    elif valut == " kzt":
        if float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) > 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Тенге к рублю:\n" + str(data_curse['Valute'][valut.upper()]['Value']) + " рублей↑")

        elif float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) < 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Тенге к рублю:\n" + str(data_curse['Valute'][valut.upper()]['Value']) + " рублей↓")

        else:
            await bot.send_message(callback_query.from_user.id,
                                   "Тенге к рублю:\n" + data_curse['Valute'][valut.upper()]['Value'] + " рублей")

    elif valut == "byn":
        if float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) > 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Белорусский рубль к Российскому рублю:\n" + str(
                                       data_curse['Valute'][valut.upper()]['Value']) + " рублей↑")

        elif float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) < 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Белорусский рубль к Российскому рублю:\n" + str(
                                       data_curse['Valute'][valut.upper()]['Value']) + " рублей↓")

        else:
            await bot.send_message(callback_query.from_user.id,
                                   "Белорусский рубль к Российскому рублю:\n" + data_curse['Valute'][valut.upper()][
                                       'Value'] + " рублей")

    elif valut == "uah":
        if float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) > 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Гривень к рублю:\n" + str(
                                       data_curse['Valute'][valut.upper()]['Value']) + " рублей↑")

        elif float(data_curse['Valute'][valut.upper()]['Value']) - float(
                data_curse['Valute'][valut.upper()]['Previous']) < 0:
            await bot.send_message(callback_query.from_user.id,
                                   "Гривень к рублю:\n" + str(
                                       data_curse['Valute'][valut.upper()]['Value']) + " рублей↓")

        else:
            await bot.send_message(callback_query.from_user.id,
                                   "Гривень к рублю:\n" + data_curse['Valute'][valut.upper()]['Value'] + " рублей")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
