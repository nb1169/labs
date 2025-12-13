import sqlite3
import pandas as pd
import os
import sys

# import the new entity class
from models.security_incident import SecurityIncident

# define the database path (adjust if your 'platform.db' is elsewhere)
# assuming 'platform.db' is in a 'database' folder at the project root level
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
db_path = os.path.join(project_root, 'database', 'platform.db')


class DatabaseManager:
    """
    manages all database interactions, holding the connection and
    performing crud operations using securityincident objects.
    """

    def __init__(self, db_path=db_path):
        self.db_path = db_path
        self._conn = None
        self._connect()

    def _connect(self):
        # initializes the database connection
        try:
            self._conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"error connecting to database: {e}")
            sys.exit(1)

    def close(self):
        # closes the database connection
        if self._conn:
            self._conn.close()

    # incident crud operations

    def insert_incident(self, incident: SecurityIncident):
        # inserts a new securityincident object into the database
        cursor = self._conn.cursor()

        sql = """
        insert into cyber_incidents 
        (incident_id, timestamp, severity, category, status, description)
        values (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            incident.get_incident_id(),
            incident.get_timestamp(),
            incident.get_severity(),
            incident.get_category(),
            incident.get_status(),
            incident.get_description()
        ))
        self._conn.commit()
        return cursor.lastrowid

    def get_all_incidents(self) -> list[SecurityIncident]:
        # retrieves all incidents and returns them as a list of securityincident objects
        query = "select * from cyber_incidents order by timestamp desc"

        # use pandas to easily fetch all rows
        df = pd.read_sql_query(query, self._conn)

        incidents = []
        for index, row in df.iterrows():
            incident = SecurityIncident(
                incident_id=row['incident_id'],
                timestamp=row['timestamp'],
                severity=row['severity'],
                category=row['category'],
                status=row['status'],
                description=row['description'],
                db_id=row['id']  # assuming 'id' is the auto increment primary key
            )
            incidents.append(incident)

        return incidents

    def update_incident_status(self, incident_id, new_status):
        # updates the status of an incident using its incident_id
        cursor = self._conn.cursor()
        sql = "update cyber_incidents set status = ? where incident_id = ?"
        cursor.execute(sql, (new_status, incident_id))
        self._conn.commit()
        return cursor.rowcount

    def delete_incident(self, incident_id):
        # removes an incident record by its incident_id
        cursor = self._conn.cursor()
        sql = "delete from cyber_incidents where incident_id = ?"
        cursor.execute(sql, (incident_id,))
        self._conn.commit()
        return cursor.rowcount