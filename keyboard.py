from aiogram import types

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
lk = types.KeyboardButton("Личный кабинет")
menu_que = types.KeyboardButton("Меню")
menu.add(menu_que, lk)

menu_next = types.InlineKeyboardMarkup(row_width=1)
convert = types.InlineKeyboardButton("Конвертация", callback_data="convert")
curse = types.InlineKeyboardButton("Курс валют", callback_data="curse")
quiz = types.InlineKeyboardButton("Викторина", callback_data="quiz")
game = types.InlineKeyboardButton("Игра", callback_data="game")
menu_next.add(convert, curse, quiz, game)

fin_help = types.InlineKeyboardMarkup(row_width=1)
next_state = types.InlineKeyboardButton("Next", callback_data="next_state")
fin_help.add(next_state)