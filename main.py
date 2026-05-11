# МОДУЛЬ ЗАПУСКА БОТА


# ИМПОРТЫ
import os
import sys
import asyncio

from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.db_connect import DBConnect



load_dotenv()



async def main() -> None:
    TOKEN_TG_BOT = os.getenv("TOKEN_TG")
    if not TOKEN_TG_BOT:
        sys.exit("TOKEN_TG НЕ БЫЛ НАЙДЕН В .env")

    dp = Dispatcher()

    if await DBConnect.conn_db_pool() is None:
        sys.exit("ОШИБКА: ПОДКЛЮЧЕНИЯ К PostrgreSQL")

    print('ПУЛ ПОДКЛЮЧЕНИЙ СОЗДАН')

    dp.include_router()

    bot = Bot(token=TOKEN_TG_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        print("БОТ УСПЕШНО ЗАПУЩЕН")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        print("БОТ ЗАВЕРШИЛ")
        await DBConnect.exit_db_pool()
        print("ПУЛ ЗАКРЫТ")









if __name__ == '__main__':
    asyncio.run(main())

