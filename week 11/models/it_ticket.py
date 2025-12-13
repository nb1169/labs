# models/it_ticket.py

class ITTicket:
    # represents an it support ticket entity

    def __init__(self, ticket_id, title, priority, status, assigned_to=None, db_id=None):
        self._ticket_id = ticket_id
        self._title = title
        self._priority = priority
        self._status = status
        self._assigned_to = assigned_to
        self._db_id = db_id

    # accessor methods (getters)
    def get_ticket_id(self):
        return self._ticket_id

    def get_title(self):
        return self._title

    def get_priority(self):
        return self._priority

    def get_status(self):
        return self._status

    def get_assigned_to(self):
        return self._assigned_to

    # mutator methods (actions)
    def assign_to(self, staff: str) -> None:
        # assigns the ticket to a staff member
        self._assigned_to = staff

    def close_ticket(self) -> None:
        # sets the status to closed
        self._status = "closed"

    def __str__(self) -> str:
        # user friendly string representation
        return f"ticket id: {self._ticket_id} | title: {self._title} | priority: {self._priority} | assigned to: {self._assigned_to}"