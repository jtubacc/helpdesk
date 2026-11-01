import pytest
from app.services.users import UserService
from app.services.tickets import TicketService

@pytest.fixture
def services():
    users = UserService()
    return users, TicketService(users)

def test_valid_user_and_updates(services):
    users, _ = services
    user = users.create(1, 'Ana', 'ana@example.invalid', 'REQUESTER')
    assert users.find(1) is user and users.list() == [user]
    users.update(1, 'Ana Dos', 'dos@example.invalid', 'TECHNICIAN', 'ACTIVO')
    assert user.name == 'Ana Dos' and user.role == 'technician'

@pytest.mark.parametrize('email,role', [('', 'REQUESTER'), ('a@example.invalid', 'INVALID')])
def test_invalid_user_is_rejected(services, email, role):
    users, _ = services
    with pytest.raises(ValueError): users.create(1, 'Ana', email, role)
    assert users.list() == []

def test_ticket_lifecycle_and_filters(services):
    users, tickets = services
    first = users.create(1, 'Ana', 'ana@example.invalid', 'REQUESTER')
    users.create(2, 'Luis', 'luis@example.invalid', 'REQUESTER')
    a = tickets.create('Sin red', 'No conecta', 'Network', 'HIGH', 1)
    b = tickets.create('Impresora', 'No imprime', 'Hardware', 'LOW', 2)
    assert a.requester is first and a.id == 1 and a.status == 'open' and a.created_at
    assert tickets.find(a.id) is a and tickets.find(999) is None
    assert tickets.list_by_requester(1) == [a] and b not in tickets.list_by_requester(1)
    tickets.change_status(a.id, 'IN_PROGRESS')
    tickets.change_priority(a.id, 'CRITICAL')
    assert a.status == 'in_progress' and a.priority == 'CRITICAL'

def test_unknown_requester_is_rejected(services):
    _, tickets = services
    with pytest.raises(ValueError, match='solicitante'): tickets.create('x', 'y', 'General', 'LOW', 999)
    assert tickets.list() == []

def test_user_service_is_required():
    with pytest.raises(TypeError):
        TicketService()
    with pytest.raises(ValueError, match='servicio de usuarios'):
        TicketService(None)

def test_tickets_always_start_open(services):
    users, tickets = services
    users.create(1, 'Ana', 'ana@example.invalid', 'REQUESTER')
    ticket = tickets.create('Sin red', 'No conecta', 'Network', 'HIGH', 1)
    assert ticket.status == 'open'
    with pytest.raises(TypeError):
        tickets.create('Otro', 'Descripción', 'Network', 'LOW', 1, status='closed')
    assert tickets.list() == [ticket]

def test_invalid_status_and_priority_do_not_mutate(services):
    users, tickets = services
    users.create(1, 'Ana', 'ana@example.invalid', 'REQUESTER')
    ticket = tickets.create('x', 'y', 'General', 'LOW', 1)
    with pytest.raises(ValueError): tickets.change_status(ticket.id, 'BAD')
    with pytest.raises(ValueError): tickets.change_priority(ticket.id, 'BAD')
    assert ticket.status == 'open' and ticket.priority == 'LOW'
