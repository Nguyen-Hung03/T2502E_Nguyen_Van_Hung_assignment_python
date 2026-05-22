from mysql.connector import Error

from db import db


def article_url_exists(url: str) -> bool:
    query = "SELECT 1 FROM articles WHERE url = %s"
    with db.cursor() as (_, cur):
        cur.execute(query, (url,))
        return cur.fetchone() is not None


def create_article(source_id: int, category_id: int, title: str, url: str) -> bool:
    if article_url_exists(url):
        return False

    query = """
        INSERT INTO articles (source_id, category_id, title, url, status)
        VALUES (%s, %s, %s, %s, 0)
    """
    try:
        with db.cursor() as (_, cur):
            cur.execute(query, (source_id, category_id, title[:500], url[:1000]))
        return True
    except Error as exc:
        if exc.errno == 1062:
            return False
        raise


def get_articles_by_status(status: int, limit: int = 100):
    query = """
        SELECT id, source_id, category_id, title, url
        FROM articles
        WHERE status = %s
        ORDER BY created_at ASC
        LIMIT %s
    """
    with db.cursor() as (_, cur):
        cur.execute(query, (status, limit))
        return cur.fetchall()


def update_article_detail(article_id: int, summary: str, content: str):
    query = """
        UPDATE articles
        SET summary = %s,
            content = %s,
            status = 1
        WHERE id = %s
    """
    with db.cursor() as (_, cur):
        cur.execute(query, (summary, content, article_id))


def get_articles_paginated(page: int, page_size: int = 10):
    offset = (page - 1) * page_size
    query = """
        SELECT a.id, a.title, a.url, a.status, a.created_at,
               s.source_name, c.category_name
        FROM articles a
        JOIN sources s ON a.source_id = s.id
        JOIN categories c ON a.category_id = c.id
        ORDER BY a.created_at DESC
        LIMIT %s OFFSET %s
    """
    with db.cursor() as (_, cur):
        cur.execute(query, (page_size, offset))
        return cur.fetchall()


def get_article_count() -> int:
    query = "SELECT COUNT(*) AS total FROM articles"
    with db.cursor() as (_, cur):
        cur.execute(query)
        row = cur.fetchone()
        return int(row["total"])
