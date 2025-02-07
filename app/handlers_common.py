from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
import app.handlers_basket as hb
import app.handlers_cycling as hc
import app.handlers_athletics as ha
import app.db.requests as rq

router = Router()
router.include_routers(hb.router, hc.router, ha.router)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id, message.from_user.first_name)
    await message.answer(f'Привет, {message.from_user.first_name} 😊\n'
                         f'Я не самый продвинутый в мире бот, и в общем-то создан только для того, чтобы мой '
                         f'разработчик потренировал свои скромные скиллы. Но я могу предложить расписание и последние '
                         f'результаты некоторых спортивных соревнований. Выбор ограничен узким кругозором '
                         f'разработчика. Может быть попозже он додумается до чего-то еще 😉',
                         reply_markup= await kb.start())

@router.callback_query(F.data.startswith("BACK"))
async def back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Вот что у меня в меню. Выбирай, если интересно.', reply_markup=await kb.start())


@router.message()
async def catch_all_messages(message: Message):
    await message.answer("Сорри, я тупой бот и не умею отвечать на сообщения. Пожалуйста, выбери что-нибудь из меню",
                         reply_markup=await kb.start())







