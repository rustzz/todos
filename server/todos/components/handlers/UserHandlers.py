import hashlib
from ..fixes import fix_data
import uuid


class User:
    def __init__(self, **kwargs) -> None:
        self.connection = kwargs.pop("connection")
        self.user = kwargs.pop("user")

        try:
            self.password_hash = hashlib.sha256(self.user.password.encode()).hexdigest()
        except AttributeError:
            pass
        return

    async def user_exists(self) -> bool:
        conn, cursor = self.connection.connect_mysql()
        sql = "SELECT COUNT(*) FROM users WHERE username=?;"
        cursor.execute(sql, (self.user.username,))
        result = cursor.fetchone()
        conn.close()
        return bool(fix_data(result[0]))

    async def is_valid_password(self) -> bool:
        conn, cursor = self.connection.connect_mysql()
        sql = "SELECT password FROM users WHERE username=?;"
        cursor.execute(sql, (self.user.username,))
        result = cursor.fetchone()
        conn.close()
        return fix_data(result[0]) == self.password_hash

    async def is_valid_token(self) -> bool:
        conn, cursor = self.connection.connect_mysql()
        sql = "SELECT token FROM users WHERE username=?;"
        cursor.execute(sql, (self.user.username,))
        result = cursor.fetchone()
        conn.close()
        return fix_data(result[0]) == self.user.token

    async def signin(self) -> dict:
        if not bool(self.user.username) or not bool(self.user.password):
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
        if not bool(self.user.username) or not bool(self.user.password):
            return {"status": False, "reason": "Одно из параметров имеет <null> тип"}
        if await self.user_exists():
            return {"status": False, "reason": "Имя пользователя занято"}

        conn, cursor = self.connection.connect_mysql()
        sql = "INSERT INTO users (username, password, token) VALUES (?, ?, ?);"
        token = hashlib.sha256(uuid.uuid4().hex.encode()).hexdigest()
        cursor.execute(sql, (
            self.user.username,
            self.password_hash,
            token
        ))
        conn.commit()
        conn.close()
        return {"status": True}
