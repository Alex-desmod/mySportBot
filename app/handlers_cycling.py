from aiogram import F, Router
from aiogram.types import CallbackQuery
from datetime import datetime, timezone, timedelta

from app import keyboards as kb

router = Router()

@router.callback_query(F.data.startswith("CYCLING"))
async def cycling(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('В процессе разработки...')