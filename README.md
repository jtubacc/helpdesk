# HelpDesk EDU — práctica de semana 7

Aplicación académica de usuarios y tickets en memoria, con consultas de semana 9. Al cerrar la aplicación se pierden los datos; esta etapa no configura una base de datos.

## Requisitos y ejecución

Python 3.11 o posterior con Tkinter disponible, y `uv` para instalar las dependencias de desarrollo. En un entorno virtual con Python y Tkinter:

```sh
uv sync --locked
uv run python main.py
uv run pytest -q
```

La pestaña **Usuarios** registra, lista, busca por ID y actualiza usuarios. La pestaña **Tickets** registra tickets para un usuario ya registrado, lista, busca por ID, filtra por solicitante y permite modificar estado y prioridad. Los ID de tickets, estado inicial y fecha de creación se generan automáticamente. Las listas viven únicamente durante la ejecución.

La interfaz conecta `TicketService` con `UserService` para validar que el solicitante exista. La construcción histórica `TicketService()` sin un servicio de usuarios se conserva para compatibilidad con las pruebas previas de semana 9 y no comprueba la existencia del solicitante; las nuevas integraciones deben proporcionar `UserService`.

## Alcance pendiente de cotejo

El documento de semana 7 se presenta en Canvas como caso de la tarea de UML; no se ha identificado una entrega independiente vigente que exija esta aplicación. No hay autenticación ni política de autorización por roles en este prototipo: el documento menciona restricción por rol pero no define un mecanismo de sesión para esta fase. Los `.pyc` ya versionados antes de esta modificación siguen en el historial y deben revisarse por separado.
