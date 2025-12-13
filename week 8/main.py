from app.data.db import connect_database
from app.services.user_service import setup_database_complete, register_user, login_user
from app.data.incidents import insert_incident, get_all_incidents, update_incident_status, delete_incident


def run_demo():
    # connect and setup database
    conn = connect_database()
    # run setup to create tables and load CSVs/users.txt
    setup_database_complete(conn)
    print("Database setup complete.")

    register_user(conn, "demo_analyst", "SecurePass123", "analyst") # registers user with name and password
    success, msg, _ = login_user(conn, "demo_analyst", "SecurePass123") # tries to login with the username and password
    print(f"Login status: {msg}") # prints whether login was successful

    # read initial count
    df_initial = get_all_incidents(conn)
    print(f"Initial incident count: {len(df_initial)}")

    # create new incident with all the fields
    new_row_id = insert_incident(
        conn,
        timestamp="2025-01-01 12:00:00",
        category="Malware",
        severity="Medium",
        status="Open",
        description="Test case for demo",
        reported_by="demo_analyst"
    )
    print(f"Created incident internal row ID: {new_row_id}")

    df_incidents = get_all_incidents(conn)    # get the unique incident id
    test_incident_id = df_incidents.iloc[0]['incident_id']    # get the unique incident_id from the newest row
    print(f"Extracted unique incident_id: {test_incident_id}")

    update_incident_status(conn, test_incident_id, "Resolved")   # update the incident status
    print(f"Updated incident {test_incident_id} status to Resolved.")    # prints confirmation that the update happened

    # delete the incident
    delete_incident(conn, test_incident_id)
    print(f"Deleted incident {test_incident_id}.")

    conn.close()


if __name__ == "__main__":
    run_demo()