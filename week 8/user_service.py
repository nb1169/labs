import bcrypt
from pathlib import Path

# Imports secure database and user management functions
from app.data.db import load_csv_to_table, DATA_DIR
from app.data.users import get_user_by_username, insert_user, get_all_users
from app.data.schema import create_all_tables


def hash_password(password):
    # Hashes a password using bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, stored_hash):
    # Verifies a plaintext password against the stored hash
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))


def migrate_users_from_file(conn, filepath=DATA_DIR / "users.txt"):
    # Reads users from users.txt and moves them to the database
    if not filepath.exists():
        return

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue

            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                role = parts[2] if len(parts) > 2 else 'user'

                insert_user(conn, username, password_hash, role)


def setup_database_complete(conn):
    # Runs all setup steps: schema creation, user migration, and CSV loading
    create_all_tables(conn)
    migrate_users_from_file(conn)


    # --- Load CSV Data ---
    load_csv_to_table(conn, DATA_DIR / "cyber_incidents.csv", "cyber_incidents")
    load_csv_to_table(conn, DATA_DIR / "datasets_metadata.csv", "datasets_metadata")
    load_csv_to_table(conn, DATA_DIR / "it_tickets.csv", "it_tickets")


def register_user(conn, username, password, role='user'):
    # Registers a new user
    user = get_user_by_username(conn, username)
    if user:
        return False, "Username already exists."

    password_hash = hash_password(password)
    user_id = insert_user(conn, username, password_hash, role)

    if user_id:
        return True, "User registered successfully."
    return False, "Failed to register user."


def login_user(conn, username, password):
    # Finds and logs in the user
    user = get_user_by_username(conn, username)
    if not user:
        return False, "User not found.", None

    stored_hash = user[2]

    if verify_password(password, stored_hash):
        return True, "Login successful!", user
    else:
        return False, "Incorrect password.", None