import uuid
from datetime import datetime


class SecurityIncident:
    """
    represents a single cyber incident entity with core attributes
    and methods for status management.
    """

    def __init__(self, incident_id, timestamp, severity, category, status,
                 description="", reported_by=None, db_id=None):
        # use existing id if loading from db, otherwise generate a new one
        self._incident_id = incident_id if incident_id else str(uuid.uuid4())
        self._db_id = db_id  # optional: for the auto-incrementing db row id

        self._timestamp = timestamp
        self._severity = severity
        self._category = category
        self._status = status
        self._description = description
        self._reported_by = reported_by

    # accessor methods (getters)
    # these methods are used to access the attributes (encapsulation)

    def get_incident_id(self):
        return self._incident_id

    def get_db_id(self):
        return self._db_id

    def get_timestamp(self):
        return self._timestamp

    def get_severity(self):
        return self._severity

    def get_category(self):
        return self._category

    def get_category(self):
        return self._category

    def get_status(self):
        return self._status

    def get_description(self):
        return self._description

    # mutator methods (setters/actions)

    def set_status(self, new_status):
        # sets the status of the incident
        self._status = new_status

    def close(self):
        # convenience method to set the status to 'closed'
        self._status = "closed"

    # utility methods

    def __str__(self):
        # provides a user friendly string representation of the incident
        return f"incident id: {self._incident_id} | status: {self._status} | severity: {self._severity} | category: {self._category} | timestamp: {self._timestamp}"