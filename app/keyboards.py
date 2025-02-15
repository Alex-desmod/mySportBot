from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
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
    kb.add(InlineKeyboardButton(text="Главное меню 🔙", callback_data='back'))

    return kb.adjust(1).as_markup()


async def nba():
    kb = InlineKeyboardBuilder()
    for menu in sports.NBA:
        kb.add(InlineKeyboardButton(text=menu.value, callback_data=menu.name))
    kb.add(InlineKeyboardButton(text="Главное меню 🔙", callback_data='back'))

    return kb.adjust(1).as_markup()


async def cycling():
    kb = InlineKeyboardBuilder()
    for menu in sports.Cycling:
        kb.add(InlineKeyboardButton(text=menu.value, callback_data=menu.name))
    kb.add(InlineKeyboardButton(text="Главное меню 🔙", callback_data='back'))

    return kb.adjust(1).as_markup()


async def athletics():
    kb = InlineKeyboardBuilder()
    for menu in sports.Athletics:
        kb.add(InlineKeyboardButton(text=menu.value, callback_data=menu.name))
    kb.add(InlineKeyboardButton(text="Главное меню 🔙", callback_data='back'))

    return kb.adjust(1).as_markup()


cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]],
    resize_keyboard=True,
    one_time_keyboard=True
)



