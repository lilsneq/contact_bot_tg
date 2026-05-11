# Модуль создания таблиц при запуске бота
import logging
from database import connect



class CreateTableSQL:
    @staticmethod
    async def create_table() -> None:
        try:
            async with connect.db_pool.acquire() as conn:
                query_users = """
                    CREATE TABLE IF NOT EXISTS users_tg_bot_contact (
                    username_id BIGINT PRIMARY KEY NOT NULL,
                    text VARCHAR(255) NULL,
                    is_active BOOLEAN NOT NULL DEFAULT FALSE,
                    is_block BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );
                """

                await conn.execute(query_users)
                logging.debug("ТАБЛИЦА СОЗДАНА УСПЕШНО")

        except Exception as e:
            logging.error(f"ОШИБКА: ТАБЛИЦА НЕ СОЗДАЛАСЬ {e}", exc_info=True)



class CreateRequests:

    @staticmethod
    async def set_user_in_bd(user_id: int) -> None:
        """ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ В БД ПРИ РЕГИСТРАЦИИ"""
        try:
            async with connect.db_pool.acquire() as conn:
                query_users = """
                    INSERT INTO users_tg_bot_contact(username_id)
                    VALUES ($1)
                    ON CONFLICT (username_id) DO NOTHING;
                """

                await conn.execute(query_users, user_id)
                logging.debug(f"ПОЛЬЗОВАТЕЛЬ {user_id} ДОБАВЛЕН В PostgreSQL")

        except Exception as e:
            logging.error(f'ОШИБКА: ЗАПРОСА НА ДОБАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯ {user_id} В БД', exc_info=True)



    @staticmethod
    async def user_in_bd(user_id: int) -> None:
        """ПРОВЕРКА ЕСТЬ ЛИ ПОЛЬЗОВАТЕЛЬ В БД"""
        try:
            async with connect.db_pool.acquire() as conn:
                query_users = """
                SELECT username_id 
                FROM users_tg_bot_contact
                WHERE username_id = $1;
                """

                logging.debug(f"ЗАПРОС НА ПРОВЕРКУ ПОЛЬЗОВАТЕЛЯ {user_id} ОТПРАВЛЕН")

                result = await conn.fetchval(query_users, user_id)

                if result:
                    logging.info(f"ПОЛЬЗОВАТЕЛЬ {user_id} ЕСТЬ В PostgreSQL")
                    return True

                logging.info(f'ПОЛЬЗОВАТЕЛЯ {user_id} НЕТ В PostgreSQL')
                return False


        except Exception as e:
            logging.error(f'ОШИБКА: ЗАПРОС НА ПРОВЕРКУ ПОЛЬЗОВАТЕЛЯ {user_id}', exc_info=True)
            return False














