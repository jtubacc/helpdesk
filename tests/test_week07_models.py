from app.services.tickets import TicketService
from app.services.users import UserService

def test_create_ticket_in_memory():
    users = UserService()
    users.create(1, 'Usuario de prueba', 'usuario@example.invalid', 'REQUESTER')
    service = TicketService(users)
    ticket = service.create(
        title="No puedo ingresar al campus virtual",
        description="El usuario recibe error de credenciales al intentar ingresar al campus virtual.",
        category="Software",
        priority="High",
        requester_id=1,
    )

    assert ticket.id == 1
    assert ticket.status == "open"
    assert len(service.list()) == 1
