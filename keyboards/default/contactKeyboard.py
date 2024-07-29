from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                               keyboard=[
                                [
                                    KeyboardButton(text="Kontakni ulashish",
                                    request_contact=True)
                                ],
                               ],)

keyboardLink = ReplyKeyboardMarkup(resize_keyboard=True,
                               keyboard=[
                                    [
                                        KeyboardButton(text="Link olish"),
                                        KeyboardButton(text="Nechta odam qo'shganingizni ko'rish")                       
                                    ],
                                ],
)