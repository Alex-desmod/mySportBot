from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import app.sports as sports

async def start():
    kb = InlineKeyboardBuilder()
    for sport in sports.Sports:
        kb.add(InlineKeyboardButton(text=sport.value, callback_data=sport.name))

    return kb.adjust(1).as_markup()

async def basket():
    kb = InlineKeyboardBuilder()
    for competition in sports.Basket:
        kb.add(InlineKeyboardButton(text=competition.value, callback_data=competition.name))

    return kb.adjust(1).as_markup()

async def euro():
    kb = InlineKeyboardBuilder()
    for menu in sports.Euro:
        kb.add(InlineKeyboardButton(text=menu.value, callback_data=menu.name))
    kb.add(InlineKeyboardButton(text="Главное меню ⬅️", callback_data='BACK'))

    return kb.adjust(1).as_markup()



