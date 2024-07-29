from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.default.contactKeyboard import keyboardLink
from data.config import CHANNELS
from keyboards.inline.subscription import check
from aiogram.utils.deep_linking import get_start_link

from utils.misc import subscription

from loader import dp, db, bot
from states.startStates import PersonData


@dp.message_handler(CommandStart())
async def get_fullname(message: types.Message):
    deep = message.get_args()
    channels_format = str()
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        channels_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"

    await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n"
                         f"{channels_format}",
                         reply_markup=check(deep),
                         disable_web_page_preview=True)
    

@dp.callback_query_handler(text_contains="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    is_all_channels_subscription = True
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f"<b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"
        else:
            is_all_channels_subscription = False
            invite_link = await channel.export_invite_link()
            result += (f"<b>{channel.title}</b> kanaliga obuna bo'lmagansiz. "
                       f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n")

    await call.message.answer(result, disable_web_page_preview=True)
    if is_all_channels_subscription:
        if not await db.check_fullname(call.from_user.id):
            deep = call.data.split('_')[2]
            if deep != "" and await db.check_user(deep):
                await db.update_count(deep)
            await db.add_user(username = call.from_user.username, telegram_id = call.from_user.id, deep_link = deep)

            await call.message.answer("To'liq ism-familiyangizni kiriting")
            await PersonData.fullname.set()
        else:
            link = await get_start_link(call.from_user.id)
            await call.message.answer(text=f"Sizning <a href='{link}'>linkingiz</a>!", reply_markup=keyboardLink, disable_web_page_preview=True)
        

@dp.message_handler(text="Link olish")
async def get_link(message: types.Message):
    link = await get_start_link(message.from_user.id)
    await message.answer(text=f"Sizning <a href='{link}'>linkingiz</a>!", reply_markup=keyboardLink, disable_web_page_preview=True)

@dp.message_handler(text="Nechta odam qo'shganingizni ko'rish")
async def get_count(message: types.Message):
    count = await db.select_user(message.from_user.id)
    await message.answer(f"Sizning havolangiz orqali {count[5]} ta odam ro'yxatdan o'tgan")
