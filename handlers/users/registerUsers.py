from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from keyboards.default.contactKeyboard import keyboard, keyboardLink
from aiogram.utils.deep_linking import get_start_link
from data.config import ADMINS

from loader import dp, db, bot
from states.startStates import PersonData

@dp.message_handler(state=PersonData.fullname)
async def enter_fullname(message: types.Message, state: FSMContext):
    fullname = message.text
    await state.update_data(
        {
            'name':fullname
        }
    )
    
    data = await state.get_data()
    name = data.get("name")

    await db.update_user_fullname(name, message.from_user.id)

    await state.finish()
    
    link = await get_start_link(message.from_user.id)
    await message.answer(f"Sizning <a href='{link}'>linkingiz</a>!", reply_markup=keyboardLink, disable_web_page_preview=True)
    
    count = await db.count_users()
    msg = f"{name} bazaga qo'shildi.\nBazada {count[0]} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)