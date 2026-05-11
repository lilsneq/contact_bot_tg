# Модуль подключения к SQL


# Импорты
import asyncpg
import os
from dotenv import load_dotenv


# Код

load_dotenv()


db_pool = None


class DBConnect:
    """КЛАСС ПОДКЛЮЧЕНИЯ И ОТКЛЮЧЕНИЯ ОТ БД"""
    @staticmethod
    async def conn_db_pool():
        global db_pool

        if db_pool is not None:
            return db_pool

        TOKEN_DB = os.getenv('DATABASE_URL')

        if not TOKEN_DB:
            print('DATABASE_URL НЕТ В .env')
            return

        db_pool = await asyncpg.create_pool(
            TOKEN_DB,
            min_size=5,
            max_size=10
        )
        print('db_pool УСПЕШНО СОЗДАН')
        return db_pool


    @staticmethod
    async def exit_db_pool():
        global db_pool
        if db_pool:
            await db_pool.close()
            db_pool = None
            print('db_pool УСПЕШНО ЗАКРЫТ')







