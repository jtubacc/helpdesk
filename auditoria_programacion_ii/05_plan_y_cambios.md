# Plan y cambios

Se implementaron consultas de Semana 9 sobre el avance existente y, por separado, la práctica gráfica descrita en el anexo de Semana 7. Una integración posterior exige `UserService` para registrar un ticket, valida que exista el solicitante y que el técnico asignado exista y tenga el rol correspondiente, e inicia los tickets siempre en OPEN. Se incorporaron Category, Assignment y Comment, con pruebas de relaciones, como dependencia del avance de Semana 9; el texto disponible de Semana 8 no estaba confirmado como consigna oficial. Las pruebas originales se adaptaron a esa dependencia, sin cambiar las reglas de consulta.

- `app/models/entities.py`: User y Ticket encapsulados y validaciones de estado/prioridad.
- `app/services/users.py` y `app/services/tickets.py`: operaciones sobre listas, asignación, comentarios y consultas por técnico, categoría, estado y solicitante.
- `app/ui/forms.py` y `main.py`: formularios Tkinter de usuarios y tickets.
- `tests/test_week07_forms_domain.py`, `tests/test_week07_models.py`, `tests/test_week09_queries.py`: casos normales y errores; `tests/test_week08_relations.py` verifica categorías, asignaciones y comentarios.
- `.gitignore` y limpieza de seguimiento de cachés: evitar nuevos artefactos generados en el índice.

El diagrama `implementacion_clases.puml` representa el código actual. El UML conceptual basado en el caso usa nombres y operaciones del caso, por lo que no debe confundirse con ese diagrama de implementación. No se implementaron permisos por rol sin reglas concretas, persistencia de etapas posteriores ni el módulo propuesto para examen.
