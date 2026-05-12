# Модуль создания таблиц при запуске бота
import logging
from database import connect
from database.connect import db_pool, DBConnect


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

                query_questionnaire = """
                    CREATE TABLE IF NOT EXISTS questions_tg_bot_contact (
                    username_id BIGINT PRIMARY KEY NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    age INT NOT NULL,
                    text VARCHAR(255) NOT NULL,
                    image_url VARCHAR(255) NOT NULL,
                    
                    FOREIGN KEY (username_id) REFERENCES users_tg_bot_contact(username_id) ON DELETE CASCADE
                    
                    );
                """

                await conn.execute(query_users)
                await conn.execute(query_questionnaire)

                logging.debug("ТАБЛИЦЫ СОЗДАНЫ УСПЕШНО")

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


    @staticmethod
    async def set_question(user_id: int, name: str, age: int, about: str, image) -> None:
        """Добавление данных пользователя в Базуданных"""
        try:
            pool = await DBConnect.conn_db_pool()
            async with pool.acquire() as conn:
                query = """
                    INSERT INTO questions_tg_bot_contact (username_id, name, age, text, image_url)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (username_id) 
                    DO UPDATE SET 
                        name = EXCLUDED.name,
                        age = EXCLUDED.age,
                        text = EXCLUDED.text,
                        image_url = EXCLUDED.image_url;
                """
                await conn.execute(query, user_id, name, age, about, image)
                logging.debug(f"ЗАПРОС ДОБАВЛЕНИЯ ДАННЫХ {user_id} ОТПРАВЛЕН В PostgreSQL")

        except Exception as e:
            logging.error(f'ОШИБКА ЗАПРОСА НА ДОБАВЛЕНИЕ ДАННЫХ ПОЛЬЗОВАТЕЛЯ {e}', exc_info=True)


    @staticmethod
    async def get_question(user_id: int):
        """ЗАПРОС НА ПОЛУЧЕНИЕ ДАННЫХ ДАННЫХ ИЗ БД"""
        try:
            async with connect.db_pool.acquire() as conn:
                query = """
                    SELECT name, age, text, image_url 
                    FROM questions_tg_bot_contact
                    WHERE username_id = $1;
                """

                logging.debug("ЗАПРОС НА ПОЛУЧЕНИЕ ДАННЫХ ПРОФИЛЯ ИЗ PostgreSQL")
                return await conn.fetchrow(query, user_id)


        except Exception as e:
            logging.error(f"ОШИБКА ЗАПРОСА НА ПОЛУЧЕНИЕ ДАННЫХ ПРОФИЛЯ {e}", exc_info=True)


    @staticmethod
    async def change_question(user_id: int, name: str, age: int, about: str, image) -> None:
        """ЗАПРОС НА ИЗМЕНЕНИЕ ДАННЫХ ПРОФИЛЯ"""
        try:
            async with connect.db_pool.acquire() as conn:
                query = """
                    INSERT INTO questions_tg_bot_contact (username_id, name, age, text, image_url)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (username_id) 
                    DO UPDATE SET 
                        name = EXCLUDED.name,
                        age = EXCLUDED.age,
                        text = EXCLUDED.text,
                        image_url = EXCLUDED.image_url;
                """
                await conn.execute(query, user_id, name, age, about, image)
                logging.debug("ЗАПРОС НА ИЗМЕНЕНИЕ ОТПРАВЛЕН")

        except Exception as e:
            logging.error(f"ОШИБКА ЗАПРОСА ИЗМЕНЕНИЯ ДАННЫХ ПРОФИЛЯ {e}", exc_info=True)

















