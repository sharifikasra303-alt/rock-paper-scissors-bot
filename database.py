import sqlite3

DB_NAME = "database.db"


def connect():
    return sqlite3.connect(DB_NAME)



def create_table():

    conn = connect()
    cursor = conn.cursor()


    # جدول کاربران
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        username TEXT,
        balance INTEGER DEFAULT 0
    )
    """)


    # جدول پرداخت‌ها
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        photo_id TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)


    conn.commit()
    conn.close()



# اضافه کردن کاربر
def add_user(user_id, first_name, username):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    INSERT OR IGNORE INTO users
    (user_id, first_name, username)
    VALUES (?, ?, ?)
    """,
    (
        user_id,
        first_name,
        username
    ))


    conn.commit()
    conn.close()



# گرفتن موجودی
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



# اضافه کردن موجودی
def add_balance(user_id, amount):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    UPDATE users
    SET balance = balance + ?
    WHERE user_id=?
    """,
    (
        amount,
        user_id
    ))


    conn.commit()
    conn.close()



# تغییر مستقیم موجودی
def set_balance(user_id, amount):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    UPDATE users
    SET balance=?
    WHERE user_id=?
    """,
    (
        amount,
        user_id
    ))


    conn.commit()
    conn.close()



# گرفتن همه کاربران
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



# ساخت درخواست خرید
def create_payment(user_id, amount, photo_id):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    INSERT INTO payments
    (user_id, amount, photo_id)
    VALUES (?, ?, ?)
    """,
    (
        user_id,
        amount,
        photo_id
    ))


    conn.commit()
    conn.close()



# گرفتن پرداخت‌های در انتظار
def get_pending_payments():

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT id, user_id, amount, photo_id
    FROM payments
    WHERE status='pending'
    """)


    payments = cursor.fetchall()


    conn.close()

    return payments



# تایید پرداخت
def approve_payment(payment_id):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT user_id, amount
    FROM payments
    WHERE id=?
    """,
    (payment_id,)
    )


    payment = cursor.fetchone()


    if payment:

        user_id, amount = payment


        cursor.execute("""
        UPDATE users
        SET balance = balance + ?
        WHERE user_id=?
        """,
        (
            amount,
            user_id
        ))


        cursor.execute("""
        UPDATE payments
        SET status='approved'
        WHERE id=?
        """,
        (payment_id,))


    conn.commit()
    conn.close()



# رد پرداخت
def reject_payment(payment_id):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    UPDATE payments
    SET status='rejected'
    WHERE id=?
    """,
    (payment_id,)
    )


    conn.commit()
    conn.close()
