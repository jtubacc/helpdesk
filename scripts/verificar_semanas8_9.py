"""Invoca controles Tk reales; diálogos interceptados; no es inspección visual."""
import tkinter as tk
from tkinter import ttk, messagebox
from app.ui.forms import HelpDeskApp

root = tk.Tk()
app = HelpDeskApp(root)
root.update()
errors = []
messagebox.showerror = lambda title, message, **kwargs: errors.append(message)
notebook = next(w for w in root.winfo_children() if isinstance(w, ttk.Notebook))
user_tab = root.nametowidget(notebook.tabs()[0])
ticket_tab = root.nametowidget(notebook.tabs()[1])

def fill(fields, values):
    for name, value in values.items():
        fields[name].set(value)

def click(tab, label):
    for frame in tab.winfo_children():
        for widget in frame.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget('text') == label:
                widget.invoke()
                root.update()
                return
    raise AssertionError(f'No se encontró el botón {label}')

for uid, role in [(1, 'REQUESTER'), (2, 'TECHNICIAN'), (3, 'REQUESTER')]:
    fill(app.user_fields, {'ID': str(uid), 'Nombre': f'Usuario {uid}',
                           'Correo': f'usuario{uid}@example.invalid', 'Rol': role, 'Estado': 'ACTIVO'})
    click(user_tab, 'Registrar')
assert len(app.users.list()) == 3
notebook.select(ticket_tab)
fill(app.ticket_fields, {'ID solicitante': '1', 'Título': 'Sin red', 'Descripción': 'Fallo ficticio',
                         'Categoría': 'Network', 'Prioridad': 'HIGH', 'Estado': 'OPEN'})
click(ticket_tab, 'Registrar')
assert app.tickets.list()[0].status == 'open'
fill(app.ticket_fields, {'ID de ticket (búsqueda)': '1', 'ID técnico': '2'})
click(ticket_tab, 'Asignar técnico')
assert app.tickets.find(1).assignee is app.users.find(2)
fill(app.ticket_fields, {'ID autor': '1', 'Comentario': 'Primera revisión'})
click(ticket_tab, 'Comentar')
assert app.tickets.find(1).comments[0].body == 'Primera revisión'
click(ticket_tab, 'Ver comentarios')
assert 'Primera revisión' in app.ticket_output.get('1.0', 'end')
click(ticket_tab, 'Por técnico')
assert 'Sin red' in app.ticket_output.get('1.0', 'end')
click(ticket_tab, 'Por categoría')
assert 'Sin red' in app.ticket_output.get('1.0', 'end')
click(ticket_tab, 'Por estado')
assert 'Sin red' in app.ticket_output.get('1.0', 'end')
fill(app.ticket_fields, {'ID técnico': '3'})
click(ticket_tab, 'Asignar técnico')
assert errors[-1] == 'El usuario asignado debe tener rol TECHNICIAN'
assert app.tickets.find(1).assignee.id == 2
fill(app.ticket_fields, {'ID autor': '999'})
click(ticket_tab, 'Comentar')
assert errors[-1] == 'Autor no encontrado' and len(app.tickets.find(1).comments) == 1
root.destroy()
print('OK: asignación, comentario y tres filtros por controles Tk; se rechazaron rol y autor inválidos.')
print('Diálogos interceptados; no se inspeccionó visualmente la ventana ni se tomaron capturas.')
