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
finhelp = types.InlineKeyboardButton("Справочная информация", callback_data="finhelp")
menu_next.add(finhelp, convert, curse, quiz, game)

fin_help = types.InlineKeyboardMarkup(row_width=1)
next_state = types.InlineKeyboardButton("Next", callback_data="next_state0")
fin_help.add(next_state)

next1 = types.InlineKeyboardMarkup(row_width=1)
n1 = types.InlineKeyboardButton("Next", callback_data="next_state1")
next1.add(n1)

curse = types.InlineKeyboardMarkup(row_width=2)
eur = types.InlineKeyboardButton("EUR", callback_data="curseeur")
usd = types.InlineKeyboardButton("USD", callback_data="curseusd")
cny = types.InlineKeyboardButton("CNY", callback_data="cursecny")
kzt = types.InlineKeyboardButton("KZT", callback_data="cursekzt")
byn = types.InlineKeyboardButton("BYN", callback_data="cursebyn")
uah = types.InlineKeyboardButton("UAH", callback_data="curseuah")
curse.add(eur, usd, cny, kzt, byn, uah)

continue_game = types.InlineKeyboardMarkup(row_width=2)
yes = types.InlineKeyboardButton("YES", callback_data="gameyes")
no = types.InlineKeyboardButton("NO", callback_data="gameno")
continue_game.add(yes, no)