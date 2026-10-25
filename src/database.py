import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "articles.db"


def init_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT,
                url TEXT NOT NULL UNIQUE,
                summary TEXT,
                collected_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

def insert_articles(articles):

    with sqlite3.connect(DB_PATH) as conn:

        for article in articles:
            conn.execute("""
                INSERT OR IGNORE INTO articles
                    (title, date, url, summary)
                VALUES (?, ?, ?, ?)
            """, (
                article["title"],
                article["date"],
                article["url"],
                article["summary"]
            ))

def get_articles():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT title, date, url, summary
            FROM articles
            ORDER BY date DESC
        """).fetchall()

    return [dict(row) for row in rows]