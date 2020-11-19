import hashlib
from ..fixes import fix_data
import uuid


class User:
    def __init__(self, connection, user) -> None:
        self.connection = connection
        self.user = user
        return

    @staticmethod
    def is_none(data) -> bool:
        if data is None:
            return True
        return False

    async def user_exists(self) -> bool:
        conn, cursor = self.connection.connect_mysql()
        sql = "SELECT COUNT(*) FROM users WHERE username=?;"
        cursor.execute(sql, (self.user.username,))
        result = cursor.fetchall()
        conn.close()
        if fix_data(result[0][0]) > 0:
            return True
        return False

    async def is_valid_password(self) -> bool:
        conn, cursor = self.connection.connect_mysql()
        sql = "SELECT password FROM users WHERE username=?;"
        cursor.execute(sql, (self.user.username,))
        result = cursor.fetchall()
        conn.close()
        if fix_data(result[0][0]) == hashlib.sha256(self.user.password.encode()).hexdigest():
            return True
        return False

    async def is_valid_token(self) -> bool:
        conn, cursor = self.connection.connect_mysql()
        sql = "SELECT token FROM users WHERE username=?;"
        cursor.execute(sql, (self.user.username,))
        result = cursor.fetchall()
        conn.close()
        if fix_data(result[0][0]) == self.user.token:
            return True
        return False

    async def signin(self) -> dict:
        if self.is_none(self.user.username) or self.is_none(self.user.password):
            return {"status": False, "reason": "Одно из параметров имеет <null> тип"}
        if not await self.user_exists():
            return {"status": False, "reason": "Данного имени пользователя не существует"}
        if not await self.is_valid_password():
            return {"status": False, "reason": "Пароль не верный"}

        conn, cursor = self.connection.connect_mysql()
        sql = "UPDATE users SET token=? WHERE username=?;"
        token = hashlib.sha256(uuid.uuid4().hex.encode()).hexdigest()
        cursor.execute(sql, (token, self.user.username))
        conn.commit()
        conn.close()
        return {"status": True, "token": token}

    async def signup(self) -> dict:
        if self.is_none(self.user.username) or self.is_none(self.user.password):
            return {"status": False, "reason": "Одно из параметров имеет <null> тип"}
        if await self.user_exists():
            return {"status": False, "reason": "Имя пользователя занято"}

        conn, cursor = self.connection.connect_mysql()
        sql = "INSERT INTO users (username, password, token) VALUES (?, ?, ?);"
        token = hashlib.sha256(uuid.uuid4().hex.encode()).hexdigest()
        cursor.execute(sql, (
            self.user.username,
            hashlib.sha256(self.user.password.encode()).hexdigest(),
            token
        ))
        conn.commit()
        conn.close()
        return {"status": True}
