import hashlib
from todos.components.fixes import fix_data


class Notes:
    data: dict = None

    def __init__(self, connection, user, data: dict = None) -> None:
        self.connection = connection
        self.user = user
        self.data = data
        return

    async def delete(self) -> dict:
        conn, cursor = self.connection[0].connect_mysql(self.connection[1].mysql_data)
        sql = 'DELETE FROM notes WHERE id=? AND owner=?;'
        cursor.execute(sql, (self.data["note_id"], self.user.username))
        conn.commit()
        conn.close()
        return {'status': True}

    async def get(self) -> dict:
        conn, cursor = self.connection[0].connect_mysql(self.connection[1].mysql_data)
        sql = 'SELECT * FROM notes WHERE owner=?;'
        cursor.execute(sql, (self.user.username,))
        result = cursor.fetchall()
        conn.close()
        notes = {}
        for note in result:
            notes[note[0]] = {'title': fix_data(note[3]), 'text': fix_data(note[4]), 'checked': bool(fix_data(note[5]))}
        return {'status': True, 'notes': notes}

    async def update(self) -> dict:
        conn, cursor = self.connection[0].connect_mysql(self.connection[1].mysql_data)
        sql = 'UPDATE notes SET hash=?,title=?,text=?,checked=? WHERE owner=? AND id=?;'
        cursor.execute(sql, (
            hashlib.sha256(str(self.data).encode()).hexdigest(),
            self.data["title"],
            self.data["text"],
            self.data["checked"],
            self.user.username,
            self.data["note_id"],
        ))
        conn.commit()
        conn.close()
        return {'status': True}

    async def add(self) -> dict:
        conn, cursor = self.connection[0].connect_mysql(self.connection[1].mysql_data)
        sql = 'INSERT INTO notes (owner, parent) VALUES (?, ?);'
        cursor.execute(sql, (self.user.username, 0))
        sql = 'SELECT MAX(id) FROM notes WHERE owner=?;'
        cursor.execute(sql, (self.user.username,))
        note_id = cursor.fetchall()
        conn.commit()
        conn.close()
        return {'status': True, 'note_id': fix_data(note_id[0][0])}
