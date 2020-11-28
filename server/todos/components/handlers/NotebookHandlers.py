import hashlib
from ..fixes import fix_data


class Notebook:
    def __init__(self, **kwargs) -> None:
        self.connection = kwargs.pop("connection")
        self.user = kwargs.pop("user")

        try:
            self.data = kwargs.pop("data")
        except KeyError:
            pass
        return

    async def delete(self) -> dict:
        conn, cursor = self.connection.connect_mysql()
        sql = "SELECT COUNT(*) FROM notes WHERE id=? AND owner=?;"
        cursor.execute(sql, (self.data.id, self.user.username))
        result = cursor.fetchone()
        if fix_data(result[0]):
            sql = "DELETE FROM notes WHERE id=? AND owner=?;"
            cursor.execute(sql, (self.data.id, self.user.username))
            conn.commit()
            conn.close()
            return {"status": True}
        return {"status": False, "reason": "Заметка не существует"}

    async def get(self) -> dict:
        conn, cursor = self.connection.connect_mysql()
        sql = "SELECT * FROM notes WHERE owner=?;"
        cursor.execute(sql, (self.user.username,))
        result = cursor.fetchall()
        conn.close()
        notes = {}
        for note in result:
            notes[note[0]] = {
                "title": fix_data(note[3]),
                "text": fix_data(note[4]),
                "checked": bool(fix_data(note[5]))
            }
        return {"status": True, "notes": notes}

    async def update(self) -> dict:
        conn, cursor = self.connection.connect_mysql()
        sql = "UPDATE notes SET hash=?,title=?,text=?,checked=? WHERE owner=? AND id=?;"
        cursor.execute(sql, (
            hashlib.sha256(str(self.data).encode()).hexdigest(),
            self.data.title,
            self.data.text,
            self.data.checked,
            self.user.username,
            self.data.id,
        ))
        conn.commit()
        conn.close()
        return {"status": True}

    async def add(self) -> dict:
        conn, cursor = self.connection.connect_mysql()
        sql = "INSERT INTO notes (owner, parent) VALUES (?, ?);"
        cursor.execute(sql, (self.user.username, 0))
        sql = "SELECT MAX(id) FROM notes WHERE owner=?;"
        cursor.execute(sql, (self.user.username,))
        result = cursor.fetchone()
        conn.commit()
        conn.close()
        return {"status": True, "id": fix_data(result[0])}
