from aiogram import types
from aiogram.types import InputFile

from data.config import ADMINS
from loader import dp, db, bot
from states.startStates import UserSelect
from aiogram.dispatcher import FSMContext
import xlsxwriter

@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = await db.select_all_users()
    for user in users:
        # print(user[3])
        user_id = user[3]
        await bot.send_message(chat_id=user_id, text="@SariqDev kanaliga obuna bo'ling!")
        await asyncio.sleep(0.05)
    

@dp.message_handler(text="/all", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    all_users = await db.select_all_users()
    workbook = xlsxwriter.Workbook('documents/users.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'id')
    worksheet.write(0, 1, 'full name')
    worksheet.write(0, 2, 'username')
    worksheet.write(0, 3, 'telegram_id')
    worksheet.write(0, 4, 'deep link')
    worksheet.write(0, 5, 'count')

    for index, data in enumerate(all_users):
        worksheet.write(index+1, 0, str(index))
        worksheet.write(index+1, 1, data[1])
        worksheet.write(index+1, 2, data[2])
        worksheet.write(index+1, 3, data[3])
        worksheet.write(index+1, 4, data[4])
        worksheet.write(index+1, 5, data[5])

    workbook.close()

    user_file = InputFile(path_or_bytesio="documents/users.xlsx")

    await message.answer_document(
        user_file, caption="Barcha foydalanuvchilar haqida ma'lumot"
    )


@dp.message_handler(text="/allgt", user_id=ADMINS)
async def send_gt_user(message: types.Message):
    await message.answer("Nechtadan ko'p odam qo'shgan foydalanuvchilarni chiqaray?")
    await UserSelect.count.set()

@dp.message_handler(state=UserSelect.count, user_id=ADMINS)
async def send_ad_to_all(message: types.Message, state: FSMContext):
    count = message.text

    await state.update_data(
        {
            'count':count
        }
    )
    
    data = await state.get_data()
    count = data.get("count")

    all_users = await db.get_gt_count(int(count))

    await state.finish()

    workbook = xlsxwriter.Workbook('documents/users.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'id')
    worksheet.write(0, 1, 'full name')
    worksheet.write(0, 2, 'username')
    worksheet.write(0, 3, 'telegram_id')
    worksheet.write(0, 4, 'deep link')
    worksheet.write(0, 5, 'count')

    for index, data in enumerate(all_users):
        worksheet.write(index+1, 0, str(index))
        worksheet.write(index+1, 1, data[1])
        worksheet.write(index+1, 2, data[2])
        worksheet.write(index+1, 3, data[3])
        worksheet.write(index+1, 4, data[4])
        worksheet.write(index+1, 5, data[5])

    workbook.close()

    user_file = InputFile(path_or_bytesio="documents/users.xlsx")

    await message.answer_document(
        user_file, caption=f"{count} tadan ko'p odam qo'shgan foydalanuvchilar haqida ma'lumot"
    )

    