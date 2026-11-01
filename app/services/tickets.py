from app.models.entities import Ticket
from app.models.enums import TicketStatus

class TicketService:
    # inicializa el servicio de ticket whith an empty list of tickets and a next_id counter
    def __init__(self) -> None:
        self._tickets: list[Ticket] = []
        self.next_id: int = 1

    # create a new ticket
    def create(
            self,
            title: str,
            description: str,
            category: str,
            priority: str,
            requester_id: int,
            status: str = "open",
    ) -> Ticket:
        ticket = Ticket(
            id=self.next_id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            requester_id=requester_id,
            status=status,
        )
        self._tickets.append(ticket)
        self.next_id += 1
        return ticket

    #list all tickets
    def list(self) -> list[Ticket]:
        return self._tickets

    def assign_technician(self, ticket_id: int, technician_id: int) -> Ticket:
        """Assign an existing ticket to a technician."""
        for ticket in self._tickets:
            if ticket.id == ticket_id:
                ticket.assignee_id = technician_id
                return ticket
        raise ValueError(f"Ticket {ticket_id} no encontrado")

    def list_by_technician(self, technician_id: int) -> list[Ticket]:
        """Return only tickets assigned to the given technician."""
        return [ticket for ticket in self._tickets if ticket.assignee_id == technician_id]

    def list_by_category(self, category: str) -> list[Ticket]:
        """Return only tickets in the given category."""
        return [ticket for ticket in self._tickets if ticket.category == category]

    def list_by_status(self, status: str | TicketStatus) -> list[Ticket]:
        """Return tickets with the requested status, ignoring case."""
        normalized = str(status).strip().casefold()
        return [ticket for ticket in self._tickets if str(ticket.status).strip().casefold() == normalized]
