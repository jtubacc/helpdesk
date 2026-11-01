from app.models.entities import Category, Comment, Ticket
from app.models.enums import Role, TicketStatus
from app.services.users import UserService


class TicketService:
    def __init__(self, users: UserService) -> None:
        if users is None:
            raise ValueError('Se requiere el servicio de usuarios')
        self._users = users
        self._tickets: list[Ticket] = []
        self._categories: dict[str, Category] = {}
        self.next_id = 1
        self._next_comment_id = 1

    def create(self, title: str, description: str, category: str, priority: str,
               requester_id: int) -> Ticket:
        requester = self._users.find(requester_id)
        if requester is None:
            raise ValueError('Usuario solicitante no encontrado')
        name = category.strip()
        category_entity = self._categories.get(name)
        is_new_category = category_entity is None
        if is_new_category:
            category_entity = Category(len(self._categories) + 1, name)
        ticket = Ticket(self.next_id, title, description, category_entity, priority, requester)
        if is_new_category:
            self._categories[name] = category_entity
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
        technician = self._users.find(technician_id)
        if technician is None:
            raise ValueError('Técnico no encontrado')
        if technician.role != Role.TECHNICIAN:
            raise ValueError('El usuario asignado debe tener rol TECHNICIAN')
        ticket._assign_technician(technician)
        return ticket

    def add_comment(self, ticket_id: int, author_id: int, body: str) -> Comment:
        ticket = self._require(ticket_id)
        if self._users.find(author_id) is None:
            raise ValueError('Autor no encontrado')
        body = body.strip()
        if not body:
            raise ValueError('El comentario no puede estar vacío')
        comment = Comment(self._next_comment_id, ticket_id, author_id, body)
        ticket._add_comment(comment)
        self._next_comment_id += 1
        return comment

    def list_by_technician(self, technician_id: int) -> list[Ticket]:
        return [t for t in self._tickets if t.assignee_id == technician_id]

    def list_by_category(self, category: str) -> list[Ticket]:
        return [t for t in self._tickets if t.category == category]

    def list_by_status(self, status: str | TicketStatus) -> list[Ticket]:
        normalized = str(status).strip().casefold()
        return [t for t in self._tickets if str(t.status).strip().casefold() == normalized]
