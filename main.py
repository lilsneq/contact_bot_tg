# МОДУЛЬ ЗАПУСКА БОТА
import logging
# ИМПОРТЫ
import os
import sys
import asyncio


from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from database.connect import DBConnect
from database.requests import CreateTableSQL


from handlers.registration import router as registration_router



load_dotenv()



async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )


    TOKEN_TG_BOT = os.getenv("TOKEN_TG")
    if not TOKEN_TG_BOT:
        sys.exit("TOKEN_TG НЕ БЫЛ НАЙДЕН В .env")

    dp = Dispatcher()

    if await DBConnect.conn_db_pool() is None:
        sys.exit("ОШИБКА: ПОДКЛЮЧЕНИЯ К PostrgreSQL")

    logging.info('ПУЛ ПОДКЛЮЧЕНИЙ ИНИЦИАЛИЗИРОВАН')
    await CreateTableSQL().create_table()


    dp.include_router(registration_router)

    bot = Bot(token=TOKEN_TG_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        logging.info('БОТ УСПЕШНО ЗАПУЩЕН')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await DBConnect.exit_db_pool()
        logging.info('БОТ УСПЕШНО ОТКЛЮЧËН')







if __name__ == '__main__':
    asyncio.run(main())

