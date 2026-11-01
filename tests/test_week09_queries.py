import pytest

from app.models.enums import TicketStatus
from app.services.tickets import TicketService


def create_ticket(service, title, category, status="open"):
    return service.create(
        title=title,
        description="Caso de prueba",
        category=category,
        priority="Medium",
        requester_id=1,
        status=status,
    )


def test_list_by_technician_returns_only_assigned_tickets():
    service = TicketService()
    first = create_ticket(service, "No imprime", "Hardware")
    second = create_ticket(service, "No ingresa", "Software")
    unassigned = create_ticket(service, "Sin asignar", "General")
    service.assign_technician(first.id, 10)
    service.assign_technician(second.id, 20)

    assert service.list_by_technician(10) == [first]
    assert service.list_by_technician(20) == [second]
    assert service.list_by_technician(30) == []
    assert unassigned.assignee_id is None


def test_assign_technician_rejects_unknown_ticket():
    service = TicketService()
    with pytest.raises(ValueError, match="no encontrado"):
        service.assign_technician(999, 10)
    assert service.list() == []


def test_list_by_category_returns_only_matching_tickets():
    service = TicketService()
    first = create_ticket(service, "No imprime", "Hardware")
    create_ticket(service, "No ingresa", "Software")
    second = create_ticket(service, "Disco lleno", "Hardware")

    assert service.list_by_category("Hardware") == [first, second]
    assert service.list_by_category("Network") == []


def test_list_by_status_normalizes_and_excludes_other_statuses():
    service = TicketService()
    first = create_ticket(service, "Abierto", "General", "open")
    progress = create_ticket(service, "En proceso", "General", TicketStatus.IN_PROGRESS)
    second = create_ticket(service, "También abierto", "Software", TicketStatus.OPEN)

    assert service.list_by_status("OPEN") == [first, second]
    assert service.list_by_status(TicketStatus.IN_PROGRESS) == [progress]
    assert service.list_by_status("closed") == []
