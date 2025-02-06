from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.keyboards as kb
import app.handlers_basket as hb


router = Router()
router.include_router(hb.router)

@router.message(CommandStart())
async def cmd_start(message: Message):
    #await rq.set_user(message.from_user.id)
    await message.answer(f'Привет, {message.from_user.first_name} 😊\n'
                         f'Я не самый продвинутый в мире бот, и в общем-то создан только для того, чтобы мой '
                         f'разработчик потренировал свои скромные скиллы. Но я могу предложить расписание и последние '
                         f'результаты некоторых спортивных соревнований. Выбор ограничен узким кругозором '
                         f'разработчика. Может быть попозже он додумается до чего-то еще 😉',
                         reply_markup= await kb.start())






