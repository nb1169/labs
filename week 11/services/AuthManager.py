import bcrypt
from typing import Optional

# import the new database service and user model
from services.database_manager import DatabaseManager
from models.user import User


class SimpleBcryptHasher:
    # provides the methods for hashing and verification using bcrypt

    def hash_password(self, password):
        # hashes a password using bcrypt
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password, stored_hash):
        # verifies a plaintext password against the stored hash
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))


class AuthManager:
    # handles user authentication and registration

    def __init__(self, db: DatabaseManager, hasher=SimpleBcryptHasher()):
        # authmanager has-a databasemanager (composition) [cite: 724]
        self._db = db
        self._hasher = hasher

    def _get_user_by_username(self, username: str) -> Optional[User]:
        # fetches a single user row, returns a user object
        sql = "SELECT username, password_hash, role FROM users WHERE username = ?"
        # use fetch_one from the databasemanager [cite: 744]
        row = self._db.fetch_one(sql, (username,))

        if row is None:
            return None

        # creates and returns a user object
        return User(row[0], row[1], row[2])

    def register_user(self, username: str, password: str, role: str = 'user') -> tuple[bool, str]:
        # registers a new user
        if self._get_user_by_username(username):
            return False, "username already exists."

        password_hash = self._hasher.hash_password(password)
        sql = "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)"

        try:
            # uses execute_query from the databasemanager [cite: 741]
            self._db.execute_query(sql, (username, password_hash, role))
            return True, "user registered successfully."
        except Exception:
            return False, "failed to register user."

    def login_user(self, username: str, password: str) -> Optional[User]:
        # finds and logs in the user [cite: 744]
        user = self._get_user_by_username(username)

        if user is None:
            return None  # user not found

        # use the user object's method to verify the password against the stored hash [cite: 607, 750]
        if user.verify_password(password, self._hasher):
            return user
        else:
            return None  # incorrect password