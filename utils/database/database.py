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
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await conn.ping(reconnect=True)  # Aloqani yangilash uchun
                await cur.execute(query, args)
                result = await cur.fetchone()
                return result

    async def fetchall(self, query: str, *args) -> list[dict]:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await conn.ping(reconnect=True)  # Aloqani yangilash uchun
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

    async def add_user(self, telegramId, fullname: str, contact: str, phone: str, preferred_time_slot: int,
                       selectedLevel: str=None, *args, **kwargs):
        sql = """
            INSERT INTO bot_users 
                (telegramId,
                 fullname,
                 telegramContact,
                 phoneNumber,
                 preferred_time_slot,
                 language,
                 selectedLevel,
                 confirmedLevel,
                 recommendedLevel,
                 registeredAt,
                 updatedAt)
            VALUES
                (%s, %s, %s, %s, %s, 'uz', %s, NULL, NULL, NOW(), NOW())
        """
        await self.execute(sql, telegramId, fullname, contact, phone, preferred_time_slot, selectedLevel)

    async def get_user(self, telegramId) -> dict:
        sql = """
            SELECT 
                telegramId,
                fullname,
                telegramContact,
                phoneNumber,
                preferred_time_slot,
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

    async def get_users(self) -> list[dict]:
        sql = """
            SELECT 
                telegramId,
                fullname,
                telegramContact,
                phoneNumber,
                preferred_time_slot,
                language,
                selectedLevel,
                confirmedLevel,
                recommendedLevel,
                registeredAt,
                updatedAt 
            FROM bot_users 
        """
        return await self.fetchall(sql)

    async def set_fullname(self, telegramId, fullname) -> None:
        sql = """
            UPDATE bot_users
            SET fullname = %s
            WHERE telegramId = %s
        """
        await self.execute(sql, fullname, telegramId)

    async def set_phone_number(self, telegramId, phone) -> None:
        sql = """
            UPDATE bot_users
            SET phoneNumber = %s
            WHERE telegramId = %s
        """
        await self.execute(sql, phone, telegramId)

    async def set_preferred_time_slot(self, telegramId, preferred_time) -> None:
        sql = """
            UPDATE bot_users
            SET preferred_time_slot = %s
            WHERE telegramId = %s
        """
        await self.execute(sql, preferred_time, telegramId)

    async def get_my_results(self, telegramId) -> list[dict]:
        sql = """
            SELECT
                id,
                user_id,
                level,
                totalQuestions,
                correctAnswers,
                completed,
                createdAt,
                completedAt
            FROM test_sessions
            WHERE user_id = %s AND completed = TRUE
            ORDER BY completedAt DESC;
        """
        return await self.fetchall(sql, telegramId)

    async def get_result_by_session_id(self, session_id: int) -> dict:
        sql = """
            SELECT
                id,
                user_id,
                level,
                totalQuestions,
                correctAnswers,
                completed,
                createdAt,
                completedAt
            FROM test_sessions
            WHERE id = %s;
        """
        return await self.fetchone(sql, session_id)
