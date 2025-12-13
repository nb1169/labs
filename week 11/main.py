# main.py

# CHANGE 1: Use the new AuthManager for OOP login
from app.data.db import connect_database
from app.services.user_service import setup_database_complete
# new service imports (assuming models and services folders are at the root)
from services.database_manager import DatabaseManager
from services.auth_manager import AuthManager


# OLD IMPORTS REMOVED: from app.data.incidents import insert_incident, get_all_incidents, update_incident_status, delete_incident


def run_demo():
    # setup database connection
    conn = connect_database()
    setup_database_complete(conn)
    conn.close()  # setup is done, close the raw connection

    print("database setup complete.")

    # initialize oop services
    db_manager = DatabaseManager()
    auth_manager = AuthManager(db_manager)

    # use new authmanager methods for registration and login
    # note: the db is accessed internally by auth_manager now
    auth_manager.register_user("demo_analyst", "SecurePass123", "analyst")
    user = auth_manager.login_user("demo_analyst", "SecurePass123")

    if user:
        # use getter methods from the user object
        print(f"login status: successful for {user.get_username()}!")
    else:
        print("login status: failed.")

    # --- incident crud operations removed as the functions no longer exist ---
    # the following code must be refactored to use an IncidentsManager class
    print("\n--- Incident CRUD functions are removed and must be refactored ---")

    # read initial count
    # df_initial = get_all_incidents(conn)
    # print(f"initial incident count: {len(df_initial)}")

    # ... rest of the old incident calls were commented out previously ...

    db_manager.close()


if __name__ == "__main__":
    run_demo()