import sqlite3
import pandas as pd
import uuid


def get_all_incidents(conn):
    # Retrieves all incidents as a pandas DataFrame
    query = "SELECT incident_id, timestamp, severity , category,status, description FROM cyber_incidents ORDER BY id DESC"
    return pd.read_sql_query(query, conn)


def update_incident_status(conn, incident_id, new_status):
    # Modifies the status of a specific incident using its incident_id
    cursor = conn.cursor()
    sql = "UPDATE cyber_incidents SET status = ? WHERE incident_id = ?"
    cursor.execute(sql, (new_status, incident_id))
    conn.commit()
    return cursor.rowcount


def delete_incident(conn, incident_id):
    # Removes an incident record by its incident_id
    cursor = conn.cursor()
    sql = "DELETE FROM cyber_incidents WHERE incident_id = ?"
    cursor.execute(sql, (incident_id,))
    conn.commit()
    return cursor.rowcount