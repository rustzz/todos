import hashlib
import random
from todos.components.fixes import fix_data


class User:
    username: str = None
    password: str = None
    token: str = None

    def __init__(self, connection, username: str, password: str = None, token: str = None) -> None:
        self.connection = connection
        self.username = username
        self.password = password
        self.token = token
        return
    
    async def user_exists(self) -> bool:
        conn, cursor = self.connection[0].connect_mysql(self.connection[1].mysql_data)
        sql = 'SELECT COUNT(*) FROM users WHERE username=?;'
        cursor.execute(sql, (self.username,))
        result = cursor.fetchall()
        conn.close()
        if fix_data(result[0][0]) > 0:
            return True
        return False

    async def is_valid_password(self) -> bool:
        conn, cursor = self.connection[0].connect_mysql(self.connection[1].mysql_data)
        sql = 'SELECT password FROM users WHERE username=?;'
        cursor.execute(sql, (self.username,))
        result = cursor.fetchall()
        conn.close()
        if fix_data(result[0][0]) == hashlib.sha256(self.password.encode()).hexdigest():
            return True
        return False

    async def is_valid_token(self) -> bool:
        conn, cursor = self.connection[0].connect_mysql(self.connection[1].mysql_data)
        sql = 'SELECT token FROM users WHERE username=?;'
        cursor.execute(sql, (self.username,))
        result = cursor.fetchall()
        conn.close()
        if fix_data(result[0][0]) == self.token:
            return True
        return False

    async def login(self) -> dict:
        if not await self.user_exists():
            return {'status': False, 'reason': 'Имя пользователя не существует'}
        if not await self.is_valid_password():
            return {'status': False, 'reason': 'Пароль не верный'}

        conn, cursor = self.connection[0].connect_mysql(self.connection[1].mysql_data)
        sql = 'UPDATE users SET token=? WHERE username=?;'
        token = hashlib.sha256(str(random.randint(100000, 999999)).encode()).hexdigest()
        cursor.execute(sql, (token, self.username))
        conn.commit()
        conn.close()
        return {'status': True, 'token': token}

    async def register(self) -> dict:
        if await self.user_exists():
            return {'status': False, 'reason': 'Имя пользователя занято'}

        conn, cursor = self.connection[0].connect_mysql(self.connection[1].mysql_data)
        sql = 'INSERT INTO users (username, password, token) VALUES (?, ?, ?);'
        token = hashlib.sha256(str(random.randint(100000, 999999)).encode()).hexdigest()
        cursor.execute(sql, (self.username, hashlib.sha256(self.password.encode()).hexdigest(), token))
        conn.commit()
        conn.close()
        return {'status': True}
