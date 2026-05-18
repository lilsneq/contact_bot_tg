# Модуль создания таблиц при запуске бота
import asyncio

import logging

from database.connect import DBConnect


class CreateTableSQL:

    @staticmethod
    async def create_table() -> None:
        """СОЗДАНИЕ ТАБЛИЦ ДЛЯ БД"""
        pool = await DBConnect.get_pool()
        if pool is None:
            return
        try:
            async with pool.acquire() as conn:

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
                    age INT CHECK (age >= 1 AND age <= 999) NOT NULL,
                    text VARCHAR(255) NOT NULL,
                    image_url TEXT NOT NULL,
                    city VARCHAR(255) NOT NULL,
                    gender VARCHAR(7) NOT NULL,
                    
                    FOREIGN KEY (username_id) REFERENCES users_tg_bot_contact(username_id) ON DELETE CASCADE
                    
                    );
                """
                query_interactions = """
                    CREATE TABLE IF NOT EXISTS interactions_tg_bot_contact (
                    username_id BIGINT NOT NULL,
                    viewed_id BIGINT NOT NULL,
                    is_like BOOLEAN NOT NULL DEFAULT FALSE,
                    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    PRIMARY KEY (username_id, viewed_id),
                    
                    FOREIGN KEY (username_id) REFERENCES users_tg_bot_contact(username_id) ON DELETE CASCADE,
                    FOREIGN KEY (viewed_id) REFERENCES users_tg_bot_contact(username_id) ON DELETE CASCADE
                    );

                """

                await conn.execute(query_users)
                await conn.execute(query_questionnaire)
                await conn.execute(query_interactions)

                logging.debug("ТАБЛИЦЫ СОЗДАНЫ УСПЕШНО")

        except Exception:
            logging.error("ОШИБКА: ТАБЛИЦА НЕ СОЗДАЛАСЬ", exc_info=True)



class CreateRequests:

    @staticmethod
    async def set_user_in_bd(user_id: int) -> None:
        """ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ В БД ПРИ РЕГИСТРАЦИИ"""

        pool = await DBConnect.get_pool()
        if pool is None:
            return

        try:
            async with pool.acquire() as conn:

                query_users = """
                    INSERT INTO users_tg_bot_contact(username_id)
                    VALUES ($1)
                    ON CONFLICT (username_id) DO NOTHING;
                """

                await conn.execute(query_users, user_id)
                logging.debug(f"ПОЛЬЗОВАТЕЛЬ {user_id} ДОБАВЛЕН В БД")

        except Exception:
            logging.error(f'ОШИБКА: ЗАПРОСА НА ДОБАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯ {user_id} В БД', exc_info=True)


    @staticmethod
    async def user_in_bd(user_id: int) -> bool:
        """ПРОВЕРКА ЕСТЬ ЛИ ПОЛЬЗОВАТЕЛЬ В БД"""

        pool = await DBConnect.get_pool()
        if pool is None:
            return

        try:
            async with pool.acquire() as conn:

                query_users = """
                SELECT username_id 
                FROM users_tg_bot_contact
                WHERE username_id = $1;
                """

                logging.debug(f"ЗАПРОС НА ПРОВЕРКУ ПОЛЬЗОВАТЕЛЯ {user_id} ОТПРАВЛЕН")

                result = await conn.fetchval(query_users, user_id)

                if result:
                    logging.info(f"ПОЛЬЗОВАТЕЛЬ {user_id} ЕСТЬ В БД")
                    return True

                logging.info(f'ПОЛЬЗОВАТЕЛЯ {user_id} НЕТ В БД')
                return False


        except Exception:
            logging.error(f'ОШИБКА: ЗАПРОСА НА ПРОВЕРКУ ПОЛЬЗОВАТЕЛЯ {user_id}', exc_info=True)
            return False


    @staticmethod
    async def set_question(user_id: int, name: str, age: int, about: str, image: str, city, gender: str) -> None:
        """Добавление данных пользователя в Базуданных или изменения их"""

        pool = await DBConnect.get_pool()
        if pool is None:
            return
        try:
            async with pool.acquire() as conn:

                query = """
                    INSERT INTO questions_tg_bot_contact (username_id, name, age, text, image_url, city, gender)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    ON CONFLICT (username_id) 
                    DO UPDATE SET 
                        name = EXCLUDED.name,
                        age = EXCLUDED.age,
                        text = EXCLUDED.text,
                        image_url = EXCLUDED.image_url,
                        city = EXCLUDED.city,
                        gender = EXCLUDED.gender;
                """
                await conn.execute(query, user_id, name, age, about, image, city, gender)
                logging.debug(f"ЗАПРОС ДОБАВЛЕНИЯ ДАННЫХ {user_id} ОТПРАВЛЕН В БД")

        except Exception:
            logging.error(f'ОШИБКА ЗАПРОСА НА ДОБАВЛЕНИЕ ДАННЫХ ПОЛЬЗОВАТЕЛЯ {user_id}', exc_info=True)


    @staticmethod
    async def get_question(user_id: int) -> None:
        """ЗАПРОС НА ПОЛУЧЕНИЕ ДАННЫХ ДАННЫХ ИЗ БД"""

        pool = await DBConnect.get_pool()
        if pool is None:
            return

        try:
            async with pool.acquire() as conn:

                query = """
                    SELECT name, age, text, image_url, city
                    FROM questions_tg_bot_contact
                    WHERE username_id = $1;
                """

                logging.debug(f"ЗАПРОС НА ПОЛУЧЕНИЕ ДАННЫХ ПРОФИЛЯ {user_id} ИЗ БД")
                return await conn.fetchrow(query, user_id)


        except Exception:
            logging.error(f"ОШИБКА ЗАПРОСА НА ПОЛУЧЕНИЕ ДАННЫХ ПРОФИЛЯ {user_id}", exc_info=True)


    @staticmethod
    async def get_boolean_active_user(user_id: int) -> None:
        """Получить будевое значение активная ли анкета или нет"""

        pool = await DBConnect.get_pool()
        if pool is None:
            return

        try:
            async with pool.acquire() as conn:

                query = """
                    SELECT is_active
                    FROM users_tg_bot_contact
                    WHERE username_id = $1;
                """

                logging.debug(f"ЗАПРОС НА ПРОВЕРКУ АКТИВНОСТИ ПРОФИЛЯ {user_id} ОТПРАВЛЕН БД")
                return await conn.fetchval(query, user_id)

        except Exception:
            logging.error(f"ОШИБКА ЗАПРОСА НА ПРОВЕРКУ АКТИВНОСТИ АНКЕТЫ {user_id}", exc_info=True)


    @staticmethod
    async def set_boolean_active_user(user_id: int, is_active: bool) -> None:
        """Изменение активности анкеты"""

        pool = await DBConnect.get_pool()
        if pool is None:
            return

        try:
            query = """
                UPDATE users_tg_bot_contact
                SET is_active = $2
                WHERE username_id = $1;
            """

            async with pool.acquire() as conn:
                await conn.execute(query, user_id, is_active)
                logging.debug(f"ЗАПРОС НА ИЗМЕНЕНИЕ АКТИВНОСТИ АНКЕТЫ ОТПРАВЛЕН {user_id} БД")

        except Exception:
            logging.error(f'ОШИБКА ИЗМЕНЕНИЯ АКТИВНОСТИ АНКЕТЫ ПОЛЬЗОВАТЕЛЯ {user_id}', exc_info=True)





class FindRequest:

    @staticmethod
    async def get_is_active_quest(user_id: int, city: str) -> None:
        """Получение все активных анкет, у которых совпали username_id, которые должны иметься в двух таблицах"""
        pool = await DBConnect.get_pool()
        if pool is None:
            return

        try:
            query = """
                SELECT u.*, q.* 
                FROM users_tg_bot_contact AS u 
                INNER JOIN questions_tg_bot_contact AS q 
                    ON u.username_id = q.username_id 
                
                LEFT JOIN interactions_tg_bot_contact AS i 
                    ON u.username_id = i.viewed_id 
                    AND i.username_id = $1
                    AND (i.is_like = TRUE OR i.viewed_at > NOW() - INTERVAL '1 DAY')
                
                WHERE u.username_id != $1 
                  AND u.is_active = TRUE 
                  AND LOWER(TRIM(q.city)) = LOWER(TRIM($2))
                  AND i.viewed_id IS NULL 
                  AND u.is_block = FALSE
                ORDER BY RANDOM() 
                LIMIT 1;
            """

            async with pool.acquire() as conn:
                res = await conn.fetchrow(query, user_id, city)
                logging.debug('ЗАПРОС НА ПОЛУЧЕНИЕ ДАННЫХ ПРОФИЛЯ И АКТИВНОСТИ ДЛЯ ПОИСКА')
                return dict(res) if res else None

        except Exception:
            logging.error('ОШИБКА ЗАПРОСА ПОИСКА АНКЕТЫ ПО is_active и городу', exc_info=True)
            return None


    @staticmethod
    async def add_interaction(user_id: int, viewed_id: str, is_like: bool) -> bool:
        """Записывает лайк или дизлайк пользователя в таблицу взаимодействий"""
        pool = await DBConnect.get_pool()
        if pool is None:
            return

        try:
            query = """
                INSERT INTO interactions_tg_bot_contact (username_id, viewed_id, is_like)
                VALUES ($1, $2, $3)
                ON CONFLICT (username_id, viewed_id)
                DO UPDATE SET is_like = EXCLUDED.is_like;
            """
            async with pool.acquire() as conn:
                await conn.execute(query, user_id, viewed_id, is_like)
                logging.debug('ЗАПРОС НА ДОБАВЛЕНИЕ В ТАБЛИЦУ ПОЛЬЗОВАТЕЛЯ')
                return True

        except Exception:
            logging.error('ОШИБКА ЗАПИСИ ВЗАИМОДЕЙСТВИЯ (лайк/дизлайк)', exc_info=True)
            return False


    @staticmethod
    async def get_city(username_id: int) -> None:
        pool = await DBConnect.get_pool()
        if pool is None:
            return

        try:

            query = """
                SELECT city
                FROM questions_tg_bot_contact AS q
                WHERE username_id = $1
            """

            async with pool.acquire() as conn:
                res = await conn.fetchrow(query, username_id)
                logging.debug('ЗАПРОС НА ПОЛУЧЕНИЕ ГОРОДА')
                return res['city'] if res else None

        except Exception:
            logging.error('ОШИБКА ПОЛУЧЕНИЯ ГОРОДА', exc_info=True)




#
# if __name__ == '__main__':
#     async def start():
#         await DBConnect.conn_db_pool()
#         res = await FindRequest.get_city(1000000000)
#         print(res)
#
#     asyncio.run(start())
