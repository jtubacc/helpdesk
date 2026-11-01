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


class Ticket:
    def __init__(self, id: int, title: str, description: str, category: str,
                 priority: str, requester_id: int, status: str = 'open', requester: User | None = None):
        if not title.strip() or not description.strip() or not category.strip():
            raise ValueError('Título, descripción y categoría son obligatorios')
        self.__id, self.__requester_id, self.__requester = id, requester_id, requester
        self.__title, self.__description, self.__category = title.strip(), description.strip(), category.strip()
        self.__assignee_id = None
        self.__created_at = datetime.now().astimezone()
        self.__updated_at = self.__created_at
        self.change_priority(priority)
        self.change_status(status)

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
    def category(self): return self.__category
    @property
    def priority(self): return self.__priority
    @property
    def status(self): return self.__status
    @property
    def assignee_id(self): return self.__assignee_id
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

    def assign_technician(self, technician_id):
        self.__assignee_id = technician_id
        self.__updated_at = datetime.now().astimezone()
