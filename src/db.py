from contextlib import contextmanager

import mysql.connector
from mysql.connector import Error

from config import settings


class Database:
    def __init__(self):
        self.config = {
            "host": settings.db_host,
            "port": settings.db_port,
            "user": settings.db_user,
            "password": settings.db_password,
            "database": settings.db_name,
            "autocommit": False,
        }

    def get_connection(self):
        return mysql.connector.connect(**self.config)

    @contextmanager
    def cursor(self, dictionary=True):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=dictionary)
            yield conn, cursor
            conn.commit()
        except Error:
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()


db = Database()
