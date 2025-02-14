import json

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
import app.handlers_basket as hb
import app.handlers_cycling as hc
import app.handlers_athletics as ha
import app.db.requests as rq

router = Router(name=__name__)
router.include_routers(hb.router, hc.router, ha.router)

with open("app/messages.json", "r", encoding="utf-8") as file:
    messages = json.load(file)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.first_name)
    await message.answer(f'Привет, {message.from_user.first_name} 😊\n{messages[0]["start"]}',
                         reply_markup= await kb.start())


@router.message(Command('basket'))
async def basket(message: Message):
    await message.answer('Выбери турнир', reply_markup= await kb.basket())


@router.message(Command('cycling'))
async def cycling(message: Message):
    await message.answer('У меня есть расписание главных велогонок планеты. Выбирай!',
                         reply_markup= await kb.cycling())


@router.message(Command('athletics'))
async def athletics(message: Message):
    await message.answer('Большие события из мира легкой атлетики',
                         reply_markup= await kb.athletics())


@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Вот что у меня в меню. Выбирай, если интересно.', reply_markup=await kb.start())


@router.message()
async def catch_all_messages(message: Message):
    await message.answer(messages[0]["sorry"],
                         reply_markup=await kb.start())







