from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import config

btnMain = KeyboardButton(text=config.MAIN_MENU)
btnStop = KeyboardButton(text=config.STOP_GAME)

# main menu
btngames = KeyboardButton(text=config.GAMES)
btnbalance = KeyboardButton(text=config.BALANCE)
btnbalance_pay = KeyboardButton(text=config.BALANCE_PAY)
btndiscr = KeyboardButton(text=config.DISCR)
btnhelp = KeyboardButton(text=config.HELP)
btnback = KeyboardButton(text=config.BACK)
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btngames, btnbalance, btnhelp, btndiscr, btnback)

# games menu
btndice_game = KeyboardButton(text=config.DICE_GAME)
btngame_slots = KeyboardButton(text=config.GAMES_SLOTS)
btngame_rps = KeyboardButton(text=config.RPS_GAME)
gamesMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btndice_game, btngame_slots, btngame_rps, btnMain)

# menu Balance Pay
balanceMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnbalance_pay, btnMain)

# menu dice
btnroll_the_dice = KeyboardButton(text=config.ROLL_THE_DICE)
menuDice = ReplyKeyboardMarkup(resize_keyboard=True).add(btnroll_the_dice, btnStop)

# menu slots
btntwist = KeyboardButton(text=config.TWIST)
menuSlots = ReplyKeyboardMarkup(resize_keyboard=True).add(btntwist, btnStop)

# menu rps
btnr = KeyboardButton(text=config.ROCK)
btnp = KeyboardButton(text=config.PAPER)
btns = KeyboardButton(text=config.SCISSORS)
menuRPS = ReplyKeyboardMarkup(resize_keyboard=True).add(btnr, btns, btnp, btnStop)
