import jtclient as jtc
from tkinter import *
from tkinter import ttk

class Client(jtc.app):
    def __init__(self):
        super().__init__()
        self.setup_dns('127.0.0.1', 4242)

        self.gui = Tk()
        self.gui.geometry('1200x800')
        self.gui.config(bg='#000')

        self.search_value = StringVar(value='thbop.code/')

        self.search_bar = ttk.Entry(self.gui, textvariable=self.search_value)
        self.search_bar.pack()

        self.btn = ttk.Button(self.gui, text="Go", command=self.go)
        self.btn.pack()

        self.content = ttk.Label(self.gui, background='black', foreground='white')
        self.content.pack()



    def go(self):
        raw_search = self.search_value.get()
        slash_pos = raw_search.find('/')

        domain = raw_search[0:slash_pos]
        route = raw_search[slash_pos:len(raw_search)]
        self.connect(domain)
        self.request(route)
        self.content.config(text=self.get_incoming_text())

    def run(self):
        self.gui.mainloop()

if __name__ == '__main__':
    client = Client()
    client.run()