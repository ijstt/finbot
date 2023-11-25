import logging
import requests
import ast

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


@dp.callback_query_handler(lambda x: x.data == "finhelp")
async def finhelp(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, config.TEXT_FOR_TERM, reply_markup=kb.fin_help)


@dp.callback_query_handler(lambda x: x.data == "next")
async def next(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, config.NEXT_TEXT_FOR_TERM, reply_markup=kb.next1)


@dp.callback_query_handler(lambda x: x.data[:10] == "next_state")
async def next_state(callback_query: types.CallbackQuery):
    data = callback_query.data[10:]

    if data == "0":
        await bot.send_message(callback_query.from_user.id, "")


@dp.callback_query_handler(lambda x: x.data[:5] == "curse")
async def curse(callback_query: types.CallbackQuery):
    data = callback_query.data
    valut = data[5:]
    data_curse = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

    if data == "curse":
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
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


@dp.callback_query_handler(lambda x: x.data[:4] == "game")
async def game(callback_query: types.CallbackQuery):
    data = callback_query.data[4:]

    if data == "no":
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, "Праильный выбор, ведь азартные игры это плохо!!")

    elif data == "yes":
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, "Не забывайте - азарт это плохо!!")

    else:
        await bot.send_message(callback_query.from_user.id, "Вы уверены что хотите играть?",
                               reply_markup=kb.continue_game)


@dp.callback_query_handler(lambda x: x.data[:4] == "quiz")
async def quiz(callback_query: types.CallbackQuery):
    data = callback_query.data
    if int(db.get_num_que(callback_query.from_user.id)) == 0:

        if data == "quiz":
            await bot.send_message(callback_query.from_user.id, "Хотиете ли вы начать тест?", reply_markup=kb.quiz_dt)

        elif data[4:] == "yes":
            await bot.send_message(callback_query.from_user.id, "Выберите сложность:", reply_markup=kb.qualiti)

        elif data[4:] == "no":
            await bot.send_message(callback_query.from_user.id, "Вы вернулись назад")

        elif data[4:] == "easy":
            db.set_quiz_lvl("easy", callback_query.from_user.id)
            db.set_data_quest(db.get_ques(7), callback_query.from_user.id)
            await check_quiz(callback_query)

        elif data[4:] == "medium":
            db.set_quiz_lvl("medium", callback_query.from_user.id)
            db.set_data_quest(db.get_ques(9), callback_query.from_user.id)
            await check_quiz(callback_query)

        elif data[4:] == "hard":
            db.set_quiz_lvl("hard", callback_query.from_user.id)
            db.set_data_quest(db.get_ques(11), callback_query.from_user.id)
            await check_quiz(callback_query)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    else:
        await bot.send_message(callback_query.from_user.id,
                               "Вы уже прошли викторину, с вашими баллами вы можете ознакомиться в личном кабинете")


@dp.callback_query_handler(lambda x: x.data in "АБВГ")
async def check_quiz(callback_query: types.CallbackQuery):
    ans = callback_query.data
    id_que = callback_query.from_user.id
    data = db.get_data_quest(id_que)
    num = int(db.get_num_que(id_que))
    flag = False

    if num == len(ast.literal_eval(data)):
        flag = True
        await bot.delete_message(id_que, callback_query.message.message_id)
        await bot.send_message(id_que, "Вы ответили на все вопросы!", reply_markup=kb.maker(3, True))

    else:
        nm = list(ast.literal_eval(data))[int(num)][3]
        await bot.send_message(id_que, text=list(ast.literal_eval(data))[num][1], reply_markup=kb.maker(nm, False))
        que = num + 1
        db.set_num_que(que, id_que)

    if not flag:
        if ans in list(ast.literal_eval(data))[num - 1][2]:
            ball = int(db.get_quiz(id_que))
            db.set_quiz(ball + 1, id_que)

        if num != 0:
            await bot.delete_message(id_que, callback_query.message.message_id)


@dp.callback_query_handler(lambda x: x.data == "end")
async def end_que(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           f"Вы набрали - {db.get_quiz(callback_query.from_user.id)} из ... баллов")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
