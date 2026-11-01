import tkinter as tk
from tkinter import messagebox, ttk

from app.services.tickets import TicketService
from app.services.users import UserService


class HelpDeskApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.users = UserService()
        self.tickets = TicketService(self.users)
        root.title('HelpDesk EDU - Semana 7')
        root.geometry('930x650')
        tabs = ttk.Notebook(root)
        tabs.pack(fill='both', expand=True, padx=10, pady=10)
        user_tab = ttk.Frame(tabs, padding=12)
        ticket_tab = ttk.Frame(tabs, padding=12)
        tabs.add(user_tab, text='Usuarios')
        tabs.add(ticket_tab, text='Tickets')
        self.user_fields = self._fields(user_tab, [('ID', None), ('Nombre', None), ('Correo', None),
                    ('Rol', ['REQUESTER', 'TECHNICIAN', 'SUPERVISOR', 'ADMINISTRATOR']),
                    ('Estado', ['ACTIVO', 'INACTIVO'])])
        self.user_output = self._output(user_tab, 8)
        self._buttons(user_tab, 5, [('Registrar', self.user_create), ('Listar', self.user_list),
                                    ('Buscar ID', self.user_find), ('Actualizar', self.user_update)])
        self.ticket_fields = self._fields(ticket_tab, [('ID de ticket (búsqueda)', None), ('ID solicitante', None),
                      ('Título', None), ('Descripción', None), ('Categoría', None),
                      ('Prioridad', ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']),
                      ('Estado', ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED', 'CANCELLED'])])
        self.ticket_output = self._output(ticket_tab, 10)
        self._buttons(ticket_tab, 7, [('Registrar', self.ticket_create), ('Listar', self.ticket_list),
                     ('Buscar ID', self.ticket_find), ('Filtrar por usuario', self.ticket_filter),
                     ('Cambiar estado', self.ticket_status), ('Cambiar prioridad', self.ticket_priority)])

    @staticmethod
    def _fields(parent, fields):
        result = {}
        for row, (label, choices) in enumerate(fields):
            ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w', pady=3)
            value = tk.StringVar(value=choices[0] if choices else '')
            widget = ttk.Combobox(parent, textvariable=value, values=choices, state='readonly') if choices else ttk.Entry(parent, textvariable=value)
            widget.grid(row=row, column=1, sticky='ew', padx=8, pady=3)
            result[label] = value
        parent.columnconfigure(1, weight=1)
        return result

    @staticmethod
    def _buttons(parent, row, buttons):
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, columnspan=2, sticky='w', pady=8)
        for label, command in buttons:
            ttk.Button(frame, text=label, command=command).pack(side='left', padx=2)

    @staticmethod
    def _output(parent, row):
        output = tk.Text(parent, width=100, height=14, state='disabled', wrap='word')
        output.grid(row=row, column=0, columnspan=2, sticky='nsew')
        parent.rowconfigure(row, weight=1)
        return output

    @staticmethod
    def _show(output, rows):
        output.configure(state='normal')
        output.delete('1.0', 'end')
        output.insert('end', '\n'.join(rows) if rows else 'Sin resultados.')
        output.configure(state='disabled')

    def _run(self, action):
        try:
            action()
        except (ValueError, TypeError) as exc:
            messagebox.showerror('Validación', str(exc), parent=self.root)

    def _u(self, name): return self.user_fields[name].get()
    def _t(self, name): return self.ticket_fields[name].get()
    def _user_rows(self, users):
        self._show(self.user_output, [f'{u.id} | {u.name} | {u.email} | {u.role.value.upper()} | {u.state}' for u in users])
    def _ticket_rows(self, tickets):
        self._show(self.ticket_output, [f'{t.id} | Usuario {t.requester_id} | {t.title} | {t.description} | {t.category} | {t.priority} | {t.status.value.upper()} | {t.created_at:%Y-%m-%d %H:%M:%S}' for t in tickets])

    def user_create(self):
        def work():
            self.users.create(int(self._u('ID')), self._u('Nombre'), self._u('Correo'), self._u('Rol'), self._u('Estado'))
            self.user_list()
        self._run(work)
    def user_list(self): self._user_rows(self.users.list())
    def user_find(self):
        def work():
            user = self.users.find(int(self._u('ID')))
            self._user_rows([user] if user else [])
        self._run(work)
    def user_update(self):
        def work():
            user = self.users.update(int(self._u('ID')), self._u('Nombre'), self._u('Correo'), self._u('Rol'), self._u('Estado'))
            self._user_rows([user])
        self._run(work)
    def ticket_create(self):
        def work():
            self.tickets.create(self._t('Título'), self._t('Descripción'), self._t('Categoría'),
                                self._t('Prioridad'), int(self._t('ID solicitante')))
            self.ticket_list()
        self._run(work)
    def ticket_list(self): self._ticket_rows(self.tickets.list())
    def ticket_find(self):
        def work():
            ticket = self.tickets.find(int(self._t('ID de ticket (búsqueda)')))
            self._ticket_rows([ticket] if ticket else [])
        self._run(work)
    def ticket_filter(self): self._run(lambda: self._ticket_rows(self.tickets.list_by_requester(int(self._t('ID solicitante')))))
    def ticket_status(self): self._run(lambda: self._ticket_rows([self.tickets.change_status(int(self._t('ID de ticket (búsqueda)')), self._t('Estado'))]))
    def ticket_priority(self): self._run(lambda: self._ticket_rows([self.tickets.change_priority(int(self._t('ID de ticket (búsqueda)')), self._t('Prioridad'))]))
