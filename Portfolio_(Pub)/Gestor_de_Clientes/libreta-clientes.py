from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title('CRM - Libreta de Clientes')

# Conexcion a Sqlite
conn = sqlite3.connect('crm.db')
c = conn.cursor()

c.execute("""
        CREATE TABLE if not exists cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            empresa TEXT NOT NULL
        );
""")


def render_clientes():
    rows = c.execute("SELECT * FROM cliente").fetchall()

    tree.delete(*tree.get_children())
    
    for row in rows:
        tree.insert('', END, row[0], values=(row[1], row[2], row[3]))


def insertar(cliente):
    # print(cliente)
    c.execute("""
        INSERT INTO cliente (nombre, telefono, empresa) VALUES (?, ?, ?)
        """, (cliente['nombre'], cliente['telefono'], cliente['empresa'])
    )
    conn.commit()
    render_clientes()


def nuevo_cliente():
    def save():
        if not e_nombre.get():
            messagebox.showerror('Error', 'El nombre es obligatorio')
            return
        if not e_telefono.get():
            messagebox.showerror('Error', 'El telefono es obligatorio')
            return
        if not e_empresa.get():
            messagebox.showerror('Error', 'El campo empresa es obligatorio')
            return
            
        cliente = {
            'nombre': e_nombre.get(),
            'telefono': e_telefono.get(),
            'empresa': e_empresa.get(),
        }
        insertar(cliente)
        top.destroy()
    
    top = Toplevel()
    top.title('Nuevo Cliente')

    l_nombre = Label(top, text='Nombre')
    l_nombre.grid(row=0, column=0)
    e_nombre = Entry(top, width=40)
    e_nombre.grid(row=0, column=1)
    
    l_telefono = Label(top, text='Telefono')
    l_telefono.grid(row=1, column=0)
    e_telefono = Entry(top, width=40)
    e_telefono.grid(row=1, column=1)
    
    l_empresa = Label(top, text='Empresa')
    l_empresa.grid(row=2, column=0)
    e_empresa = Entry(top, width=40)
    e_empresa.grid(row=2, column=1)

    btn_guardar = Button(top, text='Guardar', command=save)
    btn_guardar.grid(row=3, column=1)

    top.mainloop()


def eliminar_cliente():
    id = tree.selection()[0]
    # print(id)

    cliente = c.execute('SELECT * FROM cliente WHERE id = ?', (id, )).fetchone()
    respuesta = messagebox.askokcancel('Seguro?', 'Estas seguro de querer eliminar el cliente ' + cliente[1] + '?')
    if respuesta:
        c.execute("DELETE FROM cliente WHERE id = ?", (id, ))
        conn.commit()
        render_clientes()
    else:
        pass

btn_new = Button(root, text='Nuevo Cliente', command=nuevo_cliente)
btn_new.grid(row=0, column=0)

btn_remove = Button(root, text='Eliminar Cliente', command=eliminar_cliente)
btn_remove.grid(row=0, column=1)

tree = ttk.Treeview(root)
tree['columns'] = ('Nombre', 'Telefono', 'Empresa')
tree.column('#0', width=0, stretch=NO)
tree.column('Nombre')
tree.column('Telefono')
tree.column('Empresa')

tree.heading('Nombre', text='Nombre')
tree.heading('Telefono', text='Telefono')
tree.heading('Empresa', text='Empresa')

tree.grid(column=0, row=1, columnspan=2)


render_clientes()
root.mainloop()