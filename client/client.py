import jtclient as jtc
from tkinter import *
from tkinter import ttk

app = jtc.app()

app.connect('127.0.0.1')

root = Tk()
root.geometry('1200x800')

frm = ttk.Frame(root, padding=10)
frm.grid()

content = ttk.Label(frm)
content.grid(column=0, row=1)


def refresh():
    app.request('/')
    content.config(text=app.get_incoming_text())

ttk.Button(frm, text="Refresh", command=refresh).grid(column=0, row=0)

root.mainloop()