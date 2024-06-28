import socket
import threading


class app:
    def __init__(self):
        self.pages = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def page(self, route):
        def wrapper(pg):
            self.pages[route] = pg
            def inner(*args, **kwargs):
                return pg(*args, **kwargs)
            return inner
        return wrapper
    
    
    def connection(self, conn, addr):
        print(f'Connection received from {addr[0]}:{addr[1]}')
        while True:
            data = conn.recv(1024)
            conn.send(b'Hello there!')
            if not data: break
            print('<', data.decode())
        conn.close()
    
    def run(self, address: str = 'localhost', port: int = 4242):
        print(self.pages)
        self.sock.bind((address, port))
        print('Listening')
        while True:
            self.sock.listen()
            conn, conn_addr = self.sock.accept()
            threading.Thread(target=self.connection,args=(conn, conn_addr), daemon=True).start()
        
        self.sock.close()

        