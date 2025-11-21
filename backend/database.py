import sqlite3

def get_connection():
    return sqlite3.connect("database.db")

def create_tables():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id TEXT PRIMARY KEY,
            access_token TEXT,
            refresh_token TEXT,
            token_expiry TEXT,
            email TEXT
        )
    """)

    conn.commit()
    conn.close()

create_tables()
