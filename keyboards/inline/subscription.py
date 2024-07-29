from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def check(deep):
    check_button = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="Obunani tekshirish", callback_data=f"check_subs_{deep}")
        ]]
    )
    return check_button