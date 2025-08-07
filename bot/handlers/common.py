from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from bot.keyboards import main_markup
from db.models.user import User

router = Router(name="commonH")


@router.message(CommandStart())
async def start(ms: Message):
    user = await User.filter(id=ms.from_user.id).exists()
    if not user:
        await User.create(id=ms.from_user.id)

    await ms.answer("open", reply_markup=main_markup)
