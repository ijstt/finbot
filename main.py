import ast
import asyncio
import logging
import random
from asyncio import sleep

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

import config
import keyboard as kb
import keyboard_casino
from db import Database
from slots import get_result_text

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=storage)

db = Database("fin.db")


class GameStates(StatesGroup):
    waiting_for_bet_1 = State()
    waiting_for_roll = State()
    waiting_for_bet_2 = State()
    waiting_for_twist = State()
    waiting_for_bet_3 = State()
    waiting_for_rps = State()


# Создаем словарь пользователей и их балансов внутриигровой валюты (можно заменить на базу данных)
users = {}


def get_max_ball(quiz_level):
    max_ball = 0
    if quiz_level == "easy":
        max_ball = 6
    elif quiz_level == "medium":
        max_ball = 9
    elif quiz_level == "hard":
        max_ball = 12

    return max_ball


def parse_currency():
    data_curse = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    return data_curse['Valute']


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        db.set_nickname(message.from_user.id, message.from_user.full_name)
        await message.answer("Привет, я твой чат-бот по финансовой грамотности", reply_markup=kb.menu)
    else:
        await message.answer(f"Привет {db.get_nickname(message.from_user.id)}!", reply_markup=kb.menu)


@dp.message_handler(text=["Личный кабинет"])
async def mycabinet(message: types.Message):
    id = message.from_user.id
    full_name = message.from_user.full_name
    await message.answer(f"Твой ник - {full_name}\n"
                         f"Баллы за викторину - "
                         f"{db.get_quiz(id)} из {get_max_ball(db.get_quiz_lvl(id))} баллов", reply_markup=kb.lk_cab)


@dp.message_handler(text=["Меню"])
async def menu(message: types.Message):
    await message.answer(text="Выбери раздел", reply_markup=kb.menu_next)


@dp.message_handler(commands=["help"])
async def help_to_user(message: types.Message):
    await message.answer(text="Обратитесь в тех поддержку")


@dp.callback_query_handler(lambda x: x.data == "finhelp")
async def finhelp(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, config.TEXT_FOR_TERM, reply_markup=kb.next1)


@dp.callback_query_handler(lambda x: x.data[:4] == "next")
async def next_state(callback_query: types.CallbackQuery):
    data = callback_query.data[10:]

    if data == "1":
        await bot.send_message(callback_query.from_user.id, config.TEXT_FOR_TERM2, reply_markup=kb.next2)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    if data == "2":
        await bot.send_message(callback_query.from_user.id, config.TEXT_FOR_TERM3, reply_markup=kb.next3)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    if data == "3":
        await bot.send_message(callback_query.from_user.id, config.TEXT_FOR_TERM4, reply_markup=kb.next4)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


@dp.callback_query_handler(lambda x: x.data[:4] == "back")
async def back_state(callback_query: types.CallbackQuery):
    data = callback_query.data[10:]

    if data == "3":
        await bot.send_message(callback_query.from_user.id, config.TEXT_FOR_TERM2, reply_markup=kb.next2)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    if data == "4":
        await bot.send_message(callback_query.from_user.id, config.TEXT_FOR_TERM3, reply_markup=kb.next3)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    if data == "1":
        await bot.send_message(callback_query.from_user.id, config.TEXT_FOR_TERM4, reply_markup=kb.next4)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    else:
        await bot.send_message(callback_query.from_user.id, config.TEXT_FOR_TERM, reply_markup=kb.next1)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


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
        await start_bot(callback_query)

    else:
        await bot.send_message(callback_query.from_user.id, "Вы уверены что хотите играть?",
                               reply_markup=kb.continue_game)


# Хэндлер для запуска бота
async def start_bot(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in users:
        users[user_id] = 5000
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"""\
    <b>Добро пожаловать в наше виртуальное казино!</b>
    У вас {users[user_id]} очков 💵. Вы можете ставить ставки и играть в игры🎮.
    <b>Внимание</b>: бот предназначен исключительно для демонстрации, и ваши данные могут быть сброшены в любой момент! 
    Помните: лудомания — это болезнь, и никаких платных опций в боте нет.
    Для получения более подробной информации нажмите кнопку: Помощь 🔍
    """,
                           parse_mode="HTML",
                           reply_markup=keyboard_casino.mainMenu)


# Хэндлер для просмотра баланса
@dp.message_handler(text=[config.BALANCE])
async def cmd_balance(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Меню баланса💵',
                           parse_mode="HTML",
                           reply_markup=keyboard_casino.balanceMenu)
    # Проверяем, есть ли пользователь в словаре
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = 10000
    # Отправляем сообщение о балансе внутриигровой валюты
    await message.answer(f'Ваш баланс: {users[user_id]}\n'
                         f'Если у вас закончились деньги вы можете пополнить баланс на 100 💸')


@dp.message_handler(text=[config.BALANCE_PAY])
async def cmd_balance(message: types.Message):
    user_id = message.from_user.id
    pay_balance = message.text
    if user_id not in users:
        users[user_id] = 10000
    if pay_balance == config.BALANCE_PAY:
        if users[user_id] <= 0:
            users[user_id] = 100
            await message.answer(f'Вы успешно пополнили баланс, ваш баланс составляет 100💸')
        else:
            await message.answer(f'Ваш баланс: {users[user_id]} 💸, вы не можете пополнить баланс.')


# Хэндлер для перехода в главное меню
@dp.message_handler(text=[config.MAIN_MENU])
async def main_menu_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы перешли в главное меню🕹',
                           parse_mode="HTML",
                           reply_markup=keyboard_casino.mainMenu)


# Хэндлер для перехода в меню игр
@dp.message_handler(text=[config.GAMES])
async def game_list_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы перешли в меню игры, где можете выбрать гру в которую хотите поиграть 🎮",
                           parse_mode="HTML",
                           reply_markup=keyboard_casino.gamesMenu)


@dp.message_handler(text=[config.DISCR])
async def discr_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Простой симулятор казино 🎰. Создан исключительно в научных и развлекательных целях.",
                           parse_mode="HTML")


@dp.message_handler(text=[config.HELP])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=config.HELP_COMMAND,
                           parse_mode="HTML")


# Хэндлер для остановки игры
@dp.message_handler(text=[config.STOP_GAME], state='*')
async def stop_game_handler(message: types.Message, state: FSMContext):
    # Стираем состояние и возвращаем на начальный этап
    await state.finish()
    await message.answer('Игра остановлена ❌')
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вы перешли в меню игр 🎮",
                           parse_mode="HTML",
                           reply_markup=keyboard_casino.gamesMenu)


@dp.message_handler(text=[config.DICE_GAME])
async def main_menu_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Игра в кости 🎲',
                           parse_mode="HTML",
                           reply_markup=keyboard_casino.menuDice)
    # Отправляем сообщение с правилами игры
    await message.answer(
        'Правила игры:\n1. Сделайте ставку\n2. Киньте кубик\n3. Если у вас больше очков на кубике - получите удвоенную ставку, иначе - проиграете ставку')
    # Запускаем первый шаг состояния в ожидании ставки
    await GameStates.waiting_for_bet_1.set()


@dp.message_handler(state=GameStates.waiting_for_bet_1)
async def get_user_bet(message: types.Message, state: FSMContext):
    # Получаем ставку от пользователя
    bet = message.text
    # Проверяем, что ставка является числом
    if not bet.isdigit():
        await message.answer('Ставка должна быть целым числом. Попробуйте еще раз.')
        return
    # Проверяем, что у пользователя достаточно средств для ставки
    user_id = message.from_user.id
    if int(bet) > users[user_id]:
        await message.answer('Недостаточно средств на балансе. Попробуйте уменьшить ставку или пополнить баланс.')
        return
    # Запоминаем ставку и переходим к следующему шагу состояния
    async with state.proxy() as data:
        data['bet'] = int(bet)
    await message.answer(
        f'Вы выбрали ставку: {bet}\nКиньте кубик 🎲')
    await GameStates.waiting_for_roll.set()


@dp.message_handler(state=GameStates.waiting_for_roll)
async def get_user_bet(message: types.Message, state: FSMContext):
    # Получаем выбор пользователя
    roll = message.text
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = 10000
    # Проверяем, что выбор является числом от 1 до 4
    if roll != config.ROLL_THE_DICE:
        await message.answer('Киньте кубик 🎲')
        return
    # Получаем ставку и переходим к следующему шагу состояния
    async with state.proxy() as data:
        bet = data['bet']
    bot_data = await bot.send_dice(message.from_user.id)
    bot_data = bot_data['dice']['value']
    await sleep(5)

    user_data = await bot.send_dice(message.from_user.id)
    user_data = user_data['dice']['value']
    await sleep(5)

    if bot_data > user_data:
        users[message.from_user.id] -= bet
        await bot.send_message(message.from_user.id, f"Вы проиграли! Ваш баланс: {users[user_id]}")
    elif bot_data < user_data:
        users[message.from_user.id] += bet
        await bot.send_message(message.from_user.id, f"Вы выиграли! Ваш баланс: {users[user_id]}")
    else:
        await bot.send_message(message.from_user.id, f"Ничья! Ваш баланс: {users[user_id]}")
    # Завершаем игру и возвращаемся на начальный этап состояния
    await GameStates.waiting_for_bet_1.set()


@dp.message_handler(text=[config.GAMES_SLOTS])
async def main_menu_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Игра в слоты 🎰',
                           parse_mode="HTML",
                           reply_markup=keyboard_casino.menuSlots)
    # Отправляем сообщение с правилами игры
    await message.answer(
        'Правила игры:\n1. Сделайте ставку\n2. Крутите слот\n'
        '3. Если у вас все 3 одинаковых символа, кроме 3 семёрок - получите утроенную ставку'
        ', если у вас с самого начала только два одинаковых символа - получите удвоенную ставку,'
        ' если у вас 3 семёрки - получаете в пять раз больше, чем ставили, иначе - проиграете ставку')
    # Запускаем первый шаг состояния в ожидании ставки
    await GameStates.waiting_for_bet_2.set()


@dp.message_handler(state=GameStates.waiting_for_bet_2)
async def get_user_bet(message: types.Message, state: FSMContext):
    # Получаем ставку от пользователя
    bet = message.text
    # Проверяем, что ставка является числом
    if not bet.isdigit():
        await message.answer('Ставка должна быть целым числом. Попробуйте еще раз.')
        return
    # Проверяем, что у пользователя достаточно средств для ставки
    user_id = message.from_user.id
    if int(bet) > users[user_id]:
        await message.answer('Недостаточно средств на балансе. Попробуйте уменьшить ставку или пополнить баланс.')
        return
    # Запоминаем ставку и переходим к следующему шагу состояния
    async with state.proxy() as data:
        data['bet'] = int(bet)
    await message.answer(
        f'Вы выбрали ставку: {bet}\nКрутите слот 🎰')
    await GameStates.waiting_for_twist.set()


@dp.message_handler(state=GameStates.waiting_for_twist)
async def get_user_bet(message: types.Message, state: FSMContext):
    # Получаем выбор пользователя
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = 10000
    twist = message.text
    # Проверяем, что выбор является числом от 1 до 4
    if twist != config.TWIST:
        await message.answer('Крутите слот 🎰')
        return
    # Получаем ставку и переходим к следующему шагу состояния
    async with state.proxy() as data:
        bet = data['bet']
    result_dice = await message.answer_dice(emoji='🎰')
    await asyncio.sleep(3)
    text = get_result_text(result_dice=result_dice.dice.value, bid=bet)
    point = text[-1]
    users[message.from_user.id] += point
    await message.answer(text=text[0])
    await GameStates.waiting_for_bet_2.set()


@dp.message_handler(text=[config.RPS_GAME])
async def main_menu_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Игра в камень-ножницы-бумага ✂',
                           parse_mode="HTML",
                           reply_markup=keyboard_casino.menuRPS)
    # Отправляем сообщение с правилами игры
    await message.answer(
        'Правила игры:\n1. Сделайте ставку\n2. Выберете камень или бумагу или ножницы\n3. Если у вас камень,'
        ' а у противника ножницы - вы выиграли,'
        ' если у вас бумага, а у противника камень - вы выиграли,'
        ' если у вас ножницы, а у противника бумага - вы выиграли,'
        ' если наоборот - вы проиграли, при одинаковых комбинация - ничья, при выигрыше баланс удваивается.')
    # Запускаем первый шаг состояния в ожидании ставки
    await GameStates.waiting_for_bet_3.set()


@dp.message_handler(state=GameStates.waiting_for_bet_3)
async def get_user_bet(message: types.Message, state: FSMContext):
    # Получаем ставку от пользователя
    bet = message.text
    # Проверяем, что ставка является числом
    if not bet.isdigit():
        await message.answer('Ставка должна быть целым числом. Попробуйте еще раз.')
        return
    # Проверяем, что у пользователя достаточно средств для ставки
    user_id = message.from_user.id
    if int(bet) > users[user_id]:
        await message.answer('Недостаточно средств на балансе. Попробуйте уменьшить ставку или пополнить баланс.')
        return
    # Запоминаем ставку и переходим к следующему шагу состояния
    async with state.proxy() as data:
        data['bet'] = int(bet)
    await message.answer(
        f'Вы выбрали ставку: {bet}\nВыберите предмет!')
    await GameStates.waiting_for_rps.set()


@dp.message_handler(state=GameStates.waiting_for_rps)
async def get_user_bet(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = 10000
    # Получаем выбор пользователя
    choice_rps = message.text
    q = random.choice(['Камень✊', 'Ножницы✌', 'Бумага🖐'])
    # Получаем ставку и переходим к следующему шагу состояния
    async with state.proxy() as data:
        bet = data['bet']
    await bot.send_message(message.from_user.id, f"Вы выбрали {choice_rps}, а я выбрал {q}")
    if choice_rps == q:
        await bot.send_message(message.from_user.id, f"Ничья! Ваш баланс: {users[user_id]}")
    elif choice_rps == "Камень✊" and q == "Ножницы✌":
        users[message.from_user.id] += bet
        await bot.send_message(message.from_user.id, f"Вы выиграли! Ваш баланс: {users[user_id]}")
    elif choice_rps == "Ножницы✌" and q == "Бумага🖐":
        users[message.from_user.id] += bet
        await bot.send_message(message.from_user.id, f"Вы выиграли! Ваш баланс: {users[user_id]}")
    elif choice_rps == "Бумага🖐" and q == "Камень✊":
        users[message.from_user.id] += bet
        await bot.send_message(message.from_user.id, f"Вы выиграли! Ваш баланс: {users[user_id]}")
    elif choice_rps == "" and q == "Камень✊":
        users[message.from_user.id] += bet
        await bot.send_message(message.from_user.id, f"Вы выиграли! Ваш баланс: {users[user_id]}")

    else:
        users[message.from_user.id] -= bet
        await bot.send_message(message.from_user.id, f"Вы проиграли! Ваш баланс: {users[user_id]}")
    # Завершаем игру и возвращаемся на начальный этап состояния
    await GameStates.waiting_for_bet_3.set()


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
            db.set_data_quest(db.get_ques(10), callback_query.from_user.id)
            await check_quiz(callback_query)

        elif data[4:] == "hard":
            db.set_quiz_lvl("hard", callback_query.from_user.id)
            db.set_data_quest(db.get_ques(13), callback_query.from_user.id)
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
                           f"Вы набрали - "
                           f"{db.get_quiz(callback_query.from_user.id)} из {get_max_ball(db.get_quiz_lvl(callback_query.from_user.id))} баллов")


@dp.message_handler(text=["Вернуться в бота⬅"])
async def in_bot(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы вернулись назад", reply_markup=kb.menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
