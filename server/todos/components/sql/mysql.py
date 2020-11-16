import mysql.connector
import os


mysql_data = {
    "MYSQL_USER": os.getenv("MYSQL_USER"),
    "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD"),
    "MYSQL_HOST": os.getenv("MYSQL_HOST"),
    "MYSQL_PORT": os.getenv("MYSQL_PORT"),
    "MYSQL_DB": os.getenv("MYSQL_DB")
}

for key in mysql_data:
    if mysql_data[key] is None:
        print(f"ENVIRONMENT '{key}' EMPTY")
        exit()


def connect_mysql():
    conn = mysql.connector.connect(
        user=mysql_data['MYSQL_USER'],
        password=mysql_data['MYSQL_PASSWORD'],
        host=mysql_data['MYSQL_HOST'],
        port=mysql_data['MYSQL_PORT'],
        database=mysql_data['MYSQL_DB']
    )
    cursor = conn.cursor(prepared=True)
    return conn, cursor
