import sqlite3
from database import DB_PATH

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.execute("""
        SELECT id, title, date, collected_at
        FROM articles
        ORDER BY date DESC
    """)

    for row in cursor.fetchall():
        print(row)