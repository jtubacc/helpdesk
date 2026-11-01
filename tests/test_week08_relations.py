import pytest

from app.models.entities import Assignment, Category, Comment
from app.services.tickets import TicketService
from app.services.users import UserService


@pytest.fixture
def services():
    users = UserService()
    requester = users.create(1, 'Solicitante', 'solicitante@example.invalid', 'REQUESTER')
    technician = users.create(2, 'Técnico', 'tecnico@example.invalid', 'TECHNICIAN')
    return users, TicketService(users), requester, technician


def make_ticket(service, title, category):
    return service.create(title, 'Descripción', category, 'MEDIUM', 1)


def test_categories_are_related_and_reused(services):
    _, tickets, requester, _ = services
    first = make_ticket(tickets, 'Uno', 'Hardware')
    second = make_ticket(tickets, 'Dos', 'Hardware')
    third = make_ticket(tickets, 'Tres', 'Software')
    assert isinstance(first.category_entity, Category)
    assert first.category_entity is second.category_entity
    assert first.category_entity.id != third.category_entity.id
    assert first.requester is requester
    assert tickets.list_by_category('Hardware') == [first, second]


def test_assignment_connects_ticket_and_technician(services):
    _, tickets, _, technician = services
    ticket = make_ticket(tickets, 'Uno', 'Hardware')
    tickets.assign_technician(ticket.id, technician.id)
    assert isinstance(ticket.assignment, Assignment)
    assert (ticket.assignment.ticket_id, ticket.assignment.technician_id) == (ticket.id, technician.id)
    assert ticket.assignee is technician
    assert tickets.list_by_technician(technician.id) == [ticket]


def test_comments_are_related_to_ticket_and_author(services):
    _, tickets, requester, technician = services
    first = make_ticket(tickets, 'Uno', 'Hardware')
    other = make_ticket(tickets, 'Dos', 'Software')
    comment = tickets.add_comment(first.id, requester.id, '  Se revisa el equipo  ')
    second = tickets.add_comment(first.id, technician.id, 'Prueba completada')
    assert isinstance(comment, Comment)
    assert (comment.id, comment.ticket_id, comment.author_id, comment.body) == (1, first.id, requester.id, 'Se revisa el equipo')
    assert second.id == 2 and first.comments == (comment, second)
    assert other.comments == ()


@pytest.mark.parametrize('ticket_id, author_id, body', [(999, 1, 'Texto'), (1, 999, 'Texto'), (1, 1, '  ')])
def test_invalid_comment_has_no_effect(services, ticket_id, author_id, body):
    _, tickets, _, _ = services
    ticket = make_ticket(tickets, 'Uno', 'Hardware')
    original_update = ticket.updated_at
    with pytest.raises(ValueError):
        tickets.add_comment(ticket_id, author_id, body)
    assert ticket.comments == () and ticket.updated_at == original_update
    assert tickets.add_comment(ticket.id, 1, 'Válido').id == 1
