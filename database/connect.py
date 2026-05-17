# Модуль подключения к SQL


# Импорты
import asyncpg
import os
import logging
from dotenv import load_dotenv



# Код

load_dotenv()




class DBConnect:
    """КЛАСС ПОДКЛЮЧЕНИЯ И ОТКЛЮЧЕНИЯ ОТ БД"""
    _db_pool = None

    @classmethod
    async def get_pool(cls):
        if cls._db_pool is None:
            logging.error("ПУЛ НЕ ИНИЦИАЛИЦИРОВАН")
            return None
        return cls._db_pool


    @classmethod
    async def conn_db_pool(cls):

        if cls._db_pool is not None:
            return cls._db_pool

        TOKEN_DB = os.getenv('DATABASE_URL')

        if not TOKEN_DB:
            logging.error('DATABASE_URL НЕТ В .env')
            return None
        try:
            cls._db_pool = await asyncpg.create_pool(
                TOKEN_DB,
                min_size=5,
                max_size=10
            )
            logging.info('ПУЛ УСПЕШНО СОЗДАН')
            return cls._db_pool

        except Exception:
            logging.error('КРИТИЧЕСКАЯ ОШИБКА ПРИ СОЗДАНИИ ПУЛА', exc_info=True)
            return None


    @classmethod
    async def exit_db_pool(cls):
        if cls._db_pool is not None:
            try:
                await cls._db_pool.close()
                cls._db_pool = None
                logging.info('ПУЛ УСПЕШНО ЗАКРЫТ')
            except Exception:
                logging.error('ОШИБКА ПРИ ЗАКРЫТИИ ПУЛА', exc_info=True)






