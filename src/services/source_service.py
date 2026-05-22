from mysql.connector import Error

from db import db


def list_categories():
    query = "SELECT id, category_name FROM categories ORDER BY id"
    with db.cursor() as (_, cur):
        cur.execute(query)
        return cur.fetchall()


def category_exists(category_id: int) -> bool:
    query = "SELECT 1 FROM categories WHERE id = %s"
    with db.cursor() as (_, cur):
        cur.execute(query, (category_id,))
        return cur.fetchone() is not None


def list_sources():
    query = """
        SELECT s.id, s.source_name, s.url, s.parser_type, s.is_active,
               c.category_name, s.created_at
        FROM sources s
        JOIN categories c ON s.category_id = c.id
        ORDER BY s.id
    """
    with db.cursor() as (_, cur):
        cur.execute(query)
        return cur.fetchall()


def add_source(source_name: str, url: str, category_id: int, parser_type: str):
    if not category_exists(category_id):
        raise ValueError("Ma chuyen muc khong hop le.")

    query = """
        INSERT INTO sources (source_name, url, category_id, parser_type, is_active)
        VALUES (%s, %s, %s, %s, 1)
    """
    with db.cursor() as (_, cur):
        cur.execute(query, (source_name, url, category_id, parser_type))


def update_source(source_id: int, source_name: str, url: str, category_id: int, parser_type: str, is_active: int):
    if not category_exists(category_id):
        raise ValueError("Ma chuyen muc khong hop le.")

    query = """
        UPDATE sources
        SET source_name = %s,
            url = %s,
            category_id = %s,
            parser_type = %s,
            is_active = %s
        WHERE id = %s
    """
    with db.cursor() as (_, cur):
        cur.execute(query, (source_name, url, category_id, parser_type, is_active, source_id))
        if cur.rowcount == 0:
            raise ValueError("Khong tim thay nguon tin can cap nhat.")


def delete_source(source_id: int):
    query = "DELETE FROM sources WHERE id = %s"
    with db.cursor() as (_, cur):
        cur.execute(query, (source_id,))
        if cur.rowcount == 0:
            raise ValueError("Khong tim thay nguon tin can xoa.")


def get_active_sources():
    query = """
        SELECT id, source_name, url, category_id, parser_type
        FROM sources
        WHERE is_active = 1
        ORDER BY id
    """
    with db.cursor() as (_, cur):
        cur.execute(query)
        return cur.fetchall()


def source_exists(source_id: int) -> bool:
    query = "SELECT 1 FROM sources WHERE id = %s"
    with db.cursor() as (_, cur):
        cur.execute(query, (source_id,))
        return cur.fetchone() is not None
