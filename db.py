# db.py
import sqlite3

DB_PATH = "face.db"


def _ensure_schema(cur):
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name   TEXT,
        last_name    TEXT,
        email        TEXT UNIQUE,
        mobile       TEXT,
        voice_phrase TEXT
    )
    """
    )
    # you can also add any missing columns with ALTER TABLE if migrating old DBs


def get_users():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # <-- rows behave like dicts
    cur = conn.cursor()
    _ensure_schema(cur)

    cur.execute(
        """
        SELECT id, first_name, last_name, email, mobile, voice_phrase
        FROM users
        ORDER BY id DESC
    """
    )
    rows = cur.fetchall()
    conn.close()
    # Convert sqlite3.Row -> dict
    return [dict(r) for r in rows]
