import asyncio

from postgresql import Database


async def test():
    db = Database()
    await db.create()

    print("Users jadvalini yaratamiz...")
    # await db.drop_users()
    await db.create_table_users()
    print("Yaratildi")

    print("Foydalanuvchilarni qo'shamiz")

    await db.add_user("anvar", "+998900200171", "sariqdev", 12345678, 234123232)
    await db.add_user("olim", "+998900200171", "olim223", 12341123, 23413253)
    await db.add_user("1", "+998900200171", "1", 131231, 43241534)
    await db.add_user("1", "+998900200171", "1", 23324234, 23412312)
    await db.add_user("John", "+998900200171", "JohnDoe", 4388229)
    print("Qo'shildi")

    users = await db.select_all_users()
    print(f"Barcha foydalanuvchilar: {users}")

    user = await db.select_user(id=5)
    print(f"Foydalanuvchi: {user}")


asyncio.run(test())
