import sqlite3

DB_NAME = "database.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        username TEXT,
        balance INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def add_user(user_id, first_name, username):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users
    (user_id, first_name, username)
    VALUES (?, ?, ?)
    """, (user_id, first_name, username))

    conn.commit()
    conn.close()


def get_balance(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return 0


def update_balance(user_id, amount):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET balance = balance + ?
    WHERE user_id=?
    """, (amount, user_id))

    conn.commit()
    conn.close()


def get_all_users():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT user_id, first_name, username, balance
    FROM users
    """)

    users = cursor.fetchall()

    conn.close()

    return users
