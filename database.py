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


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        photo_id TEXT,
        status TEXT DEFAULT 'pending'

    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS duels (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        player1_id INTEGER,

        player2_id INTEGER,

        amount INTEGER,

        player1_choice TEXT,

        player2_choice TEXT,

        winner_id INTEGER,

        status TEXT DEFAULT 'waiting'

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

    """,
    (
        user_id,
        first_name,
        username
    ))

    conn.commit()
    conn.close()





def get_balance(user_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT balance
        FROM users
        WHERE user_id=?
        """,
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

    cursor.execute(
        """
        UPDATE users
        SET balance = balance + ?
        WHERE user_id=?
        """,
        (
            amount,
            user_id
        )
    )

    conn.commit()
    conn.close()





def set_balance(user_id, amount):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET balance=?
        WHERE user_id=?
        """,
        (
            amount,
            user_id
        )
    )

    conn.commit()
    conn.close()





def get_all_users():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id, first_name, username, balance
        FROM users
        """
    )

    users = cursor.fetchall()

    conn.close()

    return users





# =========================
# پرداخت ها
# =========================


def create_payment(user_id, amount, photo_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO payments
        (user_id, amount, photo_id)

        VALUES (?, ?, ?)

        """,
        (
            user_id,
            amount,
            photo_id
        )
    )

    conn.commit()
    conn.close()





def get_pending_payments():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, user_id, amount, photo_id
        FROM payments
        WHERE status='pending'
        """
    )

    payments = cursor.fetchall()

    conn.close()

    return payments





def approve_payment(payment_id):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT user_id, amount
        FROM payments
        WHERE id=?
        """,
        (payment_id,)
    )


    payment = cursor.fetchone()


    if payment:

        user_id = payment[0]
        amount = payment[1]


        cursor.execute(
            """
            UPDATE users

            SET balance = balance + ?

            WHERE user_id=?
            """,
            (
                amount,
                user_id
            )
        )


        cursor.execute(
            """
            UPDATE payments

            SET status='approved'

            WHERE id=?
            """,
            (payment_id,)
        )


    conn.commit()
    conn.close()





def reject_payment(payment_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE payments

        SET status='rejected'

        WHERE id=?
        """,
        (payment_id,)
    )

    conn.commit()
    conn.close()





# =========================
# دوئل آنلاین
# =========================


def create_duel(player_id, amount):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO duels
        (player1_id, amount)

        VALUES (?, ?)
        """,
        (
            player_id,
            amount
        )
    )

    conn.commit()
    conn.close()





def find_duel(amount, player_id):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT id, player1_id

        FROM duels

        WHERE amount=?

        AND status='waiting'

        AND player1_id != ?

        LIMIT 1
        """,
        (
            amount,
            player_id
        )
    )


    duel = cursor.fetchone()

    conn.close()

    return duel





def join_duel(duel_id, player2_id):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE duels

        SET player2_id=?,
        status='playing'

        WHERE id=?
        """,
        (
            player2_id,
            duel_id
        )
    )


    conn.commit()
    conn.close()





def save_choice(duel_id, player, choice):

    conn = connect()
    cursor = conn.cursor()


    if player == 1:

        cursor.execute(
            """
            UPDATE duels

            SET player1_choice=?

            WHERE id=?
            """,
            (
                choice,
                duel_id
            )
        )


    else:

        cursor.execute(
            """
            UPDATE duels

            SET player2_choice=?

            WHERE id=?
            """,
            (
                choice,
                duel_id
            )
        )


    conn.commit()
    conn.close()





def get_duel(duel_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *

        FROM duels

        WHERE id=?
        """,
        (duel_id,)
    )


    duel = cursor.fetchone()

    conn.close()

    return duel





def finish_duel(duel_id, winner_id):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE duels

        SET winner_id=?,
        status='finished'

        WHERE id=?
        """,
        (
            winner_id,
            duel_id
        )
    )


    conn.commit()
    conn.close()
