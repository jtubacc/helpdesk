from app.models.entities import Ticket
from app.models.enums import TicketStatus
from app.services.users import UserService


class TicketService:
    def __init__(self, users: UserService | None = None) -> None:
        # None preserva compatibilidad con los ejercicios aislados de semana 9.
        # La interfaz siempre proporciona UserService y exige solicitante existente.
        self._users = users
        self._tickets: list[Ticket] = []
        self.next_id = 1

    def create(self, title: str, description: str, category: str, priority: str,
               requester_id: int, status: str = 'open') -> Ticket:
        requester = self._users.find(requester_id) if self._users is not None else None
        if self._users is not None and requester is None:
            raise ValueError('Usuario solicitante no encontrado')
        ticket = Ticket(self.next_id, title, description, category, priority, requester_id, status, requester)
        self._tickets.append(ticket)
        self.next_id += 1
        return ticket

    def list(self) -> list[Ticket]:
        return list(self._tickets)

    def find(self, ticket_id: int) -> Ticket | None:
        return next((t for t in self._tickets if t.id == ticket_id), None)

    def _require(self, ticket_id: int) -> Ticket:
        ticket = self.find(ticket_id)
        if ticket is None:
            raise ValueError(f'Ticket {ticket_id} no encontrado')
        return ticket

    def change_status(self, ticket_id: int, status: str) -> Ticket:
        ticket = self._require(ticket_id)
        ticket.change_status(status)
        return ticket

    def change_priority(self, ticket_id: int, priority: str) -> Ticket:
        ticket = self._require(ticket_id)
        ticket.change_priority(priority)
        return ticket

    def list_by_requester(self, requester_id: int) -> list[Ticket]:
        return [t for t in self._tickets if t.requester_id == requester_id]

    def assign_technician(self, ticket_id: int, technician_id: int) -> Ticket:
        ticket = self._require(ticket_id)
        ticket.assign_technician(technician_id)
        return ticket

    def list_by_technician(self, technician_id: int) -> list[Ticket]:
        return [t for t in self._tickets if t.assignee_id == technician_id]

    def list_by_category(self, category: str) -> list[Ticket]:
        return [t for t in self._tickets if t.category == category]

    def list_by_status(self, status: str | TicketStatus) -> list[Ticket]:
        normalized = str(status).strip().casefold()
        return [t for t in self._tickets if str(t.status).strip().casefold() == normalized]
