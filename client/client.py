import jtclient as jtc
from tkinter import *
from tkinter import ttk

class Client(jtc.app):
    def __init__(self):
        super().__init__()
        self.setup_dns('209.38.154.253', 47229)

        self.gui = Tk()
        self.gui.geometry('1200x800')
        self.gui.config(bg='#000')

        self.search_value = StringVar(value='/')

        self.search_bar = ttk.Entry(self.gui, textvariable=self.search_value)
        self.search_bar.pack()

        self.btn = ttk.Button(self.gui, text="Refresh", command=self.refresh)
        self.btn.pack()

        self.content = ttk.Label(self.gui, background='black', foreground='white')
        self.content.pack()

        self.connect('thbop.code')


    def refresh(self):
        self.request(self.search_value.get())
        self.content.config(text=self.get_incoming_text())

    def run(self):
        self.gui.mainloop()

if __name__ == '__main__':
    client = Client()
    client.run()