import mysql.connector
import os, sys


mysql_data = {
    "MYSQL_USER": os.getenv("MYSQL_USER"),
    "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD"),
    "MYSQL_HOST": os.getenv("MYSQL_HOST"),
    "MYSQL_PORT": os.getenv("MYSQL_PORT"),
    "MYSQL_DB": os.getenv("MYSQL_DB")
}

for key, value in mysql_data.items():
    if value is None:
        print(f"ENVIRONMENT '{key}' EMPTY")
        sys.exit()


def connect_mysql():
    conn = mysql.connector.connect(
        user=mysql_data["MYSQL_USER"],
        password=mysql_data["MYSQL_PASSWORD"],
        host=mysql_data["MYSQL_HOST"],
        port=mysql_data["MYSQL_PORT"],
        database=mysql_data["MYSQL_DB"]
    )
    cursor = conn.cursor(prepared=True)
    return conn, cursor
