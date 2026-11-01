# Matriz de trazabilidad

Estados de implementación a la fecha de revisión; una prueba local no acredita entrega, aprobación ni revisión visual.

| ID | Módulo / tarea | Requisito verificable | Fuente | Archivo / clase | Estado inicial | Acción | Evidencia | Estado final |
|---|---|---|---|---|---|---|---|---|
| S7-01 | Primera fase | Usuario con ID, nombre, correo, rol y estado | Semana 7 pp. 11–12 | `app/models/entities.py` User; `app/services/users.py` | Faltaba | Agregar modelo y servicio | `test_week07_forms_domain.py` | Cumple pruebas de dominio; UI visual pendiente |
| S7-02 | Primera fase | Rechazar correo vacío y rol inválido | Semana 7 p. 11 | User.update / UserService.create | Faltaba | Validar | Pruebas parametrizadas | Cumple en pruebas |
| S7-03 | Primera fase | Asociar ticket a usuario existente | Semana 7 p. 12 | TicketService.create | No validado | Requerir UserService y rechazar ID ausente | `test_unknown_requester_is_rejected`, `test_user_service_is_required` | Cumple en pruebas |
| S7-04 | Primera fase | Ticket inicia OPEN; buscar, filtrar, cambiar estado/prioridad | Semana 7 pp. 11–12 | Ticket y TicketService | Parcial | Validar y añadir operaciones | `test_ticket_lifecycle_and_filters`, `test_tickets_always_start_open` | Cumple pruebas de dominio; UI visual pendiente |
| S7-05 | Primera fase | Dos formularios y lógica separada | Semana 7 pp. 11–12 | `app/ui/forms.py`, `main.py` | Faltaban | Añadir interfaz | Proceso Tk arrancó y callbacks de ambas etapas probados con datos ficticios | Parcial: falta comprobar visualmente la versión actual y capturas |
| S7-06 | Primera fase | Canal de ticket | Semana 7 p. 6 frente a pp. 11–12 | No implementado | No verificable | Aclarar discrepancia | Dos secciones difieren | No verificable |
| S7-07 | Primera fase | Limitar acciones por rol | Semana 7 p. 6 RQ-11 | Sin autenticación ni matriz de permisos | No cumple | Aclarar reglas antes de implementarlas | Inspección | No cumple / reglas no verificables |
| S8-01 | Dependencia Semana 9 | Conectar categoría, asignación y comentarios al ticket | Texto local sin confirmar de Semana 8; Semana 9 presupone relaciones | Category, Assignment, Comment y TicketService | Faltaban | Añadir relaciones necesarias | `tests/test_week08_relations.py` | Parcial: funcionalidad probada; consigna oficial autónoma no verificada |
| S9-01 | Semana 9 | Consultar por técnico, categoría y estado | Semana 9 pp. 2–4 | TicketService.list_by_* | Faltaban | Añadir consultas | `tests/test_week09_queries.py` | Cumple pruebas locales |
| S9-02 | Semana 9 | Asignación solo a técnico válido | Semana 9 ejemplo y relación de Semana 8 | TicketService.assign_technician | Faltaba | Validar usuario y rol | Pruebas de inexistente, rol y filtros | Cumple pruebas locales de asignación; origen oficial de Semana 8 no confirmado |
| S9-03 | Semana 9 | Pruebas, rama, push y PR a developer | Semana 9 pp. 2–4 | `tests/test_week09_queries.py`, historial Git | Sin consultas en rama remota inicial | Validar y gestionar PR | 21 pruebas en suite; resultado del flujo Git pendiente de verificación final | Parcial |
| UML-01 | Tarea UML | Requisitos, matriz y tres diagramas | Tarea 1 UML | Modelo conceptual de requisitos; `implementacion_clases.puml` para código actual | Pendiente | Comparar modelo y código | Modelo conceptual cotejado | Parcial: son modelos diferentes; no son el mismo diagrama |
