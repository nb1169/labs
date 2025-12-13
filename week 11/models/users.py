import sqlite3

def get_user_by_username(conn, username):
    cursor = conn.cursor()
    cursor.execute(     # run a query to find the user matching the given username
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,)
    )
    return cursor.fetchone()

def get_all_users(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    # Fetches all results, which can be used to check if the list is empty
    return cursor.fetchall()

def insert_user(conn, username, password_hash, role='user'):
    # CREATE: Inserts a new user record
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None