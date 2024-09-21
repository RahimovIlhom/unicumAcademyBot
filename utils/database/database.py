import asyncio

import aiomysql

from environs import Env

env = Env()
env.read_env()


class Database:
    def __init__(self):
        self.host = env.str('DB_HOST')
        self.port = env.int('DB_PORT')
        self.user = env.str('DB_USER')
        self.password = env.str('DB_PASSWORD')
        self.db = env.str('DB_NAME')
        self.pool = None

    async def connect(self) -> None:
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db
        )

    async def execute(self, query: str, *args) -> None:
        """
        Execute: INSERT, UPDATE, DELETE
        :param query: sql query
        :param args: values
        :return: None
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)
                await conn.commit()

    async def fetchone(self, query: str, *args) -> dict | None:
        """
        Execute: SELECT one value
        :param query: sql query
        :param args: values
        :return: dict
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                result = await cur.fetchone()
                return result

    async def fetchall(self, query: str, *args) -> list[dict]:
        """
        Execute: SELECT many value
        :param query: sql query
        :param args: values
        :return: list[dict]
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                result = await cur.fetchall()
                return result

    async def close(self) -> None:
        """
        Close database connection
        :return: None
        """
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def add_user(self, telegramId, fullname: str, contact: str, phone: str, selectedLevel: str=None, *args, **kwargs):
        sql = """
            INSERT INTO bot_users 
                (telegramId,
                 fullname,
                 telegramContact,
                 phoneNumber,
                 language,
                 selectedLevel,
                 confirmedLevel,
                 recommendedLevel,
                 registeredAt,
                 updatedAt)
            VALUES
                (%s, %s, %s, %s, 'uz', %s, NULL, NULL, NOW(), NOW())
        """
        await self.execute(sql, telegramId, fullname, contact, phone, selectedLevel)

    async def get_user(self, telegramId) -> dict:
        sql = """
            SELECT 
                telegramId,
                fullname,
                telegramContact,
                phoneNumber,
                language,
                selectedLevel,
                confirmedLevel,
                recommendedLevel,
                registeredAt,
                updatedAt 
            FROM bot_users 
            WHERE telegramId = %s
        """
        return await self.fetchone(sql, telegramId)

    async def get_users(self):
        sql = """
            SELECT 
                telegramId,
                fullname,
                telegramContact,
                phoneNumber,
                language,
                selectedLevel,
                confirmedLevel,
                recommendedLevel,
                registeredAt,
                updatedAt 
            FROM bot_users 
        """
        return await self.fetchall(sql)
