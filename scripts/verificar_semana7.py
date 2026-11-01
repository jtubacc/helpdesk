"""Invoca controles Tk reales con datos ficticios; no sustituye inspección visual.

El diálogo de error se intercepta para que la comprobación no quede esperando
interacción humana. No guarda datos ni toma capturas.
"""
import tkinter as tk
from tkinter import messagebox, ttk
from app.ui.forms import HelpDeskApp

root = tk.Tk()
app = HelpDeskApp(root)
root.update()
errors = []
messagebox.showerror = lambda title, message, **kwargs: errors.append(message)

def invoke(tab, label):
    for frame in tab.winfo_children():
        for widget in frame.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget('text') == label:
                widget.invoke()
                root.update()
                return
    raise AssertionError(f'Botón no encontrado: {label}')

notebook = next(w for w in root.winfo_children() if isinstance(w, ttk.Notebook))
users = notebook.nametowidget(notebook.tabs()[0])
tickets = notebook.nametowidget(notebook.tabs()[1])
u, f = app.user_fields, app.ticket_fields
u['ID'].set('1'); u['Nombre'].set('Prueba'); u['Correo'].set('')
invoke(users, 'Registrar')
assert errors and not app.users.list()
errors.clear()
u['Correo'].set('prueba@example.invalid'); u['Rol'].set('INVALIDO')
invoke(users, 'Registrar')
assert errors and not app.users.list()
errors.clear()
u['Rol'].set('REQUESTER'); invoke(users, 'Registrar')
for i in range(2, 6):
    u['ID'].set(str(i)); u['Nombre'].set(f'Usuario {i}')
    u['Correo'].set(f'u{i}@example.invalid'); invoke(users, 'Registrar')
assert len(app.users.list()) == 5 and 'Usuario 5' in app.user_output.get('1.0', 'end')
u['ID'].set('1'); invoke(users, 'Buscar ID')
assert 'Prueba' in app.user_output.get('1.0', 'end')
u['Nombre'].set('Prueba actualizada'); invoke(users, 'Actualizar')
assert app.users.find(1).name == 'Prueba actualizada'
f['ID solicitante'].set('999'); f['Título'].set('Error')
f['Descripción'].set('Prueba'); f['Categoría'].set('General')
invoke(tickets, 'Registrar')
assert errors and not app.tickets.list()
errors.clear()
for i in range(10):
    f['ID solicitante'].set(str(i % 5 + 1)); f['Título'].set(f'Ticket {i + 1}')
    invoke(tickets, 'Registrar')
assert len(app.tickets.list()) == 10 and 'Ticket 10' in app.ticket_output.get('1.0', 'end')
f['ID de ticket (búsqueda)'].set('1'); invoke(tickets, 'Buscar ID')
assert 'Ticket 1' in app.ticket_output.get('1.0', 'end')
f['ID de ticket (búsqueda)'].set('999'); invoke(tickets, 'Buscar ID')
assert 'Sin resultados' in app.ticket_output.get('1.0', 'end')
f['ID de ticket (búsqueda)'].set('1'); f['Estado'].set('IN_PROGRESS')
invoke(tickets, 'Cambiar estado')
assert app.tickets.find(1).status == 'in_progress'
f['Prioridad'].set('CRITICAL'); invoke(tickets, 'Cambiar prioridad')
assert app.tickets.find(1).priority == 'CRITICAL'
f['ID solicitante'].set('1'); invoke(tickets, 'Filtrar por usuario')
assert len(app.tickets.list_by_requester(1)) == 2
assert 'Ticket 2' not in app.ticket_output.get('1.0', 'end')
print('OK: 5 usuarios y 10 tickets ficticios; registro, listado, búsqueda, actualización, filtro y validaciones mediante callbacks Tk.')
print('Las alertas se interceptaron; no se verificó visualmente la interfaz ni se tomaron capturas.')
root.destroy()
