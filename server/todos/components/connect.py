import mysql.connector


def connect_mysql(config: dict) -> tuple:
    conn = mysql.connector.connect(
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port'],
        database=config['database']
    )
    cursor = conn.cursor(prepared=True)
    return conn, cursor
