from dataclasses import dataclass, field
from datetime import datetime
from app.models.enums import Role, TicketStatus


class User:
    """Usuario con estado protegido y operaciones de actualización validadas."""
    def __init__(self, id: int, name: str, email: str, role: str, state: str = 'ACTIVO'):
        if id <= 0:
            raise ValueError('El ID debe ser positivo')
        self.__id = id
        self.update(name, email, role, state)

    @property
    def id(self): return self.__id
    @property
    def name(self): return self.__name
    @property
    def email(self): return self.__email
    @property
    def role(self): return self.__role
    @property
    def state(self): return self.__state

    def update(self, name: str, email: str, role: str, state: str):
        if not name.strip() or not email.strip():
            raise ValueError('Nombre y correo son obligatorios')
        try:
            role = Role(str(role).strip().lower())
        except ValueError as exc:
            raise ValueError('Rol no permitido') from exc
        state = state.strip().upper()
        if state not in ('ACTIVO', 'INACTIVO'):
            raise ValueError('Estado de usuario no permitido')
        self.__name, self.__email, self.__role, self.__state = name.strip(), email.strip(), role, state


@dataclass(frozen=True)
class Category:
    id: int
    name: str


@dataclass(frozen=True)
class Comment:
    id: int
    ticket_id: int
    author_id: int
    body: str
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())


@dataclass(frozen=True)
class Assignment:
    ticket_id: int
    technician_id: int
    assigned_at: datetime = field(default_factory=lambda: datetime.now().astimezone())


class Ticket:
    def __init__(self, id: int, title: str, description: str, category: Category,
                 priority: str, requester: User):
        if not title.strip() or not description.strip() or not isinstance(category, Category) or not category.name.strip():
            raise ValueError('Título, descripción y categoría son obligatorios')
        if not isinstance(requester, User):
            raise ValueError('Se requiere un usuario solicitante')
        self.__id, self.__requester_id, self.__requester = id, requester.id, requester
        self.__title, self.__description, self.__category = title.strip(), description.strip(), category
        self.__assignee = None
        self.__assignment = None
        self.__comments: list[Comment] = []
        self.__created_at = datetime.now().astimezone()
        self.__updated_at = self.__created_at
        self.change_priority(priority)
        self.change_status(TicketStatus.OPEN)

    @property
    def id(self): return self.__id
    @property
    def requester_id(self): return self.__requester_id
    @property
    def requester(self): return self.__requester
    @property
    def title(self): return self.__title
    @property
    def description(self): return self.__description
    @property
    def category(self): return self.__category.name
    @property
    def category_entity(self): return self.__category
    @property
    def priority(self): return self.__priority
    @property
    def status(self): return self.__status
    @property
    def assignee_id(self): return self.__assignment.technician_id if self.__assignment else None
    @property
    def assignee(self): return self.__assignee
    @property
    def assignment(self): return self.__assignment
    @property
    def comments(self): return tuple(self.__comments)
    @property
    def created_at(self): return self.__created_at
    @property
    def updated_at(self): return self.__updated_at

    def change_status(self, status):
        try:
            self.__status = TicketStatus(str(status).strip().lower())
        except ValueError as exc:
            raise ValueError('Estado de ticket no permitido') from exc
        self.__updated_at = datetime.now().astimezone()

    def change_priority(self, priority):
        value = str(priority).strip().upper()
        if value not in ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'):
            raise ValueError('Prioridad no permitida')
        self.__priority = value
        self.__updated_at = datetime.now().astimezone()

    def _assign_technician(self, technician: User):
        self.__assignee = technician
        self.__assignment = Assignment(self.__id, technician.id)
        self.__updated_at = datetime.now().astimezone()

    def _add_comment(self, comment: Comment):
        self.__comments.append(comment)
        self.__updated_at = datetime.now().astimezone()
