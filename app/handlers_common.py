import json
import logging

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import app.keyboards as kb
import app.handlers_basket as hb
import app.handlers_cycling as hc
import app.handlers_athletics as ha
import app.db.requests as rq

router = Router(name=__name__)
router.include_routers(hb.router, hc.router, ha.router)

logger = logging.getLogger(__name__)

with open("app/messages.json", "r", encoding="utf-8") as file:
    messages = json.load(file)


#Defining the state for feedback
class FeedbackState(StatesGroup):
    waiting_for_feedback = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.first_name)
    await message.answer(f'Привет, {message.from_user.first_name} 😊\n{messages[0]["start"]}',
                         reply_markup=await kb.start())


@router.message(Command('basket'))
async def basket(message: Message):
    await message.answer(messages[0]["basket"],
                         reply_markup=await kb.basket())


@router.message(Command('cycling'))
async def cycling(message: Message):
    await message.answer(messages[0]["cycling"],
                         reply_markup=await kb.cycling())


@router.message(Command('athletics'))
async def athletics(message: Message):
    await message.answer(messages[0]["athletics"],
                         reply_markup=await kb.athletics())


@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(messages[0]["menu"],
                                  reply_markup=await kb.start())


@router.message(Command("feedback"))
async def ask_feedback(message: Message, state: FSMContext):
    await message.answer(messages[0]["feedback"],
                         reply_markup=kb.cancel_kb
                         )
    await state.set_state(FeedbackState.waiting_for_feedback)


@router.message(FeedbackState.waiting_for_feedback, F.text != "❌ Отмена")
async def forward_feedback(message: Message, bot: Bot, state: FSMContext):
    admins = await rq.get_admins()

    for admin in admins:
        await bot.send_message(
            admin.tg_id,
            f"📩 Новое сообщение от @{message.from_user.username or message.from_user.id}:\n\n{message.text}"
        )
    await message.answer(messages[0]["send"], reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(FeedbackState.waiting_for_feedback, F.text == "❌ Отмена")
async def cancel_feedback(message: Message, state: FSMContext):
    await message.answer(messages[0]["canceled"], reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message()
async def catch_all_messages(message: Message):
    await message.answer(messages[0]["sorry"],
                         reply_markup=await kb.start())
