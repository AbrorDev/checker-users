from aiogram.dispatcher.filters.state import StatesGroup, State

class PersonData(StatesGroup):
    fullname = State()
    phone = State()

class UserSelect(StatesGroup):
    count = State()