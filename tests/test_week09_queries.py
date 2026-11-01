import pytest

from app.models.enums import TicketStatus
from app.services.tickets import TicketService
from app.services.users import UserService


@pytest.fixture
def service():
    users = UserService()
    users.create(1, 'Solicitante', 'solicitante@example.invalid', 'REQUESTER')
    users.create(10, 'Técnico uno', 'tecnico1@example.invalid', 'TECHNICIAN')
    users.create(20, 'Técnico dos', 'tecnico2@example.invalid', 'TECHNICIAN')
    return TicketService(users)


def create_ticket(service, title, category):
    return service.create(
        title=title,
        description="Caso de prueba",
        category=category,
        priority="Medium",
        requester_id=1,
    )


def test_list_by_technician_returns_only_assigned_tickets(service):
    first = create_ticket(service, "No imprime", "Hardware")
    second = create_ticket(service, "No ingresa", "Software")
    unassigned = create_ticket(service, "Sin asignar", "General")
    service.assign_technician(first.id, 10)
    service.assign_technician(second.id, 20)

    assert service.list_by_technician(10) == [first]
    assert service.list_by_technician(20) == [second]
    assert service.list_by_technician(30) == []
    assert unassigned.assignee_id is None


def test_assign_technician_rejects_unknown_ticket(service):
    with pytest.raises(ValueError, match="no encontrado"):
        service.assign_technician(999, 10)
    assert service.list() == []


def test_list_by_category_returns_only_matching_tickets(service):
    first = create_ticket(service, "No imprime", "Hardware")
    create_ticket(service, "No ingresa", "Software")
    second = create_ticket(service, "Disco lleno", "Hardware")

    assert service.list_by_category("Hardware") == [first, second]
    assert service.list_by_category("Network") == []


def test_list_by_status_normalizes_and_excludes_other_statuses(service):
    first = create_ticket(service, "Abierto", "General")
    progress = create_ticket(service, "En proceso", "General")
    service.change_status(progress.id, TicketStatus.IN_PROGRESS)
    second = create_ticket(service, "También abierto", "Software")

    assert service.list_by_status("OPEN") == [first, second]
    assert service.list_by_status(TicketStatus.IN_PROGRESS) == [progress]
    assert service.list_by_status("closed") == []


@pytest.mark.parametrize('technician_id', [999, 1])
def test_assignment_rejects_missing_or_non_technician_without_mutating(service, technician_id):
    ticket = create_ticket(service, 'Caso', 'General')
    service.assign_technician(ticket.id, 10)
    original_update = ticket.updated_at
    with pytest.raises(ValueError):
        service.assign_technician(ticket.id, technician_id)
    assert ticket.assignee_id == 10
    assert ticket.updated_at == original_update
    assert service.list_by_technician(10) == [ticket]
